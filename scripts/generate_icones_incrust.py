#!/usr/bin/env python3
"""Génère l'ensemble 2 des pictos (incrustations) au format charte, et copie les deux ensembles vers modules/_shared."""
from __future__ import annotations

import json
import shutil
import urllib.request
from pathlib import Path

from io import BytesIO

import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "authoring" / "kit-com" / "icones"
SHARED = ROOT / "modules" / "_shared" / "icones"
OUT_NEW = KIT / "incrustations"

SIZE = 356
# Couleurs officielles de la charte / schéma 5 (phases du cycle)
ORANGE = (240, 130, 26, 255)   # #F0821A — recherche et expérimentation
MARINE = (29, 50, 88, 255)     # #1D3258 — propulsion
VERT = (0, 174, 104, 255)      # #00AE68 — utilité collective
PHASE = {"orange": ORANGE, "marine": MARINE, "vert": VERT}

CYCLE = [
    ("IDÉE.png", "idee.png"),
    ("CRÉATIVITÉ.png", "creativite.png"),
    ("SOLUTIONS.png", "solutions.png"),
    ("SÉLECTION.png", "selection.png"),
    ("PROTOTYPAGE.png", "prototypage.png"),
    ("EXPÉRIMENTATION.png", "experimentation.png"),
    ("DÉCOUVERTE.png", "decouverte.png"),
    ("VALORISATION.png", "valorisation.png"),
    ("TRANSFERT.png", "transfert.png"),
    ("DESIGN.png", "design.png"),
    ("PRODUCTION.png", "production.png"),
    ("DIFFUSION.png", "diffusion.png"),
    ("ADOPTION et IMPACT.png", "adoption-impact.png"),
]

# Ensemble 2 — concepts absents du schéma 5. Glyphs Tabler outline (même famille de trait).
NEW = [
    ("QUESTION", "question.png", "question-mark", "orange", "Point d’interrogation", "Question, incertitude, ouverture"),
    ("SECRET", "secret.png", "lock", "marine", "Cadenas", "Secret des affaires, confidentialité"),
    ("PROTECTION", "protection.png", "shield", "marine", "Bouclier", "Protection de la PI"),
    ("FINANCEMENT", "financement.png", "coins", "marine", "Pièces", "Financements, levée, aides"),
    ("DIALOGUE", "dialogue.png", "messages", "orange", "Bulles de dialogue", "Échange, conseils, langage commun"),
    ("ETABLISSEMENT", "etablissement.png", "building", "marine", "Immeuble", "Établissement, institution"),
    ("ENVELOPPE", "enveloppe.png", "mail", "marine", "Enveloppe", "Enveloppe Soleau"),
    ("LOGICIEL", "logiciel.png", "code", "marine", "Chevrons de code", "Logiciel, code source"),
    ("MARQUE", "marque.png", "registered", "vert", "Marque déposée", "Marques, signes distinctifs"),
    ("DROIT-AUTEUR", "droit-auteur.png", "copyright", "marine", "Copyright", "Droit d’auteur"),
    ("ACTIF", "actif.png", "diamond", "marine", "Diamant", "Actif immatériel"),
    ("STRATEGIE", "strategie.png", "chart-line", "marine", "Courbe", "Stratégie, veille économique"),
    ("ALERTE", "alerte.png", "alert-triangle", "orange", "Triangle d’alerte", "Point de vigilance"),
    ("PARTENAIRE", "partenaire.png", "lucide:handshake", "vert", "Poignée de main", "Partenariat, collaboration"),
    ("EQUILIBRE", "equilibre.png", "scale", "marine", "Balance", "Équilibre contractuel, exclusivité"),
    ("TEMPS", "temps.png", "clock", "orange", "Horloge", "Temps, durée, TRL"),
    ("CIBLE", "cible.png", "target", "orange", "Cible", "Problème à viser"),
    ("PIVOT", "pivot.png", "refresh", "orange", "Flèches circulaires", "Pivot, itération"),
    ("CONTACT", "contact.png", "notebook", "marine", "Carnet", "Contacts, annuaire"),
    ("SANS", "sans.png", "circle", "marine", "Cercle vide", "Absence, sans option"),
]


def disk(color: tuple[int, int, int, int]) -> Image.Image:
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.ellipse((2, 3, 353, 354), fill=color)
    return im


def fetch_glyph(name: str, target: int = 196) -> Image.Image:
    if ":" in name:
        pack, icon = name.split(":", 1)
    else:
        pack, icon = "tabler", name
    url = f"https://api.iconify.design/{pack}/{icon}.svg?color=%23ffffff&width=24&height=24"
    req = urllib.request.Request(url, headers={"User-Agent": "oser-pour-innover-charte"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        svg = resp.read()
    doc = fitz.open(stream=svg, filetype="svg")
    page = doc[0]
    pix = page.get_pixmap(alpha=True, matrix=fitz.Matrix(16, 16))
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    bbox = im.getbbox()
    if not bbox:
        raise RuntimeError(f"glyphe vide : {name}")
    im = im.crop(bbox)
    # trait blanc, alpha conservée
    pxm = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            _, _, _, a = pxm[x, y]
            if a:
                pxm[x, y] = (255, 255, 255, a)
    scale = target / max(w, h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def compose(glyph: Image.Image, color: tuple[int, int, int, int]) -> Image.Image:
    base = disk(color)
    gw, gh = glyph.size
    x = (SIZE - gw) // 2
    y = (SIZE - gh) // 2
    base.alpha_composite(glyph, (x, y))
    return base


def copy_cycle():
    dest = SHARED / "cycle"
    dest.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in CYCLE:
        src = KIT / src_name
        if not src.exists():
            raise FileNotFoundError(src)
        shutil.copy2(src, dest / dst_name)
        print("cycle", dst_name)


def generate_new():
    OUT_NEW.mkdir(parents=True, exist_ok=True)
    dest = SHARED / "incrustations"
    dest.mkdir(parents=True, exist_ok=True)
    for slug, filename, tabler, phase, visuel, usage in NEW:
        glyph = fetch_glyph(tabler)
        im = compose(glyph, PHASE[phase])
        kit_path = OUT_NEW / filename
        shared_path = dest / filename
        im.save(kit_path, "PNG")
        shutil.copy2(kit_path, shared_path)
        print("new", filename, phase, tabler)


def write_catalogue():
    cycle_meta = [
        ("IDÉE", "IDÉE.png", "idee.png", "Ampoule allumée", "orange", "fasc2-schema-2"),
        ("CRÉATIVITÉ", "CRÉATIVITÉ.png", "creativite.png", "Tête / cerveau ouvert, crayon et arc-en-ciel", "orange", "fasc2-schema-2"),
        ("SOLUTIONS", "SOLUTIONS.png", "solutions.png", "Ampoule avec coche", "orange", "fasc2-schema-2"),
        ("SÉLECTION", "SÉLECTION.png", "selection.png", "Documents superposés et curseur", "orange", "fasc2-schema-2"),
        ("PROTOTYPAGE", "PROTOTYPAGE.png", "prototypage.png", "Maillon / lien", "orange", "fasc2-schema-2"),
        ("EXPÉRIMENTATION", "EXPÉRIMENTATION.png", "experimentation.png", "Fiole (erlenmeyer)", "orange", "fasc2-schema-2"),
        ("DÉCOUVERTE", "DÉCOUVERTE.png", "decouverte.png", "Clé", "marine", "fasc2-schema-3"),
        ("VALORISATION", "VALORISATION.png", "valorisation.png", "Document et crayon", "marine", "fasc2-schema-3"),
        ("TRANSFERT", "TRANSFERT.png", "transfert.png", "Avion en papier", "marine", "fasc2-schema-3"),
        ("DESIGN", "DESIGN.png", "design.png", "Crayon et clé à molette", "vert", "fasc2-schema-4"),
        ("PRODUCTION", "PRODUCTION.png", "production.png", "Imprimante", "vert", "fasc2-schema-4"),
        ("DIFFUSION", "DIFFUSION.png", "diffusion.png", "Mégaphone", "vert", "fasc2-schema-4"),
        ("ADOPTION et IMPACT", "ADOPTION et IMPACT.png", "adoption-impact.png", "Mains qui portent une ampoule", "vert", "fasc2-schema-4"),
    ]
    ensemble1 = []
    for slug, fichier, runtime, visuel, couleur, source in cycle_meta:
        ensemble1.append({
            "slug": slug,
            "titre": slug,
            "visuel": visuel,
            "couleur": couleur,
            "fichier": f"icones/{fichier}",
            "runtime": f"icones/cycle/{runtime}",
            "source": source,
            "px": "356×356",
            "ensemble": "cycle",
        })
    ensemble2 = []
    for slug, filename, tabler, phase, visuel, usage in NEW:
        ensemble2.append({
            "slug": slug,
            "titre": slug.replace("-", " ").replace("ETABLISSEMENT", "ÉTABLISSEMENT").replace("STRATEGIE", "STRATÉGIE").replace("EQUILIBRE", "ÉQUILIBRE").replace("DROIT AUTEUR", "DROIT D’AUTEUR"),
            "visuel": visuel,
            "usage": usage,
            "couleur": phase,
            "fichier": f"icones/incrustations/{filename}",
            "runtime": f"icones/incrustations/{filename}",
            "source": "ensemble-2-incrustations",
            "px": "356×356",
            "ensemble": "incrustations",
        })
    # titres accentués
    titles = {
        "ETABLISSEMENT": "ÉTABLISSEMENT",
        "DROIT-AUTEUR": "DROIT D’AUTEUR",
        "STRATEGIE": "STRATÉGIE",
        "EQUILIBRE": "ÉQUILIBRE",
    }
    for item in ensemble2:
        item["titre"] = titles.get(item["slug"], item["slug"])
    data = {
        "regle": "Préférer l’ensemble 1 (cycle, schéma 5). L’ensemble 2 complète les concepts absents du cycle. Couleurs : orange = recherche et expérimentation, marine = propulsion, vert = utilité collective.",
        "ensembles": [
            {
                "id": "cycle",
                "titre": "Ensemble 1 — pictogrammes du cycle de l’innovation",
                "source": "schéma 5",
                "priorite": 1,
                "icones": ensemble1,
            },
            {
                "id": "incrustations",
                "titre": "Ensemble 2 — pictogrammes d’incrustation",
                "source": "complément charte",
                "priorite": 2,
                "icones": ensemble2,
            },
        ],
    }
    (KIT / "catalogue.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("catalogue", KIT / "catalogue.json")


def main():
    SHARED.mkdir(parents=True, exist_ok=True)
    copy_cycle()
    generate_new()
    write_catalogue()


if __name__ == "__main__":
    main()
