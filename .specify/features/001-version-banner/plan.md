# Implementation Plan: Version Banner

**Branch**: `001-version-banner` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `.specify/features/001-version-banner/spec.md`

## Summary

Ajout d'une sous-commande `projinit version` qui affiche un banner ASCII art élégant avec les informations système, similaire à `specify version`. L'option `--version` existante reste inchangée pour la rétrocompatibilité.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: rich (déjà installé), platform (stdlib), sys (stdlib)
**Storage**: N/A
**Testing**: Manuel (affichage visuel)
**Target Platform**: Linux (principal), macOS (secondaire)
**Project Type**: single - CLI Python
**Performance Goals**: Affichage < 100ms
**Constraints**: Pas de nouvelles dépendances

## Constitution Check

| Principe | Conformité | Notes |
|----------|------------|-------|
| I. Simplicité | ✅ | Un seul module ajouté (version.py) |
| II. Configuration-Driven | N/A | Pas de configuration nécessaire |
| III. Template-Based | N/A | Pas de template |
| IV. UX Interactive | ✅ | Affichage Rich élégant |
| V. Sécurité First | ✅ | Pas de données sensibles |

## Project Structure

### Fichiers Modifiés/Créés

```text
src/projinit/
├── __init__.py          # Existant (contient __version__)
├── cli.py               # Modifié: ajout sous-commande version
└── version.py           # Nouveau: logique d'affichage du banner
```

**Structure Decision**: Créer un module `version.py` séparé pour isoler la logique d'affichage du banner, conformément au principe de responsabilité unique.

## Design

### ASCII Art

```
██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
```

### Panel Informations

```
╭─────────────────── projinit CLI Information ───────────────────╮
│                                                                 │
│     CLI Version    0.1.0                                        │
│          Python    3.12.3                                       │
│        Platform    Linux                                        │
│    Architecture    x86_64                                       │
│      OS Version    6.14.0-36-generic                            │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯
```

### Modification CLI

Utiliser argparse avec sous-parsers pour ajouter la commande `version` tout en gardant `--version` fonctionnel.

```python
# Nouvelle structure
parser = argparse.ArgumentParser(...)
parser.add_argument("-v", "--version", ...)  # Garde le comportement actuel

subparsers = parser.add_subparsers(dest="command")
subparsers.add_parser("version", help="Affiche les informations de version détaillées")
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Aucune | N/A | N/A |
