# Implementation Plan: Pipeline CI/CD GitHub Actions

**Branch**: `007-github-actions-ci` | **Date**: 2025-12-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-github-actions-ci/spec.md`

## Summary

Mettre en place un pipeline GitHub Actions pour automatiser la validation du code (linting avec ruff, vérification du formatage, exécution des tests pytest) à chaque push et Pull Request. Le pipeline doit fournir des retours clairs et rapides aux développeurs.

## Technical Context

**Language/Version**: YAML (GitHub Actions workflow syntax)
**Primary Dependencies**: GitHub Actions, actions/checkout, actions/setup-python, uv (astral-sh/setup-uv)
**Storage**: N/A
**Testing**: pytest (exécuté par le pipeline)
**Target Platform**: GitHub Actions runners (ubuntu-latest)
**Project Type**: single (CLI Python project)
**Performance Goals**: Pipeline complet < 5 minutes
**Constraints**: Déclenchement < 30 secondes après push
**Scale/Scope**: Tous les pushes et PRs vers main

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Python >= 3.10 - Conforme (pyproject.toml spécifie >=3.10)
- [x] Utilisation de uv comme gestionnaire de packages - Conforme
- [x] Utilisation de ruff pour linting/formatting - Conforme
- [x] pytest pour les tests - Conforme

## Project Structure

### Documentation (this feature)

```text
specs/007-github-actions-ci/
├── plan.md              # This file
├── spec.md              # Feature specification
└── tasks.md             # Task list (to be generated)
```

### Source Code (repository root)

```text
.github/
└── workflows/
    └── ci.yml           # GitHub Actions CI workflow (NEW)
```

**Structure Decision**: Un seul fichier workflow YAML dans `.github/workflows/` suivant les conventions GitHub Actions. Le workflow sera nommé `ci.yml` pour indiquer son rôle de Continuous Integration.

## Workflow Design

### Triggers

- `push`: Sur toutes les branches
- `pull_request`: Vers la branche `main`

### Jobs

1. **lint**: Vérification du code avec `ruff check`
2. **format**: Vérification du formatage avec `ruff format --check`
3. **test**: Exécution des tests avec `pytest`

### Steps par Job

Chaque job suivra cette structure:
1. Checkout du code (actions/checkout@v4)
2. Setup Python (actions/setup-python@v5 avec python-version: "3.10")
3. Setup uv (astral-sh/setup-uv@v4)
4. Installation des dépendances (`uv sync`)
5. Exécution de la commande spécifique (ruff/pytest)

## Complexity Tracking

Aucune violation de la constitution - implémentation simple et directe.
