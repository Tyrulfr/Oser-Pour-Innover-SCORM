#!/usr/bin/env python3
"""Exporte chaque incrustation en PNG charte (1920×1080, fond transparent).

Destination : authoring/Kit-com-V2/incrustation/
Hors paquets SCORM.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "modules" / "_shared" / "incrustations.json"
ICONS = ROOT / "modules" / "_shared" / "icones"
SCHEMAS = ROOT / "modules" / "_shared" / "schemas"
FONTS = ROOT / "authoring" / "Kit-com-V2" / "charte" / "fonts"
OUT = ROOT / "authoring" / "Kit-com-V2" / "incrustation"

W, H = 1920, 1080
INK = (29, 50, 88, 255)       # #1D3258
ORANGE = (240, 130, 26, 255)  # #F0821A
CAPTION = (29, 50, 88, 190)

PICTO = {
    "fa-lightbulb": "cycle/idee.png",
    "fa-play": "cycle/idee.png",
    "fa-pen": "cycle/creativite.png",
    "fa-circle-check": "cycle/solutions.png",
    "fa-flag-checkered": "cycle/solutions.png",
    "fa-puzzle-piece": "cycle/solutions.png",
    "fa-file-magnifying-glass": "cycle/selection.png",
    "fa-link": "cycle/prototypage.png",
    "fa-stairs": "cycle/prototypage.png",
    "fa-flask": "cycle/experimentation.png",
    "fa-magnifying-glass": "cycle/decouverte.png",
    "fa-binoculars": "cycle/decouverte.png",
    "fa-location-dot": "cycle/decouverte.png",
    "fa-file-lines": "cycle/valorisation.png",
    "fa-file-signature": "cycle/valorisation.png",
    "fa-file-contract": "cycle/valorisation.png",
    "fa-book": "cycle/valorisation.png",
    "fa-diagram-project": "cycle/valorisation.png",
    "fa-person-walking": "cycle/transfert.png",
    "fa-share-nodes": "cycle/transfert.png",
    "fa-rocket": "cycle/transfert.png",
    "fa-graduation-cap": "cycle/transfert.png",
    "fa-road": "cycle/transfert.png",
    "fa-palette": "cycle/design.png",
    "fa-gear": "cycle/design.png",
    "fa-industry": "cycle/production.png",
    "fa-store": "cycle/production.png",
    "fa-bullhorn": "cycle/diffusion.png",
    "fa-newspaper": "cycle/diffusion.png",
    "fa-users": "cycle/adoption-impact.png",
    "fa-seedling": "cycle/adoption-impact.png",
    "fa-leaf": "cycle/adoption-impact.png",
    "fa-heart-pulse": "cycle/adoption-impact.png",
    "fa-circle-question": "incrustations/question.png",
    "fa-lock": "incrustations/secret.png",
    "fa-shield-halved": "incrustations/protection.png",
    "fa-coins": "incrustations/financement.png",
    "fa-comments-dollar": "incrustations/financement.png",
    "fa-comments": "incrustations/dialogue.png",
    "fa-comment": "incrustations/dialogue.png",
    "fa-building": "incrustations/etablissement.png",
    "fa-envelope": "incrustations/enveloppe.png",
    "fa-code": "incrustations/logiciel.png",
    "fa-trademark": "incrustations/marque.png",
    "fa-copyright": "incrustations/droit-auteur.png",
    "fa-gem": "incrustations/actif.png",
    "fa-chart-line": "incrustations/strategie.png",
    "fa-chess": "incrustations/strategie.png",
    "fa-triangle-exclamation": "incrustations/alerte.png",
    "fa-handshake": "incrustations/partenaire.png",
    "fa-scale-balanced": "incrustations/equilibre.png",
    "fa-clock": "incrustations/temps.png",
    "fa-stopwatch": "incrustations/temps.png",
    "fa-list": "cycle/valorisation.png",
    "fa-cubes": "cycle/production.png",
    "fa-bullseye": "incrustations/cible.png",
    "fa-code-branch": "incrustations/pivot.png",
    "fa-arrows-rotate": "incrustations/pivot.png",
    "fa-shuffle": "incrustations/pivot.png",
    "fa-address-book": "incrustations/contact.png",
    "fa-user": "incrustations/contact.png",
    "fa-circle": "incrustations/sans.png",
}

_FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
_ICON_CACHE: dict[tuple[str, int], Image.Image] = {}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (weight, size)
    if key not in _FONT_CACHE:
        names = {
            "regular": "OpenSans-Regular.ttf",
            "semi": "OpenSans-SemiBold.ttf",
            "bold": "OpenSans-Bold.ttf",
            "extra": "OpenSans-ExtraBold.ttf",
        }
        _FONT_CACHE[key] = ImageFont.truetype(str(FONTS / names[weight]), size)
    return _FONT_CACHE[key]


def picto(name: str | None, size: int = 96) -> Image.Image:
    file = PICTO.get(name or "", "incrustations/question.png")
    key = (file, size)
    if key not in _ICON_CACHE:
        im = Image.open(ICONS / file).convert("RGBA")
        im = im.resize((size, size), Image.Resampling.LANCZOS)
        _ICON_CACHE[key] = im
    return _ICON_CACHE[key].copy()


def split_parts(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\s*(?:→|->|\||⇄)\s*", str(text or "")) if p.strip()]


def wrap_text(text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = str(text or "").split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def text_block(text: str, weight: str, size: int, max_w: int, fill=INK, align="center", leading=None) -> Image.Image:
    fnt = font(weight, size)
    lines = wrap_text(text, fnt, max_w)
    lead = leading or int(size * 1.18)
    h = lead * len(lines)
    im = Image.new("RGBA", (max_w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    y = 0
    for line in lines:
        tw = fnt.getlength(line)
        x = 0 if align == "left" else (max_w - tw) / 2
        dr.text((x, y), line, font=fnt, fill=fill)
        y += lead
    return im


def stack(parts: list[Image.Image], gap=16, align="center") -> Image.Image:
    parts = [p for p in parts if p is not None]
    if not parts:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    w = max(p.width for p in parts)
    h = sum(p.height for p in parts) + gap * (len(parts) - 1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    for p in parts:
        x = 0 if align == "left" else (w - p.width) // 2
        im.alpha_composite(p, (x, y))
        y += p.height + gap
    return im


def row(parts: list[Image.Image], gap=16, align="center") -> Image.Image:
    parts = [p for p in parts if p is not None]
    if not parts:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    h = max(p.height for p in parts)
    w = sum(p.width for p in parts) + gap * (len(parts) - 1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = 0
    for p in parts:
        y = 0 if align == "top" else (h - p.height) // 2
        im.alpha_composite(p, (x, y))
        x += p.width + gap
    return im


def cell(texte: str, icone: str | None = None, detail: str = "", w: int = 260) -> Image.Image:
    bits = []
    if icone:
        bits.append(picto(icone, 72))
    bits.append(text_block(texte, "extra", 26, w))
    if detail:
        bits.append(text_block(detail, "semi", 18, w, fill=CAPTION))
    return stack(bits, gap=8)


def arrow(txt="→", size=56) -> Image.Image:
    """Flèches dessinées : Open Sans n’a pas → / ⇄."""
    dual = txt in ("⇄", "↔", "<>")
    w, h = (86, 48) if dual else (54, 40)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    cy = h // 2

    def chevron(x0, x1, y, flip=False):
        if flip:
            x0, x1 = x1, x0
        dr.line([(x0, y), (x1 - 8, y)], fill=ORANGE, width=6)
        dr.polygon([(x1 - 14, y - 10), (x1, y), (x1 - 14, y + 10)], fill=ORANGE)

    if dual:
        chevron(10, w - 10, cy - 8)
        chevron(10, w - 10, cy + 8, flip=True)
    else:
        chevron(6, w - 4, cy)
    return im


def grid(cells: list[Image.Image], cols: int, gap=14) -> Image.Image:
    if not cells:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    cols = max(1, cols)
    cw = max(c.width for c in cells)
    ch = max(c.height for c in cells)
    rows = (len(cells) + cols - 1) // cols
    im = Image.new("RGBA", (cols * cw + (cols - 1) * gap, rows * ch + (rows - 1) * gap), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        r, col = divmod(i, cols)
        x = col * (cw + gap) + (cw - c.width) // 2
        y = r * (ch + gap)
        im.alpha_composite(c, (x, y))
    return im


def compose_hd(overlay: Image.Image) -> Image.Image:
    if overlay.size == (W, H):
        return overlay
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = (W - overlay.width) // 2
    y = (H - overlay.height) // 2
    canvas.alpha_composite(overlay, (max(24, x), max(24, y)))
    return canvas


def schema_16x9(path: str, titre: str = "") -> Image.Image:
    """Schéma important : canvas 16:9, pas de cadre, schéma au plus grand."""
    src = SCHEMAS / Path(path).name
    im = Image.open(src).convert("RGBA")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    margin = 48
    title_h = 80 if titre else 0
    max_w, max_h = W - margin * 2, H - margin * 2 - title_h
    scale = min(max_w / im.width, max_h / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (W - nw) // 2
    y = margin + title_h + (max_h - nh) // 2
    canvas.alpha_composite(im, (x, y))
    if titre:
        tb = text_block(titre, "extra", 36, W - 96)
        canvas.alpha_composite(tb, ((W - tb.width) // 2, margin))
    return canvas


def frise(parts: list[str], icons: list[str] | None = None) -> Image.Image:
    bits = []
    for i, part in enumerate(parts):
        if i:
            bits.append(arrow())
        ico = icons[i] if icons and i < len(icons) else None
        bits.append(cell(part, ico, w=240))
    return row(bits, gap=12)


def render_item(item: dict) -> Image.Image:
    vue = item.get("vue") or ""
    typ = item.get("type") or ""
    ecran = item.get("ecran") or item.get("schema") or ""
    titre = item.get("titre") or ""
    caption = item.get("caption") or ""
    icone = item.get("icone")
    image = item.get("image")

    if image:
        return schema_16x9(image, ecran)

    if vue == "texte" or typ in ("concept", "acronyme") and not vue:
        bits = []
        if icone or typ != "acronyme":
            bits.append(picto(icone or "fa-lightbulb", 110))
        size = 56 if typ == "acronyme" and len(ecran) <= 8 else 42
        bits.append(text_block(ecran, "extra", size, 1280))
        extra = item.get("developpe") or caption
        if extra:
            bits.append(text_block(extra, "semi", 24, 1100, fill=CAPTION))
        return stack(bits, gap=14)

    if vue == "deux-messages":
        bits = [picto(icone or "fa-comments", 96)]
        for msg in item.get("messages") or [ecran]:
            bits.append(text_block(msg, "extra", 38, 1200))
        return stack(bits, gap=12)

    if vue in ("grille", "successifs"):
        cells_data = item.get("cellules") or []
        cols = item.get("colonnes") or (3 if vue == "successifs" else (2 if len(cells_data) != 3 else 3))
        if len(cells_data) == 4:
            cols = item.get("colonnes") or 4
        if len(cells_data) >= 6 and not item.get("colonnes"):
            cols = 3
        cells = [cell(c.get("texte", ""), c.get("icone"), c.get("detail", ""), w=250) for c in cells_data]
        bits = []
        if titre:
            bits.append(text_block(titre, "bold", 28, 1200, fill=CAPTION))
        bits.append(grid(cells, cols))
        if caption:
            bits.append(text_block(caption, "semi", 22, 1100, fill=CAPTION))
        return stack(bits, gap=16)

    if vue == "liste":
        rows = []
        for ligne in item.get("lignes") or []:
            rows.append(row([picto("fa-circle-check", 40), text_block(ligne, "bold", 26, 720, align="left")], gap=12))
        bits = []
        if titre:
            bits.append(text_block(titre, "bold", 28, 800, fill=CAPTION))
        bits.append(stack(rows, gap=10, align="left"))
        return stack(bits, gap=14)

    if vue in ("frise", "etapes", "pivot"):
        parts = split_parts(item.get("schema") or ecran)
        bits = []
        if titre:
            bits.append(text_block(titre, "bold", 28, 1400, fill=CAPTION))
        bits.append(frise(parts, item.get("icones")))
        if caption:
            bits.append(text_block(caption, "semi", 22, 1200, fill=CAPTION))
        return stack(bits, gap=16)

    if vue == "boucle":
        parts = split_parts((item.get("schema") or ecran).replace("⇄", "→"))
        icos = item.get("icones") or []
        a = cell(parts[0] if parts else "A", icos[0] if icos else None, w=320)
        b = cell(parts[1] if len(parts) > 1 else "B", icos[1] if len(icos) > 1 else None, w=320)
        bits = [row([a, arrow("⇄", 54), b], gap=18)]
        if caption:
            bits.append(text_block(caption, "semi", 22, 900, fill=CAPTION))
        return stack(bits, gap=14)

    if vue == "deux-parties":
        parties = item.get("parties") or split_parts(item.get("schema") or ecran)
        chips = []
        for i, p in enumerate(parties):
            if i:
                chips.append(text_block("ou", "extra", 28, 80, fill=ORANGE))
            num = text_block(str(i + 1), "extra", 22, 40, fill=ORANGE)
            chips.append(row([num, text_block(p, "bold", 26, 360, align="left")], gap=10))
        bits = []
        if titre:
            bits.append(text_block(titre, "bold", 26, 1100, fill=CAPTION))
        bits.append(row(chips, gap=16))
        if caption:
            bits.append(text_block(caption, "semi", 20, 1000, fill=CAPTION))
        return stack(bits, gap=14)

    if vue == "questions":
        qs = item.get("questions") or []
        qico = ["fa-flag-checkered", "fa-shuffle"]
        bits = [row([picto(qico[i] if i < 2 else "fa-circle-question", 56), text_block(q, "extra", 30, 900, align="left")], gap=14) for i, q in enumerate(qs)]
        return stack(bits, gap=16)

    if vue == "hub":
        sats = item.get("satellites") or []
        chips = [cell(s.get("texte", ""), s.get("icone"), w=240) for s in sats]
        core = cell(item.get("centre") or ecran, None, w=280)
        bits = []
        if titre:
            bits.append(text_block(titre, "bold", 26, 1000, fill=CAPTION))
        if len(chips) >= 4:
            bits.append(stack([row(chips[:2], gap=14), core, row(chips[2:4], gap=14)], gap=12))
        else:
            bits.append(stack([row(chips, gap=14), core], gap=12))
        return stack(bits, gap=14)

    if vue == "tableaux":
        cols = []
        for bloc in item.get("blocs") or []:
            lines = [text_block(bloc.get("titre", ""), "extra", 24, 360)]
            for ligne in bloc.get("lignes") or []:
                lines.append(text_block("· " + ligne, "semi", 20, 360, align="left"))
            cols.append(stack(lines, gap=8, align="left"))
        bits = []
        if titre:
            bits.append(text_block(titre, "bold", 26, 1100, fill=CAPTION))
        bits.append(row(cols, gap=28, align="top"))
        return stack(bits, gap=16)

    if vue == "horloge":
        a = stack([text_block("55", "extra", 64, 200, fill=ORANGE), text_block("minutes", "semi", 22, 200, fill=CAPTION)], gap=2)
        b = stack([text_block("5", "extra", 64, 160, fill=ORANGE), text_block("min", "semi", 22, 160, fill=CAPTION)], gap=2)
        return stack([picto("fa-clock", 96), row([a, b], gap=40), text_block("pour définir le problème · pour le résoudre", "semi", 22, 900, fill=CAPTION)], gap=14)

    if vue == "cible":
        return stack([picto("fa-bullseye", 96), frise(["Le bon problème", "La bonne solution"])], gap=16)

    if vue == "dialogue":
        return stack([picto("fa-comments", 110), text_block(ecran, "extra", 40, 1200)], gap=14)

    if vue == "morph":
        return stack([
            picto("fa-arrows-rotate", 96),
            row([cell("Culture de recherche", w=300), arrow(), cell("Culture de valorisation", w=300)], gap=12),
            text_block(ecran, "semi", 24, 1000, fill=CAPTION),
        ], gap=14)

    if vue == "traverse":
        walk = row([picto("fa-flask", 80), arrow(), picto("fa-person-walking", 80), arrow(), picto("fa-users", 80)], gap=10)
        return stack([walk, text_block(ecran, "extra", 36, 1100)], gap=16)

    if vue == "colonnes":
        left = stack([text_block("Techno Push", "extra", 26, 360), frise(["Technologie", "Produit", "Marché"])], gap=10)
        right = stack([text_block("Market Pull", "extra", 26, 360), frise(["Besoin", "Solution", "Technologie"])], gap=10)
        return row([left, text_block("vs", "extra", 32, 80, fill=ORANGE), right], gap=24)

    if vue == "puzzle":
        return stack([
            row([cell("Problème", "fa-puzzle-piece", w=240), cell("Solution", "fa-puzzle-piece", w=240)], gap=12),
            text_block("Problem–Solution Fit", "extra", 36, 800),
        ], gap=16)

    if vue == "conclusion":
        return stack([picto("fa-handshake", 110), text_block(ecran, "extra", 40, 1200)], gap=14)

    if typ == "schema" and item.get("schema"):
        parts = split_parts(item["schema"])
        if len(parts) >= 2:
            bits = [frise(parts)]
            if ecran and ecran != item["schema"]:
                bits.insert(0, text_block(ecran, "bold", 26, 1200, fill=CAPTION))
            return stack(bits, gap=14)
        return text_block(ecran or item["schema"], "extra", 40, 1200)

    return stack([picto(icone or "fa-lightbulb", 96), text_block(ecran or "Incrustation", "extra", 40, 1200)], gap=14)


def item_id(code: str, index: int, item: dict) -> str:
    raw = str(item.get("id") or "").strip()
    if raw:
        return raw
    return f"IN-{code}-{index:02d}"


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    catalogue = {
        "format": "1920×1080 PNG RGBA, fond transparent, sans cadre",
        "source": "monica",
        "charte": {
            "fonts": "Open Sans ExtraBold / Bold / SemiBold",
            "couleurs": {"marine": "#1D3258", "orange": "#F0821A", "vert": "#00AE68", "prune": "#63003C"},
            "pictos": "ensemble 1 cycle, ensemble 2 seulement si le concept n’existe pas",
            "schemas": "16:9",
        },
        "videos": [],
        "schemas": [],
    }
    total = 0
    for code, video in data.get("videos", {}).items():
        if video.get("source") != "monica":
            continue
        items = video.get("items") or []
        folder = OUT / code
        folder.mkdir(parents=True, exist_ok=True)
        entry = {
            "code": code,
            "source": "monica",
            "nb": len(items),
            "items": [],
        }
        for i, item in enumerate(items, 1):
            iid = item_id(code, i, item)
            overlay = render_item(item)
            frame = compose_hd(overlay)
            dest = folder / f"{iid}.png"
            frame.save(dest, "PNG", optimize=True)
            entry["items"].append({
                "id": iid,
                "fichier": f"incrustation/{code}/{iid}.png",
                "debut": item.get("debut", ""),
                "fin": item.get("fin", ""),
                "vue": item.get("vue") or item.get("type"),
                "ecran": item.get("ecran") or item.get("schema") or "",
                "schema16x9": bool(item.get("image")),
            })
            total += 1
            print(f"{code} {iid}")
        catalogue["videos"].append(entry)

    schemas_dir = OUT / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    for schema in data.get("schemas_fascicule") or []:
        sid = schema.get("id") or Path(schema.get("image", "")).stem
        dest = schemas_dir / f"{sid}.png"
        schema_16x9(schema["image"], schema.get("titre") or "").save(dest, "PNG", optimize=True)
        catalogue["schemas"].append({
            "id": sid,
            "fichier": f"incrustation/schemas/{sid}.png",
            "titre": schema.get("titre", ""),
            "format": "16:9",
        })
        print("schema", sid)
        total += 1

    catalogue["total"] = total
    (OUT / "catalogue.json").write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "\n".join([
            "# Incrustations — stills Monica",
            "",
            "PNG **1920×1080**, fond transparent, **sans cadre**. Dossier de conception : **hors paquets SCORM**.",
            "Uniquement les incrustations **Monica** (E3, E5–E11, E13, E14, E16–E19).",
            "",
            "- Open Sans ExtraBold / Bold / SemiBold (`charte/fonts/`)",
            "- Texte marine `#1D3258`, flèches orange `#F0821A`",
            "- Pictos et schémas seuls : pas de cartouche gris ni de carte marine",
            "- Schémas importants en **16:9** (`schemas/` + stills qui portent un schéma fascicule)",
            "",
            f"**{total}** fichiers. Catalogue machine : `catalogue.json`.",
            "",
            "Régénération : `python3 scripts/export_incrustations_png.py`",
            "",
        ]),
        encoding="utf-8",
    )
    print("total", total, "->", OUT)


if __name__ == "__main__":
    main()
