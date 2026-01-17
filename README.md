# projinit

```
██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
         Project Lifecycle Management Tool v2.0
```

[![CI](https://github.com/TiPunchLabs/projinit/actions/workflows/ci.yml/badge.svg)](https://github.com/TiPunchLabs/projinit/actions/workflows/ci.yml)

> CLI pour initialiser, auditer et mettre a jour des projets selon des standards definis.

> **Linux first** — Concu pour les environnements Linux. Peut fonctionner sur macOS, non teste sur Windows.

## Fonctionnalites v2.0

| Commande | Description |
|----------|-------------|
| `projinit check` | Auditer la conformite d'un projet |
| `projinit update` | Corriger automatiquement les non-conformites |
| `projinit new` | Creer un nouveau projet selon les standards |
| `projinit config` | Gerer la configuration |

## Installation

### Depuis les sources

```bash
# Cloner le depot
git clone https://github.com/xgueret/projinit.git
cd projinit

# Installer les dependances
uv sync

# Lancer
uv run projinit --version
```

### Installation globale (recommande)

```bash
# Installer comme outil global
uv tool install git+https://github.com/xgueret/projinit.git

# Verifier l'installation
projinit --version
```

## Utilisation

### Auditer un projet

Verifier la conformite d'un projet existant aux standards definis :

```bash
# Audit du projet courant (type auto-detecte)
projinit check

# Audit d'un projet specifique
projinit check /path/to/project

# Forcer le type de projet
projinit check -t python-cli

# Format de sortie (text, json, markdown)
projinit check -f markdown > audit-report.md

# Mode verbose (temps d'execution, fichiers scannes)
projinit check -v
```

Types de projets supportes :
- `python-cli` : Application CLI Python
- `python-lib` : Bibliotheque Python
- `node-frontend` : Application frontend Node.js
- `infrastructure` : Projet Terraform/Ansible
- `documentation` : Documentation MkDocs

### Corriger automatiquement

Appliquer les corrections automatiques pour atteindre la conformite :

```bash
# Correction automatique (avec backup)
projinit update

# Mode dry-run (voir sans appliquer)
projinit update --dry-run

# Mode interactif (confirmer chaque action)
projinit update --interactive

# Sans backup
projinit update --no-backup
```

### Creer un nouveau projet

Generer un nouveau projet conforme aux standards :

```bash
# Creation interactive
projinit new mon-projet

# Specifier le type
projinit new mon-projet -t python-cli

# Mode non-interactif
projinit new mon-projet -t python-cli -d "Description du projet" -y

# Dans un dossier specifique
projinit new mon-projet -p /path/to/parent
```

### Gerer la configuration

```bash
# Voir la configuration actuelle
projinit config show

# Voir les chemins de configuration
projinit config paths

# Creer un fichier de configuration
projinit config init --global  # ~/.config/projinit/config.yaml
projinit config init --local   # .projinit.yaml
```

## Configuration

### Hierarchie de configuration

1. **Valeurs par defaut** (integrees)
2. **Configuration globale** : `~/.config/projinit/config.yaml`
3. **Configuration locale** : `.projinit.yaml` (projet)

### Options de configuration

```yaml
# projinit configuration
author:
  name: "Votre Nom"
  email: "votre.email@example.com"

# Version Python par defaut
python_version: "3.10"

# Licence par defaut
default_license: "MIT"

# Personnalisation des standards
standards:
  # Changer le niveau d'un check
  check_overrides:
    has_claude_md: required  # Rendre CLAUDE.md obligatoire

  # Desactiver des checks
  disabled_checks:
    - has_py_typed

  # Ajouter des hooks pre-commit
  extra_precommit_hooks:
    - repo: https://github.com/example/hook
      rev: v1.0.0
      hooks:
        - id: example-hook

# Templates personnalises
templates:
  templates_dir: ~/.config/projinit/templates
  overrides:
    README.md.j2: ~/.config/projinit/templates/my-readme.j2
```

## Standards verifies

### Checks obligatoires (required)

| Check | Description |
|-------|-------------|
| `has_readme` | README.md present |
| `has_license` | Fichier LICENSE present |
| `has_gitignore` | .gitignore present |
| `has_pyproject` | pyproject.toml (Python) |
| `has_package_json` | package.json (Node.js) |

### Checks recommandes (recommended)

| Check | Description |
|-------|-------------|
| `has_claude_md` | CLAUDE.md pour les instructions IA |
| `has_precommit` | Configuration pre-commit |
| `has_src_dir` | Structure src/ (Python) |
| `has_tests_dir` | Repertoire tests/ |
| `has_ruff_config` | Configuration Ruff (Python) |

## Exemple de workflow

```bash
# 1. Auditer un projet existant
projinit check ~/mon-vieux-projet
# Score: 45.5% - NON-COMPLIANT

# 2. Voir ce qui serait corrige
projinit update ~/mon-vieux-projet --dry-run

# 3. Appliquer les corrections
projinit update ~/mon-vieux-projet

# 4. Verifier la conformite
projinit check ~/mon-vieux-projet
# Score: 100.0% - COMPLIANT

# 5. Creer un nouveau projet conforme
projinit new nouveau-projet -t python-cli
# Score: 100.0% - COMPLIANT
```

## Integration CI/CD

### GitHub Actions

```yaml
name: Conformity Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv tool install projinit
      - run: projinit check -f markdown >> $GITHUB_STEP_SUMMARY
```

### Export Markdown avec badges

```bash
projinit check -f markdown > CONFORMITY.md
```

Genere un rapport avec badges shields.io :

![Status](https://img.shields.io/badge/status-passing-brightgreen)
![Score](https://img.shields.io/badge/score-100%25-brightgreen)

## Developpement

```bash
# Cloner et installer
git clone https://github.com/xgueret/projinit.git
cd projinit
uv sync

# Lancer en developpement
uv run projinit check .

# Linting
uvx ruff check src/

# Tests
uv run pytest
```

## Licence

MIT
