# Gabarit site + SCORM

Coquille vide pour un nouveau programme. Aucun contenu du MOOC « L’Esprit d’innover ».

## Deux portes

1. **Portail concepteur** — `concepteur/index.html`  
   Annonce le titre, le nombre de modules et de grains.
2. **Site apprenant** — `index.html`  
   Généré ensuite, avec un ZIP SCORM par module.

## Créer la structure

1. Ouvrir `concepteur/index.html` (idéalement via un serveur local).
2. Régler modules / grains, puis **Télécharger programme.json**.
3. Remplacer `concepteur/programme.json` par ce fichier.
4. À la racine du gabarit :

```bash
python3 scripts/generer.py
```

5. Construire les paquets Moodle :

```bash
./build.sh
```

Chaque dossier `modules/module-N/` devient `module-N.zip` (imsmanifest à la racine du ZIP).

## Ce qui est généré

- Accueil à tuiles
- Un sommaire par module
- Une page de grain avec emplacement vidéo (à coller) et points d’accroche quiz / memory
- `imsmanifest.xml` + `SCORM_API.js` + suivi d’avancement

## Ce qui n’y est pas

Vidéos, quiz rédigés, transcripts, incrustations, capsules ressources, charte du projet précédent.

Les quiz se remplissent plus tard dans `modules/_shared/eval-bank.js` (puis relancer `./build.sh`, qui recopie le moteur dans chaque module).
