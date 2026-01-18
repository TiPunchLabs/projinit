# Systeme de Standards YAML

## Concept

Les standards definissent les criteres de conformite d'un projet. Ils sont externalises en fichiers YAML pour permettre leur personnalisation sans modifier le code.

## Structure des Fichiers

```
standards/
├── loader.py           # Charge et fusionne les standards
└── defaults/
    ├── base.yaml       # Checks communs a TOUS les types
    ├── python.yaml     # Specifique Python CLI/Lib
    ├── node.yaml       # Specifique Node.js
    ├── infra.yaml      # Specifique Infrastructure
    ├── documentation.yaml  # Specifique Documentation (MkDocs)
    └── lab.yaml        # Specifique Lab/Tutorial
```

## Anatomie d'un Fichier Standard

```yaml
# python.yaml
name: Python Standards
version: "1.0"
description: Standards for Python CLI and Library projects

checks:
  - id: has_pyproject
    description: pyproject.toml must exist
    level: required
    type: file_exists
    path: pyproject.toml
    template: templates/pyproject.toml.j2

  - id: has_src_dir
    description: src/ directory should exist
    level: recommended
    type: dir_exists
    path: src

  - id: has_ruff_config
    description: Ruff should be configured
    level: recommended
    type: content_contains
    path: pyproject.toml
    patterns:
      - "[tool.ruff]"
      - "ruff"
```

## Types de Checks

### 1. `file_exists`

Verifie qu'un fichier existe.

```yaml
- id: has_readme
  type: file_exists
  path: README.md
  template: templates/README.md.j2  # Template pour auto-fix
```

**Implementation** (`checker.py`) :
```python
def _check_file_exists(project_path: Path, check: dict) -> CheckResult:
    file_path = project_path / check["path"]
    if file_path.exists():
        return CheckResult(id=check["id"], status=CheckStatus.PASSED, ...)
    return CheckResult(id=check["id"], status=CheckStatus.FAILED, ...)
```

### 2. `dir_exists`

Verifie qu'un repertoire existe.

```yaml
- id: has_tests_dir
  type: dir_exists
  path: tests
```

### 3. `content_contains`

Verifie qu'un fichier contient certains patterns.

```yaml
- id: has_ruff_config
  type: content_contains
  path: pyproject.toml
  patterns:
    - "[tool.ruff]"
    - "ruff"
```

**Logique** : Au moins un pattern doit etre present (OR).

### 4. `any_exists`

Verifie qu'au moins un des fichiers existe.

```yaml
- id: has_eslint_config
  type: any_exists
  paths:
    - eslint.config.js
    - eslint.config.mjs
    - .eslintrc.js
    - .eslintrc.json
```

## Niveaux de Severite

| Niveau | Description | Impact sur le score |
|--------|-------------|---------------------|
| `required` | Obligatoire | Echec = non-compliant |
| `recommended` | Recommande | Echec = warning, affecte le score |
| `optional` | Optionnel | Informatif seulement |

## Chargement des Standards

Le `loader.py` fusionne les standards :

```python
def load_standards(project_type: ProjectType) -> list[dict]:
    """Charge base.yaml + fichier specifique au type."""
    checks = []

    # 1. Charger base.yaml (toujours)
    base_checks = _load_yaml("base.yaml")
    checks.extend(base_checks)

    # 2. Charger le fichier du type
    type_file = TYPE_MAPPING.get(project_type)
    if type_file:
        type_checks = _load_yaml(type_file)
        checks.extend(type_checks)

    return checks
```

**Mapping type -> fichier** :
```python
TYPE_MAPPING = {
    ProjectType.PYTHON_CLI: "python.yaml",
    ProjectType.PYTHON_LIB: "python.yaml",
    ProjectType.NODE_FRONTEND: "node.yaml",
    ProjectType.INFRASTRUCTURE: "infra.yaml",
    ProjectType.DOCUMENTATION: "documentation.yaml",
    ProjectType.LAB: "lab.yaml",
}
```

## Personnalisation

### Via configuration locale

Dans `.projinit.yaml` du projet :

```yaml
standards:
  # Changer le niveau d'un check
  check_overrides:
    has_claude_md: required    # Rendre obligatoire
    has_tests_dir: optional    # Rendre optionnel

  # Desactiver des checks
  disabled_checks:
    - has_py_typed
    - envrc_uses_pass
```

### Via configuration globale

Dans `~/.config/projinit/config.yaml` :

```yaml
standards:
  # Memes options que local
  check_overrides:
    has_precommit: required
```

## Ajouter un Nouveau Check

### Etape 1 : Definir dans le YAML

```yaml
# Dans python.yaml
- id: has_mypy_config
  description: mypy configuration should exist
  level: recommended
  type: any_exists
  paths:
    - mypy.ini
    - .mypy.ini
    - pyproject.toml  # avec [tool.mypy]
```

### Etape 2 : Si nouveau type de check

Dans `core/checker.py` :

```python
def _check(project_path: Path, check: dict) -> CheckResult:
    check_type = check["type"]

    if check_type == "file_exists":
        return _check_file_exists(project_path, check)
    elif check_type == "dir_exists":
        return _check_dir_exists(project_path, check)
    elif check_type == "content_contains":
        return _check_content_contains(project_path, check)
    elif check_type == "any_exists":
        return _check_any_exists(project_path, check)
    # Ajouter ici
    elif check_type == "my_new_type":
        return _check_my_new_type(project_path, check)
```

## Standards par Type de Projet

### Python (CLI/Lib)

| Check | Niveau | Description |
|-------|--------|-------------|
| `has_pyproject` | required | pyproject.toml |
| `has_src_dir` | recommended | Structure src/ |
| `has_tests_dir` | recommended | Repertoire tests/ |
| `has_ruff_config` | recommended | Configuration Ruff |
| `has_py_typed` | optional | Marker py.typed (lib) |

### Node.js Frontend

| Check | Niveau | Description |
|-------|--------|-------------|
| `has_package_json` | required | package.json |
| `has_src_dir` | recommended | Structure src/ |
| `has_tsconfig` | recommended | TypeScript config |
| `has_eslint_config` | recommended | ESLint config |
| `has_vite_config` | recommended | Vite config |

### Infrastructure

| Check | Niveau | Description |
|-------|--------|-------------|
| `has_terraform_main` | required | main.tf |
| `has_terraform_variables` | required | variables.tf |
| `has_ansible_playbook` | recommended | playbook.yml |

### Lab/Tutorial

| Check | Niveau | Description |
|-------|--------|-------------|
| `has_labs_or_exercises` | required | labs/, exercises/ ou modules/ |
| `has_lab_readme` | required | README.md avec instructions |
| `has_solutions` | recommended | solutions/, answers/ ou corrections/ |
| `has_documentation` | recommended | mkdocs.yml ou docs/index.md |
| `has_prerequisites` | recommended | Section prerequis dans README |
| `has_progression` | optional | Numerotation des labs |
| `has_assets` | optional | Dossier assets/ ou images/ |
| `mkdocs_has_nav` | recommended | Navigation MkDocs configuree |

### Base (tous types)

| Check | Niveau | Description |
|-------|--------|-------------|
| `has_readme` | required | README.md |
| `has_license` | required | LICENSE |
| `has_gitignore` | required | .gitignore |
| `has_claude_md` | recommended | CLAUDE.md |
| `has_precommit` | recommended | .pre-commit-config.yaml |
| `precommit_has_basic_hooks` | recommended | Hooks de base (trailing-whitespace, end-of-file-fixer) |
| `has_claude_commands` | recommended | .claude/commands/ |
| `has_technical_docs` | recommended | doc/ ou docs/ avec documentation technique |
| `envrc_uses_pass` | recommended | .envrc avec pass |

## Debugging

Voir les checks charges :

```python
from projinit.standards.loader import load_standards
from projinit.core.models import ProjectType

checks = load_standards(ProjectType.PYTHON_CLI)
for c in checks:
    print(f"{c['id']}: {c['level']} - {c['type']}")
```
