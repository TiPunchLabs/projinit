# Open Source Ready Check

Verifie si le projet est pret a etre publie en open source et propose de creer les fichiers manquants.

## Arguments

| Argument | Description |
|----------|-------------|
| (aucun) | Analyse complete avec rapport |
| `--fix` | Analyse + creation des fichiers manquants |
| `--security` | Focus sur les verifications de securite |
| `--docs` | Focus sur la documentation |

$ARGUMENTS

---

## PHASE 1 : DETECTION DU TYPE DE PROJET

Type detecte : **Python CLI Application**

Fichiers de configuration attendus : `pyproject.toml`, `src/`, `tests/`

---

## PHASE 2 : DOCUMENTATION (25 points)

### 2.1 Fichiers essentiels

| Fichier | Points | Description | Obligatoire |
|---------|--------|-------------|-------------|
| `README.md` | 5 | Documentation principale | Oui |
| `LICENSE` | 5 | Licence du projet | Oui |
| `CONTRIBUTING.md` | 4 | Guide de contribution | Recommande |
| `CODE_OF_CONDUCT.md` | 3 | Code de conduite | Recommande |
| `CHANGELOG.md` | 3 | Historique des versions | Recommande |
| `SECURITY.md` | 3 | Politique de securite | Recommande |
| `CLAUDE.md` | 2 | Contexte pour Claude Code | Optionnel |

### 2.2 Qualite du README

Verifier la presence des sections :

| Section | Points |
|---------|--------|
| Description/Overview | 1 |
| Installation/Quick Start | 1 |
| Usage/Configuration | 1 |
| Prerequisites | 1 |
| Contributing | 1 |
| License mention | 1 |

### 2.3 Verification

```bash
# Fichiers de documentation
ls README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md CHANGELOG.md SECURITY.md 2>/dev/null
```

---

## PHASE 3 : SECURITE (25 points)

### 3.1 Scan des secrets dans le code

Patterns a detecter :

```
# API Keys
[A-Za-z0-9_]{20,}
api[_-]?key
secret[_-]?key
access[_-]?token

# Passwords
password\s*=\s*["'][^"']+["']
passwd\s*=
pwd\s*=

# AWS
AKIA[0-9A-Z]{16}
aws[_-]?secret

# Tokens
bearer\s+[A-Za-z0-9\-._~+/]+=*
token\s*=\s*["'][^"']+["']

# Private keys
-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----
```

### 3.2 Scan de l'historique git

```bash
# Rechercher des secrets dans l'historique
git log -p --all | grep -iE "(password|secret|api.?key|token)" | head -20
```

### 3.3 Verification .gitignore

Fichiers sensibles qui doivent etre ignores :

| Pattern | Description |
|---------|-------------|
| `.env` | Variables d'environnement |
| `*.pem` | Cles privees |
| `*.key` | Cles privees |
| `*credentials*` | Fichiers de credentials |
| `*secret*` | Fichiers secrets |
| `.venv/` | Environnement virtuel |
| `__pycache__/` | Cache Python |
| `*.egg-info/` | Metadata package |

### 3.4 Scoring securite

| Verification | Points |
|--------------|--------|
| Pas de secrets dans le code | 8 |
| Pas de secrets dans l'historique git | 5 |
| .gitignore complet | 5 |
| SECURITY.md present | 3 |

---

## PHASE 4 : GITHUB/GIT (20 points)

### 4.1 Templates GitHub

Verifier la presence de `.github/` :

| Fichier | Points | Description |
|---------|--------|-------------|
| `.github/ISSUE_TEMPLATE/bug_report.md` | 3 | Template bug |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 3 | Template feature |
| `.github/PULL_REQUEST_TEMPLATE.md` | 3 | Template PR |
| `.github/CODEOWNERS` | 2 | Proprietaires du code |
| `.github/FUNDING.yml` | 1 | Sponsors |
| `.github/dependabot.yml` | 2 | Mises a jour auto |

### 4.2 GitHub Actions (CI/CD)

| Fichier | Points | Description |
|---------|--------|-------------|
| `.github/workflows/ci.yml` | 3 | Integration continue |
| `.github/workflows/release.yml` | 2 | Release automatique |

### 4.3 Configuration git

```bash
# Verifier .gitignore
test -f .gitignore && echo "OK" || echo "MANQUANT"

# Verifier .gitattributes
test -f .gitattributes && echo "OK" || echo "MANQUANT"
```

---

## PHASE 5 : QUALITE DU CODE (20 points)

### 5.1 Linters et formatters

| Outil | Points | Verification |
|-------|--------|--------------|
| Pre-commit configure | 5 | `.pre-commit-config.yaml` existe |
| Linters passent | 5 | `pre-commit run --all-files` |
| EditorConfig | 2 | `.editorconfig` existe |

### 5.2 Tests (si applicable)

| Element | Points |
|---------|--------|
| Tests presents | 3 |
| Tests passent | 3 |
| Couverture > 50% | 2 |

### 5.3 Verification Python

```bash
# Linting
uvx ruff check src/

# Format
uvx ruff format --check src/

# Tests
uv run pytest
```

---

## PHASE 6 : METADONNEES (10 points)

### 6.1 Informations du projet

| Element | Points | Verification |
|---------|--------|--------------|
| Description dans README | 2 | Premiere section claire |
| Version definie | 2 | Tag git ou fichier version |
| Auteur/Maintainer | 2 | Dans README ou package |
| URL du repo | 2 | Dans README |
| Badges | 2 | Status, license, version |

---

## PHASE 7 : RAPPORT ET SCORING

### Format du rapport

```
Open Source Ready Check
=======================

Projet : projinit
Type   : Python CLI Application
Date   : {date}

SCORE GLOBAL : {X}/100 - {STATUT}

Statuts :
  90-100 : READY        - Pret pour publication
  70-89  : ALMOST READY - Quelques ajustements
  50-69  : NEEDS WORK   - Travail necessaire
  0-49   : NOT READY    - Non pret
```

---

## PHASE 8 : CREATION DES FICHIERS MANQUANTS

Si `--fix` ou confirmation, creer les fichiers avec des templates adaptes.

### 8.1 CONTRIBUTING.md

```markdown
# Contributing to projinit

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Code Style

- Run `pre-commit run --all-files` before committing
- Follow existing code patterns

## Questions?

Open an issue for any questions or concerns.
```

### 8.2 CODE_OF_CONDUCT.md

```markdown
# Code of Conduct

## Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

## Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

Examples of unacceptable behavior:

- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could be considered inappropriate

## Enforcement

Instances of abusive behavior may be reported to the project maintainers.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org/).
```

### 8.3 SECURITY.md

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do not** open a public issue
2. Email the maintainers directly
3. Include details about the vulnerability
4. Allow time for a fix before public disclosure

We take security seriously and will respond promptly.
```

### 8.4 CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Initial release

### Changed

### Fixed

### Removed
```

### 8.5 .editorconfig

```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[*.yml]
indent_size = 2

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
```

### 8.6 .github/workflows/ci.yml (Python)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uvx ruff check src/

  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uvx ruff format --check src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync
      - run: uv run pytest
```

---

## NOTES

- Toujours demander confirmation avant de creer des fichiers
- Adapter les templates au contexte du projet
- Le scoring est indicatif, certains elements peuvent etre optionnels selon le projet
- Verifier les licences des dependances pour compatibilite
