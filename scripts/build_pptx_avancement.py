#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le PPTX d'avancement du MOOC (3 slides) a la charte « Esprit Innover ».

Reprend la grammaire graphique du modele : format 10 x 5.625 in, titres Arial 27 pt
bold #2A346D, cartes a coins arrondis bordees d'une couleur d'accent, pastilles
circulaires. Le theme (couleurs + polices) est repris de document/theme-esprit-innover.xml.

Usage : .venv/bin/python scripts/build_pptx_avancement.py [sortie.pptx]
"""
import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_XML = os.path.join(REPO, "document", "theme-esprit-innover.xml")
THEME_RELTYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"

# --- Charte reprise du modele ---
BLUE = RGBColor(0x2A, 0x34, 0x6D)      # dk1 / texte principal
ORANGE = RGBColor(0xF6, 0x86, 0x2C)    # accent1
TEAL = RGBColor(0x35, 0xBA, 0x84)      # accent2
BORDEAUX = RGBColor(0x63, 0x00, 0x3D)  # accent3
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
# Le modele utilise #CBD5E1 / #94A3B8 pour le texte secondaire, illisibles sur
# fond blanc : on garde la hierarchie en remontant le contraste.
GREY = RGBColor(0x47, 0x55, 0x69)
GREY_LIGHT = RGBColor(0x64, 0x74, 0x8B)
TINT = {
    "teal": RGBColor(0xEC, 0xFA, 0xF4),
    "orange": RGBColor(0xFF, 0xF4, 0xEA),
    "bordeaux": RGBColor(0xF9, 0xEC, 0xF4),
    "blue": RGBColor(0xEE, 0xF1, 0xF8),
}
ACCENT = {"teal": TEAL, "orange": ORANGE, "bordeaux": BORDEAUX, "blue": BLUE}

FONT = "Arial"
DATE_LABEL = "Instantané au 22/09/2026"


# ----------------------------------------------------------------- primitives
def text_box(slide, left, top, width, height, runs, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, spacing=None):
    """runs = liste de (texte, taille_pt, gras, couleur) ; un element par ligne."""
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, (txt, size, bold, color) in enumerate(runs):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        if spacing:
            para.space_after = Pt(spacing)
        run = para.add_run()
        run.text = txt
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return box


def card(slide, left, top, width, height, accent, fill=None, radius=0.16667):
    """Rectangle a coins arrondis borde d'une couleur d'accent (cf. modele)."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.adjustments[0] = radius
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = ACCENT[accent]
    shape.line.width = Pt(1.25)
    shape.shadow.inherit = False
    shape.text_frame.word_wrap = True
    return shape


def badge(slide, left, top, diam, accent, label, size=15, color=WHITE):
    """Pastille circulaire pleine (le modele utilise un arrondi a fond d'accent)."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(diam), Inches(diam))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT[accent]
    shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para = tf.paragraphs[0]
    para.alignment = PP_ALIGN.CENTER
    run = para.add_run()
    run.text = label
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = color
    return shape


def slide_head(slide, title, kicker):
    text_box(slide, 0.84, 0.52, 8.41, 0.45, [(title, 27, True, BLUE)])
    text_box(slide, 0.84, 1.06, 8.41, 0.24, [(kicker, 11.5, False, GREY)])


def slide_foot(slide, note):
    text_box(slide, 0.84, 5.12, 6.6, 0.22, [(note, 8.5, False, GREY_LIGHT)])
    text_box(slide, 7.44, 5.12, 1.81, 0.22,
             [(DATE_LABEL, 8.5, False, GREY_LIGHT)], align=PP_ALIGN.RIGHT)


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# --------------------------------------------------------------------- slide 1
def slide_indicateurs(prs):
    s = blank(prs)
    slide_head(s, "Avancement du MOOC — indicateurs",
               "Le dispositif est livré et packagé. L'effort se concentre désormais sur le remplissage.")

    kpis = [
        ("13 / 13", "Vidéos témoins", "filmées · montage V1 en validation", "teal"),
        ("14 / 23", "Vidéos expert", "filmées · V0 à valider", "orange"),
        ("0 / 36", "Vidéos intégrées", "36 emplacements câblés, 0 rempli", "bordeaux"),
        ("176", "Incrustations", "propositions à arbitrer", "blue"),
    ]
    w, gap, top, h = 1.96, 0.19, 1.46, 1.30
    for i, (value, label, sub, accent) in enumerate(kpis):
        left = 0.84 + i * (w + gap)
        card(s, left, top, w, h, accent, fill=TINT[accent])
        text_box(s, left + 0.06, top + 0.14, w - 0.12, 0.42,
                 [(value, 24, True, ACCENT[accent])], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.06, top + 0.60, w - 0.12, 0.22,
                 [(label, 11, True, BLUE)], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.08, top + 0.85, w - 0.16, 0.38,
                 [(sub, 8.5, False, GREY)], align=PP_ALIGN.CENTER)

    text_box(s, 0.84, 3.00, 8.41, 0.24,
             [("État des rushes expert par module", 12.5, True, BLUE)])

    mods = [
        ("MR", "complet", "teal"), ("M1", "partiel", "orange"), ("M2", "complet", "teal"),
        ("M3", "bloqué", "bordeaux"), ("M4", "partiel", "orange"), ("M5", "complet", "teal"),
        ("M6", "complet", "teal"),
    ]
    cw, cgap, ctop, ch = 1.09, 0.13, 3.32, 0.62
    for i, (code, state, accent) in enumerate(mods):
        left = 0.84 + i * (cw + cgap)
        card(s, left, ctop, cw, ch, accent, fill=TINT[accent], radius=0.12)
        text_box(s, left, ctop + 0.09, cw, 0.24,
                 [(code, 13, True, ACCENT[accent])], align=PP_ALIGN.CENTER)
        text_box(s, left, ctop + 0.34, cw, 0.20,
                 [(state, 8.5, False, GREY)], align=PP_ALIGN.CENTER)

    text_box(s, 0.84, 4.10, 8.41, 0.24,
             [("Les 3 modules verts sont intégrables dès validation des V1 témoin et V0 expert.",
               10.5, True, TEAL)])

    card(s, 0.84, 4.42, 8.41, 0.58, "blue", fill=TINT["blue"], radius=0.14)
    text_box(s, 1.02, 4.52, 8.05, 0.40,
             [("Plateforme : 7 paquets SCORM 1.2 opérationnels · module Ressources finalisé "
               "(21 capsules, 3 séquences) · reprise de parcours, suivi de complétion et remontée de score.",
               10, False, BLUE)])

    slide_foot(s, "L'intégration vidéo est une opération de renseignement des lecteurs : aucun développement restant.")


# --------------------------------------------------------------------- slide 2
def slide_decisions(prs):
    s = blank(prs)
    slide_head(s, "Trois décisions attendues",
               "Le calendrier ne tient que si ces trois points sont tranchés cette semaine.")

    items = [
        ("bordeaux", "1", "E12 / E14 — Fatoumata",
         "Au planning du 11/09, non importées en V0. Absentes du plateau du 24/09.",
         "Bloque 100 % du module 3", "T7 = E12 + E13 · T8 = E14 + E15"),
        ("orange", "2", "Décompte des experts",
         "L'architecture donne 14 capsules filmées, 15 sont annoncées.",
         "23 ou 24 emplacements ?", "Un slot à ouvrir si 24e expert"),
        ("teal", "3", "Périmètre SPOC / MOOC",
         "Aucune différenciation à ce jour : les paquets sont en variante unique.",
         "Fixe les seuils de réussite", "À trancher avant production des quiz"),
    ]
    w, gap, top, h = 2.637, 0.25, 1.46, 2.72
    for i, (accent, mark, title, body, impact, detail) in enumerate(items):
        left = 0.84 + i * (w + gap)
        card(s, left, top, w, h, accent)
        badge(s, left + w / 2 - 0.26, top + 0.20, 0.52, accent, mark, size=18)
        text_box(s, left + 0.16, top + 0.86, w - 0.32, 0.26,
                 [(title, 12.5, True, ACCENT[accent])], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.18, top + 1.16, w - 0.36, 0.62,
                 [(body, 9.5, False, GREY)], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.16, top + 1.88, w - 0.32, 0.26,
                 [(impact, 11, True, BLUE)], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.18, top + 2.18, w - 0.36, 0.40,
                 [(detail, 8.5, False, GREY_LIGHT)], align=PP_ALIGN.CENTER)

    card(s, 0.84, 4.42, 8.41, 0.58, "orange", fill=TINT["orange"], radius=0.14)
    text_box(s, 1.02, 4.52, 8.05, 0.40,
             [("À confirmer : E3 (Burgé) est annoncé « courant octobre » tout en figurant au plateau du 24/09. "
               "Plateau du 24/09 à IncubAlliance : 7 capsules (E2, E3, E4, E13, E15, E17, E18).",
               10, False, BLUE)])

    slide_foot(s, "Si le plateau du 24/09 se déroule complet, il ne restera que E12 et E14 à planifier.")


# --------------------------------------------------------------------- slide 3
def slide_trajectoire(prs):
    s = blank(prs)
    slide_head(s, "Trajectoire et mise en ligne",
               "Livraison en trois lots pour ne pas faire dépendre l'ensemble du module 3.")

    lots = [
        ("teal", "1", "Lot 1 — MR, M2, M5, M6",
         "Rushes experts complets · intégrable dès validation des V1/V0", "Prêt"),
        ("orange", "2", "Lot 2 — M1, M4",
         "Débloqué par le plateau du 24/09 : E2, E3, E4, E17, E18", "Octobre"),
        ("bordeaux", "3", "Lot 3 — M3",
         "Suspendu à la décision sur E12 / E14 — aucun rush disponible", "Sans date"),
    ]
    top, h, gap = 1.44, 0.66, 0.08
    for i, (accent, num, title, body, tag) in enumerate(lots):
        y = top + i * (h + gap)
        card(s, 0.84, y, 8.41, h, accent, fill=TINT[accent], radius=0.20)
        badge(s, 1.00, y + 0.15, 0.36, accent, num, size=12)
        text_box(s, 1.50, y + 0.12, 5.10, 0.24, [(title, 12, True, ACCENT[accent])])
        text_box(s, 1.50, y + 0.36, 5.90, 0.24, [(body, 9.5, False, GREY)])
        text_box(s, 7.50, y + 0.20, 1.60, 0.28,
                 [(tag, 11.5, True, ACCENT[accent])], align=PP_ALIGN.RIGHT)

    jalons = [
        ("teal", "Décembre 2026", "Ouverture partielle",
         "MR, M2, M5, M6 — suppose d'accepter une ouverture module par module"),
        ("blue", "Fin janvier 2027", "Parcours complet",
         "Sous réserve que E12 / E14 soient tournées en octobre"),
    ]
    jw, jtop, jh = 4.08, 3.72, 0.90
    for i, (accent, when, what, cond) in enumerate(jalons):
        left = 0.84 + i * (jw + 0.25)
        card(s, left, jtop, jw, jh, accent, fill=TINT[accent], radius=0.16)
        text_box(s, left + 0.18, jtop + 0.11, jw - 0.36, 0.24,
                 [(when, 12, True, ACCENT[accent])])
        text_box(s, left + 0.18, jtop + 0.34, jw - 0.36, 0.24, [(what, 11, True, BLUE)])
        text_box(s, left + 0.18, jtop + 0.58, jw - 0.36, 0.28, [(cond, 8.5, False, GREY)])

    card(s, 0.84, 4.70, 8.41, 0.52, "bordeaux", fill=TINT["bordeaux"], radius=0.14)
    text_box(s, 1.02, 4.80, 8.05, 0.34,
             [("Angle mort : 13 quiz d'évaluation formative et 1 évaluation sommative à produire — "
               "0 implémenté dans M1 à M6, charge non estimée à ce jour.", 10, True, BORDEAUX)])

    text_box(s, 0.84, 5.32, 7.10, 0.22,
             [("Hypothèses : montage V0 ≈ 3 sem. après tournage · 1 cycle de validation (2 + 2 sem.) "
               "· aucun re-tournage · 2 sem. de recette LMS.", 8, False, GREY_LIGHT)])
    text_box(s, 7.94, 5.32, 1.31, 0.22,
             [(DATE_LABEL, 8.5, False, GREY_LIGHT)], align=PP_ALIGN.RIGHT)


# ------------------------------------------------------------------------ main
def apply_theme(prs):
    """Remplace le theme par celui du modele (couleurs + polices)."""
    if not os.path.exists(THEME_XML):
        print("! theme absent, conservation du theme par defaut", file=sys.stderr)
        return
    with open(THEME_XML, "rb") as fh:
        blob = fh.read()
    for master in prs.slide_masters:
        try:
            master.part.part_related_by(THEME_RELTYPE)._blob = blob
        except KeyError:
            pass


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        REPO, "avancement-mooc-2026-09-22.pptx")
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    apply_theme(prs)
    slide_indicateurs(prs)
    slide_decisions(prs)
    slide_trajectoire(prs)
    prs.save(out)
    print(f"OK {out} ({os.path.getsize(out) / 1024:.0f} Ko, {len(prs.slides.__iter__.__self__._sldIdLst)} slides)")


if __name__ == "__main__":
    main()
