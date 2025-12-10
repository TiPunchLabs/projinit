# Technical Research: Chemin de Destination Personnalisé

**Feature**: 003-output-path
**Date**: 2025-12-09

## Overview

Recherche technique sur la gestion des chemins de fichiers en Python pour implémenter l'argument `--path` / `-p` dans projinit.

## Path Handling in Python

### pathlib vs os.path

Python offre deux approches pour la gestion des chemins :

| Aspect | `pathlib` | `os.path` |
|--------|-----------|-----------|
| Style | Orienté objet | Fonctionnel |
| Modernité | Python 3.4+ | Legacy |
| Lisibilité | Excellente | Bonne |
| Concaténation | `/` operator | `os.path.join()` |

**Choix**: `pathlib.Path` - déjà utilisé dans le projet, moderne et expressif.

### Key Operations

```python
from pathlib import Path

# Résolution du tilde (~)
path = Path("~/projects").expanduser()
# Result: /home/user/projects

# Résolution des chemins relatifs
path = Path("../other").resolve()
# Result: /absolute/path/to/other

# Combinaison des deux
path = Path("~/dev/../projects").expanduser().resolve()
# Result: /home/user/projects
```

### Edge Cases

| Cas | Input | Comportement |
|-----|-------|--------------|
| Tilde seul | `~` | Résolu vers home directory |
| Tilde avec user | `~user` | Résolu vers home de l'utilisateur spécifié |
| Chemin vide | `""` | Doit fallback vers `Path.cwd()` |
| Chemin absolu | `/tmp/proj` | Utilisé tel quel |
| Chemin relatif | `./subdir` | Résolu par rapport à cwd |
| Double dot | `../parent` | Résolu correctement |

## Permission Checking

### os.access() vs try/except

```python
import os
from pathlib import Path

# Méthode 1: os.access (vérification préalable)
def check_write_permission(path: Path) -> bool:
    parent = path.parent
    while not parent.exists():
        parent = parent.parent
    return os.access(parent, os.W_OK)

# Méthode 2: try/except (EAFP)
def try_create(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        return False
```

**Choix**: `os.access()` pour vérifier AVANT la génération, conformément à FR-007 et SC-004.

### Finding the First Existing Parent

```python
def get_first_existing_parent(path: Path) -> Path:
    """Trouve le premier parent existant pour vérifier les permissions."""
    current = path.resolve()
    while not current.exists():
        current = current.parent
    return current
```

## Argparse Integration

### Current State

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(...)
    parser.add_argument("-v", "--version", ...)
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("version", ...)
    return parser.parse_args()
```

### Adding --path Argument

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(...)
    parser.add_argument("-v", "--version", ...)
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=None,
        help="Chemin de destination pour le projet (défaut: dossier courant)",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("version", ...)
    return parser.parse_args()
```

## Path Validation Strategy

### Validation Order

1. **Résolution**: `expanduser()` + `resolve()` pour obtenir le chemin absolu
2. **Type check**: Vérifier que ce n'est pas un fichier existant
3. **Permission check**: Vérifier les droits d'écriture sur le parent existant
4. **Display**: Afficher le chemin résolu dans le récapitulatif

### Implementation Pattern

```python
def resolve_output_path(path_arg: str | None) -> Path:
    """Résout et valide le chemin de destination."""
    if not path_arg:
        return Path.cwd()

    # Résolution
    resolved = Path(path_arg).expanduser().resolve()

    # Validation: pas un fichier
    if resolved.is_file():
        raise ValueError(f"Le chemin '{resolved}' est un fichier, pas un dossier")

    # Validation: permissions d'écriture
    first_existing = get_first_existing_parent(resolved)
    if not os.access(first_existing, os.W_OK):
        raise PermissionError(f"Pas de permission d'écriture sur '{first_existing}'")

    return resolved
```

## Error Messages (French)

| Erreur | Message |
|--------|---------|
| Fichier existant | `Le chemin '{path}' est un fichier, pas un dossier` |
| Permission denied | `Pas de permission d'écriture sur '{parent}'` |
| Invalid path | `Chemin invalide: '{path}'` |

## Compatibility Notes

- `Path.expanduser()` fonctionne sur Linux, macOS, Windows
- `os.access()` avec `os.W_OK` est portable
- Les chemins avec espaces sont gérés nativement par `pathlib`
- Les caractères spéciaux (unicode) sont supportés si le filesystem le permet

## Conclusion

L'implémentation utilise:
- `pathlib.Path` pour toutes les opérations sur les chemins
- `expanduser()` + `resolve()` pour la résolution complète
- `os.access()` pour la vérification préalable des permissions
- Messages d'erreur en français pour la cohérence avec l'UX existante
