#!/usr/bin/env python3
"""Génère un Word par vidéo : intro + transcript + outro."""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "downloads" / "intro-transcript-outro"
ZIP_PATH = ROOT / "downloads" / "intro-transcript-outro.zip"
ANIM = ROOT / "modules" / "_shared" / "animateur.json"
TEMOINS = ROOT / "authoring" / "transcripts" / "temoins"
EXPERTS = ROOT / "authoring" / "transcripts" / "experts"
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

TITLES = {
    "T1": "Pourquoi oser ?",
    "E1": "Origines d’une innovation",
    "T2": "De la recherche à l’innovation",
    "E2": "D’une techno à un problème à résoudre",
    "E3": "Poser le bon problème",
    "T3": "Identifier un besoin réel",
    "E4": "POC, prototype, MVP, TRL",
    "E5": "Dérisquer par étapes",
    "T4": "Une idée ne suffit pas",
    "E6": "Déclaration d’invention avant divulgation",
    "E7": "À qui parler, avec quoi arriver",
    "T5": "Protection et valorisation",
    "E8": "Choisir un mode de protection",
    "E9": "La PI comme actif stratégique",
    "T6": "Transfert et licensing",
    "E10": "Quelle voie de valorisation",
    "E11": "Mécanismes juridiques du transfert",
    "T7": "Vous n’êtes pas seul(e)",
    "E12": "Prématuration → maturation",
    "E13": "Ce que fait un incubateur",
    "E13bis": "Design Spot, fablab, OTT",
    "T8": "Financements, concours, temps",
    "E14": "Chaîne des financements (Fatoumata)",
    "E15": "Logique des investisseurs",
    "T9": "Partenariats et équipe",
    "E16": "Posture entrepreneuriale et vocabulaire",
    "E17": "Relation entre fondateurs",
    "T10": "Enrichir son langage",
    "E18": "Organiser juridiquement l’équipe projet",
    "E19": "Financer et dérisquer un projet Deep Tech",
    "T11": "Évolution dans le métier du chercheur",
    "E20": "Concilier recherche et engagement",
    "E21": "Innover comme apprentissage (TRL, pivot, MVP)",
    "T12": "Dispositifs et collaborations",
    "E22": "Collaboration équilibrée",
    "E23": "Sécuriser juridiquement (NDA, PI, contrat)",
    "E24": "Dispositifs de collaboration",
    "T13": "Conclusion : passer à l’action",
}

SPEAKERS = (
    "Stephanie", "Stéphanie", "Arielle", "Antoine", "Bernard", "Virginia",
    "Virgnia", "Soizic", "Yoann", "Pascal", "Rémi", "Remi", "Eneli", "Nelly",
    "Grégoire", "Gregoire", "Stanislas", "Fatoumata",
)


def transcript_path(code: str) -> Path | None:
    if code.startswith("T") and code[1:].isdigit():
        p = TEMOINS / f"{code}.docx"
        return p if p.exists() else None
    if code == "E13bis":
        p = EXPERTS / "E14_Yoann.docx"
        return p if p.exists() else None
    if code == "E14":
        return None
    matches = sorted(EXPERTS.glob(f"{code}_*.docx"))
    return matches[0] if matches else None


def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paras = []
    for p_el in root.iter(f"{W_NS}p"):
        texts = [t.text or "" for t in p_el.iter(f"{W_NS}t")]
        line = "".join(texts).strip()
        if line:
            paras.append(line)
    raw = "\n".join(paras)
    return re.sub(r"(?=\d{2}:\d{2}:\d{2}\s)", "\n", raw).strip()


def format_line(line: str) -> str:
    m = re.match(r"^(\d{2}:\d{2}:\d{2})\s*(.*)$", line)
    if not m:
        return line
    time, rest = m.group(1), m.group(2)
    for name in SPEAKERS:
        if rest.startswith(name):
            after = rest[len(name):].lstrip(" :—-")
            return f"{time}  {name} — {after}"
    return f"{time}  {rest}"


def w_p(text: str, style: str | None = None, italic: bool = False, color: str | None = None) -> str:
    pr = ""
    if style:
        pr = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>"
    rpr_bits = []
    if italic:
        rpr_bits.append("<w:i/>")
    if color:
        rpr_bits.append(f"<w:color w:val=\"{color}\"/>")
    rpr = f"<w:rPr>{''.join(rpr_bits)}</w:rPr>" if rpr_bits else ""
    chunks = []
    if not text:
        return f"<w:p>{pr}</w:p>"
    for i, part in enumerate(text.split("\n")):
        if i:
            chunks.append("<w:br/>")
        chunks.append(f"<w:t xml:space=\"preserve\">{escape(part)}</w:t>")
    return f"<w:p>{pr}<w:r>{rpr}{''.join(chunks)}</w:r></w:p>"


def document_xml(code: str, title: str, intro: str, lines: list[str], outro: str, missing: str | None) -> str:
    kind = "Vidéo témoin chorale" if code.startswith("T") else "Vidéo expert"
    body = [
        w_p(f"{code} — {title}", "Heading1"),
        w_p(kind, italic=True),
        w_p("Intro", "Heading2", color="2EAF7D"),
        w_p(intro, color="2EAF7D"),
        w_p("Transcript", "Heading2"),
    ]
    if missing:
        body.append(w_p(missing, italic=True))
    else:
        body.extend(w_p(format_line(line)) for line in lines if line.strip())
    body += [
        w_p("Outro", "Heading2", color="F48C2E"),
        w_p(outro, color="F48C2E"),
    ]
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(body)}
    <w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr>
  </w:body>
</w:document>
"""


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/><w:color w:val="580F45"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>
    <w:pPr><w:spacing w:before="280" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="F48C2E"/></w:rPr>
  </w:style>
</w:styles>
"""


def write_docx(path: Path, xml: str) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", xml)


def main() -> None:
    data = json.loads(ANIM.read_text(encoding="utf-8"))
    videos = data["videos"]
    if OUT_DIR.exists():
        for old in OUT_DIR.glob("*.docx"):
            old.unlink()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    missing_codes = []
    for i, code in enumerate(videos, start=1):
        entry = videos[code]
        src = transcript_path(code)
        missing = None
        lines: list[str] = []
        if src is None:
            missing = "Transcript non disponible — vidéo pas encore filmée, ou fichier source absent."
            missing_codes.append(code)
        else:
            text = extract_docx_text(src)
            lines = [ln for ln in text.splitlines() if ln.strip()]
            if not lines:
                missing = "Transcript source vide."
                missing_codes.append(code)
        xml = document_xml(
            code,
            TITLES.get(code, code),
            entry["intro"],
            lines,
            entry["outro"],
            missing,
        )
        write_docx(OUT_DIR / f"{i:02d}_{code}.docx", xml)

    readme = OUT_DIR / "00_LISEZMOI.txt"
    readme.write_text(
        "Intro / transcript / outro — un Word par vidéo\n"
        "MOOC L’Esprit d’innover\n\n"
        "Chaque fichier : Intro (texte animateur) · Transcript · Outro (texte animateur).\n"
        "Ordre des fichiers = ordre pédagogique du parcours.\n\n"
        "Transcripts encore absents : " + (", ".join(missing_codes) if missing_codes else "aucun") + ".\n"
        "E13bis reprend le transcript Yoann (Design Spot). E14 est prévue pour Fatoumata.\n",
        encoding="utf-8",
    )

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT_DIR.iterdir()):
            if p.name.startswith("."):
                continue
            z.write(p, arcname=f"intro-transcript-outro/{p.name}")
    print(f"{len(videos)} Word → {OUT_DIR}")
    print(f"ZIP → {ZIP_PATH} ({ZIP_PATH.stat().st_size} octets)")
    if missing_codes:
        print("Sans transcript :", ", ".join(missing_codes))


if __name__ == "__main__":
    main()
