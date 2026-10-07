#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
SHARED="$ROOT/modules/_shared"
API="$ROOT/scorm-api/SCORM_API.js"
copy_shared() {
  local dir="$1"
  [ -f "$API" ] && [ -d "$ROOT/modules/$dir" ] && cp "$API" "$ROOT/modules/$dir/SCORM_API.js"
  [ -d "$SHARED" ] && [ -d "$ROOT/modules/$dir" ] && cp "$SHARED"/eval.css "$SHARED"/eval.js "$SHARED"/eval-bank.js "$SHARED"/progress.js "$ROOT/modules/$dir/"
}
build_one() {
  local dir="$1"
  local zipname="$2"
  if [ -d "$ROOT/modules/$dir" ]; then
    copy_shared "$dir"
    cd "$ROOT/modules/$dir"
    rm -f "$ROOT/$zipname"
    zip -r -q "$ROOT/$zipname" . -x ".DS_Store" "*/.DS_Store"
    echo "Build OK: $zipname"
  fi
}
build_one "module-1" "module-1.zip"
build_one "module-2" "module-2.zip"
