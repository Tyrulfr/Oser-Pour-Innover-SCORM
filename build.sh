#!/usr/bin/env bash
# Build SCORM ZIP : contenu du module a la racine du ZIP (imsmanifest.xml au root).
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

build_one() {
  local dir="$1"
  local zipname="$2"
  if [ -d "$ROOT/modules/$dir" ]; then
    cd "$ROOT/modules/$dir"
    zip -r "$ROOT/$zipname" .
    echo "Build OK: $zipname"
  else
    echo "Skip (absent): modules/$dir"
  fi
}

build_one "module-r-avancement" "module-r-avancement.zip"
build_one "module1-retours" "module1-retours.zip"
build_one "module2-pi" "module2-pi.zip"
build_one "module3-ecosysteme" "module3-ecosysteme.zip"
build_one "module4-partenariats" "module4-partenariats.zip"
build_one "module5-action" "module5-action.zip"
build_one "module6-synthese" "module6-synthese.zip"
