# ADR-0004: Detection par scoring avec poids

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit doit detecter automatiquement le type de projet (python-cli, node-frontend, infrastructure, etc.) en analysant la structure du repertoire. La methode de detection doit gerer les cas ambigus et les projets hybrides.

## Options considerees

1. **Rules-based** - Regles if/else sequentielles, premier match gagne, simple mais rigide
2. **Scoring** - Systeme de poids par marker, le type avec le meilleur score gagne, gere les ambiguites
3. **ML** - Modele de classification, puissant mais overhead disproportionne pour le cas d'usage

## Decision

Adopter un systeme de **scoring avec poids par marker** pour la detection du type de projet.

```python
PROJECT_MARKERS = {
    ProjectType.PYTHON_CLI: {
        "pyproject.toml": 0.3,
        "src/": 0.2,
        "__main__.py": 0.2,
    },
    ...
}
```

Chaque type de projet a un ensemble de markers avec des poids. Le score total determine le type detecte, avec un confidence score pour indiquer la fiabilite de la detection.

## Justification

- Gere naturellement les projets hybrides (un projet peut matcher plusieurs types)
- Permet la nuance grace aux poids differencies par marker
- Facile a debugger (on peut afficher les scores de chaque type)
- Pas d'overhead ML pour un probleme qui reste simple
- Extensible : ajouter un nouveau type = ajouter une entree dans le dictionnaire

## Consequences

- Necessite une calibration des poids pour eviter les faux positifs
- Peut etre ambigu pour les projets hybrides (ex: monorepo Python + infra)
- Le confidence score aide l'utilisateur a valider la detection
- Les poids doivent etre ajustes au fil du temps avec les retours utilisateurs
