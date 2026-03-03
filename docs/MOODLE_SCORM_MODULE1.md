# Déployer le Module 1 en SCORM sur Moodle

## Option A : Package SCORM prêt à l’emploi (ZIP)

Le ZIP doit contenir **uniquement le module 1**. À l’intérieur du ZIP, à la **racine**, il doit y avoir exactement :
- `imsmanifest.xml`
- le dossier `scorm-runtime/`
- le dossier `modules/` **dans lequel il n’y a que** `module1/` (pas de module2, etc.)

---

### Méthode 1 : Créer un dossier puis compresser (recommandé si vous voulez n’avoir que le module 1)

1. **Créer un dossier** (ex. `SCORM-Module1`).
2. **Y copier** :
   - le fichier **`imsmanifest.xml`** (à la racine du projet) ;
   - le dossier **`scorm-runtime`** (en entier) ;
   - un dossier **`modules`** dans lequel vous mettez **uniquement** le dossier **`module1`** (tout le contenu de `modules/module1` du projet : `index.html`, grains, sommaires, `assets/`, etc.).  
   → Ne pas copier `module2` ni d’autres modules dans `modules/`.
3. **Compresser ce dossier** pour obtenir un fichier `.zip`.

   **Important** : à l’ouverture du ZIP, la **première chose visible** doit être `imsmanifest.xml`, `scorm-runtime` et `modules` (et pas un seul dossier parent).  
   - **Correct** : ouvrir le ZIP → on voit tout de suite `imsmanifest.xml`, `scorm-runtime/`, `modules/`.  
   - **Incorrect** : ouvrir le ZIP → on voit un seul dossier (ex. `SCORM-Module1`) et il faut cliquer dedans pour voir le reste.

   **Sous Windows** : si vous compressez le dossier `SCORM-Module1` en « Envoyer vers > Dossier compressé », la racine du ZIP sera `SCORM-Module1`. Il faut alors **ouvrir le ZIP**, sélectionner tout ce qu’il y a **à l’intérieur** de `SCORM-Module1` (imsmanifest.xml, scorm-runtime, modules), les extraire, puis créer un **nouveau** ZIP à partir de ces trois éléments.  
   Ou : ne pas compresser le dossier, mais **sélectionner** dans l’explorateur les trois éléments (imsmanifest.xml, scorm-runtime, modules) → clic droit → « Envoyer vers > Dossier compressé » pour que la racine du ZIP soit bonne.

---

### Méthode 2 : À la racine du projet (si `modules/` ne contient déjà que `module1`)

À la **racine du projet** (là où se trouvent `imsmanifest.xml`, `scorm-runtime/` et `modules/`), créez une archive contenant **exactement** :

- `imsmanifest.xml`
- le dossier `scorm-runtime/`
- le dossier `modules/` (avec **uniquement** `module1/` à l’intérieur si vous ne voulez que le module 1)

**Sous Windows (PowerShell)** :
```powershell
cd "c:\Users\cduboi4\Documents\Ingénierie\01_INNOV\04_Conception\Oser-Pour-Innover-SCORM"
Compress-Archive -Path imsmanifest.xml, scorm-runtime, modules -DestinationPath Oser-Pour-Innover-Module1-SCORM.zip
```

(Si votre dossier `modules` contient aussi module2, supprimez ou déplacez `module2` avant de lancer la commande, ou utilisez la Méthode 1 en ne copiant que `module1` dans un nouveau dossier `modules`.)

### 2. Déposer le package dans Moodle

1. **Créer une ressource SCORM**
   - Dans votre cours Moodle : **Activer le mode édition** → **Ajouter une ressource ou une activité** → **Paquetage SCORM**.

2. **Paramètres recommandés**
   - **Nom** : ex. « Module 1 : Sensibilisation — OSER POUR INNOVER »
   - **Fichier du paquetage** : glisser-déposer (ou parcourir) le fichier `Oser-Pour-Innover-Module1-SCORM.zip`.
   - **Fenêtre** : « Fenêtre courante » ou « Fenêtre surgissante » selon votre charte.
   - **Note pour la réussite** : par ex. 0 (ou la note minimale souhaitée). Le module envoie un score 0–100 et un statut « completed » quand tout est validé.
   - **Tenter à nouveau** : selon votre politique (ex. autoriser plusieurs tentatives).

3. **Enregistrer et afficher**
   - Enregistrer la ressource. En cliquant sur l’activité, Moodle ouvrira le sommaire du module 1 (`modules/module1/index.html`).

Le contenu utilise l’API SCORM pour enregistrer la progression et le score dans Moodle (suspend_data, score, completion).

---

## Option B : Ce que le LMS (Moodle) doit « voir »

Si vous ne déployez pas en ZIP mais que vous voulez savoir ce que le LMS exécute :

- **Point d’entrée (launch)** : le fichier lancé par le paquet SCORM est **`modules/module1/index.html`**.
- **Contexte de chargement** : ce fichier est servi depuis la racine du dépaquetage du ZIP. Tous les chemins sont relatifs à cette racine :
  - `scorm-runtime/scorm-api.js`
  - `modules/module1/sommaire_sequence1.html`, `grain1.html`, etc.
  - `modules/module1/assets/` (images, ex. logo)
- **API SCORM** : le contenu appelle l’API du LMS (GetValue, SetValue, Commit) pour :
  - `cmi.core.lesson_status` (ex. completed)
  - `cmi.core.score.raw` / `min` / `max`
  - `cmi.suspend_data` (état détaillé : grains validés, scores, thème)

Vous n’avez rien à copier-coller dans Moodle : il suffit d’importer le **fichier ZIP** du package (Option A).

---

## Dépannage

- **« Fichier manifest introuvable »** : le ZIP doit contenir `imsmanifest.xml` à la **racine** (pas dans un sous-dossier).
- **Page blanche ou 404** : vérifier que le ZIP contient bien `scorm-runtime/scorm-api.js` et `modules/module1/index.html`.
- **Pas de suivi / pas de score** : le module est conçu pour être lancé **dans une iframe** par le LMS (contexte SCORM). Ouvrir `index.html` directement dans le navigateur ne connecte pas l’API — il faut passer par l’activité « Paquetage SCORM » dans Moodle.
