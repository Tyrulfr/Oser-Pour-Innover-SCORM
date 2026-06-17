#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les paquets SCORM modules 2 à 6 (structure grains, contenus placeholder)."""
import os
import shutil
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES_DIR = os.path.join(REPO, "modules")
SCORM_API_SRC = os.path.join(REPO, "modules", "module1-retours", "SCORM_API.js")

MODULES = [
    {
        "folder": "module2-pi",
        "dev_folder": "module2",
        "num": 2,
        "intro_desc": "Présentation des enjeux de la propriété intellectuelle et du fil conducteur du module.",
        "title": "Protéger et Valoriser la PI",
        "subtitle": "Sécuriser vos résultats de recherche et construire une stratégie de propriété intellectuelle cohérente.",
        "tag_cat": "Protéger",
        "tag_info": "PI & valorisation",
        "manifest_id": "OSER-MODULE2-PI",
        "org_id": "OSER-M2-PI-ORG",
        "suspend_key": "module2_pi_suspend",
        "data_module": "module2-pi",
        "hero_gradient": "135deg, var(--bordeaux), var(--teal)",
        "nav_label": "Propriété intellectuelle",
        "grains": [
            {
                "id": "grain_reflexe_declaration",
                "file": "grain_reflexe_declaration.html",
                "title": "Réflexe « déclaration »",
                "desc": "Comprendre quand et comment déclarer une invention ou un résultat avant toute diffusion.",
                "icon": "fa-bell",
                "accent": "teal",
                "hero": "Adopter le bon réflexe dès la production d'un résultat de recherche.",
                "subtitle": "La déclaration est la première étape pour protéger et valoriser vos travaux.",
            },
            {
                "id": "grain_strategie_pi",
                "file": "grain_strategie_pi.html",
                "title": "Stratégie de propriété intellectuelle",
                "desc": "Articuler brevets, secrets, droits d'auteur et publications dans une stratégie globale.",
                "icon": "fa-chess",
                "accent": "orange",
                "hero": "Construire une stratégie de PI adaptée à votre projet.",
                "subtitle": "Choisir les bonnes formes de protection selon l'usage visé et le marché cible.",
            },
            {
                "id": "grain_copro_mandataire",
                "file": "grain_copro_mandataire.html",
                "title": "Copropriété et mandataire unique",
                "desc": "Gérer les situations multi-laboratoires, multi-partenaires et le rôle du mandataire.",
                "icon": "fa-handshake",
                "accent": "blue",
                "hero": "Clarifier la copropriété et la gouvernance de la PI.",
                "subtitle": "Organiser les droits et les décisions lorsque plusieurs acteurs contribuent au résultat.",
            },
            {
                "id": "grain_transfert_licensing",
                "file": "grain_transfert_licensing.html",
                "title": "Transfert / licensing",
                "desc": "Les modalités de transfert de technologie et de licensing vers l'industrie ou une startup.",
                "icon": "fa-file-contract",
                "accent": "bordeaux",
                "hero": "Du laboratoire à l'usage : transfert et licensing.",
                "subtitle": "Les voies contractuelles pour mettre la PI au service de la valorisation.",
            },
        ],
    },
    {
        "folder": "module3-ecosysteme",
        "dev_folder": "module3",
        "num": 3,
        "intro_desc": "Cartographier l'écosystème d'innovation et comprendre comment s'y orienter.",
        "title": "Naviguer dans l'écosystème",
        "subtitle": "Repérer les acteurs, dispositifs et ressources qui accompagnent la maturation et le développement de votre projet.",
        "tag_cat": "Naviguer",
        "tag_info": "Écosystème",
        "manifest_id": "OSER-MODULE3-ECO",
        "org_id": "OSER-M3-ECO-ORG",
        "suspend_key": "module3_ecosysteme_suspend",
        "data_module": "module3-ecosysteme",
        "hero_gradient": "135deg, var(--teal), var(--blue)",
        "nav_label": "Écosystème",
        "grains": [
            {
                "id": "grain_transfert_maturation",
                "file": "grain_transfert_maturation.html",
                "title": "Transfert et maturation",
                "desc": "SATT, offices de transfert et dispositifs de maturation technologique.",
                "icon": "fa-flask-vial",
                "accent": "teal",
                "hero": "Franchir la maturation avec les bons acteurs.",
                "subtitle": "Comprendre le rôle du transfert et de la maturation dans la trajectoire d'innovation.",
            },
            {
                "id": "grain_incubation_structures",
                "file": "grain_incubation_structures.html",
                "title": "Incubation et structures",
                "desc": "Incubateurs, accélérateurs et structures d'accompagnement de projet.",
                "icon": "fa-seedling",
                "accent": "orange",
                "hero": "S'appuyer sur les structures d'incubation.",
                "subtitle": "Identifier les structures adaptées au stade et à l'ambition de votre projet.",
            },
            {
                "id": "grain_financement_developpement",
                "file": "grain_financement_developpement.html",
                "title": "Financement et développement",
                "desc": "Subventions, amorçage, investisseurs et leviers de financement de l'innovation.",
                "icon": "fa-coins",
                "accent": "blue",
                "hero": "Financer le développement de l'innovation.",
                "subtitle": "Panorama des sources de financement selon la maturité du projet.",
            },
            {
                "id": "grain_lieux_formations",
                "file": "grain_lieux_formations.html",
                "title": "Lieux et formations",
                "desc": "Pépinières, tiers-lieux, formations et ressources pour monter en compétence.",
                "icon": "fa-map-location-dot",
                "accent": "bordeaux",
                "hero": "Trouver les lieux et formations utiles.",
                "subtitle": "S'orienter dans l'offre de lieux, réseaux et formations de l'écosystème.",
            },
        ],
    },
    {
        "folder": "module4-partenariats",
        "dev_folder": "module4",
        "num": 4,
        "intro_desc": "Poser les bases d'une collaboration réussie avec les acteurs industriels.",
        "title": "Partenariats et posture",
        "subtitle": "Développer une relation partenariale efficace avec l'industrie et adapter votre communication.",
        "tag_cat": "Collaborer",
        "tag_info": "Partenariats",
        "manifest_id": "OSER-MODULE4-PART",
        "org_id": "OSER-M4-PART-ORG",
        "suspend_key": "module4_partenariats_suspend",
        "data_module": "module4-partenariats",
        "hero_gradient": "135deg, var(--orange), var(--blue)",
        "nav_label": "Partenariats",
        "grains": [
            {
                "id": "grain_posture_partenariale",
                "file": "grain_posture_partenariale.html",
                "title": "Posture partenariale, relation industrielle et recrutement",
                "desc": "Adopter une posture ouverte, construire la relation industrielle et recruter les bons profils.",
                "icon": "fa-people-arrows",
                "accent": "teal",
                "hero": "Construire une posture partenariale crédible.",
                "subtitle": "Relation industrielle, confiance et montée en compétences de l'équipe.",
            },
            {
                "id": "grain_enseignements_conseils",
                "file": "grain_enseignements_conseils.html",
                "title": "Enseignements et conseils",
                "desc": "Retours d'expérience, bonnes pratiques et pièges à éviter en partenariat.",
                "icon": "fa-lightbulb",
                "accent": "orange",
                "hero": "Tirer parti des enseignements du terrain.",
                "subtitle": "Conseils pratiques pour sécuriser et fluidifier les collaborations.",
            },
            {
                "id": "grain_discours_non_scientifiques",
                "file": "grain_discours_non_scientifiques.html",
                "title": "Adaptation du discours aux interlocuteur(rice)s non scientifiques",
                "desc": "Parler valeur, usage et impact aux décideurs, investisseurs et partenaires non experts.",
                "icon": "fa-comments",
                "accent": "blue",
                "hero": "Adapter son discours à chaque interlocuteur(rice).",
                "subtitle": "Traduire la science en bénéfices compréhensibles hors du milieu académique.",
            },
        ],
    },
    {
        "folder": "module5-action",
        "dev_folder": "module5",
        "num": 5,
        "intro_desc": "Identifier les dispositifs et choix stratégiques pour concrétiser votre projet.",
        "title": "Passer à l'action",
        "subtitle": "Concrétiser votre trajectoire : dispositifs, positionnement et mise en situation.",
        "tag_cat": "Agir",
        "tag_info": "Mise en action",
        "manifest_id": "OSER-MODULE5-ACTION",
        "org_id": "OSER-M5-ACTION-ORG",
        "suspend_key": "module5_action_suspend",
        "data_module": "module5-action",
        "hero_gradient": "135deg, var(--blue), var(--bordeaux)",
        "nav_label": "Passer à l'action",
        "grains": [
            {
                "id": "grain_dispositifs_collaborations",
                "file": "grain_dispositifs_collaborations.html",
                "title": "Dispositifs et collaborations",
                "desc": "CIFRE, chaire, consortium, collaboration contractuelle : choisir le bon dispositif.",
                "icon": "fa-network-wired",
                "accent": "teal",
                "hero": "Choisir le dispositif de collaboration adapté.",
                "subtitle": "Panorama des montages possibles pour structurer votre action.",
            },
            {
                "id": "grain_test_positionnement",
                "file": "grain_test_positionnement.html",
                "title": "Test de positionnement : transfert, start-up, consortiums",
                "desc": "Évaluer la voie la plus cohérente : transfert, création d'entreprise ou consortium.",
                "icon": "fa-compass",
                "accent": "orange",
                "hero": "Où situer votre projet sur la carte des possibles ?",
                "subtitle": "Transfert, start-up ou consortium : critères de choix et signaux d'alerte.",
            },
            {
                "id": "grain_simulation",
                "file": "grain_simulation.html",
                "title": "Simulation envisageable",
                "desc": "Mise en situation pour préparer vos décisions et vos échanges avec les parties prenantes.",
                "icon": "fa-vr-cardboard",
                "accent": "blue",
                "hero": "S'entraîner avant de passer à l'acte.",
                "subtitle": "Simulation pédagogique pour tester options, arguments et scénarios.",
            },
        ],
    },
    {
        "folder": "module6-synthese",
        "dev_folder": "module6",
        "num": 6,
        "intro_desc": "Consolider les acquis du parcours et préparer la suite de votre trajectoire.",
        "title": "Synthèse et projection",
        "subtitle": "Consolider vos acquis et construire votre feuille de route pour la suite de votre parcours.",
        "tag_cat": "Projeter",
        "tag_info": "Synthèse",
        "manifest_id": "OSER-MODULE6-SYNTH",
        "org_id": "OSER-M6-SYNTH-ORG",
        "suspend_key": "module6_synthese_suspend",
        "data_module": "module6-synthese",
        "hero_gradient": "135deg, var(--teal), var(--orange)",
        "nav_label": "Synthèse",
        "grains": [
            {
                "id": "grain_bilan_parcours",
                "file": "grain_bilan_parcours.html",
                "title": "Bilan du parcours",
                "desc": "Reprendre les apprentissages clés des modules précédents et identifier vos forces.",
                "icon": "fa-clipboard-list",
                "accent": "teal",
                "hero": "Faire le bilan de votre parcours.",
                "subtitle": "Consolider les concepts, méthodes et réflexes acquis.",
            },
            {
                "id": "grain_feuille_route",
                "file": "grain_feuille_route.html",
                "title": "Construire sa feuille de route",
                "desc": "Prioriser les prochaines étapes, les ressources et les interlocuteur(rice)s à mobiliser.",
                "icon": "fa-route",
                "accent": "orange",
                "hero": "Structurer votre feuille de route.",
                "subtitle": "Du diagnostic à un plan d'action réaliste et daté.",
            },
            {
                "id": "grain_prochain_pas",
                "file": "grain_prochain_pas.html",
                "title": "Définir le prochain pas",
                "desc": "Formuler une action concrète, mesurable, à engager dès la fin de la formation.",
                "icon": "fa-shoe-prints",
                "accent": "bordeaux",
                "hero": "Quelle est votre prochaine action ?",
                "subtitle": "Passer de la réflexion à une décision engageante et réaliste.",
            },
        ],
    },
]

ACCENT = {
    "teal": ("var(--teal)", "border-orange", "icon-orange", "rgba(46, 175, 125, 0.1)"),
    "orange": ("var(--orange)", "border-blue", "icon-blue", "rgba(244, 140, 46, 0.1)"),
    "blue": ("var(--blue)", "border-bordeaux", "icon-bordeaux", "rgba(42, 50, 94, 0.1)"),
    "bordeaux": ("var(--bordeaux)", "border-orange", "icon-orange", "rgba(88, 15, 69, 0.1)"),
}


def video_placeholder_iframe(video_id_key: str) -> str:
    """Zone vidéo 16:9 — remplacer VIDEO_ID_* dans le src lors de l'intégration YouTube."""
    return f"""\
            <div class="video-wrapper">
                <!-- Remplacer {video_id_key} par l'identifiant YouTube (ex. dQw4w9WgXcQ) -->
                <iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id_key}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>"""


def grain_html(mod: dict, grain: dict) -> str:
    gid = grain["id"]
    v1_label = grain.get("video1_label", "Témoignage")
    v2_label = grain.get("video2_label", "Regard d'expert / debrief")
    v1_meta = grain.get("video1_meta", "[Intervenant(e) / Organisation] — Durée : --:--")
    v2_meta = grain.get("video2_meta", "Expertise, debrief ou complément pédagogique")
    v1_id = grain.get("video1_id", "VIDEO_ID_1")
    v2_id = grain.get("video2_id", "VIDEO_ID_2")
    v1_context = grain.get("video1_context", grain["desc"])
    v2_context = grain.get("video2_context", "")
    points_title = grain.get("points_title", "Les points clés à retenir")

    cards = [
        ("Point clé 1", "Contenu de la flash card à compléter.", "fa-star", "var(--bordeaux)"),
        ("Point clé 2", "Contenu de la flash card à compléter.", "fa-star", "var(--orange)"),
        ("Point clé 3", "Contenu de la flash card à compléter.", "fa-star", "var(--blue)"),
    ]
    cards_html = ""
    for i, (title, text, icon, color) in enumerate(cards):
        border = "" if i == 0 else f' style="border-top-color: {color};"'
        icon_bg = "" if i == 0 else f' style="background: {color};"'
        cards_html += f"""
            <div class="point-card"{border}>
                <div class="point-icon"{icon_bg}><i class="fa-solid {icon}"></i></div>
                <div class="point-title">{title}</div>
                <div class="point-text">{text}</div>
            </div>"""

    video2_footer = ""
    if v2_context:
        video2_footer = f"""
            <div class="video-footer">
                <i class="fa-solid fa-circle-info" style="color:var(--orange); margin-right:5px;"></i>
                <strong>Contexte :</strong> {v2_context}
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{grain["title"]} | Module {mod["num"]} — L'esprit d'innover</title>
    <script src="../SCORM_API.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{ --bordeaux: #580F45; --orange: #F48C2E; --teal: #2EAF7D; --blue: #2A325E; --bg-page: #F8F9FA; --bg-card: #FFFFFF; --text-main: #2A325E; --text-light: #555; }}
        body.dark-mode {{ --bg-page: #1A1D2E; --bg-card: #232742; --text-main: #EAEAEA; --text-light: #BBB; }}
        * {{ box-sizing: border-box; transition: all 0.3s ease; }}
        body {{ margin: 0; padding: 0; font-family: 'Open Sans', sans-serif; background-color: var(--bg-page); color: var(--text-main); line-height: 1.6; padding-bottom: 100px; background-image: radial-gradient(rgba(42, 50, 94, 0.1) 1px, transparent 1px); background-size: 30px 30px; }}
        body.dark-mode {{ background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px); }}
        h1, h2, h3, h4 {{ font-family: 'Montserrat', sans-serif; color: var(--bordeaux); }}
        body.dark-mode h1, body.dark-mode h2, body.dark-mode h3 {{ color: var(--orange); }}
        .top-bar {{ background: var(--bg-card); padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-bottom: 3px solid var(--bordeaux); }}
        .btn-back {{ text-decoration: none; color: var(--text-main); font-weight: 700; display: flex; align-items: center; gap: 10px; }}
        .btn-back:hover {{ color: var(--orange); }}
        .content-container {{ max-width: 1000px; margin: 2rem auto; padding: 0 1.5rem; }}
        .hero-title {{ font-size: 2.5rem; font-weight: 900; margin-bottom: 0.5rem; line-height: 1.2; }}
        .hero-subtitle {{ font-size: 1.1rem; color: var(--text-light); margin-bottom: 2rem; border-left: 4px solid var(--teal); padding-left: 15px; }}
        .video-card {{ background: var(--bg-card); border-radius: 20px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.1); margin: 3rem 0; border: 1px solid rgba(0,0,0,0.05); }}
        .video-header {{ padding: 1.5rem; display: flex; align-items: center; gap: 15px; border-bottom: 1px solid rgba(0,0,0,0.05); background: linear-gradient(to right, rgba(46, 175, 125, 0.1), transparent); }}
        .play-icon {{ width: 50px; height: 50px; background: var(--teal); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem; box-shadow: 0 5px 15px rgba(46, 175, 125, 0.3); }}
        .video-title-group h3 {{ margin: 0; font-size: 1.3rem; }}
        .video-meta {{ font-size: 0.9rem; color: var(--text-light); }}
        .video-wrapper {{ position: relative; padding-bottom: 56.25%; height: 0; background: #000; }}
        .video-wrapper iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }}
        .video-footer {{ padding: 1.5rem; font-size: 0.95rem; color: var(--text-light); border-top: 1px solid rgba(0,0,0,0.05); }}
        .points-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 3rem; }}
        .point-card {{ background: var(--bg-card); padding: 2rem; border-radius: 15px; position: relative; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border-top: 5px solid var(--bordeaux); transition: transform 0.3s; }}
        .point-card:hover {{ transform: translateY(-5px); }}
        .point-icon {{ position: absolute; top: -25px; left: 50%; transform: translateX(-50%); background: var(--bordeaux); color: white; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 1.2rem; box-shadow: 0 5px 10px rgba(0,0,0,0.1); }}
        .point-title {{ text-align: center; margin-top: 15px; font-weight: 800; color: var(--text-main); margin-bottom: 10px; }}
        .point-text {{ font-size: 0.95rem; color: var(--text-light); line-height: 1.6; text-align: center; }}
        .quiz-section {{ margin-top: 4rem; padding: 2rem; background: var(--bg-card); border-radius: 15px; border: 1px solid #ddd; border-left: 5px solid var(--orange); }}
        .quiz-question {{ font-weight: 700; margin-bottom: 1rem; font-size: 1.1rem; }}
        .quiz-option {{ margin-bottom: 10px; display: flex; align-items: center; gap: 10px; cursor: pointer; }}
        .modal-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: none; justify-content: center; align-items: center; z-index: 2000; opacity: 0; transition: opacity 0.3s ease; }}
        .modal-overlay.active {{ display: flex; opacity: 1; }}
        .modal-box {{ background: var(--bg-card); padding: 2rem; border-radius: 15px; max-width: 600px; text-align: center; border-top: 5px solid var(--teal); transform: translateY(20px); transition: transform 0.3s ease; }}
        .modal-overlay.active .modal-box {{ transform: translateY(0); }}
        .modal-title {{ font-size: 1.5rem; font-weight: 900; margin-bottom: 1rem; color: var(--teal); }}
        .modal-btn {{ background: var(--teal); color: white; border: none; padding: 10px 25px; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 1rem; }}
        .action-footer {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--bg-card); padding: 1rem 5%; border-top: 1px solid #ddd; display: flex; justify-content: flex-end; align-items: center; z-index: 1000; box-shadow: 0 -5px 20px rgba(0,0,0,0.1); }}
        .btn-validate {{ background: var(--blue); color: white; border: none; padding: 12px 30px; border-radius: 50px; font-weight: 800; font-size: 1rem; cursor: pointer; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(42, 50, 94, 0.3); text-decoration: none; }}
        .btn-validate:hover {{ transform: translateY(-3px); box-shadow: 0 8px 20px rgba(42, 50, 94, 0.4); }}
    </style>
</head>
<body data-module="{mod["data_module"]}" data-grain="{gid}">

    <nav class="top-bar">
        <a href="../index.html" class="btn-back"><i class="fa-solid fa-chevron-left"></i> Retour</a>
        <div style="font-weight: 800; color: var(--bordeaux);">{mod["nav_label"]}</div>
        <button type="button" onclick="toggleTheme()" style="background:none; border:none; cursor:pointer; font-size:1.2rem; color:var(--text-main);" aria-label="Thème"><i class="fa-solid fa-moon"></i></button>
    </nav>

    <div class="content-container">

        <h1 class="hero-title">{grain["hero"]}</h1>
        <div class="hero-subtitle">{grain["subtitle"]}</div>

        <div class="video-card">
            <div class="video-header">
                <div class="play-icon"><i class="fa-solid fa-play"></i></div>
                <div class="video-title-group">
                    <h3>{v1_label}</h3>
                    <div class="video-meta">{v1_meta}</div>
                </div>
            </div>
{video_placeholder_iframe(v1_id)}
            <div class="video-footer">
                <i class="fa-solid fa-circle-info" style="color:var(--teal); margin-right:5px;"></i>
                <strong>Contexte :</strong> {v1_context}
            </div>
        </div>

        <div class="video-card">
            <div class="video-header" style="background: linear-gradient(to right, rgba(244, 140, 46, 0.1), transparent);">
                <div class="play-icon" style="background: var(--orange); box-shadow: 0 5px 15px rgba(244, 140, 46, 0.3);"><i class="fa-solid fa-play"></i></div>
                <div class="video-title-group">
                    <h3>{v2_label}</h3>
                    <div class="video-meta">{v2_meta}</div>
                </div>
            </div>
{video_placeholder_iframe(v2_id)}
{video2_footer}
        </div>

        <h2 style="margin-top: 4rem; color:var(--bordeaux);">{points_title}</h2>

        <div class="points-grid">{cards_html}
        </div>

        <div class="quiz-section">
            <h3><i class="fa-solid fa-clipboard-check"></i> Compréhension</h3>
            <p class="quiz-question">[Question à compléter]</p>
            <form id="videoQuiz">
                <div class="quiz-option">
                    <input type="radio" id="opt1_{gid}" name="quiz" value="wrong">
                    <label for="opt1_{gid}">[Proposition A — à compléter]</label>
                </div>
                <div class="quiz-option">
                    <input type="radio" id="opt2_{gid}" name="quiz" value="correct">
                    <label for="opt2_{gid}">[Proposition B — réponse correcte à définir]</label>
                </div>
                <div class="quiz-option">
                    <input type="radio" id="opt3_{gid}" name="quiz" value="wrong">
                    <label for="opt3_{gid}">[Proposition C — à compléter]</label>
                </div>
            </form>
            <button type="button" id="btnQuizValidate" onclick="checkQuiz()" style="margin-top:15px; background:var(--bordeaux); color:white; border:none; padding:8px 20px; border-radius:5px; cursor:pointer;">Valider</button>
        </div>

    </div>

    <div class="action-footer">
        <a href="../index.html" class="btn-validate">Retour au Sommaire <i class="fa-solid fa-list"></i></a>
    </div>

    <div class="modal-overlay" id="resultModal">
        <div class="modal-box">
            <div class="modal-title" id="mTitle">Bravo !</div>
            <p id="mText">[Feedback réponse correcte — à compléter]</p>
            <button type="button" class="modal-btn" id="btnModalClose" onclick="closeModal()">Fermer</button>
        </div>
    </div>

    <script>
        var GRAIN_ID = '{gid}';
        var SUSPEND_KEY = '{mod["suspend_key"]}';

        function parseState(str) {{ try {{ return str ? JSON.parse(str) : {{}}; }} catch (e) {{ return {{}}; }} }}
        function mergeStates(a, b) {{
            var c = {{ completed: [], scores: {{}}, theme: a.theme || b.theme || 'light' }};
            var seen = {{}};
            (a.completed || []).concat(b.completed || []).forEach(function (g) {{ if (!seen[g]) {{ seen[g] = true; c.completed.push(g); }} }});
            var scores = {{}}; [a.scores, b.scores].forEach(function (s) {{ if (s) for (var k in s) if (s[k] !== undefined) scores[k] = s[k]; }});
            c.scores = scores;
            return c;
        }}
        function getState() {{
            var fromAPI = (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) ? (ScormAPI.getSuspendData() || '') : '';
            var fromLS = ''; try {{ fromLS = localStorage.getItem(SUSPEND_KEY) || ''; }} catch (e) {{}}
            return mergeStates(parseState(fromAPI), parseState(fromLS));
        }}
        function setState(o) {{
            var s = JSON.stringify(o);
            if (s.length > 4000) return;
            if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) {{ ScormAPI.setSuspendData(s); ScormAPI.commit(); }}
            try {{ localStorage.setItem(SUSPEND_KEY, s); }} catch (e) {{}}
        }}

        function toggleTheme() {{
            document.body.classList.toggle('dark-mode');
            var theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            var state = getState(); state.theme = theme; setState(state);
        }}

        function markCompleted(scorePct) {{
            var state = getState();
            state.completed = state.completed || [];
            if (state.completed.indexOf(GRAIN_ID) === -1) state.completed.push(GRAIN_ID);
            state.scores = state.scores || {{}};
            state.scores[GRAIN_ID] = scorePct >= 100 ? 1 : 0;
            setState(state);
            if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) {{
                ScormAPI.setScore(scorePct, 0, 100);
                ScormAPI.setLessonStatus(scorePct >= 100 ? 'completed' : 'incomplete');
                ScormAPI.commit();
            }}
        }}

        function checkQuiz() {{
            var radios = document.getElementsByName('quiz');
            var val = '';
            for (var i = 0; i < radios.length; i++) if (radios[i].checked) val = radios[i].value;

            var modal = document.getElementById('resultModal');
            var mTitle = document.getElementById('mTitle');
            var mText = document.getElementById('mText');
            var mBox = modal.querySelector('.modal-box');
            var mBtn = document.getElementById('btnModalClose');

            if (val === 'correct') {{
                mTitle.innerText = 'Exactement !';
                mTitle.style.color = 'var(--teal)';
                mBox.style.borderTopColor = 'var(--teal)';
                mBtn.style.backgroundColor = 'var(--teal)';
                mText.innerText = "[Feedback réponse correcte — à compléter]";
                modal.classList.add('active');
                markCompleted(100);
            }} else if (val === 'wrong') {{
                mTitle.innerText = 'Pas tout à fait';
                mTitle.style.color = 'var(--orange)';
                mBox.style.borderTopColor = 'var(--orange)';
                mBtn.style.backgroundColor = 'var(--orange)';
                mText.innerText = "[Feedback réponse incorrecte — à compléter]";
                modal.classList.add('active');
            }} else {{
                alert('Veuillez sélectionner une réponse.');
            }}
        }}

        function closeModal() {{ document.getElementById('resultModal').classList.remove('active'); }}

        window.addEventListener('load', function () {{
            if (typeof ScormAPI !== 'undefined') ScormAPI.LMSInitialize();
            var state = getState();
            if (state.theme === 'dark') document.body.classList.add('dark-mode');
        }});
        window.addEventListener('beforeunload', function () {{
            if (typeof ScormAPI !== 'undefined') {{ ScormAPI.LMSCommit(); ScormAPI.LMSFinish(); }}
        }});
    </script>
</body>
</html>
"""


def sommaire_cards_html(mod: dict, pages_prefix: str = "pages/") -> str:
    """Cartes du sommaire : intro (01) + grains (02..N) + synthèse (dernier numéro)."""
    accents = ["teal", "orange", "blue", "bordeaux"]
    cards = f"""
            <div class="grain-card locked">
                <div class="card-number">01</div>
                <div class="card-body">
                    <div class="card-icon"><i class="fa-solid fa-flag-checkered"></i></div>
                    <div class="card-title">Introduction au module</div>
                    <div class="card-desc">{mod["intro_desc"]}</div>
                </div>
                <div class="card-footer"><span class="btn-locked"><i class="fa-solid fa-person-digging"></i> Bientôt</span></div>
            </div>"""
    for i, grain in enumerate(mod["grains"]):
        num = i + 2
        acc = accents[i % len(accents)]
        border_class = "" if acc == "teal" else f" border-{acc}"
        icon_class = "" if acc == "teal" else f" icon-{acc}"
        cards += f"""
            <div class="grain-card{border_class}">
                <div class="card-number">{num:02d}</div>
                <div class="card-body">
                    <div class="card-icon{icon_class}"><i class="fa-solid {grain['icon']}"></i></div>
                    <div class="card-title">{grain["title"]}</div>
                    <div class="card-desc">{grain["desc"]}</div>
                </div>
                <div class="card-footer"><a href="{pages_prefix}{grain['file']}" class="btn-start">Accéder <i class="fa-solid fa-play"></i></a></div>
            </div>"""
    synth_num = len(mod["grains"]) + 2
    cards += f"""
            <div class="grain-card border-bordeaux locked">
                <div class="card-number">{synth_num:02d}</div>
                <div class="card-body">
                    <div class="card-icon icon-bordeaux"><i class="fa-solid fa-star"></i></div>
                    <div class="card-title">Synthèse du module</div>
                    <div class="card-desc">Ce qu'il faut retenir et appliquer à votre situation. Check-list de maturité.</div>
                </div>
                <div class="card-footer"><span class="btn-locked"><i class="fa-solid fa-lock"></i> Verrouillé</span></div>
            </div>"""
    return cards


SOMMAIRE_CSS = """
        :root { --bordeaux: #580F45; --orange: #F48C2E; --teal: #2EAF7D; --blue: #2A325E; --bg-page: #F8F9FA; --bg-card: #FFFFFF; --text-main: #2A325E; --text-light: #555; }
        body.dark-mode { --bg-page: #1A1D2E; --bg-card: #232742; --text-main: #EAEAEA; --text-light: #BBB; }
        * { box-sizing: border-box; transition: all 0.3s ease; }
        body { margin: 0; padding: 0; font-family: 'Open Sans', sans-serif; background-color: var(--bg-page); color: var(--text-main); line-height: 1.6; padding-bottom: 100px; background-image: radial-gradient(rgba(42, 50, 94, 0.1) 1px, transparent 1px); background-size: 30px 30px; }
        body.dark-mode { background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px); }
        h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; color: var(--bordeaux); }
        body.dark-mode h1, body.dark-mode h2, body.dark-mode h3 { color: var(--orange); }
        .top-bar { background: var(--bg-card); padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-bottom: 3px solid var(--bordeaux); min-height: 120px; }
        .brand-logo-link { display: block; line-height: 0; margin-bottom: -8px; pointer-events: none; }
        .brand-logo-link img { height: 108px; width: auto; max-width: 540px; object-fit: contain; display: block; }
        .nav-center { display: flex; flex-direction: column; align-items: center; gap: 0; }
        .breadcrumbs { font-size: 0.85rem; color: var(--text-light); margin-top: 0; }
        .breadcrumbs .separator { opacity: 0.4; margin: 0 5px; }
        .btn-back { text-decoration: none; color: var(--text-main); font-weight: 700; display: flex; align-items: center; gap: 10px; font-size: 1.1rem; }
        .btn-back:hover { color: var(--orange); }
        .content-container { max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem; }
        .hero-section { text-align: center; margin-bottom: 4rem; padding: 3rem 1rem; border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(42, 50, 94, 0.3); }
        .hero-title { font-size: 2.5rem; margin-bottom: 1rem; color: white; }
        .hero-desc { font-size: 1.1rem; opacity: 0.9; max-width: 700px; margin: 0 auto; }
        .progress-bar-container { width: 100%; max-width: 400px; background: rgba(255,255,255,0.2); height: 10px; border-radius: 5px; margin: 2rem auto 0; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: var(--orange); border-radius: 5px; transition: width 1s ease; }
        .grains-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }
        .grain-card { background: var(--bg-card); border-radius: 15px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: transform 0.3s, box-shadow 0.3s; display: flex; flex-direction: column; position: relative; border-top: 5px solid var(--teal); }
        .grain-card:hover { transform: translateY(-10px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
        .grain-card.locked { opacity: 0.7; border-top-color: #ccc; cursor: not-allowed; }
        .grain-card.locked:hover { transform: none; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .grain-card.locked .card-icon { background: rgba(0,0,0,0.05); color: #999; }
        .card-number { position: absolute; top: 15px; right: 15px; font-size: 2.5rem; font-weight: 900; color: rgba(0,0,0,0.05); font-family: 'Montserrat', sans-serif; }
        .card-body { padding: 2rem 1.5rem; flex-grow: 1; }
        .card-icon { font-size: 2rem; color: var(--teal); margin-bottom: 1rem; background: rgba(46, 175, 125, 0.1); width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
        .card-title { font-size: 1.2rem; font-weight: 800; margin-bottom: 0.5rem; color: var(--text-main); }
        .card-desc { font-size: 0.9rem; color: var(--text-light); line-height: 1.5; }
        .card-footer { padding: 1rem 1.5rem; border-top: 1px solid rgba(0,0,0,0.05); text-align: right; }
        .btn-start { display: inline-block; text-decoration: none; background: var(--blue); color: white; padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; transition: background 0.3s; }
        .btn-start:hover { background: var(--orange); }
        .btn-locked { display: inline-block; background: #e0e0e0; color: #888; padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; cursor: not-allowed; }
        .border-orange { border-top-color: var(--orange); }
        .border-blue { border-top-color: var(--blue); }
        .border-bordeaux { border-top-color: var(--bordeaux); }
        .icon-orange { color: var(--orange); background: rgba(244, 140, 46, 0.1); }
        .icon-blue { color: var(--blue); background: rgba(42, 50, 94, 0.1); }
        .icon-bordeaux { color: var(--bordeaux); background: rgba(88, 15, 69, 0.1); }
"""


def sommaire_script(mod: dict, scorm_api_src: str = "") -> str:
    grain_ids = [g["id"] for g in mod["grains"]]
    pages_js = ", ".join(f"'{g}'" for g in grain_ids)
    api_tag = f'\n            <script src="{scorm_api_src}"></script>' if scorm_api_src else ""
    return f"""{api_tag}
            <script>
                var PAGES = [{pages_js}];
                var SUSPEND_KEY = '{mod["suspend_key"]}';

                function parseState(str) {{ try {{ return str ? JSON.parse(str) : {{}}; }} catch (e) {{ return {{}}; }} }}
                function mergeStates(a, b) {{
                    var c = {{ completed: [], scores: {{}}, theme: a.theme || b.theme || 'light' }};
                    var seen = {{}};
                    (a.completed || []).concat(b.completed || []).forEach(function (g) {{
                        if (!seen[g]) {{ seen[g] = true; c.completed.push(g); }}
                    }});
                    var scores = {{}};
                    [a.scores, b.scores].forEach(function (s) {{
                        if (s) for (var k in s) if (s[k] !== undefined) scores[k] = s[k];
                    }});
                    c.scores = scores;
                    return c;
                }}
                function getState() {{
                    var fromAPI = (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) ? (ScormAPI.getSuspendData() || '') : '';
                    var fromLS = ''; try {{ fromLS = localStorage.getItem(SUSPEND_KEY) || ''; }} catch (e) {{}}
                    return mergeStates(parseState(fromAPI), parseState(fromLS));
                }}
                function setState(o) {{
                    var s = JSON.stringify(o);
                    if (s.length > 4000) return;
                    if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) {{
                        ScormAPI.setSuspendData(s);
                        ScormAPI.commit();
                    }}
                    try {{ localStorage.setItem(SUSPEND_KEY, s); }} catch (e) {{}}
                }}
                function toggleTheme() {{
                    document.body.classList.toggle('dark-mode');
                    var state = getState();
                    state.theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
                    setState(state);
                }}
                function refreshProgress() {{
                    var state = getState();
                    var done = (state.completed || []).filter(function (g) {{ return PAGES.indexOf(g) !== -1; }}).length;
                    var pct = PAGES.length ? Math.round((done / PAGES.length) * 100) : 0;
                    var bar = document.getElementById('hero-progress-bar');
                    var text = document.getElementById('progress-text');
                    if (bar) bar.style.width = pct + '%';
                    if (text) text.textContent = done;
                    if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) {{
                        ScormAPI.setScore(pct, 0, 100);
                        if (pct >= 100) ScormAPI.setLessonStatus('completed');
                        ScormAPI.commit();
                    }}
                }}
                window.addEventListener('load', function () {{
                    if (typeof ScormAPI !== 'undefined') ScormAPI.LMSInitialize();
                    var state = getState();
                    if (state.theme === 'dark') document.body.classList.add('dark-mode');
                    refreshProgress();
                }});
                window.addEventListener('beforeunload', function () {{
                    if (typeof ScormAPI !== 'undefined') {{ ScormAPI.LMSCommit(); ScormAPI.LMSFinish(); }}
                }});
            </script>"""


def index_html(mod: dict) -> str:
    cards = sommaire_cards_html(mod, pages_prefix="pages/")
    n = len(mod["grains"])
    return textwrap.dedent(f"""\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sommaire Module {mod["num"]} : {mod["title"]} | L'esprit d'innover</title>
            <script src="SCORM_API.js"></script>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
        {SOMMAIRE_CSS}
                .hero-section {{ background: linear-gradient({mod["hero_gradient"]}); }}
            </style>
        </head>
        <body data-module="{mod["data_module"]}">

            <nav class="top-bar">
                <a href="../portal_sensi.html" class="btn-back"><i class="fa-solid fa-chevron-left"></i> Portail</a>
                <div class="nav-center">
                    <span class="brand-logo-link"><img src="../document/assets/image/logo_oser_pour_innover.png" alt="L'esprit d'innover" onerror="this.style.display='none'" /></span>
                    <div class="breadcrumbs">Accueil <span class="separator">/</span> Sensibilisation <span class="separator">/</span> Module {mod["num"]}</div>
                </div>
                <button type="button" onclick="toggleTheme()" style="background:none; border:none; cursor:pointer; font-size:1.2rem; color:var(--text-main);" aria-label="Thème"><i class="fa-solid fa-moon"></i></button>
            </nav>

            <div class="content-container">
                <div class="hero-section">
                    <h1 class="hero-title">Module {mod["num"]} : {mod["title"]}</h1>
                    <p class="hero-desc">{mod["subtitle"]}</p>
                    <div class="progress-bar-container"><div class="progress-bar" id="hero-progress-bar" style="width: 0%"></div></div>
                    <p style="font-size:0.8rem; margin-top:10px; opacity:0.8;"><span id="progress-text">0</span> / {n} grains</p>
                </div>

                <div class="grains-grid">{cards}
                </div>
            </div>
        {sommaire_script(mod)}
        </body>
        </html>
        """)


def dev_index_html(mod: dict) -> str:
    """Sommaire hors paquet SCORM (modules/module2/, etc.) — modèle module1/index.html."""
    scorm_folder = mod["folder"]
    cards = sommaire_cards_html(mod, pages_prefix=f"../{scorm_folder}/pages/")
    n = len(mod["grains"])
    return textwrap.dedent(f"""\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sommaire Module {mod["num"]} : {mod["title"]} | L'esprit d'innover</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
        {SOMMAIRE_CSS}
                .hero-section {{ background: linear-gradient({mod["hero_gradient"]}); }}
                .brand-text {{ font-weight: 900; font-size: 1.2rem; color: var(--bordeaux); letter-spacing: 1px; }}
                body.dark-mode .brand-text {{ color: var(--orange); }}
            </style>
        </head>
        <body data-module="{mod["data_module"]}">

            <nav class="top-bar">
                <a href="../portal_sensi.html" class="btn-back"><i class="fa-solid fa-chevron-left"></i> Portail</a>
                <span class="brand-text">L'esprit d'innover</span>
                <button type="button" onclick="toggleTheme()" style="background:none; border:none; cursor:pointer; font-size:1.2rem; color:var(--text-main);" aria-label="Thème"><i class="fa-solid fa-moon"></i></button>
            </nav>

            <div class="content-container">
                <div class="hero-section">
                    <h1 class="hero-title">Module {mod["num"]} : {mod["title"]}</h1>
                    <p class="hero-desc">{mod["subtitle"]}</p>
                    <div class="progress-bar-container"><div class="progress-bar" id="hero-progress-bar" style="width: 0%"></div></div>
                    <p style="font-size:0.8rem; margin-top:10px; opacity:0.8;"><span id="progress-text">0</span> / {n} grains</p>
                </div>

                <div class="grains-grid">{cards}
                </div>
            </div>
        {sommaire_script(mod, scorm_api_src="../../scorm-api/SCORM_API.js")}
        </body>
        </html>
        """)


def manifest_xml(mod: dict) -> str:
    files = "\n".join(
        f'      <file href="pages/{g["file"]}"/>' for g in mod["grains"]
    )
    # La déclaration <?xml doit être en première ligne, sans espace (requis Moodle / SCORM).
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{mod["manifest_id"]}" version="1.0"
  xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_v1p3"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1 imscp_v1p1.xsd
                      http://www.imsglobal.org/xsd/imsmd_v1p2 imsmd_v1p2p2.xsd
                      http://www.adlnet.org/xsd/adlcp_v1p3 adlcp_v1p3.xsd">

  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>2004 4th Edition</schemaversion>
  </metadata>

  <organizations default="{mod["org_id"]}">
    <organization identifier="{mod["org_id"]}">
      <metadata>
        <title>Module {mod["num"]} : {mod["title"]} — L'esprit d'innover</title>
      </metadata>
      <title>Module {mod["num"]} : {mod["title"]}</title>
      <item identifier="ITEM-M{mod["num"]}" identifierref="RES-M{mod["num"]}">
        <title>Sommaire Module {mod["num"]}</title>
      </item>
    </organization>
  </organizations>

  <resources>
    <resource identifier="RES-M{mod["num"]}" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/>
      <file href="SCORM_API.js"/>
{files}
    </resource>
  </resources>
</manifest>
"""


def generate_module(mod: dict) -> None:
    base = os.path.join(MODULES_DIR, mod["folder"])
    pages = os.path.join(base, "pages")
    os.makedirs(pages, exist_ok=True)
    shutil.copy2(SCORM_API_SRC, os.path.join(base, "SCORM_API.js"))
    with open(os.path.join(base, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(index_html(mod))
    with open(os.path.join(base, "imsmanifest.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(manifest_xml(mod))
    for grain in mod["grains"]:
        with open(os.path.join(pages, grain["file"]), "w", encoding="utf-8", newline="\n") as f:
            f.write(grain_html(mod, grain))
    dev_dir = os.path.join(MODULES_DIR, mod["dev_folder"])
    os.makedirs(dev_dir, exist_ok=True)
    with open(os.path.join(dev_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(dev_index_html(mod))
    print(f"OK {mod['folder']} + sommaire {mod['dev_folder']}/ ({len(mod['grains'])} grains)")


def main() -> None:
    for mod in MODULES:
        generate_module(mod)
    print("Done.")


if __name__ == "__main__":
    main()
