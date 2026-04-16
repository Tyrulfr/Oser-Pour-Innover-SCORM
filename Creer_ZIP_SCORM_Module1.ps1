# Creer_ZIP_SCORM_Module1.ps1
# DEPRECATED : l'ancienne structure SCORM_MODULE1_A_ZIPPER n'existe plus.
# Utiliser a la place :  .\build.ps1
# Genere module0-avancement.zip (Module 0 sensibilisation) et module1-retours.zip (Module 1 temoignages).

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$buildPs1 = Join-Path $scriptDir "build.ps1"

if (Test-Path $buildPs1) {
    Write-Host "Lancement de build.ps1 (remplace l'ancien flux SCORM_MODULE1_A_ZIPPER)..."
    & $buildPs1
} else {
    Write-Error "build.ps1 introuvable dans $scriptDir"
    exit 1
}
