# Changelog

Tous les changements notables de ce projet sont documentes dans ce fichier.

Le format est base sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhere a [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Added
- Documentation technique avec MkDocs
- Tests unitaires et d'integration (129 tests)
- Commande `/opensource-ready` pour verifier la preparation open source
- Commandes `/sync-docs` et `/sync-tech-docs` pour synchroniser la documentation
- Support du type de projet LAB (tutoriels/labs)
- Support direnv + pass pour la gestion des secrets
- Generation automatique du dossier `doc/` avec documentation technique
- Generation des commandes Claude Code (`.claude/commands/`)

### Changed
- Amelioration de la detection de type de projet
- Standards YAML externalises et configurables

### Fixed
- Correction de `_merge_standards` qui modifiait le dict original
- Correction de l'import dans `__main__.py`

## [2.0.0] - 2025-01-17

### Added
- Architecture v2.0 complete
- Systeme de standards YAML externalises
- Detection automatique du type de projet
- Support de 6 types de projets (Python CLI, Python Lib, Node Frontend, Infrastructure, Documentation, Lab)
- Commandes `check`, `new`, `update`, `config`
- Templates Jinja2 pour la generation de fichiers
- Configuration hierarchique (defauts < global < local)
- Pre-commit hooks configurables par type de projet

### Changed
- Refactoring complet depuis v1.x
- Nouvelle structure de projet modulaire

## [1.0.0] - 2024-12-01

### Added
- Version initiale
- Support basique Python et Terraform
