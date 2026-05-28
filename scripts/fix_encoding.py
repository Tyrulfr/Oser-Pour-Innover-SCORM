#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige les caractères UTF-8 corrompus (�, �?) dans les grains du module R."""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_COMMIT = "16e7ec9"

MAPPINGS = [
    ("modules/module0-avancement/pages", "modules/module-r-avancement/pages"),
    ("modules/module0", "modules/module-r"),
]

RENAME_IN_CLEAN = [
    ("module0_suspend", "module-r_suspend"),
    ("module0", "module-r"),
]


from typing import Optional


def git_show(path: str) -> Optional[str]:
    try:
        data = subprocess.check_output(
            ["git", "-C", REPO, "show", f"{CLEAN_COMMIT}:{path}"],
            stderr=subprocess.DEVNULL,
        )
        return data.decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def merge_line(clean: str, broken: str) -> str:
    broken = broken.lstrip("\ufeff")
    if clean == broken:
        return broken
    if "\ufffd" in broken and "\ufffd" not in clean:
        line = clean
        for old, new in RENAME_IN_CLEAN:
            if old in broken and old not in clean:
                line = line.replace(old, new)
        return line
    return broken


def merge_file(clean: str, broken: str) -> str:
    clean_lines = clean.splitlines()
    broken_lines = broken.splitlines()
    if len(clean_lines) != len(broken_lines):
        return fix_text_regex(broken)
    merged = [merge_line(c, b) for c, b in zip(clean_lines, broken_lines)]
    text = "\n".join(merged)
    if broken.endswith("\n"):
        text += "\n"
    return fix_text_regex(text)


def fix_text_regex(text: str) -> str:
    text = text.lstrip("\ufeff")
    text = text.replace("\ufffd?T", "'")
    text = text.replace('\ufffd"uvre', "œuvre")
    text = text.replace('c\ufffd"ur', "cœur")
    text = text.replace("\ufffd^", "È")
    text = text.replace("\ufffd,ge", "Âge")
    text = text.replace("\ufffd?\ufffd", "≠")
    text = text.replace("\ufffd?", "é")
    text = re.sub(r"é([A-Z])", lambda m: "É" + m.group(1), text)
    text = text.replace("équipe Multidisciplinaire", "Équipe Multidisciplinaire")
    text = text.replace("é quoi", "À quoi")
    text = text.replace("é quel", "À quel")
    text = text.replace("é ce", "À ce")
    text = text.replace("é partir", "À partir")
    text = text.replace("échouer", "Échouer")
    text = text.replace("éliminer", "Éliminer")
    text = text.replace("écouter", "Écouter")
    text = text.replace("écologique", "Écologique")
    text = text.replace("étude", "Étude")
    text = text.replace("économique", "Économique")
    text = text.replace("émotions", "Émotions")
    text = text.replace("énergétique", "Énergétique")
    text = text.replace("≠conomique", "Économique")
    return text


def process_file(old_git_path: Optional[str], file_path: str) -> bool:
    with open(file_path, encoding="utf-8") as f:
        original = f.read()

    if "\ufffd" not in original and not original.startswith("\ufeff"):
        return False

    clean = git_show(old_git_path) if old_git_path else None
    if clean:
        fixed = merge_file(clean, original)
    else:
        fixed = fix_text_regex(original)

    if fixed != original:
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(fixed)
        return True
    return False


def main() -> int:
    changed = []
    for old_base, new_base in MAPPINGS:
        new_dir = os.path.join(REPO, new_base)
        if not os.path.isdir(new_dir):
            continue
        for name in sorted(os.listdir(new_dir)):
            if not name.endswith(".html"):
                continue
            rel = os.path.join(new_base, name)
            old_rel = os.path.join(old_base, name)
            if process_file(old_rel, os.path.join(REPO, rel)):
                changed.append(rel)

    extra = [
        "modules/module-r-avancement/index.html",
        "modules/module-r-avancement/SCORM_API.js",
        "modules/module-r/index.html",
        "modules/scorm-download.html",
        "modules/module1-retours/pages/temoignage_silvia.html",
        "modules/module1/temoignage_silvia.html",
        "scorm-api/SCORM_API.js",
    ]
    old_extra = {
        "modules/module-r-avancement/index.html": "modules/module0-avancement/index.html",
        "modules/module-r/index.html": "modules/module0/index.html",
        "modules/module-r-avancement/SCORM_API.js": "modules/module0-avancement/SCORM_API.js",
        "scorm-api/SCORM_API.js": "scorm-api/SCORM_API.js",
    }
    for rel in extra:
        path = os.path.join(REPO, rel)
        if os.path.isfile(path) and process_file(old_extra.get(rel), path):
            changed.append(rel)

    remaining = []
    for root, _, files in os.walk(os.path.join(REPO, "modules")):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            text = open(path, encoding="utf-8").read()
            if "\ufffd" in text:
                remaining.append(os.path.relpath(path, REPO))

    print(f"Fichiers corrigés: {len(changed)}")
    for f in changed:
        print(f"  - {f}")
    if remaining:
        print(f"Caractères corrompus restants: {len(remaining)}")
        for f in remaining:
            print(f"  ! {f}")
        return 1
    print("Aucun caractère corrompu restant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
