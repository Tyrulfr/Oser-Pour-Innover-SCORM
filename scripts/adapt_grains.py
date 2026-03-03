# -*- coding: utf-8 -*-
import re, os

base = r"c:\Users\cduboi4\Documents\Ingénierie\01_INNOV\04_Conception\Oser-Pour-Innover-SCORM\modules\module1"
config = [
    ('grain4', 'sommaire_sequence1.html'), ('grain5', 'sommaire_sequence1.html'),
    ('grain6', 'sommaire_sequence2.html'), ('grain7', 'sommaire_sequence2.html'), ('grain8', 'sommaire_sequence2.html'),
    ('grain9', 'sommaire_sequence2.html'), ('grain10', 'sommaire_sequence2.html'), ('grain11', 'sommaire_sequence2.html'),
    ('grain12', 'sommaire_sequence2.html'), ('grain13', 'sommaire_sequence2.html'), ('grain_exp21', 'sommaire_sequence2.html'),
    ('grain14', 'sommaire_sequence3.html'), ('grain15', 'sommaire_sequence3.html'), ('grain16', 'sommaire_sequence3.html'),
    ('grain17', 'sommaire_sequence3.html'), ('grain18', 'sommaire_sequence3.html'),
]

scorm_block = '''        var GRAIN_ID = '{gid}';
        var SOMMAIRE_URL = '{seq}';
        function getState() {{ var raw = (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) ? ScormAPI.getSuspendData() : ''; if (!raw) try {{ raw = localStorage.getItem('module1_suspend'); }} catch (e) {{}} try {{ return raw ? JSON.parse(raw) : {{}}; }} catch (e) {{ return {{}}; }} }}
        function setState(o) {{ var s = JSON.stringify(o); if (s.length > 4000) return; if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) {{ ScormAPI.setSuspendData(s); ScormAPI.commit(); }} try {{ localStorage.setItem('module1_suspend', s); }} catch (e) {{}} }}
        function scormMarkCompleted() {{ var state = getState(); state.completed = state.completed || []; if (state.completed.indexOf(GRAIN_ID) === -1) state.completed.push(GRAIN_ID); setState(state); }}
        function toggleTheme() {{ document.body.classList.toggle('dark-mode'); var state = getState(); state.theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light'; setState(state); }}
        if (getState().theme === 'dark') document.body.classList.add('dark-mode');

'''

theme_pat = re.compile(
    r"(\s*)// Theme Management\s*\n\s*function toggleTheme\(\) \{\s*\n\s*document\.body\.classList\.toggle\('dark-mode'\);\s*\n\s*localStorage\.setItem\('theme', document\.body\.classList\.contains\('dark-mode'\) \? 'dark' : 'light'\);\s*\n\s*\}\s*\n\s*if\(localStorage\.getItem\('theme'\) === 'dark'\) document\.body\.classList\.add\('dark-mode'\);",
    re.MULTILINE
)
theme_pat2 = re.compile(
    r"(\s*)function toggleTheme\(\) \{\s*\n\s*document\.body\.classList\.toggle\('dark-mode'\);\s*\n\s*localStorage\.setItem\('theme', document\.body\.classList\.contains\('dark-mode'\) \? 'dark' : 'light'\);\s*\n\s*\}\s*\n\s*if\(localStorage\.getItem\('theme'\) === 'dark'\) document\.body\.classList\.add\('dark-mode'\);",
    re.MULTILINE
)

for gid, seq in config:
    path = os.path.join(base, gid + '.html')
    if not os.path.isfile(path):
        print('Skip', gid)
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    # 1. Add scorm script after viewport
    if 'scorm-runtime/scorm-api.js' not in html:
        html = html.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <script src="../../scorm-runtime/scorm-api.js"></script>\n    <title>',
            1
        )
    # 2. Remove progress-indicators.css
    html = re.sub(r'\s*<link rel="stylesheet" href="../../../../../assets/css/progress-indicators\.css">\s*', '\n', html)
    # 3. Replace sommaire_module1.html with seq
    html = html.replace('sommaire_module1.html', seq)
    # 4. Replace theme block with SCORM block
    repl = scorm_block.format(gid=gid, seq=seq)
    if theme_pat.search(html):
        html = theme_pat.sub(repl, html, count=1)
    elif theme_pat2.search(html):
        html = theme_pat2.sub(repl, html, count=1)
    # 5. Replace redirect: btn.onclick = ... window.location.href = 'sommaire_sequenceN.html#grainX' -> scormMarkCompleted + SOMMAIRE_URL
    html = re.sub(
        r"btn\.onclick = function\(\) \{ window\.location\.href = '" + re.escape(seq) + r"#" + re.escape(gid) + r"'; \};",
        "btn.onclick = function() { scormMarkCompleted(); window.location.href = SOMMAIRE_URL + '#" + gid + "'; };",
        html
    )
    html = re.sub(
        r"btn\.onclick = function\(\) \{ window\.location\.href = '" + re.escape(seq) + r"'; \};",
        "btn.onclick = function() { scormMarkCompleted(); window.location.href = SOMMAIRE_URL; };",
        html
    )
    # 6. Remove progress-indicators.js
    html = re.sub(r'\s*<script src="../../../../../assets/js/progress-indicators\.js"></script>\s*', '\n', html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK', gid)
