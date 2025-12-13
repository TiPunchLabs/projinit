# Implementation Plan: Version Banner Stylisé

**Branch**: `004-version-banner` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-version-banner/spec.md`

## Summary

Améliorer l'affichage de la commande `projinit --version` pour afficher un banner stylisé complet incluant l'ASCII art, une description, la liste des fonctionnalités et des exemples d'usage, similaire à l'interface de ckad-dojo. L'implémentation modifiera le comportement de l'option `--version` d'argparse pour utiliser une action personnalisée.

## Technical Context

**Language/Version**: Python >= 3.10 (conforme à la constitution)
**Primary Dependencies**: rich >= 13.0.0 (déjà présent dans le projet)
**Storage**: N/A
**Testing**: pytest (à définir si nécessaire)
**Target Platform**: Linux/macOS/Windows (CLI cross-platform)
**Project Type**: single
**Performance Goals**: Affichage instantané < 1 seconde
**Constraints**: Terminal 80 caractères minimum, support Unicode pour ASCII art
**Scale/Scope**: Modification de 2 fichiers existants (cli.py, version.py)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe | Statut | Notes |
|----------|--------|-------|
| I. Simplicité et Minimalisme | ✅ PASS | Modification minimale de code existant |
| II. Configuration-Driven | ✅ PASS | Pas de configuration nécessaire |
| III. Template-Based Generation | ✅ N/A | Pas de génération de fichiers |
| IV. Expérience Utilisateur Interactive | ✅ PASS | Améliore l'UX avec un affichage riche |
| V. Sécurité First | ✅ N/A | Pas d'impact sécurité |

**Stack Technique**:
- ✅ Python >= 3.10: Conforme
- ✅ rich >= 13.0.0: Déjà utilisé dans version.py
- ✅ argparse (stdlib): Utilisé dans cli.py

## Project Structure

### Documentation (this feature)

```text
specs/004-version-banner/
├── plan.md              # This file
├── spec.md              # Feature specification
└── checklists/
    └── requirements.md  # Validation checklist
```

### Source Code (repository root)

```text
src/projinit/
├── __init__.py          # Version string (__version__)
├── cli.py               # À MODIFIER: Custom action pour --version
├── version.py           # À MODIFIER: Banner complet avec Description/Features/Usage
├── config.py
├── validators.py
├── checks.py
├── generator.py
└── templates/
```

**Structure Decision**: Projet existant de type "single". Modification de 2 fichiers dans `src/projinit/`:
- `cli.py`: Remplacer l'action "version" d'argparse par une action personnalisée
- `version.py`: Enrichir `display_version_banner()` avec les nouvelles sections

## Implementation Strategy

### Approche Technique

1. **Créer une action argparse personnalisée** dans `cli.py`:
   - Classe `VersionAction(argparse.Action)` qui appelle `display_version_banner()`
   - Remplace `action="version"` par `action=VersionAction`

2. **Enrichir `display_version_banner()`** dans `version.py`:
   - Conserver l'ASCII art existant
   - Ajouter la version centrée sous le banner
   - Ajouter section "Description"
   - Ajouter section "Features" avec liste à puces
   - Ajouter section "Usage" avec exemples de commandes

3. **Supprimer la redondance**:
   - La sous-commande `version` appelle déjà `display_version_banner()`
   - Après modification, `--version` et `version` seront cohérents

### Format de Sortie Cible

```
██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
            Project Scaffolding with Terraform + GitHub

                        CLI v0.2.1

Description:
  Générateur de structure projet avec configuration Terraform
  GitHub intégrée. Créez des projets prêts à déployer avec
  infrastructure as code en quelques secondes.

Features:
  - Génération de structure projet avec Terraform GitHub
  - Configuration automatique du provider GitHub
  - Support direnv + pass pour les secrets
  - Sélection des technologies (.gitignore adapté)
  - Chemin de sortie personnalisable

Usage:
  projinit                 # Menu interactif
  projinit -p ~/projets    # Spécifier le chemin de sortie
  projinit --help          # Afficher l'aide
```

## Complexity Tracking

> Aucune violation de la constitution - pas de justification nécessaire.
