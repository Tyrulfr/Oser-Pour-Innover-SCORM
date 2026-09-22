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
               "SPOC Paris-Saclay. Le dispositif est livré et packagé : l'effort porte sur le remplissage.")

    kpis = [
        ("13 / 13", "Vidéos témoins", "filmées · montage V1 en validation", "teal"),
        ("15 / 25", "Vidéos expert", "filmées · V0 à valider", "orange"),
        ("0 / 38", "Vidéos intégrées", "37 emplacements câblés · 1 à créer", "bordeaux"),
        ("76", "Intro / outro", "segments · 40 à 57 min à produire", "blue"),
        ("176", "Incrustations", "propositions à arbitrer", "teal"),
    ]
    gap, top, h = 0.17, 1.46, 1.30
    w = (8.41 - gap * (len(kpis) - 1)) / len(kpis)
    for i, (value, label, sub, accent) in enumerate(kpis):
        left = 0.84 + i * (w + gap)
        card(s, left, top, w, h, accent, fill=TINT[accent])
        text_box(s, left + 0.05, top + 0.13, w - 0.10, 0.38,
                 [(value, 21, True, ACCENT[accent])], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.05, top + 0.56, w - 0.10, 0.20,
                 [(label, 10, True, BLUE)], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.07, top + 0.79, w - 0.14, 0.44,
                 [(sub, 8, False, GREY)], align=PP_ALIGN.CENTER)

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
             [("Les 4 modules verts sont intégrables dès validation des V1/V0 — mais M2 ou M5 "
               "accueillera la capsule PACTE.", 10.5, True, TEAL)])

    card(s, 0.84, 4.42, 8.41, 0.58, "blue", fill=TINT["blue"], radius=0.14)
    text_box(s, 1.02, 4.52, 8.05, 0.40,
             [("Plateforme : 7 paquets SCORM 1.2 opérationnels · module Ressources finalisé "
               "(21 capsules, 3 séquences) · reprise de parcours, suivi de complétion et remontée de score.",
               10, False, BLUE)])

    slide_foot(s, "L'intégration vidéo est une opération de renseignement des lecteurs : aucun développement restant.")


# --------------------------------------------------------------------- slide 2
def slide_decisions(prs):
    s = blank(prs)
    slide_head(s, "Quatre points à trancher",
               "Le calendrier ne tient que si ces quatre points sont arbitrés dans les prochains jours.")

    items = [
        ("bordeaux", "E12 / E14",
         "Capsules Fatoumata, non importées en V0 et absentes du 24/09.",
         "Bloque le module 3", "T7 et T8 incomplets"),
        ("orange", "Capsule loi PACTE",
         "Sujet apparu en captation, sans emplacement prévu.",
         "M2 ou M5 à arbitrer", "25e capsule · lecteur à créer"),
        ("teal", "Scripts intro / outro",
         "À valider avant mi-octobre, tournage derrière.",
         "76 segments à produire", "38 vidéos × intro + outro"),
        ("blue", "Charge des quiz",
         "Aucune estimation de charge à ce jour.",
         "13 formatifs + 1 finale", "évaluation sommative · 0 implémenté"),
    ]
    gap, top, h = 0.25, 1.46, 2.72
    w = (8.41 - gap * (len(items) - 1)) / len(items)
    for i, (accent, title, body, impact, detail) in enumerate(items):
        left = 0.84 + i * (w + gap)
        card(s, left, top, w, h, accent)
        badge(s, left + w / 2 - 0.24, top + 0.20, 0.48, accent, str(i + 1), size=16)
        text_box(s, left + 0.12, top + 0.82, w - 0.24, 0.28,
                 [(title, 11.5, True, ACCENT[accent])], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.14, top + 1.14, w - 0.28, 0.68,
                 [(body, 9, False, GREY)], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.12, top + 1.90, w - 0.24, 0.28,
                 [(impact, 9.5, True, BLUE)], align=PP_ALIGN.CENTER)
        text_box(s, left + 0.14, top + 2.22, w - 0.28, 0.42,
                 [(detail, 8, False, GREY_LIGHT)], align=PP_ALIGN.CENTER)

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
         "Rushes complets · sous réserve du rattachement de la capsule PACTE", "Prêt"),
        ("orange", "2", "Lot 2 — M1, M4",
         "Débloqué par le plateau du 24/09 : E2, E3, E4, E17, E18", "Octobre"),
        ("bordeaux", "3", "Lot 3 — M3",
         "Suspendu à E12 / E14 · E13bis tournée, E13 et E15 le 24/09", "Sans date"),
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
         "Sous réserve de E12 / E14 en octobre et du volume intro / outro"),
    ]
    jw, jtop, jh = 4.08, 3.72, 0.90
    for i, (accent, when, what, cond) in enumerate(jalons):
        left = 0.84 + i * (jw + 0.25)
        card(s, left, jtop, jw, jh, accent, fill=TINT[accent], radius=0.16)
        text_box(s, left + 0.18, jtop + 0.11, jw - 0.36, 0.24,
                 [(when, 12, True, ACCENT[accent])])
        text_box(s, left + 0.18, jtop + 0.34, jw - 0.36, 0.24, [(what, 11, True, BLUE)])
        text_box(s, left + 0.18, jtop + 0.58, jw - 0.36, 0.28, [(cond, 8.5, False, GREY)])

    card(s, 0.84, 4.70, 8.41, 0.52, "blue", fill=TINT["blue"], radius=0.14)
    text_box(s, 1.02, 4.80, 8.05, 0.34,
             [("Périmètre : SPOC Paris-Saclay — le terme « MOOC » est conservé en communication. "
               "Une éventuelle déclinaison à périmètre élargi est un sujet ultérieur du projet.",
               10, False, BLUE)])

    text_box(s, 0.84, 5.32, 7.10, 0.22,
             [("Hypothèses : montage V0 ≈ 3 sem. · validation 2 + 2 sem. · recette LMS 2 sem. "
               "· 76 intro / outro non chiffrés.", 8, False, GREY_LIGHT)])
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
