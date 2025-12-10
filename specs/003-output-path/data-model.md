# Data Model: Chemin de Destination Personnalisé

**Feature**: 003-output-path
**Date**: 2025-12-09

## Overview

Cette feature n'ajoute pas de nouveau modèle de données persistant. Elle étend uniquement le parsing des arguments CLI et la logique de résolution du chemin.

## Current State

### cli.py - parse_args()

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="projinit",
        description="CLI pour générer la structure d'un projet avec configuration Terraform GitHub",
    )
    parser.add_argument("-v", "--version", ...)
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("version", ...)
    return parser.parse_args()
```

**Retourne**: `Namespace(command=None)` ou `Namespace(command='version')`

### cli.py - main()

```python
def main() -> None:
    # ...
    target_dir = Path.cwd() / project_name  # Hardcoded to cwd
    # ...
```

## Target State

### cli.py - parse_args() (modifié)

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="projinit",
        description="CLI pour générer la structure d'un projet avec configuration Terraform GitHub",
    )
    parser.add_argument("-v", "--version", ...)
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=None,
        metavar="PATH",
        help="Chemin de destination pour le projet (défaut: dossier courant)",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("version", ...)
    return parser.parse_args()
```

**Retourne**: `Namespace(command=None, path=None)` ou `Namespace(command=None, path='/custom/path')`

### cli.py - resolve_output_path() (nouvelle fonction)

```python
def resolve_output_path(path_arg: str | None) -> Path:
    """Résout et valide le chemin de destination.

    Args:
        path_arg: Le chemin fourni via --path, ou None pour le dossier courant.

    Returns:
        Le chemin résolu et validé.

    Raises:
        ValueError: Si le chemin pointe vers un fichier existant.
        PermissionError: Si pas de permission d'écriture.
    """
    if not path_arg or path_arg.strip() == "":
        return Path.cwd()

    resolved = Path(path_arg).expanduser().resolve()

    if resolved.is_file():
        raise ValueError(f"Le chemin '{resolved}' est un fichier, pas un dossier")

    first_existing = _get_first_existing_parent(resolved)
    if not os.access(first_existing, os.W_OK):
        raise PermissionError(f"Pas de permission d'écriture sur '{first_existing}'")

    return resolved
```

### cli.py - _get_first_existing_parent() (nouvelle fonction helper)

```python
def _get_first_existing_parent(path: Path) -> Path:
    """Trouve le premier parent existant pour vérifier les permissions."""
    current = path.resolve()
    while not current.exists():
        current = current.parent
    return current
```

### cli.py - main() (modifié)

```python
def main() -> None:
    args = parse_args()

    if args.command == "version":
        display_version_banner()
        return

    # Résoudre le chemin de destination
    try:
        base_path = resolve_output_path(args.path)
    except ValueError as e:
        console.print(f"[red]Erreur: {e}[/red]")
        sys.exit(1)
    except PermissionError as e:
        console.print(f"[red]Erreur: {e}[/red]")
        sys.exit(1)

    # ... questionnaire ...

    # target_dir utilise maintenant base_path
    target_dir = base_path / project_name

    # ...
```

### cli.py - display_summary() (modifié)

```python
def display_summary(project_config: ProjectConfig, target_dir: Path) -> None:
    """Affiche le récapitulatif de la configuration."""
    console.print()
    console.print("[bold]Récapitulatif :[/bold]")
    console.print(f"  Nom        : [cyan]{project_config.name}[/cyan]")
    console.print(f"  Chemin     : [cyan]{target_dir}[/cyan]")  # NEW
    console.print(f"  Description: [cyan]{project_config.description}[/cyan]")
    # ... rest unchanged ...
```

## No Changes Required

### generator.py

La fonction `generate_project(config, target_dir)` accepte déjà un `target_dir` en paramètre. Aucune modification requise.

### ProjectConfig dataclass

La dataclass `ProjectConfig` n'a pas besoin de stocker le chemin de destination car:
1. Le chemin est utilisé uniquement pour la génération
2. Il n'est pas persisté dans les fichiers générés
3. Il est passé directement à `generate_project()`

## Import Changes

### cli.py - imports (modifié)

```python
import os  # NEW - for os.access()
```

## Validation Flow

```
User Input (--path)
       │
       ▼
┌──────────────────┐
│ resolve_output_  │
│     path()       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │ Empty?  │──Yes──▶ Path.cwd()
    └────┬────┘
         │ No
         ▼
┌──────────────────┐
│ expanduser() +   │
│   resolve()      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   is_file()?     │──Yes──▶ ValueError
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Check W_OK on    │
│ first existing   │──No───▶ PermissionError
│ parent           │
└────────┬─────────┘
         │ Yes
         ▼
    Resolved Path
```

## Summary

| Fichier | Changements |
|---------|-------------|
| `cli.py` | Ajouter argument `--path`, fonctions `resolve_output_path()` et `_get_first_existing_parent()`, modifier `main()` et `display_summary()`, import `os` |
| `generator.py` | Aucun changement |
| `validators.py` | Aucun changement (logique inline dans cli.py pour simplicité) |
