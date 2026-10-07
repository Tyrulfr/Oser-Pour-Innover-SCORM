#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le site apprenant et les paquets SCORM à partir de concepteur/programme.json."""
from __future__ import annotations

import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "concepteur" / "programme.json"
SHARED = ROOT / "modules" / "_shared"
API = ROOT / "scorm-api" / "SCORM_API.js"


def slug(text: str, fallback: str) -> str:
    norm = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    out = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    return out or fallback


def html(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_programme() -> dict:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    modules = []
    for i, mod in enumerate(data.get("modules") or [], start=1):
        mid = slug(mod.get("id") or "", f"module-{i}")
        grains = []
        for j, grain in enumerate(mod.get("grains") or [], start=1):
            gid = slug(grain.get("id") or "", f"grain-{j}")
            grains.append(
                {
                    "id": gid,
                    "file": f"{gid}.html",
                    "titre": grain.get("titre") or f"Grain {j}",
                    "sous_titre": grain.get("sous_titre") or "À compléter",
                }
            )
        if not grains:
            grains = [{"id": "grain-1", "file": "grain-1.html", "titre": "Premier grain", "sous_titre": "À compléter"}]
        modules.append(
            {
                "id": mid,
                "titre": mod.get("titre") or f"Module {i}",
                "resume": mod.get("resume") or "",
                "grains": grains,
                "suspend": mid.replace("-", "") + "_suspend",
                "pages_js": json.dumps([g["id"] for g in grains], ensure_ascii=False),
            }
        )
    return {
        "titre": data.get("titre") or "Nouveau programme",
        "sous_titre": data.get("sous_titre") or "",
        "modules": modules,
    }


def write_accueil(prog: dict) -> None:
    cards = []
    for mod in prog["modules"]:
        n = len(mod["grains"])
        cards.append(
            f"""
            <a class="card" href="modules/{mod['id']}/index.html">
                <span class="icon"><i class="fa-solid fa-layer-group"></i></span>
                <h3>{html(mod['titre'])}</h3>
                <p>{html(mod['resume'] or (str(n) + ' grain' + ('s' if n > 1 else '')))}</p>
                <span class="btn">{n} grain{'s' if n > 1 else ''}</span>
            </a>"""
        )
    (ROOT / "index.html").write_text(
        ACCUEIL.format(
            titre=html(prog["titre"]),
            sous_titre=html(prog["sous_titre"]),
            cards="\n".join(cards),
        ),
        encoding="utf-8",
    )


def write_module(prog: dict, mod: dict) -> None:
    dest = ROOT / "modules" / mod["id"]
    pages = dest / "pages"
    pages.mkdir(parents=True)
    shutil.copy2(API, dest / "SCORM_API.js")
    for name in ("eval.css", "eval.js", "eval-bank.js", "progress.js"):
        shutil.copy2(SHARED / name, dest / name)

    cards = []
    files = ["index.html", "SCORM_API.js", "progress.js", "eval-bank.js", "eval.js", "eval.css"]
    for idx, grain in enumerate(mod["grains"], start=1):
        files.append(f"pages/{grain['file']}")
        cards.append(
            f"""
            <div class="grain-card">
                <div class="card-number">{idx:02d}</div>
                <div class="card-body">
                    <div class="card-icon"><i class="fa-solid fa-play"></i></div>
                    <div class="code-pill">Grain {idx}</div>
                    <div class="card-title">{html(grain['titre'])}</div>
                    <div class="card-desc">{html(grain['sous_titre'])}</div>
                </div>
                <div class="card-footer"><a href="pages/{grain['file']}" class="btn-start">Accéder</a></div>
            </div>"""
        )
        (pages / grain["file"]).write_text(
            GRAIN.format(
                programme=html(prog["titre"]),
                module_titre=html(mod["titre"]),
                module_id=mod["id"],
                grain_id=grain["id"],
                grain_titre=html(grain["titre"]),
                grain_sous_titre=html(grain["sous_titre"]),
                suspend=mod["suspend"],
                pages_js=mod["pages_js"],
            ),
            encoding="utf-8",
        )

    file_tags = "\n".join(f'      <file href="{name}"/>' for name in files)
    (dest / "imsmanifest.xml").write_text(
        MANIFEST.format(
            ident=mod["id"].upper().replace("-", "_"),
            titre=html(mod["titre"]),
            files=file_tags,
        ),
        encoding="utf-8",
    )
    (dest / "index.html").write_text(
        MODULE_INDEX.format(
            programme=html(prog["titre"]),
            module_titre=html(mod["titre"]),
            module_resume=html(mod["resume"]),
            n_grains=len(mod["grains"]),
            cards="\n".join(cards),
            suspend=mod["suspend"],
            pages_js=mod["pages_js"],
        ),
        encoding="utf-8",
    )


def write_build(prog: dict) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -e",
        'ROOT="$(cd "$(dirname "$0")" && pwd)"',
        'SHARED="$ROOT/modules/_shared"',
        'API="$ROOT/scorm-api/SCORM_API.js"',
        "copy_shared() {",
        '  local dir="$1"',
        '  [ -f "$API" ] && [ -d "$ROOT/modules/$dir" ] && cp "$API" "$ROOT/modules/$dir/SCORM_API.js"',
        '  [ -d "$SHARED" ] && [ -d "$ROOT/modules/$dir" ] && cp "$SHARED"/eval.css "$SHARED"/eval.js "$SHARED"/eval-bank.js "$SHARED"/progress.js "$ROOT/modules/$dir/"',
        "}",
        "build_one() {",
        '  local dir="$1"',
        '  local zipname="$2"',
        '  if [ -d "$ROOT/modules/$dir" ]; then',
        '    copy_shared "$dir"',
        '    cd "$ROOT/modules/$dir"',
        '    rm -f "$ROOT/$zipname"',
        '    zip -r -q "$ROOT/$zipname" . -x ".DS_Store" "*/.DS_Store"',
        '    echo "Build OK: $zipname"',
        "  fi",
        "}",
    ]
    for mod in prog["modules"]:
        lines.append(f'build_one "{mod["id"]}" "{mod["id"]}.zip"')
    (ROOT / "build.sh").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "build.sh").chmod(0o755)


def clean_generated(prog: dict) -> None:
    keep = {mod["id"] for mod in prog["modules"]} | {"_shared"}
    modules_dir = ROOT / "modules"
    if not modules_dir.exists():
        return
    for child in modules_dir.iterdir():
        if child.is_dir() and child.name not in keep:
            shutil.rmtree(child)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Fichier manquant : {SRC}")
    prog = load_programme()
    clean_generated(prog)
    write_accueil(prog)
    for mod in prog["modules"]:
        dest = ROOT / "modules" / mod["id"]
        if dest.exists():
            shutil.rmtree(dest)
        write_module(prog, mod)
    write_build(prog)
    print(f"Généré : {len(prog['modules'])} module(s), {sum(len(m['grains']) for m in prog['modules'])} grain(s).")


ACCUEIL = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titre}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ --accent: #2A325E; --teal: #2EAF7D; --orange: #F48C2E; --bg: #F8F9FA; }}
        body {{ margin: 0; font-family: 'Open Sans', sans-serif; background: var(--bg); color: var(--accent);
            background-image: radial-gradient(rgba(42,50,94,0.08) 1px, transparent 1px); background-size: 28px 28px; }}
        .navbar {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem 6%; background: #fff; border-bottom: 1px solid #e6e6e6; }}
        .navbar a {{ color: var(--accent); font-weight: 700; text-decoration: none; }}
        .hero {{ text-align: center; padding: 4rem 1.5rem 2rem; }}
        h1 {{ font-family: Montserrat, sans-serif; font-size: 2.6rem; margin: 0 0 0.8rem; }}
        .subtitle {{ max-width: 720px; margin: 0 auto 2.5rem; opacity: 0.8; }}
        .cards {{ display: flex; flex-wrap: wrap; gap: 1.2rem; justify-content: center; padding: 0 1rem 4rem; }}
        .card {{ width: 280px; background: #fff; border-radius: 16px; padding: 1.6rem; text-decoration: none; color: inherit;
            box-shadow: 0 10px 24px rgba(0,0,0,0.06); }}
        .card:hover {{ transform: translateY(-4px); }}
        .icon {{ font-size: 1.6rem; color: var(--teal); display: block; margin-bottom: 0.8rem; }}
        .btn {{ display: inline-block; margin-top: 1rem; padding: 8px 16px; border-radius: 999px; border: 2px solid var(--teal); color: var(--teal); font-weight: 800; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <strong>{titre}</strong>
        <a href="concepteur/index.html">Portail concepteur</a>
    </nav>
    <div class="hero">
        <h1>{titre}</h1>
        <p class="subtitle">{sous_titre}</p>
    </div>
    <div class="cards">
{cards}
    </div>
</body>
</html>
"""

MODULE_INDEX = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_titre}</title>
    <script src="SCORM_API.js"></script>
    <script src="progress.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ --accent: #2A325E; --teal: #2EAF7D; --orange: #F48C2E; --bg: #F8F9FA; --card: #fff; }}
        body {{ margin: 0; font-family: 'Open Sans', sans-serif; background: var(--bg); color: var(--accent); padding-bottom: 80px; }}
        .top-bar {{ background: var(--card); padding: 0.9rem 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid var(--accent); }}
        .btn-back {{ text-decoration: none; color: inherit; font-weight: 700; }}
        .content {{ max-width: 1100px; margin: 2rem auto; padding: 0 1.4rem; }}
        .hero {{ background: linear-gradient(135deg, var(--teal), var(--accent)); color: #fff; border-radius: 18px; padding: 2.4rem 1.4rem; text-align: center; }}
        .hero h1 {{ font-family: Montserrat, sans-serif; margin: 0 0 0.6rem; }}
        .grains-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.4rem; margin-top: 2rem; }}
        .grain-card {{ background: var(--card); border-radius: 14px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.06); display: flex; flex-direction: column; position: relative; border-top: 5px solid var(--teal); }}
        .card-number {{ position: absolute; top: 12px; right: 14px; font-size: 1.6rem; font-weight: 900; opacity: 0.08; }}
        .card-body {{ padding: 1.6rem 1.3rem; flex: 1; }}
        .card-icon {{ width: 52px; height: 52px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: rgba(46,175,125,0.12); color: var(--teal); margin-bottom: 0.8rem; }}
        .code-pill {{ font-size: 0.75rem; font-weight: 800; color: var(--teal); margin-bottom: 0.35rem; }}
        .card-title {{ font-family: Montserrat, sans-serif; font-weight: 800; margin-bottom: 0.4rem; }}
        .card-desc {{ font-size: 0.92rem; opacity: 0.75; }}
        .card-footer {{ padding: 0.9rem 1.3rem; border-top: 1px solid #eee; text-align: right; }}
        .btn-start {{ background: var(--accent); color: #fff; text-decoration: none; padding: 8px 16px; border-radius: 999px; font-weight: 700; font-size: 0.85rem; }}
    </style>
</head>
<body>
    <nav class="top-bar">
        <a class="btn-back" href="../../index.html">Accueil</a>
        <strong>{programme}</strong>
        <span></span>
    </nav>
    <div class="content">
        <div class="hero">
            <h1>{module_titre}</h1>
            <p>{module_resume}</p>
            <p>{n_grains} grain(s)</p>
        </div>
        <div class="grains-grid">
{cards}
        </div>
    </div>
    <script>
        ProgressApp.boot({{ suspendKey: "{suspend}", pages: {pages_js} }});
    </script>
</body>
</html>
"""

GRAIN = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{grain_titre}</title>
    <script src="../SCORM_API.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../eval.css">
    <style>
        :root {{ --accent: #2A325E; --teal: #2EAF7D; --bg: #F8F9FA; --card: #fff; --muted: #555; }}
        body {{ margin: 0; font-family: 'Open Sans', sans-serif; background: var(--bg); color: var(--accent); padding-bottom: 140px; }}
        .top-bar {{ background: var(--card); padding: 0.9rem 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid var(--accent); }}
        .btn-back {{ text-decoration: none; color: inherit; font-weight: 700; }}
        .content {{ max-width: 920px; margin: 2rem auto; padding: 0 1.4rem; }}
        .hero-title {{ font-family: Montserrat, sans-serif; font-size: 2rem; margin: 0 0 0.4rem; }}
        .hero-subtitle {{ opacity: 0.75; border-left: 4px solid var(--teal); padding-left: 12px; }}
        .video-card {{ background: var(--card); border-radius: 18px; overflow: hidden; box-shadow: 0 12px 28px rgba(0,0,0,0.06); margin: 2rem 0; }}
        .video-header {{ padding: 1.2rem 1.4rem; border-bottom: 1px solid #eee; }}
        .video-wrapper {{ min-height: 220px; background: #111; color: #fff; display: flex; align-items: center; justify-content: center; text-align: center; padding: 2rem; }}
        .video-wrapper p {{ max-width: 28rem; opacity: 0.85; }}
        .action-footer {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--card); padding: 1rem 5%; display: flex; justify-content: flex-end; box-shadow: 0 -6px 18px rgba(0,0,0,0.08); }}
        .btn-validate {{ background: var(--accent); color: #fff; text-decoration: none; padding: 12px 22px; border-radius: 999px; font-weight: 800; }}
    </style>
</head>
<body data-grain="{grain_id}">
    <nav class="top-bar">
        <a class="btn-back" href="../index.html">Retour</a>
        <strong>{module_titre}</strong>
        <span></span>
    </nav>
    <div class="content">
        <h1 class="hero-title">{grain_titre}</h1>
        <p class="hero-subtitle">{grain_sous_titre}</p>
        <div class="video-card">
            <div class="video-header"><strong>Vidéo</strong> — coller ici le lecteur (iframe eMedia, YouTube…)</div>
            <div class="video-wrapper">
                <p>Emplacement vidéo. Remplacez ce bloc par l’iframe du média.</p>
            </div>
        </div>
        <div id="eval-after-e"></div>
        <div id="eval-memory"></div>
    </div>
    <div class="action-footer">
        <a class="btn-validate" href="../index.html" onclick="markCompleted(100)">Retour au sommaire</a>
    </div>
    <script src="../eval-bank.js"></script>
    <script src="../eval.js"></script>
    <script src="../progress.js"></script>
    <script>
        ProgressApp.boot({{
            grainId: "{grain_id}",
            suspendKey: "{suspend}",
            pages: {pages_js}
        }});
    </script>
</body>
</html>
"""

MANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{ident}" version="1.4"
  xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_v1p3"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>2004 4th Edition</schemaversion>
  </metadata>
  <organizations default="{ident}-ORG">
    <organization identifier="{ident}-ORG">
      <title>{titre}</title>
      <item identifier="ITEM-{ident}" identifierref="RES-{ident}">
        <title>Sommaire</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES-{ident}" type="webcontent" adlcp:scormtype="sco" href="index.html">
{files}
    </resource>
  </resources>
</manifest>
"""


if __name__ == "__main__":
    main()
