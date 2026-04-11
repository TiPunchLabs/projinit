# Guide d'extension

**Derniere mise a jour**: 2026-01-18

Ce guide explique comment etendre projinit avec de nouveaux types de projets, checks, et commandes.

## Ajouter un nouveau type de projet

### 1. Ajouter l'enum

**Fichier**: `src/projinit/core/models.py`

```python
class ProjectType(Enum):
    # Types existants...
    MY_NEW_TYPE = "my-new-type"
    # ...

    @property
    def display_name(self) -> str:
        names = {
            # ...
            ProjectType.MY_NEW_TYPE: "My New Type Project",
        }
        return names.get(self, self.value)
```

### 2. Ajouter les markers de detection

**Fichier**: `src/projinit/core/detector.py`

```python
PROJECT_MARKERS: dict[ProjectType, dict[str, float]] = {
    # ...
    ProjectType.MY_NEW_TYPE: {
        "my-config.yaml": 0.5,     # Fichier specifique
        "specific-dir/": 0.3,      # Repertoire caracteristique
        "marker-file.txt": 0.2,    # Autre marker
    },
}
```

Optionnel: Ajouter des markers distinctifs basés sur le contenu:

```python
DISTINGUISHING_MARKERS: dict[str, tuple[ProjectType, float]] = {
    # ...
    "my-specific-pattern": (ProjectType.MY_NEW_TYPE, 0.2),
}
```

### 3. Creer le fichier de standards

**Fichier**: `src/projinit/standards/defaults/my-new-type.yaml`

```yaml
name: My New Type Standards
version: "1.0"
description: Standards for My New Type projects
applies_to:
  - my-new-type

markers:
  - my-config.yaml

checks:
  - id: has_config
    description: my-config.yaml must exist
    level: required
    type: file_exists
    path: my-config.yaml
    template: templates/my-config.yaml.j2

  - id: has_src
    description: Source directory should exist
    level: recommended
    type: dir_exists
    path: src/

  - id: config_has_version
    description: Config should specify version
    level: recommended
    type: content_contains
    path: my-config.yaml
    patterns:
      - "version:"

precommit_hooks:
  - repo: https://github.com/my-linter
    rev: v1.0.0
    hooks:
      - id: my-lint
```

### 4. Ajouter la generation dans init_cmd.py

**Fichier**: `src/projinit/cli/init_cmd.py`

```python
def _get_files_for_type(project_type: ProjectType) -> list[str]:
    # ...
    type_specific = {
        # ...
        ProjectType.MY_NEW_TYPE: [
            "my-config.yaml",
            "src/main.xyz",
            "tests/",
        ],
    }
    return common + type_specific.get(project_type, [])


def _generate_project(...):
    # ...
    elif project_type == ProjectType.MY_NEW_TYPE:
        _generate_my_new_type_project(env, target_dir, context)


def _generate_my_new_type_project(
    env: Environment,
    target_dir: Path,
    context: dict,
) -> None:
    """Generate My New Type project files."""
    # Config file
    (target_dir / "my-config.yaml").write_text(f"""
version: "1.0"
name: {context["project_name"]}
""")

    # Source directory
    src_dir = target_dir / "src"
    src_dir.mkdir(exist_ok=True)
    (src_dir / "main.xyz").write_text("# Main file\n")

    # Tests
    tests_dir = target_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
```

### 5. Ajouter les templates (optionnel)

**Fichier**: `src/projinit/templates/my-config.yaml.j2`

```jinja
# Configuration for {{ project_name }}
version: "1.0"
name: {{ project_name }}
description: {{ description }}
```

### 6. Tester

```bash
# Detection
projinit check /path/to/my-new-type-project

# Generation
projinit new test-project -t my-new-type
```

---

## Ajouter un nouveau type de check

### 1. Ajouter le handler

**Fichier**: `src/projinit/core/checker.py`

```python
def _run_single_check(self, check_def: dict) -> CheckResult:
    # ...
    if check_type == "file_exists":
        return self._check_file_exists(...)
    elif check_type == "my_new_check_type":
        return self._check_my_new_type(check_def, check_id, level, description)
    # ...


def _check_my_new_type(
    self,
    check_def: dict,
    check_id: str,
    level: CheckLevel,
    description: str,
) -> CheckResult:
    """Check something specific."""
    # Get parameters from check_def
    path = check_def.get("path", "")
    expected_value = check_def.get("expected_value", "")

    file_path = self.project_path / path

    if not file_path.exists():
        return CheckResult(
            id=check_id,
            status=CheckStatus.SKIPPED,
            message=f"File {path} not found",
            level=level,
            file_path=file_path,
        )

    # Your check logic here
    content = file_path.read_text()
    if expected_value in content:
        return CheckResult(
            id=check_id,
            status=CheckStatus.PASSED,
            message=f"Found {expected_value} in {path}",
            level=level,
            file_path=file_path,
        )

    return CheckResult(
        id=check_id,
        status=CheckStatus.FAILED,
        message=f"{description} - {expected_value} not found in {path}",
        level=level,
        suggestion=f"Add {expected_value} to {path}",
        file_path=file_path,
    )
```

### 2. Utiliser dans les standards

```yaml
checks:
  - id: my_custom_check
    description: Check for something specific
    level: recommended
    type: my_new_check_type
    path: config.yaml
    expected_value: "required-string"
```

---

## Ajouter une nouvelle commande CLI

### 1. Creer le fichier de commande

**Fichier**: `src/projinit/cli/mycommand_cmd.py`

```python
"""My command for projinit."""

import argparse
import sys
from pathlib import Path

from rich.console import Console

console = Console()


def add_mycommand_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the mycommand subcommand to the parser."""
    parser = subparsers.add_parser(
        "mycommand",
        help="Description of my command",
        description="Longer description.",
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Path argument",
    )
    parser.add_argument(
        "-o",
        "--option",
        type=str,
        help="Some option",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.set_defaults(func=run_mycommand)


def run_mycommand(args: argparse.Namespace) -> int:
    """
    Run my command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code.
    """
    project_path = Path(args.path).resolve()

    if not project_path.is_dir():
        console.print(f"[red]Error: {project_path} is not a directory[/red]")
        return 2

    # Command logic here
    console.print(f"[green]Running mycommand on {project_path}[/green]")

    if args.verbose:
        console.print("[dim]Verbose output...[/dim]")

    return 0


def main() -> None:
    """Standalone entry point."""
    parser = argparse.ArgumentParser(
        prog="projinit mycommand",
        description="My command description",
    )
    parser.add_argument("path", type=str, nargs="?", default=".")
    parser.add_argument("-o", "--option", type=str)
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    sys.exit(run_mycommand(args))


if __name__ == "__main__":
    main()
```

### 2. Enregistrer dans main_cli.py

**Fichier**: `src/projinit/main_cli.py`

```python
from projinit.cli.mycommand_cmd import add_mycommand_parser, run_mycommand

def parse_args() -> argparse.Namespace:
    # ...
    add_mycommand_parser(subparsers)  # Ajouter cette ligne
    # ...


def main() -> None:
    # ...
    if args.command == "mycommand":
        exit_code = run_mycommand(args)
        sys.exit(exit_code)
    # ...
```

### 3. Tester

```bash
projinit mycommand --help
projinit mycommand /path/to/project -v
```

---

## Ajouter un template personnalise

### 1. Creer le template

**Fichier**: `src/projinit/templates/my-template.xyz.j2`

```jinja
# {{ project_name }}
# Generated by projinit

{% if project_type == "python-cli" %}
# Python CLI specific content
{% endif %}

name: {{ project_name }}
version: {{ version | default("0.1.0") }}
author: {{ author.name | default("Unknown") }}
```

### 2. Utiliser dans un check

```yaml
checks:
  - id: has_my_file
    description: my-file.xyz should exist
    level: recommended
    type: file_exists
    path: my-file.xyz
    template: templates/my-template.xyz.j2
```

### 3. Variables disponibles

| Variable | Description |
|----------|-------------|
| `project_name` | Nom du projet |
| `project_name_snake` | Nom en snake_case |
| `project_type` | Type de projet |
| `project_type_display` | Nom affiche du type |
| `description` | Description du projet |
| `year` | Annee courante |
| `python_version` | Version Python (si applicable) |
| `author` | Objet auteur (name, email) |

---

## Tests

Apres toute extension, verifier:

```bash
# Linting
uvx ruff check src/

# Formating
uvx ruff format src/

# Tests
uv run pytest tests/ -v

# Test manuel
projinit check .
```
