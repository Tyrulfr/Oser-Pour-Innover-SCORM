# Adapte les grains site -> SCORM (module1)
$src = "c:\Users\cduboi4\Documents\Ingénierie\01_INNOV\04_Conception\projet_inno_pui\pages\apprenant\cours\sensibilisation\module1"
$dst = "c:\Users\cduboi4\Documents\Ingénierie\01_INNOV\04_Conception\Oser-Pour-Innover-SCORM\modules\module1"

$grainToSeq = @{
    'grain1'='sommaire_sequence1.html'; 'grain2'='sommaire_sequence1.html'; 'grain3'='sommaire_sequence1.html'; 'grain4'='sommaire_sequence1.html'; 'grain5'='sommaire_sequence1.html'
    'grain6'='sommaire_sequence2.html'; 'grain7'='sommaire_sequence2.html'; 'grain8'='sommaire_sequence2.html'; 'grain9'='sommaire_sequence2.html'; 'grain10'='sommaire_sequence2.html'; 'grain11'='sommaire_sequence2.html'; 'grain12'='sommaire_sequence2.html'; 'grain13'='sommaire_sequence2.html'; 'grain_exp21'='sommaire_sequence2.html'
    'grain14'='sommaire_sequence3.html'; 'grain15'='sommaire_sequence3.html'; 'grain16'='sommaire_sequence3.html'; 'grain17'='sommaire_sequence3.html'; 'grain18'='sommaire_sequence3.html'
}

$scormHead = '    <script src="../../scorm-runtime/scorm-api.js"></script>
'
$scormScriptStart = @'
        var GRAIN_ID = 'GRAINID';
        var SOMMAIRE_URL = 'SOMMAIREURL';
        function getState() { var raw = (typeof ScormAPI !== "undefined" && ScormAPI.isAvailable()) ? ScormAPI.getSuspendData() : ""; if (!raw) try { raw = localStorage.getItem("module1_suspend"); } catch (e) {} try { return raw ? JSON.parse(raw) : {}; } catch (e) { return {}; } }
        function setState(o) { var s = JSON.stringify(o); if (s.length > 4000) return; if (typeof ScormAPI !== "undefined" && ScormAPI.isAvailable()) { ScormAPI.setSuspendData(s); ScormAPI.commit(); } try { localStorage.setItem("module1_suspend", s); } catch (e) {} }
        function scormMarkCompleted() { var state = getState(); state.completed = state.completed || []; if (state.completed.indexOf(GRAIN_ID) === -1) state.completed.push(GRAIN_ID); setState(state); }
        function toggleTheme() { document.body.classList.toggle("dark-mode"); var state = getState(); state.theme = document.body.classList.contains("dark-mode") ? "dark" : "light"; setState(state); }
        if (getState().theme === "dark") document.body.classList.add("dark-mode");

'@

$grains = @('grain1','grain2','grain3','grain4','grain5','grain6','grain7','grain8','grain9','grain10','grain11','grain12','grain13','grain14','grain15','grain16','grain17','grain18','grain_exp21')
foreach ($g in $grains) {
    $file = $g + '.html'
    $srcPath = Join-Path $src $file
    $dstPath = Join-Path $dst $file
    if (-not (Test-Path $srcPath)) { Write-Host "Skip $file (not found)"; continue }
    $html = Get-Content $srcPath -Raw -Encoding UTF8
    $seq = $grainToSeq[$g]
    # 1. Remove progress-indicators.css
    $html = $html -replace '\s*<link rel="stylesheet" href="../../../../../assets/css/progress-indicators\.css">\s*', "`n"
    # 2. Add scorm-api.js after viewport meta
    $html = $html -replace '(<meta name="viewport"[^>]+>)', "`$1`n$scormHead"
    # 3. Replace sommaire_module1.html with correct sequence
    $html = $html -replace 'sommaire_module1\.html', $seq
    # 4. Remove progress-indicators.js
    $html = $html -replace '\s*<script src="../../../../../assets/js/progress-indicators\.js"></script>\s*', "`n"
    # 5. Add SCORM script block after <script> (first script tag content)
    $scriptBlock = $scormScriptStart -replace 'GRAINID', "'$g'" -replace 'SOMMAIREURL', "'$seq'"
    $html = $html -replace '(<script>\s*)(// Theme Management|// Theme|function toggleTheme)', "`$1$scriptBlock`$2"
    # 6. Replace toggleTheme and theme load (remove old localStorage-only)
    $html = $html -replace 'function toggleTheme\(\) \{\s*document\.body\.classList\.toggle\([''"]dark-mode[''"]\);\s*localStorage\.setItem\([''"]theme[''"][^}]+\}\s*if\(localStorage\.getItem\([''"]theme[''"]\) === [''"]dark[''"]\) document\.body\.classList\.add\([''"]dark-mode[''"]\);', ''
    # 7. Replace redirect in btn.onclick
    $html = $html -replace "btn\.onclick = function\(\) \{ window\.location\.href = ['\"]sommaire_sequence\d\.html#${g}['\"]; \};", "btn.onclick = function() { scormMarkCompleted(); window.location.href = SOMMAIRE_URL + '#$g'; };"
    $html = $html -replace "window\.location\.href = ['\"]sommaire_sequence\d\.html['\"];", "scormMarkCompleted(); window.location.href = SOMMAIRE_URL;"
    [System.IO.File]::WriteAllText($dstPath, $html, [System.Text.UTF8Encoding]::new($false))
    Write-Host "OK $file"
}
