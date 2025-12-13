# Implementation Plan: Génération automatique de pre-commit config

**Branch**: `005-precommit-config` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-precommit-config/spec.md`

## Summary

Générer automatiquement un fichier `.pre-commit-config.yaml` lors de la création de projet, basé sur les technologies sélectionnées par l'utilisateur. Ajouter Ansible comme nouvelle technologie sélectionnable. Utiliser le même pattern de fragments Jinja2 que pour la génération du `.gitignore`.

## Technical Context

**Language/Version**: Python >= 3.10 (conforme à la constitution)
**Primary Dependencies**: Jinja2 >= 3.1.0 (templates), questionary >= 2.0.0 (CLI)
**Storage**: N/A (génération de fichiers)
**Testing**: pytest (validation manuelle pour MVP)
**Target Platform**: Linux/macOS/Windows (CLI cross-platform)
**Project Type**: single
**Performance Goals**: Génération instantanée
**Constraints**: Fichier YAML valide, compatible pre-commit
**Scale/Scope**: 7 technologies (Python, Node, Go, Terraform, Docker, IDE, Ansible) + hooks communs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Statut | Notes |
|----------|--------|-------|
| I. Simplicité et Minimalisme | ✅ PASS | Réutilisation du pattern fragments existant |
| II. Configuration-Driven | ✅ PASS | Pas de nouvelle config nécessaire |
| III. Template-Based Generation | ✅ PASS | Utilise Jinja2 comme les autres templates |
| IV. Expérience Utilisateur Interactive | ✅ PASS | Intégration transparente dans le flow existant |
| V. Sécurité First | ✅ N/A | Pas d'impact sécurité |

**Stack Technique**:
- ✅ Python >= 3.10: Conforme
- ✅ Jinja2 >= 3.1.0: Déjà utilisé
- ✅ questionary >= 2.0.0: Déjà utilisé pour la sélection des technos

## Project Structure

### Documentation (this feature)

```text
specs/005-precommit-config/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Décisions techniques
├── quickstart.md        # Guide de test
└── checklists/
    └── requirements.md  # Validation checklist
```

### Source Code (repository root)

```text
src/projinit/
├── __init__.py
├── cli.py               # À MODIFIER: Ajouter Ansible aux choix
├── generator.py         # À MODIFIER: Générer .pre-commit-config.yaml
└── templates/
    ├── gitignore/
    │   ├── _common.j2
    │   ├── ansible.j2   # NOUVEAU: Patterns Ansible
    │   └── ... (existants)
    └── precommit/       # NOUVEAU: Dossier pour fragments pre-commit
        ├── _header.j2   # En-tête YAML + hooks communs
        ├── python.j2
        ├── node.j2
        ├── go.j2
        ├── terraform.j2
        ├── docker.j2
        └── ansible.j2
```

**Structure Decision**: Projet existant de type "single". Création d'un nouveau dossier `templates/precommit/` avec le même pattern de fragments que `templates/gitignore/`.

## Implementation Strategy

### Approche Technique

1. **Créer les templates de fragments pre-commit** dans `templates/precommit/`:
   - `_header.j2`: En-tête YAML + hooks communs (pre-commit-hooks, yamllint, shfmt, shellcheck)
   - Un fichier par technologie avec les hooks spécifiques

2. **Ajouter la fonction `generate_precommit_content()`** dans `generator.py`:
   - Similaire à `generate_gitignore_content()`
   - Concatène header + fragments selon les technos sélectionnées

3. **Modifier `generate_project()`** dans `generator.py`:
   - Appeler `generate_precommit_content()` et écrire `.pre-commit-config.yaml`

4. **Ajouter Ansible aux technologies**:
   - Modifier `ask_technologies()` dans `cli.py`
   - Créer `templates/gitignore/ansible.j2`
   - Créer `templates/precommit/ansible.j2`

### Hooks par technologie

| Fragment | Repos/Hooks |
|----------|-------------|
| _header.j2 | pre-commit-hooks (end-of-file-fixer, trailing-whitespace, check-merge-conflict, check-yaml, detect-private-key), yamllint, shfmt, shellcheck |
| python.j2 | ruff |
| node.j2 | eslint, prettier |
| go.j2 | gofmt, golangci-lint |
| terraform.j2 | terraform_fmt, terraform_validate, terraform_tflint |
| docker.j2 | hadolint |
| ansible.j2 | ansible-lint |

## Complexity Tracking

> Aucune violation de la constitution - pas de justification nécessaire.
