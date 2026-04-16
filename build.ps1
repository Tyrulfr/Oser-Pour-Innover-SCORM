# build.ps1 - Cree les ZIP SCORM (module0-avancement, module1-retours) avec lecture partagee
# Chaque ZIP a imsmanifest.xml a la racine pour Moodle.
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Build-ModuleZip {
    param([string]$modulePath, [string]$zipName)
    $src = Join-Path $root $modulePath
    $zipPath = Join-Path $root $zipName
    if (-not (Test-Path $src)) { Write-Warning "Source introuvable: $src"; return }
    if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
    $files = Get-ChildItem -Path $src -Recurse -File
    $baseLen = $src.TrimEnd('\').Length + 1
    $zip = [System.IO.Compression.ZipFile]::Open($zipPath, 'Create')
    try {
        foreach ($f in $files) {
            $entryName = $f.FullName.Substring($baseLen).Replace('\', '/')
            try {
                $stream = [System.IO.File]::Open($f.FullName, 'Open', 'Read', 'Read')
                try {
                    $entry = $zip.CreateEntry($entryName)
                    $entryStream = $entry.Open()
                    try { $stream.CopyTo($entryStream) } finally { $entryStream.Close() }
                } finally { $stream.Close() }
            } catch { Write-Warning "Ignore: $entryName - $_" }
        }
    } finally { $zip.Dispose() }
    $size = [math]::Round((Get-Item $zipPath).Length / 1KB, 1)
    Write-Host "Build OK: $zipName ($size Ko)"
}

# Module 0 : Sensibilisation (paquet SCORM autonome)
Build-ModuleZip -modulePath "modules\module0-avancement" -zipName "module0-avancement.zip"
# Module 1 : Retours d'experience / temoignages
Build-ModuleZip -modulePath "modules\module1-retours" -zipName "module1-retours.zip"
