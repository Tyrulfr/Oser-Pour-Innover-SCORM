#!/usr/bin/env python3
"""Importe le KIT COM / LOGOS hors SCORM : sources, PNG, icônes nommées par concept."""
from __future__ import annotations

import json
import shutil
import unicodedata
import zipfile
from collections import deque
from pathlib import Path

import fitz
from PIL import Image, ImageChops, ImageDraw

KIT = Path("/Users/ups_ifpoc/Desktop/KIT COM et LOGOS")
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "authoring" / "Kit-com-V2"

SCALE_SCHEMA = 3.0
SCALE_ICON = 8.0
SCALE_KAKEMONO = 1.25

SCHEMA_MAP = {
    "fasc1-schema-1": {
        "slug": "f1-ecosysteme-innovation",
        "titre": "Écosystème de l’innovation (France / Europe / International)",
    },
    "fasc2-schema-1": {
        "slug": "f2-cycle-3-phases",
        "titre": "Cycle de l’innovation — 3 phases (idée → adoption et impact)",
    },
    "fasc2-schema-2": {
        "slug": "f2-cycle-phase-recherche",
        "titre": "Phase recherche et expérimentation",
    },
    "fasc2-schema-3": {
        "slug": "f2-cycle-phase-propulsion",
        "titre": "Phase propulsion (expérimentation → transfert)",
    },
    "fasc2-schema-4": {
        "slug": "f2-cycle-phase-utilite",
        "titre": "Phase utilité collective (transfert → adoption)",
    },
    "fasc2-schema-5": {
        "slug": "f2-cycle-complet",
        "titre": "Le cycle de l’innovation (vue d’ensemble)",
    },
    "fasc2-schema-6": {
        "slug": "f2-chaine-valorisation",
        "titre": "Chaîne de valorisation (recherche → innovation)",
    },
    "fasc2-schema-7": {
        "slug": "f2-valorisation-shs",
        "titre": "Valorisation en SHS (cinq voies)",
    },
    "fasc2-schema-8": {
        "slug": "f2-parcours-sensibilisation-esr",
        "titre": "Parcours de sensibilisation / acculturation des cadres de l’ESR",
    },
    "fasc2-schema-9": {
        "slug": "f2-parcours-entrepreneuriat",
        "titre": "Parcours entrepreneuriat (détection → transfert) et écosystème",
    },
}

# Noms = libellés du schéma 5 (cycle complet). Extraction depuis les frises 2–4
# (mêmes pictogrammes, isolés, sans flèches collées).
ICON_SEQUENCE = {
    "fasc2-schema-2": [
        ("IDÉE", "Ampoule allumée", "orange"),
        ("CRÉATIVITÉ", "Tête / cerveau ouvert, crayon et arc-en-ciel", "orange"),
        ("SOLUTIONS", "Ampoule avec coche", "orange"),
        ("SÉLECTION", "Documents superposés et curseur", "orange"),
        ("PROTOTYPAGE", "Maillon / lien", "orange"),
        ("EXPÉRIMENTATION", "Fiole (erlenmeyer)", "orange"),
    ],
    "fasc2-schema-3": [
        ("EXPÉRIMENTATION", "Fiole (erlenmeyer)", "orange"),
        ("DÉCOUVERTE", "Clé", "marine"),
        ("VALORISATION", "Document et crayon", "marine"),
        ("TRANSFERT", "Avion en papier", "marine"),
    ],
    "fasc2-schema-4": [
        ("TRANSFERT", "Avion en papier", "marine"),
        ("DESIGN", "Crayon et clé à molette", "vert"),
        ("PRODUCTION", "Imprimante", "vert"),
        ("DIFFUSION", "Mégaphone", "vert"),
        ("ADOPTION et IMPACT", "Mains qui portent une ampoule", "vert"),
    ],
}

CHARTE_MEDIA = {
    "media1.mp4": "logo-standard-anime-sonorise.mp4",
    "media2.mp4": "logo-expert-temoignage-anime-sonorise.mp4",
    "media3.wav": "jingle-a.wav",
    "media4.wav": "jingle-b.wav",
    "media5.mp4": "bandeau-intervenant.mp4",
    "media6.mp4": "transition.mp4",
    "media7.mp4": "exemples-illustrations-animees.mp4",
    "media8.mp4": "texte-anime-1.mp4",
    "media9.mp4": "texte-anime-2.mp4",
    "media10.mp4": "texte-anime-3.mp4",
    "media11.mp4": "texte-anime-4.mp4",
}


def ascii_stem(name: str) -> str:
    n = unicodedata.normalize("NFD", name.lower())
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    n = n.replace("’", "-").replace("'", "-")
    return n


def find_pdf_or_ai(key: str) -> Path:
    """fasc1-schema-1 → fichier réel fasc1-schéma-1.ai (accents variables)."""
    num = key.split("-")[-1]
    prefix = "fasc1" if key.startswith("fasc1") else "fasc2"
    search = []
    src_dir = DEST / "sources"
    if src_dir.is_dir():
        search.extend(sorted(src_dir.iterdir()))
    if KIT.is_dir():
        search.extend(sorted(KIT.iterdir()))
    for p in search:
        if not p.is_file():
            continue
        stem = ascii_stem(p.stem)
        if p.suffix.lower() == ".ai" and stem.startswith(prefix) and stem.endswith(num) and "schema" in stem:
            return p
    raise FileNotFoundError(key)


def render_page(src: Path, dest: Path, scale: float) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(src)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    pix.save(str(dest))
    doc.close()
    return dest


def find_icon_blobs(im: Image.Image, min_side: int = 90) -> list[tuple[int, int, int, int, int]]:
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    blobs: list[tuple[int, int, int, int, int]] = []

    def fg(x: int, y: int) -> bool:
        return px[x, y][3] > 70

    for y in range(h):
        for x in range(w):
            i = y * w + x
            if seen[i] or not fg(x, y):
                continue
            q = deque([(x, y)])
            seen[i] = 1
            minx = maxx = x
            miny = maxy = y
            n = 0
            while q:
                cx, cy = q.pop()
                n += 1
                if cx < minx:
                    minx = cx
                elif cx > maxx:
                    maxx = cx
                if cy < miny:
                    miny = cy
                elif cy > maxy:
                    maxy = cy
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if not seen[j] and fg(nx, ny):
                            seen[j] = 1
                            q.append((nx, ny))
            bw = maxx - minx + 1
            bh = maxy - miny + 1
            if min(bw, bh) < min_side:
                continue
            ratio = bw / bh
            if ratio < 0.72 or ratio > 1.38:
                continue
            fill = n / (bw * bh)
            if fill < 0.35:
                continue
            blobs.append((minx, miny, maxx, maxy, n))
    blobs.sort(key=lambda b: b[0])
    return blobs


def crop_pad(im: Image.Image, box: tuple[int, int, int, int], pad: int = 8) -> Image.Image:
    x0, y0, x1, y1 = box
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    crop = im.crop((x0, y0, x1, y1))
    side = max(crop.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(crop, ((side - crop.width) // 2, (side - crop.height) // 2))
    return punch_circle(canvas)


def punch_circle(im: Image.Image) -> Image.Image:
    """Masque circulaire : extérieur 100 % transparent (pas de fond noir/blanc)."""
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, w - 2, h - 2), fill=255)
    out = im.copy()
    out.putalpha(ImageChops.multiply(out.split()[3], mask))
    return out


def copy_sources() -> None:
    src_dir = DEST / "sources"
    src_dir.mkdir(parents=True, exist_ok=True)
    for p in sorted(KIT.iterdir()):
        if not p.is_file():
            continue
        if p.name.startswith("~$"):
            continue
        if p.suffix.lower() == ".zip":
            continue
        dest = src_dir / p.name
        if dest.exists() and dest.stat().st_size == p.stat().st_size:
            print("skip copy", p.name)
            continue
        print("copy", p.name)
        shutil.copy2(p, dest)


def extract_charte_media() -> None:
    pptx = next(p for p in KIT.glob("Charte graphique*.pptx") if not p.name.startswith("~"))
    out_av = DEST / "charte" / "motion"
    out_img = DEST / "charte" / "media"
    out_av.mkdir(parents=True, exist_ok=True)
    out_img.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(pptx) as z:
        for info in z.infolist():
            if not info.filename.startswith("ppt/media/"):
                continue
            name = Path(info.filename).name
            if name in CHARTE_MEDIA:
                dest = out_av / CHARTE_MEDIA[name]
            else:
                dest = out_img / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(z.read(info.filename))
            print("extract", dest.relative_to(DEST), info.file_size)


def export_icons_only() -> list[dict]:
    icon_dir = DEST / "icones"
    icon_dir.mkdir(parents=True, exist_ok=True)
    for old in icon_dir.glob("*.png"):
        old.unlink()
    catalog: dict[str, dict] = {}
    for key, sequence in ICON_SEQUENCE.items():
        src = find_pdf_or_ai(key)
        tmp = DEST / ".tmp" / f"{key}.png"
        render_page(src, tmp, SCALE_ICON)
        im = Image.open(tmp).convert("RGBA")
        blobs = find_icon_blobs(im, min_side=int(40 * SCALE_ICON / 2))
        if len(blobs) > len(sequence):
            blobs = sorted(blobs, key=lambda b: b[4], reverse=True)[: len(sequence)]
            blobs.sort(key=lambda b: b[0])
        print(f"icons {key}: {len(blobs)} blobs (attendu {len(sequence)})")
        n = min(len(blobs), len(sequence))
        if n != len(sequence):
            print("  ATTENTION décalage blobs/labels", [(b[0], b[2] - b[0], b[3] - b[1]) for b in blobs])
        for blob, spec in zip(blobs[:n], sequence):
            nom, visuel, couleur = spec
            if nom in catalog:
                continue
            crop = crop_pad(im, blob[:4], pad=2)
            out = icon_dir / f"{nom}.png"
            crop.save(out)
            catalog[nom] = {
                "slug": nom,
                "titre": nom,
                "visuel": visuel,
                "couleur": couleur,
                "fichier": f"icones/{nom}.png",
                "source": key,
                "px": f"{crop.width}×{crop.height}",
            }
            print("  icon", nom, crop.size)
        tmp.unlink()
    tmpdir = DEST / ".tmp"
    if tmpdir.exists():
        shutil.rmtree(tmpdir)
    return list(catalog.values())


def export_schemas_and_icons() -> list[dict]:
    schema_dir = DEST / "schemas"
    schema_dir.mkdir(parents=True, exist_ok=True)
    for key, meta in SCHEMA_MAP.items():
        src = find_pdf_or_ai(key)
        dest = schema_dir / f"{meta['slug']}.png"
        print("render", src.name, "→", dest.name)
        render_page(src, dest, SCALE_SCHEMA)
    return export_icons_only()


def export_kakemono_and_logos() -> None:
    logos = DEST / "logos"
    logos.mkdir(parents=True, exist_ok=True)
    for name in ("logo signature.png", "Oser pour innover QR.png", "Capture logos 2026 32 partenaires.JPG"):
        src = KIT / name
        if src.exists():
            shutil.copy2(src, logos / name)
    kak = next(KIT.glob("Panneau*.ai"))
    dest = DEST / "supports" / "kakemono-generique.png"
    print("render kakemono")
    render_page(kak, dest, SCALE_KAKEMONO)


def write_readme(icons: list[dict]) -> None:
    lines = [
        "# Kit com, logos et icônes — documents de conception",
        "",
        "Ce dossier **n’entre pas dans les paquets SCORM**. `build.sh` ne zippe que `modules/`.",
        "Ce sont des **références et guides** pour la conception (charte, schémas, icônes, motion).",
        "",
        "Source d’origine : `~/Desktop/KIT COM et LOGOS` (importées telles quelles dans `sources/`).",
        "",
        "## Arborescence",
        "",
        "- `sources/` — originaux (AI, PDF, PPTX, DOCX, PNG)",
        "- `schemas/` — schémas fascicules exportés en PNG transparent",
        "- `icones/` — pictogrammes du cycle, **nommés par concept**",
        "- `logos/` — signature Oser pour innover, QR, bandeau 32 partenaires",
        "- `charte/` — médias extraits de la charte graphique vidéos (motion + images)",
        "- `supports/` — kakemono générique en PNG",
        "",
        "## Icônes du cycle de l’innovation",
        "",
        "Pictogrammes isolés des schémas 2 à 5, **nommés comme sur le schéma 5**, PNG sans fond (extérieur transparent).",
        "Couleurs : **orange** = phase recherche et expérimentation ; **marine** = phase propulsion ; **vert** = phase utilité collective.",
        "",
        "| Fichier | Concept | Visuel | Couleur |",
        "|---|---|---|---|",
    ]
    for ic in icons:
        lines.append(f"| `{ic['fichier']}` | **{ic['titre']}** | {ic['visuel']} | {ic['couleur']} |")
    lines += [
        "",
        "Aperçu :",
        "",
    ]
    for ic in icons:
        lines.append(f"![{ic['titre']}]({ic['fichier']})")
        lines.append("")
    lines += [
        "## Schémas (PNG)",
        "",
        "| Fichier | Contenu |",
        "|---|---|",
    ]
    for meta in SCHEMA_MAP.values():
        lines.append(f"| `schemas/{meta['slug']}.png` | {meta['titre']} |")
    lines += [
        "",
        "## Charte graphique vidéos",
        "",
        "Originaux : `sources/Charte graphique vidéos MOOC.pptx` et `sources/Modèle type Oser pour innover.pptx`.",
        "",
        "Motion extrait dans `charte/motion/` :",
        "",
        "- `logo-standard-anime-sonorise.mp4`",
        "- `logo-expert-temoignage-anime-sonorise.mp4`",
        "- `jingle-a.wav` / `jingle-b.wav`",
        "- `bandeau-intervenant.mp4`",
        "- `transition.mp4`",
        "- `exemples-illustrations-animees.mp4`",
        "- `texte-anime-1.mp4` … `texte-anime-4.mp4`",
        "",
        "Le PPTX `icones et images cycle inno MH.pptx` contient le même cycle (formes natives PowerPoint, pas d’images liées).",
        "",
        "## Logos et supports",
        "",
        "- `logos/logo signature.png` — logotype OSER POUR INNOVER + visuel neuronal",
        "- `logos/Oser pour innover QR.png`",
        "- `logos/Capture logos 2026 32 partenaires.JPG` — fondateurs / partenaires / financeur",
        "- `supports/kakemono-generique.png` — panneau BAT",
        "",
        "Le ZIP `transfer_*.zip` du bureau n’a pas été recopié : il dupliquait déjà les AI/PDF des schémas.",
        "",
    ]
    (DEST / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (DEST / "icones" / "catalogue.json").write_text(
        json.dumps(icons, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    copy_sources()
    extract_charte_media()
    icons = export_schemas_and_icons()
    export_kakemono_and_logos()
    write_readme(icons)
    print("OK", DEST)
    print("icones:", [i["slug"] for i in icons])


if __name__ == "__main__":
    main()
