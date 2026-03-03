# SCORM — Règles suspend_data et bonnes pratiques

## Limites

- **SCORM 1.2** : `cmi.suspend_data` est limité à **4 Ko** (4096 caractères).
- **SCORM 2004** : limites plus souples selon l’implémentation du LMS ; rester raisonnable (ex. 64 Ko).

## Bonnes pratiques

1. **Compacter** : stocker uniquement les données nécessaires à la reprise (états, progression, réponses).
2. **Format** : préférer JSON minifié ou une structure courte (clé=valeur séparées par `&`).
3. **Éviter** : texte long, HTML, données déjà côté serveur.
4. **Découper** : si besoin de plus de 4 Ko en 1.2, utiliser plusieurs éléments (ex. `cmi.suspend_data` + objectifs ou éléments personnalisés si le LMS le permet).

## Utilisation avec scorm-api.js

Le runtime fourni expose des helpers pour lire/écrire `suspend_data`. Toujours vérifier la taille avant `SetValue` en environnement SCORM 1.2.
