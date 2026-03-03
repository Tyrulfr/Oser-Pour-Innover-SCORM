# Oser Pour Innover — SCORM

Formation e-learning SCORM « Oser Pour Innover » (Module 1 : Sensibilisation).

## Structure du projet

- **imsmanifest.xml** — Manifeste SCORM 1.2 (point d’entrée : `modules/module1/index.html`)
- **scorm-runtime/** — API JS pour communiquer avec le LMS
- **modules/module1/** — Sommaire, 3 séquences, grains (quiz, progression, scores)
- **docs/** — Documentation (suspend_data, Moodle)

## Package SCORM pour Moodle (module 1)

Un manifeste **SCORM 1.2** est fourni à la racine. Pour obtenir un package prêt à déposer dans Moodle :

1. **Fermer** les fichiers du projet dans l’éditeur (éviter les fichiers verrouillés).
2. **Créer un ZIP** à la racine du projet contenant **uniquement** :
   - `imsmanifest.xml`
   - le dossier `scorm-runtime/`
   - le dossier `modules/`
3. **Sous Windows (PowerShell)** :
   ```powershell
   cd "chemin\vers\Oser-Pour-Innover-SCORM"
   Compress-Archive -Path imsmanifest.xml, scorm-runtime, modules -DestinationPath Oser-Pour-Innover-Module1-SCORM.zip -Force
   ```
4. Dans Moodle : **Ajouter une ressource ou une activité** → **Paquetage SCORM** → déposer le fichier `.zip`.

**Guide détaillé** : voir **`docs/MOODLE_SCORM_MODULE1.md`** (paramètres Moodle, dépannage).

Voir `docs/SCORM_SUSPEND_DATA.md` pour les règles sur les données de reprise (suspend_data).
