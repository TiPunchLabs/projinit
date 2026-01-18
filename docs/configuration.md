# Configuration

## Hierarchie

projinit utilise une configuration hierarchique a 3 niveaux :

```
1. Defauts (code)      ← Priorite basse
2. Global (~/.config)
3. Local (.projinit)   ← Priorite haute
```

Les valeurs de niveau superieur ecrasent celles de niveau inferieur.

## Fichiers de Configuration

| Niveau | Chemin | Usage |
|--------|--------|-------|
| Global | `~/.config/projinit/config.yaml` | Preferences utilisateur |
| Local | `.projinit.yaml` (racine projet) | Configuration projet |

## Format

```yaml
# ~/.config/projinit/config.yaml

# Informations auteur
author:
  name: "John Doe"
  email: "john@example.com"

# Valeurs par defaut
defaults:
  python_version: "3.10"
  license: "MIT"
  visibility: "private"
  use_direnv: false

# Pass secret path
pass_secret_path: "projects/secrets"

# Owners GitHub
owners:
  - name: "myorg"
    label: "My Organization"
  - name: "personal"
    label: "Personal Account"

# Personnalisation standards
standards:
  # Changer niveau d'un check
  check_overrides:
    has_claude_md: required
    has_precommit: required

  # Desactiver des checks
  disabled_checks:
    - has_py_typed
    - envrc_uses_pass

  # Hooks pre-commit supplementaires
  extra_precommit_hooks:
    - repo: https://github.com/example/hook
      rev: v1.0.0
      hooks:
        - id: my-hook

# Templates personnalises
templates:
  templates_dir: ~/.config/projinit/templates
  overrides:
    README.md.j2: ~/.config/projinit/templates/my-readme.j2
```

## Options Detaillees

### author

Informations par defaut pour les fichiers generes.

```yaml
author:
  name: "John Doe"      # Pour LICENSE, pyproject.toml
  email: "john@example.com"  # Pour pyproject.toml
```

### defaults

Valeurs par defaut pour les questions interactives.

```yaml
defaults:
  python_version: "3.10"    # Version Python minimum
  license: "MIT"            # Type de licence
  visibility: "private"     # public/private
  use_direnv: false         # Activer direnv par defaut
```

### pass_secret_path

Chemin dans `pass` pour stocker les secrets projet.

```yaml
pass_secret_path: "projects/secrets"
# Les secrets seront: projects/secrets/<project-name>/...
```

### owners

Liste des owners GitHub disponibles.

```yaml
owners:
  - name: "tipunchlabs"
    label: "TiPunch Labs (Organization)"
  - name: "xgueret"
    label: "Xavier Gueret (Personal)"
```

### standards

Personnalisation des checks de conformite.

```yaml
standards:
  # Modifier le niveau d'un check
  check_overrides:
    has_claude_md: required      # Rendre obligatoire
    has_tests_dir: optional      # Rendre optionnel

  # Desactiver completement des checks
  disabled_checks:
    - has_py_typed               # Ne pas verifier py.typed
    - envrc_uses_pass            # Ignorer check direnv

  # Ajouter des hooks pre-commit
  extra_precommit_hooks:
    - repo: https://github.com/pre-commit/mirrors-prettier
      rev: v3.0.0
      hooks:
        - id: prettier
```

### templates

Personnalisation des templates Jinja2.

```yaml
templates:
  # Repertoire de templates personnalises
  templates_dir: ~/.config/projinit/templates

  # Remplacer des templates specifiques
  overrides:
    README.md.j2: ~/.config/projinit/templates/my-readme.j2
    LICENSE.j2: ~/.config/projinit/templates/my-license.j2
```

## Chargement

### Implementation

```python
# core/config.py

from dataclasses import dataclass
from pathlib import Path
import yaml

DEFAULT_CONFIG = {
    "python_version": "3.10",
    "license": "MIT",
    "visibility": "private",
    "use_direnv": False,
    "pass_secret_path": "projects/secrets",
}

GLOBAL_CONFIG_PATH = Path.home() / ".config" / "projinit" / "config.yaml"
LOCAL_CONFIG_NAME = ".projinit.yaml"

def load_config(project_path: Path = None) -> dict:
    """Charge et fusionne la configuration."""
    config = DEFAULT_CONFIG.copy()

    # Global
    if GLOBAL_CONFIG_PATH.exists():
        with open(GLOBAL_CONFIG_PATH) as f:
            global_config = yaml.safe_load(f)
            config = _merge(config, global_config)

    # Local
    if project_path:
        local_path = project_path / LOCAL_CONFIG_NAME
        if local_path.exists():
            with open(local_path) as f:
                local_config = yaml.safe_load(f)
                config = _merge(config, local_config)

    return config

def _merge(base: dict, override: dict) -> dict:
    """Fusionne deux dicts recursivement."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result
```

## Commandes Config

### Voir la configuration

```bash
$ projinit config show
```

Affiche la configuration fusionnee (defauts + global + local).

### Voir les chemins

```bash
$ projinit config paths

Configuration paths:
  Global: ~/.config/projinit/config.yaml (exists)
  Local:  .projinit.yaml (not found)
```

### Initialiser

```bash
# Creer config globale
$ projinit config init --global

# Creer config locale
$ projinit config init --local
```

## Exemples d'Utilisation

### Configuration Minimaliste

```yaml
# ~/.config/projinit/config.yaml
author:
  name: "John Doe"
  email: "john@example.com"
```

### Configuration Complete

```yaml
# ~/.config/projinit/config.yaml
author:
  name: "John Doe"
  email: "john@example.com"

defaults:
  python_version: "3.11"
  visibility: "private"
  use_direnv: true

pass_secret_path: "work/secrets"

owners:
  - name: "company"
    label: "Company Org"
  - name: "personal"
    label: "Personal"

standards:
  check_overrides:
    has_claude_md: required
    has_precommit: required
  disabled_checks:
    - has_py_typed

templates:
  templates_dir: ~/.config/projinit/templates
```

### Configuration Projet

```yaml
# .projinit.yaml
# Override pour ce projet specifique

standards:
  check_overrides:
    has_tests_dir: required  # Tests obligatoires ici
  disabled_checks:
    - envrc_uses_pass  # Pas de direnv pour ce projet
```

## Variables d'Environnement

Certaines valeurs peuvent etre definies via variables d'environnement :

| Variable | Description |
|----------|-------------|
| `PROJINIT_CONFIG` | Chemin config globale alternatif |
| `GITHUB_TOKEN` | Token pour operations GitHub |

```bash
export PROJINIT_CONFIG=/path/to/custom/config.yaml
export GITHUB_TOKEN=$(pass show github/token)
```

## Debugging

Afficher la configuration effective :

```python
from projinit.core.config import load_config
from pathlib import Path

config = load_config(Path.cwd())
import json
print(json.dumps(config, indent=2))
```

## Migration

Si le format de configuration change entre versions :

```python
def migrate_config(config: dict) -> dict:
    """Migre les anciennes configurations."""
    # v1 -> v2: renommer python_min_version
    if "python_min_version" in config:
        config["python_version"] = config.pop("python_min_version")

    return config
```
