#!/usr/bin/env python3
"""Charte graphique Oser pour innover — même modèle que la charte Université Paris-Saclay."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "authoring" / "Kit-com-V2"
FONTS = KIT / "charte" / "fonts"
VAR = KIT / "logos" / "variantes"
OUT = KIT / "charte" / "Charte-graphique-Oser-pour-innover.pdf"

W, H = A4
M = 36
PRUNE = HexColor("#63003C")
BLEU = HexColor("#1D3258")
ORANGE = HexColor("#F0821A")
VERT = HexColor("#00AE68")
GRIS = HexColor("#313E48")
GRIS_C = HexColor("#7C8790")
GRIS_BG = HexColor("#F3F4F6")
GRIS_L = HexColor("#D6DBDF")
ROUGE_NON = HexColor("#C60B46")

pdfmetrics.registerFont(TTFont("OS", str(FONTS / "OpenSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("OSB", str(FONTS / "OpenSans-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("OSBD", str(FONTS / "OpenSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("OSEB", str(FONTS / "OpenSans-ExtraBold.ttf")))


def rgb_cmyk(hex_color: str) -> tuple[int, int, int, tuple[int, int, int, int]]:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    rf, gf, bf = r / 255, g / 255, b / 255
    k = 1 - max(rf, gf, bf)
    if k >= 0.999:
        return r, g, b, (0, 0, 0, 100)
    c = round((1 - rf - k) / (1 - k) * 100)
    m = round((1 - gf - k) / (1 - k) * 100)
    y = round((1 - bf - k) / (1 - k) * 100)
    return r, g, b, (c, m, y, round(k * 100))


def wrap(c: canvas.Canvas, text: str, font: str, size: float, x: float, y: float, max_w: float, leading: float, color=GRIS, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines):
        if align == "right":
            c.drawRightString(x + max_w, y - i * leading, line)
        else:
            c.drawString(x, y - i * leading, line)
    return len(lines) * leading


def pstyle(name, font, size, color, leading, align="left"):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        textColor=color,
        leading=leading,
        alignment={"left": 0, "center": 1, "right": 2}[align],
    )


def para(c, html, x, y, w, h, style):
    p = Paragraph(html, style)
    p.wrapOn(c, w, h)
    p.drawOn(c, x, y - p.height)
    return p.height


def img(c, path, x, y, w, h, preserve=True):
    p = Path(path)
    if not p.exists():
        return
    ir = ImageReader(str(p))
    iw, ih = ir.getSize()
    if preserve:
        scale = min(w / iw, h / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(ir, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")
    else:
        c.drawImage(ir, x, y, w, h, mask="auto")


def footer(c, n, total=14, url="Programme Oser pour innover"):
    c.setFillColor(PRUNE)
    c.setFont("OSB", 8)
    c.drawString(M, 18, url)
    c.setFillColor(GRIS_C)
    c.setFont("OS", 8)
    c.drawRightString(W - M, 18, f"Charte graphique — Oser pour innover   {n}")
    c.setStrokeColor(GRIS_L)
    c.setLineWidth(0.4)
    c.line(M, 28, W - M, 28)


def header_title(c, title, subtitle=None):
    img(c, VAR / "logo-wordmark-couleur.png", M, H - 62, 118, 38)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 16)
    c.drawString(168, H - 42, title)
    if subtitle:
        c.setFillColor(black)
        c.setFont("OSBD", 16)
        c.drawString(168, H - 60, subtitle)


def swatch(c, x, y, w, h, hex_color, title, extra_lines):
    col = HexColor(hex_color)
    c.setFillColor(col)
    c.rect(x, y, w, h, fill=1, stroke=0)
    bright = hex_color.upper() in {"#F0821A", "#00AE68", "#D6DBDF"}
    c.setFillColor(black if bright else white)
    c.setFont("OSBD", 8)
    c.drawString(x + 8, y + h - 16, title)
    c.setFont("OS", 7)
    ty = y + h - 28
    for line in extra_lines:
        c.drawString(x + 8, ty, line)
        ty -= 10


def page1(c):
    img(c, VAR / "logo-wordmark-couleur.png", M, H - 58, 130, 40)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 16)
    c.drawString(178, H - 38, "Charte graphique :")
    c.drawString(178, H - 56, "les essentiels de notre marque")
    c.setFillColor(GRIS_C)
    c.setFont("OS", 8)
    c.drawRightString(W - M, H - 38, "Octobre 2026")

    body = pstyle("b", "OS", 8.2, GRIS, 11.2)
    intro = (
        "Oser pour innover est le programme de sensibilisation "
        "et d’acculturation à l’innovation des cadres de l’ESR, "
        "coporté par l’Université Paris-Saclay, AgroParisTech et "
        "l’Institut d’Optique Graduate School, au sein d’Innovation "
        "Alliance Université Paris-Saclay, et financé par France 2030."
        "<br/><br/>Ce document décrit les consignes et points de "
        "repère qui permettent de contribuer au rayonnement du "
        "programme et de la formation <b>L’Esprit d’innover</b> :"
        "<br/>• décrypter les fondamentaux de l’innovation,"
        "<br/>• libérer le potentiel d’agir des chercheuses et chercheurs,"
        "<br/>• relier recherche, protection, transfert et impact,"
        "<br/>• parler un langage commun avec l’écosystème."
        "<br/><br/>Ce guide fixe les standards de notre identité "
        "visuelle. Il est indispensable de les respecter pour "
        "garantir la cohérence des supports (vidéos, fascicules, "
        "SCORM, kakemono, diaporamas)."
        "<br/><br/>Vous y trouverez :"
        "<br/>• logo, couleurs, typo et règles d’utilisation,"
        "<br/>• icônes du cycle, pictos d’incrustation, schémas MOOC,"
        "<br/>• exemples d’usage (vidéo, formation, partenaires)."
        "<br/><br/>Une charte graphique est un outil de travail. "
        "Pour un cas particulier, contactez la Direction de la "
        "marque et de la communication de l’Université Paris-Saclay, "
        "objet «&nbsp;Oser pour innover — marque&nbsp;» :"
        "<br/><b>communication@universite-paris-saclay.fr</b>"
    )
    para(c, intro, M, H - 78, 175, 680, body)

    c.setFillColor(GRIS_BG)
    c.roundRect(222, 42, 337, 720, 4, fill=1, stroke=0)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(236, 742, "Notre logotype")
    img(c, VAR / "logo-couleur.png", 236, 688, 175, 48)
    c.setFillColor(GRIS)
    c.setFont("OSBD", 8)
    c.drawString(236, 676, "En couleur")
    wrap(c, "RVB à l’écran, CMJN à l’impression. Version officielle, avec visuel neuronal.", "OS", 7, 236, 664, 168, 9, GRIS)

    img(c, VAR / "logo-wordmark-noir.png", 236, 600, 160, 42)
    c.setFillColor(GRIS)
    c.setFont("OSBD", 8)
    c.drawString(236, 588, "En noir")
    wrap(c, "Uniquement si la reproduction couleur est impossible.", "OS", 7, 236, 576, 168, 9, GRIS)

    c.setFillColor(PRUNE)
    c.rect(236, 508, 168, 52, fill=1, stroke=0)
    img(c, VAR / "logo-wordmark-blanc.png", 244, 516, 152, 36)
    c.setFillColor(GRIS)
    c.setFont("OSBD", 8)
    c.drawString(236, 496, "En défonce")
    wrap(c, "Fonds foncés ou photo, si la lisibilité est garantie.", "OS", 7, 236, 484, 168, 9, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(416, 742, "Notre palette")
    swatch(c, 416, 658, 128, 72, "#63003C", "La couleur prune", [
        "Pantone 229",
        "CMJN 24 100 17 60",
        "RVB 99 0 60",
        "HEX #63003C",
    ])
    swatch(c, 416, 598, 62, 52, "#1D3258", "Bleu", ["RVB 29 50 88", "#1D3258"])
    swatch(c, 482, 598, 62, 52, "#F0821A", "Orange", ["RVB 240 130 26", "#F0821A"])
    swatch(c, 416, 538, 62, 52, "#00AE68", "Vert", ["RVB 0 174 104", "#00AE68"])
    swatch(c, 482, 538, 62, 52, "#D6DBDF", "Gris", ["#D6DBDF"])
    c.setFillColor(GRIS_C)
    c.setFont("OS", 7)
    c.drawString(416, 524, "Plus de couleurs page 3")

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(236, 448, "Notre nom de marque")
    wrap(c, "En français : Oser pour innover. Le logotype s’écrit OSER POUR INNOVER. En phrase, ne pas tout capitaliser. Baseline : Décrypter les fondamentaux et libérer son potentiel. Formation : L’Esprit d’innover.", "OS", 7.2, 236, 434, 150, 9.4, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(400, 448, "La typographie principale")
    wrap(c, "Open Sans, police libre de droit, officielle (comme l’Université Paris-Saclay). Titres numériques : Montserrat toléré dans les grains SCORM. En savoir plus page 4.", "OS", 7.2, 400, 434, 145, 9.4, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(236, 330, "Le visuel neuronal")
    img(c, VAR / "visuel-neuronal.png", 236, 52, 68, 260)
    wrap(c, "Le réseau de bulles (prune, bleu, orange, vert) est le signe distinctif du programme. Il se couple à droite ou à gauche du logotype, jamais déformé, jamais recoloré hors palette.", "OS", 7.2, 316, 312, 220, 9.5, GRIS)

    footer(c, 1)


def page2(c):
    header_title(c, "Notre logotype", "Règles d’utilisation")

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(M, H - 88, "Logo officiel")
    img(c, VAR / "logo-couleur.png", M, H - 150, 165, 48)
    wrap(c, "Le logotype prune, avec visuel neuronal, est le logo officiel du programme. Il s’utilise sur toute communication émise par Oser pour innover (formation, vidéos, fascicules, site, kakemono).", "OS", 7.4, M, H - 162, 165, 10, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(216, H - 88, "Wordmark seul")
    img(c, VAR / "logo-wordmark-couleur.png", 216, H - 150, 150, 46)
    wrap(c, "Sans visuel neuronal, lorsque l’espace est trop étroit (bandeau vidéo, favicon, pied de page). Ne pas inventer d’autre composition.", "OS", 7.4, 216, H - 162, 155, 10, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(386, H - 88, "Logo cartouche")
    img(c, VAR / "logo-cartouche-prune.png", 386, H - 150, 170, 50)
    wrap(c, "Blanc dans un cartouche prune : pour les entités externes et lorsque le programme est partenaire, non commanditaire.", "OS", 7.4, 386, H - 162, 172, 10, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 250, "Quel fichier utiliser ?")
    wrap(c, "Écran : fichiers PNG en RVB (authoring/Kit-com-V2/logos/). Impression : PNG haute définition ou AI/PDF des sources. Ne pas extraire le logo d’une photo ou d’une capture.", "OS", 8, M, H - 266, 250, 11, GRIS)
    wrap(c, "Baseline : « Décrypter les fondamentaux et libérer son potentiel » peut accompagner le logo sur les supports programme (kakemono, génériques vidéo). Pas obligatoire sur chaque grain SCORM.", "OS", 8, 300, H - 266, 258, 11, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 330, "Utilisation sur fond")
    # mosaïque fonds
    boxes = [
        (M, H - 430, W / 2 - 42, 86, white, "logo-couleur.png", GRIS_L),
        (W / 2 + 6, H - 430, W / 2 - 42, 86, HexColor("#F8E6C8"), "logo-couleur.png", None),
        (M, H - 522, W / 2 - 42, 86, BLEU, "logo-blanc.png", None),
        (W / 2 + 6, H - 522, W / 2 - 42, 86, PRUNE, "logo-blanc.png", None),
        (M, H - 614, W / 2 - 42, 86, ORANGE, "logo-blanc.png", None),
        (W / 2 + 6, H - 614, W / 2 - 42, 86, VERT, "logo-blanc.png", None),
    ]
    for x, y, w, hgt, bg, fn, stroke in boxes:
        c.setFillColor(bg)
        c.rect(x, y, w, hgt, fill=1, stroke=0)
        if stroke:
            c.setStrokeColor(stroke)
            c.setLineWidth(0.4)
            c.rect(x, y, w, hgt, fill=0, stroke=1)
        img(c, VAR / fn, x + 18, y + 16, w - 36, hgt - 32)

    wrap(c, "Couleur sur fonds clairs unis. Défonce sur fonds foncés (prune, bleu, orange, vert) si le contraste est suffisant. Le visuel neuronal se lit mieux sur blanc ou gris très clair.", "OS", 7.5, M, H - 628, 520, 10, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 668, "Les interdictions — merci de ne pas :")
    bullets = [
        "Utiliser le noir quand la couleur est possible",
        "Déformer, étirer, incliner ou contourner le logo",
        "Changer les couleurs ou recréer le visuel neuronal",
        "Le poser sur un fond illisible ou trop chargé",
        "Ajouter une ombre, un filet ou un slogan non validé",
        "Descendre sous la taille minimale (page 12)",
        "Utiliser le cartouche blanc + logo prune (non autorisé)",
    ]
    wrap_y = H - 684
    c.setFont("OS", 7.6)
    c.setFillColor(GRIS)
    for b in bullets:
        c.drawString(M + 8, wrap_y, "•  " + b)
        wrap_y -= 11

    # tampon NON
    c.setFillColor(ROUGE_NON)
    c.circle(W - 78, 78, 22, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("OSBD", 9)
    c.drawCentredString(W - 78, 74, "NON")

    footer(c, 2)


def page3(c):
    header_title(c, "Éléments de la charte", "Notre palette")
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 88, "Palette principale")

    swatch(c, M, H - 250, 250, 148, "#63003C", "La couleur prune du programme", [
        "(couleur institutionnelle Paris-Saclay)",
        "Pantone 229",
        "CMJN 24 100 17 60",
        "RVB 99 0 60",
        "HEX #63003C",
    ])
    specs = [
        ("#1D3258", "Bleu marine — phase propulsion", 250),
        ("#F0821A", "Orange — phase recherche", 186),
        ("#00AE68", "Vert — phase utilité collective", 122),
        ("#D6DBDF", "Gris clair — fonds et filets", 58),
    ]
    x0 = M + 262
    for hex_c, title, yoff in [
        ("#1D3258", "Bleu marine", H - 134),
        ("#7C8790", "Gris moyen", H - 192),
        ("#D6DBDF", "Gris clair", H - 250),
    ]:
        rr, gg, bb, kk = rgb_cmyk(hex_c)
        swatch(c, x0, yoff, 258, 50, hex_c, title, [f"RVB {rr} {gg} {bb}   {hex_c}", f"CMJN {' '.join(map(str, kk))}"])

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 280, "Palette du cycle de l’innovation")
    wrap(c, "Les trois couleurs d’accompagnement structurent le récit pédagogique. Elles ne remplacent jamais la prune pour le logotype.", "OS", 8, M, H - 296, 520, 11, GRIS)

    phases = [
        ("#F0821A", "Phase recherche", "et expérimentation", "Idée, créativité, solutions, sélection, prototypage, expérimentation"),
        ("#1D3258", "Phase propulsion", "", "Découverte, valorisation, transfert"),
        ("#00AE68", "Phase utilité", "collective", "Design, production, diffusion, adoption et impact"),
    ]
    for i, (hx, t1, t2, desc) in enumerate(phases):
        x = M + i * 175
        swatch(c, x, H - 430, 165, 100, hx, t1, [t2] if t2 else [])
        wrap(c, desc, "OS", 7.2, x, H - 444, 165, 9.5, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 500, "Teintes du visuel neuronal")
    wrap(c, "Les bulles du réseau n’introduisent pas de 5e couleur : elles reprennent prune, bleu, orange et vert. Les versions pastel (génériques vidéo) sont réservées aux fonds animés, jamais au logotype.", "OS", 8, M, H - 516, 520, 11, GRIS)

    for i, hx in enumerate(["#63003C", "#1D3258", "#F0821A", "#00AE68"]):
        c.setFillColor(HexColor(hx))
        c.circle(M + 28 + i * 46, H - 575, 16, fill=1, stroke=0)
    # pastels
    pastels = ["#C9A3B6", "#A8B0C4", "#F5C99A", "#9FDBC4"]
    for i, hx in enumerate(pastels):
        c.setFillColor(HexColor(hx))
        c.circle(M + 260 + i * 46, H - 575, 16, fill=1, stroke=0)
    c.setFillColor(GRIS)
    c.setFont("OS", 7.5)
    c.drawString(M, H - 604, "Plein (supports print, icônes, schémas)")
    c.drawString(M + 248, H - 604, "Pastel (motion, fonds, incrustations douces)")

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 640, "Usages")
    usage = (
        "• Prune : marque, titres, logo, éléments institutionnels.<br/>"
        "• Orange : amont du cycle, alertes pédagogiques, intro/outro « avant la vidéo ».<br/>"
        "• Bleu : propulsion, contrats, PI, schémas de transfert.<br/>"
        "• Vert : impact, adoption, validation, incrustations « concept acquis ».<br/>"
        "• Interface SCORM / site : les mêmes HEX, via --bordeaux, --orange, --blue, --teal.<br/>"
        "• Ne pas créer de dégradés hors prune vers bleu discrets. Pas de néon, pas d’or. Exception vidéo : bandeau intervenant = texte blanc sur fond noir."
    )
    para(c, usage, M, H - 656, 520, 120, pstyle("u", "OS", 8, GRIS, 11.2))
    footer(c, 3)


def page4(c):
    header_title(c, "Éléments de la charte", "La typographie")
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 90, "Typographie officielle")
    txt = (
        "Merci d’utiliser la police officielle d’Oser pour innover, "
        "alignée sur l’Université Paris-Saclay : <b>Open Sans</b>."
        "<br/><br/>Open Sans est un caractère humaniste sans empattement, "
        "libre de droit, conçu par Steve Matteson. Il est optimisé pour "
        "l’impression, le web et le mobile, et disponible sur Google Fonts "
        "et Adobe Fonts."
        "<br/><br/>Dans la formation SCORM, <b>Montserrat</b> peut être "
        "conservé pour les titres de grains (hiérarchie déjà en place). "
        "Le corps de texte reste Open Sans."
        "<br/><br/>Écriture inclusive : l’utiliser dans les textes pédagogiques "
        "et institutionnels. Majuscule uniquement en tête des noms et prénoms."
    )
    para(c, txt, M, H - 108, 200, 420, pstyle("t", "OS", 8, GRIS, 11.4))

    c.setFillColor(GRIS_BG)
    c.roundRect(250, 210, 310, 560, 4, fill=1, stroke=0)
    samples = [
        ("OS", 18, "Open Sans Regular", 740),
        ("OSB", 18, "Open Sans Semibold", 620),
        ("OSBD", 18, "Open Sans Bold", 500),
        ("OSEB", 16, "Open Sans ExtraBold", 380),
    ]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    nums = "1234567890  àéèêç — &"
    for font, size, label, y in samples:
        c.setFillColor(GRIS_C)
        c.setFont("OS", 8)
        c.drawString(264, y, label)
        c.setFillColor(black)
        c.setFont(font, 13)
        c.drawString(264, y - 20, "Oser pour innover")
        c.setFont(font, 10)
        c.drawString(264, y - 38, alphabet)
        c.drawString(264, y - 52, lower)
        c.drawString(264, y - 66, nums)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 188, "Typographies de substitution")
    wrap(c, "Si Open Sans n’est pas disponible : Arial (Windows / Office) ou Helvetica (macOS). Jamais de Comic Sans, Impact, Times pour les supports programme.", "OS", 8, M, 172, 250, 11, GRIS)

    c.setFillColor(GRIS_BG)
    c.roundRect(300, 48, 120, 140, 3, fill=1, stroke=0)
    c.setFillColor(GRIS)
    c.setFont("OS", 8)
    c.drawString(312, 172, "Arial")
    c.setFont("Helvetica", 12)
    c.drawString(312, 152, "Oser pour innover")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(312, 132, "Oser pour innover")

    c.setFillColor(GRIS_BG)
    c.roundRect(432, 48, 126, 140, 3, fill=1, stroke=0)
    c.setFillColor(GRIS)
    c.setFont("OS", 8)
    c.drawString(444, 172, "Helvetica")
    c.setFont("Helvetica", 12)
    c.drawString(444, 152, "Oser pour innover")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(444, 132, "Oser pour innover")
    footer(c, 4)


def page5(c):
    header_title(c, "Éléments de la charte", "Règles d’écriture")
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 90, "Nommer le programme")
    rules = (
        "<b>1</b> En phrase : <b>Oser pour innover</b> (O, et i de innover en capitale). "
        "Le logotype reste en capitales OSER POUR INNOVER.<br/><br/>"
        "<b>2</b> Ne pas écrire « oser pour innover » tout en minuscules, ni « OSER POUR INNOVER » "
        "dans un paragraphe courant.<br/><br/>"
        "<b>3</b> La formation se nomme <b>L’Esprit d’innover</b>. "
        "C’est le titre du MOOC / SPOC, distinct du nom de programme.<br/><br/>"
        "<b>4</b> Baseline officielle : <i>Décrypter les fondamentaux et libérer son potentiel</i>. "
        "Ne pas la réécrire ni la raccourcir.<br/><br/>"
        "<b>5</b> Version courte : <b>#OserPourInnover</b>. Éviter OPI en communication externe "
        "(réservé aux dossiers internes).<br/><br/>"
        "<b>6</b> En anglais, conserver <b>Oser pour innover</b>. "
        "« Dare to innovate » n’est pas un nom de marque."
    )
    para(c, rules, M, H - 108, 250, 420, pstyle("r", "OS", 8, GRIS, 11.3))

    c.setFillColor(GRIS_BG)
    c.roundRect(300, 430, 258, 330, 4, fill=1, stroke=0)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 8)
    c.drawString(314, 740, "OUI")
    oui = [
        "Oser pour innover",
        "L’Esprit d’innover",
        "Décrypter les fondamentaux et libérer son potentiel",
        "#OserPourInnover",
        "Innovation Alliance Université Paris-Saclay",
    ]
    c.setFillColor(GRIS)
    c.setFont("OSB", 9)
    y = 722
    for i, t in enumerate(oui, 1):
        c.drawString(314, y, f"{i}  {t}")
        y -= 16

    c.setStrokeColor(GRIS_C)
    c.setLineWidth(1.4)
    c.rect(300, 250, 258, 168, fill=0, stroke=1)
    c.setFillColor(ROUGE_NON)
    c.circle(530, 400, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("OSBD", 8)
    c.drawCentredString(530, 396, "NON")
    c.setFillColor(GRIS_C)
    c.setFont("OS", 9)
    non = ["oser pour innover (tout minuscule)", "OSER POUR INNOVER en phrase", "L esprit d innover", "OPI le mooc", "Dare to Innovate", "Oser-Pour-Innover"]
    y = 392
    for t in non:
        c.drawString(314, y, t)
        y -= 14
    c.setStrokeColor(GRIS_C)
    c.line(308, 402, 548, 268)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 228, "Langage pédagogique")
    lang = (
        "• Vocabulaire de l’innovation et des fascicules (idée, preuve de concept, TRL, "
        "valorisation, transfert) plutôt que slogans.<br/>"
        "• Écriture inclusive dans les textes longs.<br/>"
        "• Majuscule en tête des prénoms des témoins et experts uniquement.<br/>"
        "• Acronymes : SATT, PI, TRL, POC, NPE — toujours développés à la première occurrence."
    )
    para(c, lang, M, 210, 520, 140, pstyle("l", "OS", 8, GRIS, 11.2))
    footer(c, 5)


def page6(c):
    header_title(c, "Éléments de la charte", "Icônes du cycle de l’innovation")
    wrap(c, "Ensemble 1 — pictogrammes du schéma 5. À utiliser en priorité dès que le concept existe (IDÉE, EXPÉRIMENTATION, TRANSFERT…). Ne pas les retracer ni les remplacer par des pictos génériques. L’ensemble 2 (page 13) complète uniquement les concepts absents du cycle. Objets isolés des schémas 8 et 9 : page 14.", "OS", 8, M, H - 88, 520, 11, GRIS)

    icons = [
        ("IDÉE.png", "IDÉE", ORANGE),
        ("CRÉATIVITÉ.png", "CRÉATIVITÉ", ORANGE),
        ("SOLUTIONS.png", "SOLUTIONS", ORANGE),
        ("SÉLECTION.png", "SÉLECTION", ORANGE),
        ("PROTOTYPAGE.png", "PROTOTYPAGE", ORANGE),
        ("EXPÉRIMENTATION.png", "EXPÉRIMENTATION", ORANGE),
        ("DÉCOUVERTE.png", "DÉCOUVERTE", BLEU),
        ("VALORISATION.png", "VALORISATION", BLEU),
        ("TRANSFERT.png", "TRANSFERT", BLEU),
        ("DESIGN.png", "DESIGN", VERT),
        ("PRODUCTION.png", "PRODUCTION", VERT),
        ("DIFFUSION.png", "DIFFUSION", VERT),
        ("ADOPTION et IMPACT.png", "ADOPTION et IMPACT", VERT),
    ]
    icdir = KIT / "icones"
    cols = 5
    box = 78
    gap = 18
    start_y = H - 210
    for i, (fn, label, col) in enumerate(icons):
        coln, row = i % cols, i // cols
        x = M + coln * (box + gap)
        y = start_y - row * (box + 36)
        img(c, icdir / fn, x, y, box, box)
        c.setFillColor(col)
        c.setFont("OSBD", 6.2)
        c.drawCentredString(x + box / 2, y - 12, label)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 268, "Règles")
    rules = (
        "• Conserver le disque coloré : il fait partie de l’icône (orange / marine / vert).<br/>"
        "• Fond transparent autour du disque. Pas d’ombre portée.<br/>"
        "• Taille minimale 24 px à l’écran, 8 mm à l’impression.<br/>"
        "• Toujours légender avec le nom du schéma 5 (IDÉE, CRÉATIVITÉ…).<br/>"
        "• Priorité au style fascicule (disques illustrés). Ne pas les remplacer par les pictos filaires du PPTX vidéo.<br/>"
        "• Fichiers : authoring/Kit-com-V2/icones/ — bibliothèque authoring/Kit-com-V2/bibliotheque/cycle/."
    )
    para(c, rules, M, 250, 520, 160, pstyle("ir", "OS", 8, GRIS, 11.2))
    footer(c, 6)


def page7(c):
    header_title(c, "Éléments de la charte", "Schémas incrustés dans le MOOC")
    wrap(c, "Style fascicule uniquement — PNG réellement posés sous les vidéos (modules/_shared/schemas/). Pas les schémas filaires du PPTX. Les planches AI complètes restent dans authoring/Kit-com-V2/schemas/.", "OS", 8, M, H - 88, 520, 11, GRIS)

    schemas = [
        ("f2-cycle-3.png", "3 phases"),
        ("f2-cycle-amont.png", "Recherche"),
        ("f2-cycle-propulsion.png", "Propulsion"),
        ("f2-cycle-adoption.png", "Utilité collective"),
        ("f2-cycle-complet.png", "Cycle complet"),
        ("f2-chaine-valo.png", "Chaîne de valorisation"),
        ("f1-ecosysteme.png", "Écosystème"),
        ("f1-pi-branches.png", "Branches de la PI"),
        ("f2-push-pull.png", "Tech-push / market-pull"),
        ("f2-finance.png", "Financement"),
        ("f2-trl.png", "Échelle TRL"),
    ]
    sdir = ROOT / "modules" / "_shared" / "schemas"
    bw, bh = 122, 100
    gapx, gapy = 9, 24
    for i, (fn, label) in enumerate(schemas):
        col, row = i % 4, i // 4
        x = M + col * (bw + gapx)
        y = H - 112 - bh - row * (bh + gapy)
        c.setFillColor(GRIS_BG)
        c.roundRect(x, y, bw, bh, 3, fill=1, stroke=0)
        img(c, sdir / fn, x + 6, y + 16, bw - 12, bh - 22)
        c.setFillColor(PRUNE)
        c.setFont("OSB", 6.4)
        c.drawString(x + 6, y + 5, label)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 210, "Style de schémas")
    st = (
        "• Style fascicule uniquement : PNG extraits des planches AI, pas les schémas filaires du PPTX vidéo.<br/>"
        "• Fonds blancs ou transparents, jamais de 3D ni d’ombres réalistes.<br/>"
        "• Une couleur de phase par étape. Titres en prune.<br/>"
        "• Overlay MOOC : modules/_shared/schemas/ — bibliothèque : authoring/Kit-com-V2/bibliotheque/schemas/"
    )
    para(c, st, M, 192, 520, 120, pstyle("s", "OS", 8, GRIS, 11.2))
    footer(c, 7)


def page8(c):
    header_title(c, "Exemples d’usage", "Vidéos et motion")
    wrap(
        c,
        "Référence = ce qui est déjà monté dans les capsules. Pictos et schémas : style fascicule, pas les pictos filaires du PPTX.",
        "OS",
        8,
        M,
        H - 86,
        520,
        11,
        GRIS,
    )
    media = KIT / "charte" / "media"

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 112, "Ouverture (capsules actuelles)")
    c.setFillColor(GRIS_BG)
    c.roundRect(M, H - 248, 523, 128, 4, fill=1, stroke=0)
    img(c, media / "ouverture-video.png", M + 8, H - 240, 507, 112)
    wrap(
        c,
        "Fond blanc. Logo 2D (visuel neuronal + wordmark prune) à gauche. Titre de la capsule en vert, 2–3 lignes. Nom de l’intervenant en vert plus petit. La pastille lecture est l’interface eMedia, pas un élément de charte. Ne pas revenir au générique 3D du PPTX.",
        "OS",
        7.4,
        M,
        H - 258,
        523,
        10,
        GRIS,
    )

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 312, "Transition")
    c.setFillColor(GRIS_BG)
    c.roundRect(M, H - 454, 250, 128, 4, fill=1, stroke=0)
    img(c, media / "transition-video.png", M + 6, H - 448, 238, 116)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M + 268, H - 312, "Bandeau intervenant")
    c.setFillColor(black)
    c.roundRect(M + 268, H - 454, 255, 128, 4, fill=1, stroke=0)
    img(c, media / "bandeau-intervenant.png", M + 274, H - 448, 243, 116)

    wrap(c, "Bandes diagonales orange / marine / prune / vert. Sans texte, sans bouton play.", "OS", 7.2, M, H - 466, 250, 9.6, GRIS)
    wrap(c, "Texte blanc sur fond noir. Nom en capitales, fonction en dessous. Pas de bandeau prune sur blanc.", "OS", 7.2, M + 268, H - 466, 255, 9.6, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 338, "Dans l’image")
    rules = (
        "• Pictos : disques du schéma 5 (ensemble 1), ensemble 2 seulement si le concept n’existe pas au cycle.<br/>"
        "• Schémas : PNG fascicules (page 7), jamais les versions filaires du PPTX.<br/>"
        "• Jingles A / B et textes animés du dossier motion restent valides."
    )
    para(c, rules, M, 322, 520, 90, pstyle("vr", "OS", 8, GRIS, 11.2))

    c.setFillColor(GRIS_BG)
    c.roundRect(M, 48, 523, 78, 4, fill=1, stroke=0)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(M + 14, 110, "Fichiers")
    wrap(
        c,
        "Stills : charte/media/ouverture-video.png · transition-video.png · bandeau-intervenant.png.  Motion : charte/motion/bandeau-intervenant.mp4 · transition.mp4 · jingle-a/b.wav · texte-anime-1 à 4.mp4.",
        "OS",
        7.3,
        M + 14,
        96,
        495,
        9.8,
        GRIS,
    )
    footer(c, 8)


def page9(c):
    header_title(c, "Exemples d’usage", "Supports print et signature")
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 90, "Kakemono générique")
    img(c, KIT / "supports" / "kakemono-generique.png", M, 200, 150, 520)
    wrap(c, "Panneau BAT : logotype + baseline, visuel neuronal, bandeau partenaires et mention France 2030. Ne pas y ajouter de visages ni de visuels hors charte.", "OS", 8, 200, H - 90, 330, 11, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(200, H - 180, "QR code officiel")
    img(c, KIT / "logos" / "Oser pour innover QR.png", 200, H - 300, 90, 90)
    wrap(c, "Seul QR autorisé pour pointer vers le programme. Fond blanc, module noir, zone de silence respectée.", "OS", 7.5, 300, H - 200, 230, 10, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(200, H - 340, "Signature des mails")
    c.setStrokeColor(GRIS_L)
    c.setLineWidth(0.6)
    c.roundRect(200, H - 500, 330, 145, 3, fill=0, stroke=1)
    img(c, VAR / "logo-wordmark-couleur.png", 210, H - 390, 110, 32)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(210, H - 412, "Prénom NOM")
    c.setFillColor(GRIS)
    c.setFont("OS", 8)
    c.drawString(210, H - 426, "Fonction — Oser pour innover")
    c.drawString(210, H - 440, "Innovation Alliance Université Paris-Saclay")
    c.drawString(210, H - 454, "prenom.nom@universite-paris-saclay.fr")
    c.setFillColor(PRUNE)
    c.setFont("OS", 7.5)
    c.drawString(210, H - 474, "Décrypter les fondamentaux et libérer son potentiel")
    wrap(c, "Une seule signature. Pas de fonds colorés, pas de citations personnelles, pas de second logo hors alliance.", "OS", 7.5, 200, H - 512, 330, 10, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(200, 160, "Pictos à réutiliser (style fascicule)")
    icdir = KIT / "icones"
    for i, fn in enumerate(["IDÉE.png", "EXPÉRIMENTATION.png", "TRANSFERT.png", "ADOPTION et IMPACT.png"]):
        img(c, icdir / fn, 200 + i * 80, 52, 72, 72)
    wrap(c, "Disques du schéma 5. Pas les cartes / puces du PPTX vidéo.", "OS", 7, 200, 48, 330, 9, GRIS)
    footer(c, 9)


def page10(c):
    header_title(c, "Endossement du logotype", "Partenaires et alliance")
    wrap(c, "Lorsque le programme s’affiche avec l’écosystème, respecter la hiérarchie : Oser pour innover d’abord, puis Innovation Alliance Université Paris-Saclay, puis partenaires, puis France 2030.", "OS", 8, M, H - 88, 520, 11, GRIS)

    img(c, KIT / "logos" / "Capture logos 2026 32 partenaires.JPG", M, H - 340, 523, 200)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 370, "Règles d’endossement")
    end = (
        "• Le logotype Oser pour innover n’est jamais plus petit que le logo d’un partenaire sur un support coproduit par le programme.<br/>"
        "• Les logos fondateurs (Université Paris-Saclay, AgroParisTech, Institut d’Optique…) restent dans leur charte d’origine.<br/>"
        "• France 2030 : mention « Financé par » + logo officiel, sans recoloration.<br/>"
        "• Interdit de recomposer le bandeau 32 logos : utiliser le fichier fourni.<br/>"
        "• Un partenaire qui cite le programme utilise le cartouche prune (page 2), pas une version « maison »."
    )
    para(c, end, M, H - 388, 520, 200, pstyle("e", "OS", 8, GRIS, 11.3))

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 200, "Coportage")
    wrap(c, "Action coportée par l’Université Paris-Saclay, AgroParisTech et l’Institut d’Optique Graduate School. Cette mention figure sur le kakemono et les génériques ; elle n’a pas à être répétée sur chaque grain SCORM.", "OS", 8, M, 184, 520, 11, GRIS)
    footer(c, 10)


def page11(c):
    header_title(c, "Exemples d’usage", "Diaporamas et formation")
    wrap(c, "Le fichier « Modèle type Oser pour innover.pptx » est le gabarit officiel 16:9. Formats 4:3 déconseillés.", "OS", 8, M, H - 88, 520, 11, GRIS)

    # mock slides
    def slide(x, y, w, h, kind):
        c.setFillColor(white)
        c.setStrokeColor(GRIS_L)
        c.setLineWidth(0.7)
        c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
        if kind == "cover":
            c.setFillColor(PRUNE)
            c.rect(x, y, 8, h, fill=1, stroke=0)
            img(c, VAR / "logo-wordmark-couleur.png", x + 16, y + h - 36, 70, 22)
            c.setFillColor(PRUNE)
            c.setFont("OSBD", 9)
            c.drawString(x + 16, y + h / 2, "Titre de séance")
            c.setFillColor(ORANGE)
            c.setFont("OS", 7)
            c.drawString(x + 16, y + h / 2 - 14, "L’Esprit d’innover")
        elif kind == "content":
            c.setFillColor(PRUNE)
            c.rect(x, y + h - 8, w, 8, fill=1, stroke=0)
            c.setFillColor(PRUNE)
            c.setFont("OSBD", 8)
            c.drawString(x + 12, y + h - 28, "Titre de partie")
            c.setFillColor(GRIS)
            c.setFont("OS", 7)
            c.drawString(x + 18, y + h - 48, "•  Niveau 1")
            c.drawString(x + 26, y + h - 60, "•  Niveau 2")
            c.drawString(x + 34, y + h - 72, "•  Niveau 3")
        else:
            c.setFillColor(BLEU)
            c.rect(x, y, w, h, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont("OSBD", 9)
            c.drawString(x + 16, y + h / 2, "Ouverture de chapitre")

    slide(M, H - 280, 165, 92, "cover")
    slide(M + 180, H - 280, 165, 92, "content")
    slide(M + 360, H - 280, 165, 92, "chapter")
    c.setFillColor(GRIS_C)
    c.setFont("OS", 7)
    c.drawCentredString(M + 82, H - 294, "Ouverture")
    c.drawCentredString(M + 262, H - 294, "Contenu")
    c.drawCentredString(M + 442, H - 294, "Chapitre")

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 330, "Grains SCORM")
    sc = (
        "Les modules HTML utilisent la palette officielle : "
        "prune #63003C (--bordeaux), orange #F0821A (--orange), "
        "bleu #1D3258 (--blue), vert #00AE68 (--teal). "
        "Open Sans pour le corps, Montserrat pour les titres. "
        "Incrustations et intro/outro de l’animateur suivent les mêmes couleurs "
        "(vert concept, orange intro/outro). Ne pas introduire de 5e couleur d’interface."
        "<br/><br/>Pictos et schémas : style fascicule (pages 6, 7 et 13). "
        "Les pictos filaires et cartes du PPTX vidéo ne s’utilisent pas dans les grains."
    )
    para(c, sc, M, H - 348, 520, 140, pstyle("sc", "OS", 8, GRIS, 11.3))

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 250, "Hiérarchie des titres (diaporama)")
    c.setFillColor(PRUNE)
    c.setFont("OSEB", 16)
    c.drawString(M, 222, "Titre de slide — Open Sans ExtraBold prune")
    c.setFillColor(BLEU)
    c.setFont("OSBD", 12)
    c.drawString(M, 200, "Intertitre — Open Sans Bold bleu")
    c.setFillColor(GRIS)
    c.setFont("OS", 10)
    c.drawString(M, 180, "Corps de texte — Open Sans Regular 18 pt à l’écran, interligne 1,35")
    c.setFillColor(ORANGE)
    c.setFont("OSB", 10)
    c.drawString(M, 160, "Accent / phase recherche — Orange")
    c.setFillColor(VERT)
    c.setFont("OSB", 10)
    c.drawString(M, 144, "Accent / impact — Vert")
    footer(c, 11)


def page12(c):
    img(c, VAR / "logo-wordmark-couleur.png", M, H - 58, 130, 40)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 15)
    c.drawString(178, H - 40, "Oser pour innover :")
    c.drawString(178, H - 58, "règles d’usage pour les partenaires")

    c.setFillColor(GRIS_BG)
    c.roundRect(M, H - 300, 523, 220, 4, fill=1, stroke=0)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 9)
    c.drawString(M + 14, H - 100, "Notre logotype")
    c.setFillColor(GRIS)
    c.setFont("OSBD", 8)
    c.drawString(M + 14, H - 118, "En couleur")
    img(c, VAR / "logo-cartouche-prune.png", M + 14, H - 188, 150, 58)
    wrap(c, "RVB écran / CMJN print. Version à privilégier.", "OS", 7, M + 14, H - 200, 150, 9, GRIS)

    c.setFont("OSBD", 8)
    c.setFillColor(GRIS)
    c.drawString(M + 180, H - 118, "En noir et blanc")
    img(c, VAR / "logo-noir.png", M + 180, H - 188, 150, 58)
    wrap(c, "Uniquement si la couleur est impossible.", "OS", 7, M + 180, H - 200, 150, 9, GRIS)

    c.setFont("OSBD", 8)
    c.setFillColor(GRIS)
    c.drawString(M + 350, H - 118, "Zone de protection")
    # zone
    c.setFillColor(HexColor("#D6EAF8"))
    c.rect(M + 360, H - 210, 170, 80, fill=1, stroke=0)
    img(c, VAR / "logo-wordmark-couleur.png", M + 385, H - 188, 120, 36)
    c.setStrokeColor(BLEU)
    c.setDash(2, 2)
    c.rect(M + 378, H - 198, 134, 56, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(GRIS)
    c.setFont("OS", 7)
    c.drawString(M + 360, H - 228, "Marge = hauteur du mot POUR")
    c.setFont("OSBD", 8)
    c.drawString(M + 360, H - 248, "Taille minimum")
    wrap(c, "18 mm ou 100 px de largeur (wordmark).", "OS", 7, M + 360, H - 262, 170, 9, GRIS)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, H - 330, "Notre nom")
    wrap(c, "Oser pour innover. Logotype : OSER POUR INNOVER. Formation : L’Esprit d’innover. Baseline : Décrypter les fondamentaux et libérer son potentiel.", "OS", 8, M, H - 348, 200, 11, GRIS)

    swatch(c, 250, H - 430, 150, 80, "#63003C", "La couleur prune", [
        "Pantone 229",
        "CMJN 24 100 17 60",
        "RVB 99 0 60",
        "HEX #63003C",
    ])

    wrap(c, "Questions : Direction de la marque et de la communication — Université Paris-Saclay — communication@universite-paris-saclay.fr — objet « Oser pour innover — marque ».", "OS", 8, 420, H - 348, 140, 11, GRIS)

    c.setFillColor(HexColor("#FDECEC"))
    c.roundRect(M, 48, 523, 250, 4, fill=1, stroke=0)
    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M + 14, 278, "Les interdictions — merci de ne pas :")
    c.setFillColor(GRIS)
    c.setFont("OS", 8)
    ints = [
        "Utiliser le noir quand la couleur est possible",
        "Déformer, inverser, recolorer le logotype",
        "Ajouter un slogan ou un pictogramme collé au logo",
        "Poser le logo sur un fond illisible",
        "Utiliser un cartouche blanc + prune",
        "Descendre sous 18 mm / 100 px",
        "Remplacer les icônes fascicules par des pictos filaires ou des cartes PPTX",
    ]
    y = 260
    for t in ints:
        c.drawString(M + 18, y, "•  " + t)
        y -= 14

    c.setFillColor(ROUGE_NON)
    c.circle(W - 90, 120, 26, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("OSBD", 10)
    c.drawCentredString(W - 90, 116, "NON")

    c.setFillColor(GRIS_C)
    c.setFont("OS", 8)
    c.drawString(M, 18, "Octobre 2026")
    c.drawRightString(W - M, 18, "Charte graphique — Oser pour innover")


def page13(c):
    header_title(c, "Éléments de la charte", "Ensemble 2 — pictogrammes d’incrustation")
    wrap(c, "Complément du schéma 5, pour la PI, les contrats et l’écosystème. Même format : trait blanc sur disque coloré, 356×356, fond transparent. Ne pas les utiliser à la place d’un pictogramme du cycle.", "OS", 8, M, H - 88, 520, 11, GRIS)

    icons = [
        ("question.png", "QUESTION", ORANGE),
        ("secret.png", "SECRET", BLEU),
        ("protection.png", "PROTECTION", BLEU),
        ("financement.png", "FINANCEMENT", BLEU),
        ("dialogue.png", "DIALOGUE", ORANGE),
        ("etablissement.png", "ÉTABLISSEMENT", BLEU),
        ("enveloppe.png", "ENVELOPPE", BLEU),
        ("logiciel.png", "LOGICIEL", BLEU),
        ("marque.png", "MARQUE", VERT),
        ("droit-auteur.png", "DROIT D’AUTEUR", BLEU),
        ("actif.png", "ACTIF", BLEU),
        ("strategie.png", "STRATÉGIE", BLEU),
        ("alerte.png", "ALERTE", ORANGE),
        ("partenaire.png", "PARTENAIRE", VERT),
        ("equilibre.png", "ÉQUILIBRE", BLEU),
        ("temps.png", "TEMPS", ORANGE),
        ("cible.png", "CIBLE", ORANGE),
        ("pivot.png", "PIVOT", ORANGE),
        ("contact.png", "CONTACT", BLEU),
        ("sans.png", "SANS", BLEU),
    ]
    icdir = KIT / "icones" / "incrustations"
    cols = 5
    box = 72
    gap = 22
    start_y = H - 200
    for i, (fn, label, col) in enumerate(icons):
        coln, row = i % cols, i // cols
        x = M + coln * (box + gap)
        y = start_y - row * (box + 32)
        img(c, icdir / fn, x, y, box, box)
        c.setFillColor(col)
        c.setFont("OSBD", 6)
        c.drawCentredString(x + box / 2, y - 11, label)

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 168, "Couleurs de phase (schéma 5)")
    rules = (
        "• Orange #F0821A — recherche et expérimentation (question, alerte, dialogue, temps, cible, pivot).<br/>"
        "• Marine #1D3258 — propulsion (secret, protection, financement, logiciel, contrat / actif).<br/>"
        "• Vert #00AE68 — utilité collective (partenaire, marque).<br/>"
        "• Fichiers : authoring/Kit-com-V2/icones/incrustations/ — runtime modules/_shared/icones/incrustations/ — bibliothèque authoring/Kit-com-V2/bibliotheque/incrustations/."
    )
    para(c, rules, M, 150, 520, 120, pstyle("i2", "OS", 8, GRIS, 11.2))
    footer(c, 13)


def page14(c):
    header_title(c, "Éléments de la charte", "Objets isolés des fascicules")
    wrap(c, "Pictogrammes extraits des schémas 8 (sensibilisation ESR) et 9 (parcours entrepreneuriat). PNG sans fond, à réutiliser tels quels. Ne pas les redessiner.", "OS", 8, M, H - 88, 520, 11, GRIS)

    fdir = KIT / "bibliotheque" / "fascicules"
    small = [
        ("CARTOGRAPHIE.png", "CARTOGRAPHIE"),
        ("ETAPE-1-RENCONTRES.png", "ÉTAPE 1"),
        ("ETAPE-2-THEORIE.png", "ÉTAPE 2"),
        ("ETAPE-3-PRATIQUES.png", "ÉTAPE 3"),
        ("LABEL.png", "LABEL"),
        ("AMBASSADEURS.png", "AMBASSADEURS"),
        ("DETECTION.png", "DÉTECTION"),
        ("PREUVE-DE-CONCEPT.png", "PREUVE DE CONCEPT"),
        ("MATURATION.png", "MATURATION"),
        ("TRANSFERT-PARCOURS.png", "TRANSFERT"),
    ]
    box = 78
    gap = 22
    start_y = H - 210
    for i, (fn, label) in enumerate(small):
        col, row = i % 5, i // 5
        x = M + col * (box + gap)
        y = start_y - row * (box + 32)
        img(c, fdir / fn, x, y, box, box)
        c.setFillColor(PRUNE)
        c.setFont("OSBD", 6)
        c.drawCentredString(x + box / 2, y - 11, label)

    c.setFillColor(GRIS_BG)
    c.roundRect(M, 188, 523, 118, 4, fill=1, stroke=0)
    img(c, fdir / "FRISE-SENSIBILISATION.png", M + 10, 208, 503, 86)
    c.setFillColor(PRUNE)
    c.setFont("OSB", 7.5)
    c.drawString(M + 10, 196, "FRISE SENSIBILISATION — schéma 8")

    c.setFillColor(PRUNE)
    c.setFont("OSBD", 10)
    c.drawString(M, 168, "Règles")
    rules = (
        "• Schéma 8 : cartographie, pastilles 1-2-3, label, ambassadeurs, frise programme.<br/>"
        "• Schéma 9 : détection, preuve de concept, maturation, transfert (parcours).<br/>"
        "• Fichiers : authoring/Kit-com-V2/bibliotheque/fascicules/ — catalogue.json."
    )
    para(c, rules, M, 150, 520, 110, pstyle("f14", "OS", 8, GRIS, 11.2))
    footer(c, 14)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4)
    for fn in (page1, page2, page3, page4, page5, page6, page7, page8, page9, page10, page11, page12, page13, page14):
        fn(c)
        c.showPage()
    c.save()
    print("OK", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
