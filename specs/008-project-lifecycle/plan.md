# Implementation Plan: Project Lifecycle Management

**Branch**: `008-project-lifecycle` | **Date**: 2026-01-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/008-project-lifecycle/spec.md`
**Target Version**: v2.0.0

## Summary

Transformation de projinit d'un générateur de projets en un **gestionnaire de cycle de vie** avec 3 commandes principales : `init` (enrichi), `check` (audit de conformité), et `update` (mise à jour automatique). L'approche technique repose sur une architecture modulaire avec des standards externalisés en YAML et un système de détection automatique du type de projet.

## Technical Context

**Language/Version**: Python >= 3.10 (conforme à la constitution)
**Primary Dependencies**:
- questionary >= 2.0.0 (CLI interactif)
- rich >= 13.0.0 (affichage console)
- Jinja2 >= 3.1.0 (templates)
- PyYAML >= 6.0 (configuration)
- click >= 8.0.0 (commandes CLI - optionnel, à évaluer vs argparse)

**Storage**: Fichiers YAML pour les standards, système de fichiers pour les projets
**Testing**: pytest avec pytest-cov
**Target Platform**: Linux, macOS, Windows (CLI cross-platform)
**Project Type**: Single CLI application
**Performance Goals**: Audit < 5s pour projets < 1000 fichiers
**Constraints**: Pas de dépendances lourdes, installation via pipx/uv
**Scale/Scope**: Gestion de projets individuels, pas de monorepos (v2.0)

## Constitution Check

*Vérifié par rapport à `.specify/memory/constitution.md`*

| Principe | Statut | Notes |
|----------|--------|-------|
| Python >= 3.10 | ✓ Conforme | Maintenu |
| Structure src/tests | ✓ Conforme | Structure existante conservée |
| Simplicité avant abstraction | ✓ Conforme | Une classe par responsabilité |
| Templates Jinja2 | ✓ Conforme | Réutilisation des templates existants |
| Tests obligatoires | ✓ Conforme | Chaque commande testée |

## Project Structure

### Documentation (this feature)

```text
specs/008-project-lifecycle/
├── spec.md              # Spécification fonctionnelle
├── plan.md              # Ce fichier
└── tasks.md             # Tâches d'implémentation
```

### Source Code (repository root)

```text
src/
├── projinit/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée CLI (existant, à enrichir)
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── init_cmd.py      # Commande init (enrichie)
│   │   ├── check_cmd.py     # Commande check (nouveau)
│   │   └── update_cmd.py    # Commande update (nouveau)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── detector.py      # Détection type de projet
│   │   ├── checker.py       # Moteur d'audit
│   │   ├── updater.py       # Moteur de mise à jour
│   │   └── reporter.py      # Génération de rapports
│   ├── standards/
│   │   ├── __init__.py
│   │   ├── loader.py        # Chargement YAML
│   │   └── defaults/        # Standards par défaut
│   │       ├── base.yaml    # Standards obligatoires
│   │       ├── python.yaml  # Standards Python
│   │       ├── node.yaml    # Standards Node.js
│   │       └── infra.yaml   # Standards Infrastructure
│   └── templates/           # Templates Jinja2 (existants)

tests/
├── unit/
│   ├── test_detector.py
│   ├── test_checker.py
│   ├── test_updater.py
│   └── test_reporter.py
├── integration/
│   ├── test_init_cmd.py
│   ├── test_check_cmd.py
│   └── test_update_cmd.py
└── fixtures/
    ├── project_python/      # Projet Python de test
    ├── project_node/        # Projet Node.js de test
    └── project_infra/       # Projet Infrastructure de test
```

**Structure Decision**: Extension de la structure existante avec séparation claire entre CLI (commandes), Core (logique métier), et Standards (configuration). Les templates Jinja2 existants sont conservés et enrichis.

## Architecture

### Diagramme de flux

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLI       │────▶│   Core      │────▶│  Standards  │
│ (commands)  │     │  (logic)    │     │   (YAML)    │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                    │
      ▼                   ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Reporter   │     │  Templates  │     │   Schemas   │
│  (output)   │     │  (Jinja2)   │     │ (validation)│
└─────────────┘     └─────────────┘     └─────────────┘
```

### Composants principaux

1. **Detector** - Analyse le répertoire pour déterminer le type de projet
   - Recherche de fichiers marqueurs (pyproject.toml, package.json, main.tf)
   - Retourne un `ProjectType` avec score de confiance

2. **Checker** - Évalue la conformité aux standards
   - Charge les standards appropriés selon le type
   - Exécute les vérifications (fichier existe, contenu valide, etc.)
   - Retourne une liste de `CheckResult`

3. **Updater** - Applique les corrections
   - Crée les fichiers manquants à partir des templates
   - Fusionne intelligemment les configurations existantes
   - Gère les sauvegardes et rollback

4. **Reporter** - Génère les rapports
   - Formats: texte (rich), JSON, markdown
   - Score de conformité global
   - Suggestions de correction

### Format des standards YAML

```yaml
# standards/defaults/python.yaml
name: Python Project Standards
version: "1.0"
applies_to:
  markers:
    - pyproject.toml
    - setup.py

checks:
  - id: has_pyproject
    description: "pyproject.toml doit exister"
    level: required  # required | recommended | optional
    type: file_exists
    path: pyproject.toml

  - id: has_ruff_config
    description: "Configuration ruff dans pyproject.toml"
    level: recommended
    type: content_contains
    path: pyproject.toml
    pattern: "[tool.ruff]"

  - id: has_precommit
    description: "Pre-commit configuré"
    level: required
    type: file_exists
    path: .pre-commit-config.yaml
    template: precommit/python.yaml.j2

templates:
  - source: templates/pyproject.toml.j2
    target: pyproject.toml
    merge_strategy: smart  # smart | overwrite | skip_existing
```

## Phases d'implémentation

### Phase 1 - Fondations (Core)
- Detector: détection automatique du type de projet
- Standards loader: chargement et validation YAML
- Checker de base: vérifications file_exists

### Phase 2 - Commande Check
- CLI check avec options (--format, --verbose)
- Reporter: sortie texte et JSON
- Tests d'intégration sur fixtures

### Phase 3 - Commande Update
- Updater: création de fichiers manquants
- Gestion des sauvegardes
- Mode dry-run et interactif

### Phase 4 - Init enrichi
- Refactoring de init existant
- Utilisation des nouveaux standards
- Assistant interactif amélioré

### Phase 5 - Configuration externe
- Support ~/.config/projinit/
- Support .projinit.yaml local
- Documentation utilisateur

## Complexity Tracking

| Aspect | Choix | Alternative rejetée | Raison |
|--------|-------|---------------------|--------|
| Standards en YAML | Fichiers externes | Hardcodé Python | Personnalisation sans code |
| Merge strategy | Smart merge | Overwrite | Préserver config utilisateur |
| CLI framework | argparse (stdlib) | click | Moins de dépendances |

## Risques et mitigations

| Risque | Impact | Mitigation |
|--------|--------|-----------|
| Conflits de merge sur YAML | Moyen | Mode dry-run par défaut, sauvegardes |
| Détection type incorrecte | Faible | Option --type pour forcer |
| Standards trop rigides | Moyen | 3 niveaux (required/recommended/optional) |
