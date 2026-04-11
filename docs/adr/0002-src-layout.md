# ADR-0002: Organisation src/ layout

**Date**: 2024-12
**Statut**: Accepte

## Contexte

L'organisation du code source Python impacte la facon dont les imports fonctionnent, la separation entre code de production et tests, et la coherence avec les projets generes par projinit.

## Options considerees

1. **Flat layout** - Package directement a la racine (`projinit/`), simple mais peut causer des conflits d'import
2. **src/ layout** - Package dans `src/projinit/`, separation claire entre source et configuration

## Decision

Adopter le **src/ layout** avec le code source dans `src/projinit/`.

## Justification

- Separation claire entre le code source et les fichiers de configuration/tests
- Evite les imports accidentels du package local dans les tests (force l'installation)
- Recommande par les PEP 517/518 et les outils modernes de packaging Python
- Coherent avec la structure que projinit genere pour les nouveaux projets Python

## Consequences

- Necessite la configuration `package-dir` dans `pyproject.toml`
- Les imports locaux passent par `pip install -e .` ou `uv sync` (pas d'import direct)
- Structure plus explicite et moins ambigue pour les contributeurs
