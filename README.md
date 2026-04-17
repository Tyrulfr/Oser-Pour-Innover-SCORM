# L'esprit d'innover �?" SCORM (projet modulaire)

Formation e-learning SCORM « L'esprit d'innover ». Chaque module est un **paquet SCORM 2004 (4th Edition)** indépendant, prêt à être zippé et déployé sur un LMS (Moodle, etc.).

## Structure du projet

```
projet-scorm-pedagogique/
�"o�"?�"? README.md
�"o�"?�"? build.sh / build.ps1   # Génèrent les ZIP SCORM (lecture partagée sous Windows)
�"o�"?�"? scorm-api/
�",   �""�"?�"? SCORM_API.js
�"o�"?�"? modules/
�",   �"o�"?�"? module-r-avancement/   # Module Ressources : Sensibilisation (imsmanifest + pages + grains)
�",   �""�"?�"? module1-retours/      # Module 1 : Retours d'expérience (témoignages)
�"o�"?�"? tests/
�""�"?�"? docs/
```

- **Module Ressources** (`module-r-avancement/`) : sensibilisation, 3 séquences, grains.
- **Module 1** (`module1-retours/`) : témoignages (ex. Sylvia Cohen-Kaminsky).

## Build (créer les ZIP SCORM)

- **PowerShell (recommandé)** :
  ```powershell
  .\build.ps1
  ```
  Produit à la racine du projet :
  - `module-r-avancement.zip` �?" à déposer dans Moodle pour le Module Ressources
  - `module1-retours.zip` �?" pour le Module 1

- **Git Bash / WSL** :
  ```bash
  ./build.sh
  ```
  Même sortie si les dossiers `modules/module-r-avancement` et `modules/module1-retours` existent.

- **Creer_ZIP_SCORM_Module1.ps1** : délègue à `build.ps1` (ancienne structure SCORM_MODULE1_A_ZIPPER obsolète).

## Déploiement LMS

1. Lancer `.\build.ps1` (ou `./build.sh`).
2. Moodle : **Paquetage SCORM** �?' déposer `module-r-avancement.zip` ou `module1-retours.zip`.
3. Voir **docs/MOODLE_SCORM_MODULE1.md** (déploiement Module Ressources).

## Documentation

- **docs/MOODLE_SCORM_MODULE1.md** �?" Moodle, dépannage.
- **docs/SCORM_SUSPEND_DATA.md** �?" suspend_data.

## Tracking

- `LMSInitialize` / `LMSCommit` / `LMSFinish`, CMI 2004 : `cmi.completion_status`, `cmi.score.scaled`, `cmi.suspend_data`.
