# ADR-0001: argparse vs click pour le framework CLI

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit a besoin d'un framework CLI pour parser les arguments et gerer les sous-commandes (`check`, `update`, `new`, `config`). Le choix du framework impacte l'experience developpeur, les dependances et la maintenabilite.

## Options considerees

1. **click** - Framework CLI declaratif avec decorateurs, tres populaire, completion shell integree
2. **typer** - Surcouche de click basee sur les type hints Python, moderne mais ajoute une dependance supplementaire
3. **argparse** - Module de la stdlib Python, pas de dependance externe, API imperative

## Decision

Utiliser **argparse** (stdlib) pour le parsing CLI, combine avec **questionary** pour les prompts interactifs.

## Justification

- Pas de dependance externe pour le parsing CLI, argparse fait partie de la stdlib
- Suffisant pour le cas d'usage de projinit (sous-commandes, flags, options)
- questionary couvre les besoins d'interactivite (choix, confirmations, prompts)
- Reduit la surface de dependances du projet

## Consequences

- Code plus verbeux que click pour definir les commandes et arguments
- Pas de completion shell automatique (necessiterait un ajout manuel)
- Flexibilite totale sur le parsing et la validation des arguments
