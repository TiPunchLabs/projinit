# Research: Version Banner Stylisé

**Feature**: 004-version-banner
**Date**: 2025-12-12

## Décision 1: Méthode pour intercepter --version

**Décision**: Créer une action argparse personnalisée (`VersionAction`)

**Rationale**:
- L'action standard `action="version"` d'argparse affiche juste une chaîne et termine
- Une action personnalisée permet d'exécuter du code arbitraire (notre banner Rich)
- Pattern standard et documenté dans la documentation argparse

**Alternatives considérées**:
1. **Parser manuel des arguments avant argparse**: Trop complexe, duplique la logique
2. **Utiliser click au lieu d'argparse**: Changement trop important pour une feature simple
3. **Post-traitement des arguments**: Ne fonctionne pas car `action="version"` termine immédiatement

## Décision 2: Structure du banner

**Décision**: Utiliser Rich Console et Text pour le formatage

**Rationale**:
- Rich est déjà une dépendance du projet
- Rich gère automatiquement la détection des capacités du terminal
- Rich permet un formatage cohérent et élégant

**Alternatives considérées**:
1. **Print simple avec ANSI codes**: Moins portable, plus de code à maintenir
2. **Colorama**: Dépendance supplémentaire non nécessaire

## Décision 3: Contenu des sections

**Décision**: Sections inspirées de ckad-dojo avec adaptation pour projinit

| Section | Contenu |
|---------|---------|
| ASCII Art | Banner "PROJINIT" existant |
| Tagline | "Project Scaffolding with Terraform + GitHub" |
| Version | "CLI vX.Y.Z" centré |
| Description | Explication courte du but de l'outil |
| Features | Liste des 5 fonctionnalités principales |
| Usage | 3 exemples de commandes typiques |

**Rationale**: Format clair et informatif, cohérent avec l'exemple fourni par l'utilisateur
