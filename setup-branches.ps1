# �? exécuter dans la racine du repo (Oser-Pour-Innover-SCORM)
# Assure les 3 branches main, develop, sauv avec le même premier commit

$list = git branch --list
if ($list -notmatch '\bmain\b') { git branch main }
git checkout main
git add .
git status
git commit -m "Structure initiale : README, docs, scorm-runtime, modules, packaging"
# Recréer develop et sauv à partir de main pour qu'elles aient le même commit
git branch -D develop 2>$null; git branch develop
git branch -D sauv 2>$null; git branch sauv
git checkout develop
Write-Host "OK. Branches : main, develop, sauv (meme commit). Vous etes sur develop."
