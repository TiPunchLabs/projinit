# Implementation Plan: Sélection de Technologies pour .gitignore Adapté

**Branch**: `002-tech-gitignore` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-tech-gitignore/spec.md`

## Summary

Ajouter une question multi-select au questionnaire projinit permettant à l'utilisateur de sélectionner les technologies de son projet. Le fichier `.gitignore` sera généré dynamiquement par concaténation de fragments Jinja2 modulaires correspondant aux technologies sélectionnées. Terraform est présélectionné par défaut, les patterns communs sont toujours inclus.

## Technical Context

**Language/Version**: Python >= 3.10 (conforme à la constitution)
**Primary Dependencies**: questionary >= 2.0.0, Jinja2 >= 3.1.0, rich >= 13.0.0
**Storage**: N/A (pas de persistance, génération à la volée)
**Testing**: pytest (à implémenter selon constitution)
**Target Platform**: CLI Linux/macOS/Windows
**Project Type**: single (CLI Python existant)
**Performance Goals**: Génération < 2 secondes (existant)
**Constraints**: Pas de dépendance réseau, fragments embarqués dans le package
**Scale/Scope**: 6 technologies supportées initialement

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Statut | Justification |
|----------|--------|---------------|
| **I. Simplicité et Minimalisme** | ✅ PASS | Feature ciblée, pas de sur-ingénierie. Multi-select natif questionary, concaténation simple de fragments. |
| **II. Configuration-Driven** | ✅ PASS | Technologies par défaut pourraient être configurables en YAML (extension future). Pour MVP, liste hardcodée acceptable. |
| **III. Template-Based Generation** | ✅ PASS | Utilise Jinja2 pour les fragments .gitignore, cohérent avec l'architecture existante. |
| **IV. Expérience Utilisateur Interactive** | ✅ PASS | Question multi-select avec questionary, affichage dans le résumé avec Rich. |
| **V. Sécurité First** | ✅ PASS | Pas de données sensibles impliquées. |

**Gate Status**: ✅ PASSED - Aucune violation des principes constitutionnels.

## Project Structure

### Documentation (this feature)

```text
specs/002-tech-gitignore/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── checklists/
    └── requirements.md  # Spec validation checklist
```

### Source Code (repository root)

```text
src/projinit/
├── cli.py               # [MODIFY] Ajouter ask_technologies()
├── generator.py         # [MODIFY] Ajouter ProjectConfig.technologies, generate_gitignore()
├── config.py            # [NO CHANGE] (extension future pour technologies par défaut)
├── validators.py        # [NO CHANGE]
├── checks.py            # [NO CHANGE]
└── templates/
    ├── gitignore.j2     # [DELETE] Remplacé par fragments modulaires
    └── gitignore/       # [NEW] Répertoire des fragments
        ├── _common.j2   # Patterns universels (.DS_Store, logs, etc.)
        ├── python.j2    # __pycache__, *.pyc, .venv/, etc.
        ├── node.j2      # node_modules/, dist/, etc.
        ├── go.j2        # /bin, *.exe, vendor/, etc.
        ├── terraform.j2 # .terraform/, *.tfstate (existant)
        ├── docker.j2    # .docker/, *.log, etc.
        └── ide.j2       # .idea/, .vscode/, *.swp, etc.
```

**Structure Decision**: Extension de l'architecture existante. Nouveau sous-répertoire `templates/gitignore/` pour les fragments modulaires. Modification minimale de `cli.py` et `generator.py`.

## Complexity Tracking

> Aucune violation - pas de justification nécessaire.

## Implementation Approach

### Modifications Required

1. **cli.py**
   - Ajouter fonction `ask_technologies()` avec `questionary.checkbox()`
   - Insérer la question après `ask_direnv()`
   - Afficher les technologies dans `display_summary()`

2. **generator.py**
   - Étendre `ProjectConfig` avec `technologies: list[str]`
   - Créer fonction `generate_gitignore_content(technologies)` pour concaténer les fragments
   - Modifier `generate_project()` pour utiliser la nouvelle génération

3. **templates/gitignore/**
   - Créer 7 fichiers fragments (6 technos + common)
   - Chaque fragment avec header commenté identifiant la technologie

### Technology Choices

| Choix | Option Retenue | Alternatives Écartées |
|-------|----------------|----------------------|
| Multi-select | `questionary.checkbox()` | Prompt texte libre (moins UX) |
| Fragments | Fichiers .j2 séparés | Template unique avec conditionnels (moins maintenable) |
| Déduplication | Pas de déduplication auto | Parsing des patterns (over-engineering) |
| Ordre | common → alphabétique | Pas d'importance fonctionnelle |
