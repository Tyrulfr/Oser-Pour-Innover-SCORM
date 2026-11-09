#!/usr/bin/env python3
"""Serveur local avec Range HTTP — indispensable pour seeker une preview mp4."""
from __future__ import annotations

import argparse
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class RangeRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return SimpleHTTPRequestHandler.send_head(self)
        if not os.path.isfile(path):
            self.send_error(404, "File not found")
            return None
        ctype = self.guess_type(path)
        try:
            file_obj = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None
        fs = os.fstat(file_obj.fileno())
        size = fs.st_size
        range_header = self.headers.get("Range")
        if not range_header:
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(size))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return file_obj
        match = re.match(r"bytes=(\d*)-(\d*)", range_header.strip())
        if not match:
            file_obj.close()
            self.send_error(416, "Invalid range")
            return None
        start_s, end_s = match.groups()
        start = int(start_s) if start_s else 0
        end = int(end_s) if end_s else size - 1
        if start >= size or end >= size or start > end:
            file_obj.close()
            self.send_error(416, "Requested range not satisfiable")
            return None
        self.send_response(206)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Range", "bytes %s-%s/%s" % (start, end, size))
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        file_obj.seek(start)
        self._range_remaining = end - start + 1
        return file_obj

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_range_remaining", None)
        if remaining is None:
            return SimpleHTTPRequestHandler.copyfile(self, source, outputfile)
        while remaining > 0:
            chunk = source.read(min(65536, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)
        self._range_remaining = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8894)
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--dir", default=".")
    args = parser.parse_args()
    os.chdir(args.dir)
    httpd = ThreadingHTTPServer((args.bind, args.port), RangeRequestHandler)
    print("Preview server http://%s:%s (Range OK)" % (args.bind, args.port), flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
