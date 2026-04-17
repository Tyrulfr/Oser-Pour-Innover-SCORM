# Déployer le Module Ressources en SCORM sur Moodle

Le module est au format **SCORM 2004 (4th Edition)**. Moodle accepte les paquets SCORM 1.2 et 2004.

## Option A : Package SCORM prêt à l�?Temploi (ZIP)

Utilisez **`.\build.ps1`** (ou `./build.sh`) pour générer **`module-r-avancement.zip`**. Le ZIP contient à la **racine** :
- `imsmanifest.xml` (SCORM 2004 4th Edition)
- `index.html`
- `SCORM_API.js`
- les dossiers `pages/` et `assets/`

**Générer le ZIP** (voir README) :
- PowerShell : `.\build.ps1` �?' crée `module-r-avancement.zip` (et `module1-retours.zip` si le dossier existe).
- Git Bash : `./build.sh` �?' idem.

**Important** : à l�?Touverture du ZIP, la racine doit contenir directement `imsmanifest.xml`, `index.html`, `SCORM_API.js`, `pages/`, `assets/` (pas de dossier parent unique).

### Déposer le package dans Moodle

1. **Créer une ressource SCORM**
   - Dans votre cours Moodle : **Activer le mode édition** �?' **Ajouter une ressource ou une activité** �?' **Paquetage SCORM**.

2. **Paramètres recommandés**
   - **Nom** : ex. « Module Ressources : Sensibilisation �?" L'esprit d'innover »
   - **Fichier du paquetage** : glisser-déposer (ou parcourir) le fichier `module-r-avancement.zip`.
   - **Fenêtre** : « Fenêtre courante » ou « Fenêtre surgissante » selon votre charte.
   - **Note pour la réussite** : par ex. 0 (ou la note minimale souhaitée). Le module envoie un score 0�?"100 et un statut « completed » quand tout est validé.
   - **Tenter à nouveau** : selon votre politique (ex. autoriser plusieurs tentatives).

3. **Enregistrer et afficher**
   - Enregistrer la ressource. En cliquant sur l�?Tactivité, Moodle ouvrira le sommaire du Module Ressources (`index.html` à la racine du paquet).

Le contenu utilise l�?TAPI SCORM 2004 pour enregistrer la progression et le score dans Moodle (`cmi.completion_status`, `cmi.score.scaled`, `cmi.suspend_data`).

---

## Ce que le LMS (Moodle) exécute

- **Point d�?Tentrée** : `index.html` (à la racine du ZIP).
- **Chemins relatifs** : `SCORM_API.js`, `pages/sommaire_sequence1.html`, `pages/grain1.html`, etc., `assets/`.
- **API SCORM 2004** : le contenu appelle Initialize/Terminate, GetValue/SetValue, Commit pour :
  - `cmi.completion_status` (completed / incomplete)
  - `cmi.score.scaled` (0�?"1) et `cmi.score.raw` / `min` / `max`
  - `cmi.suspend_data` (état détaillé : grains validés, scores).

Importer le **fichier ZIP** généré par `build.sh` dans l�?Tactivité Paquetage SCORM.

---

## Dépannage

- **« Fichier manifest introuvable »** : le ZIP doit contenir `imsmanifest.xml` à la **racine** (pas dans un sous-dossier).
- **Page blanche ou 404** : vérifier que le ZIP contient bien `imsmanifest.xml`, `index.html`, `SCORM_API.js` et le dossier `pages/` à la racine.
- **Pas de suivi / pas de score** : le module est conçu pour être lancé **dans une iframe** par le LMS (contexte SCORM). Ouvrir `index.html` directement dans le navigateur ne connecte pas l�?TAPI �?" il faut passer par l�?Tactivité « Paquetage SCORM » dans Moodle.
