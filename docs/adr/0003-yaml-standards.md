# ADR-0003: YAML pour les standards de conformite

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit definit des standards de conformite (checks) pour chaque type de projet. Ces standards doivent etre stockes dans un format lisible, modifiable et extensible par les utilisateurs.

## Options considerees

1. **Python** - Definitions directement dans le code, pas de fichier de configuration externe
2. **JSON** - Format structure, largement supporte, mais pas de commentaires
3. **YAML** - Format lisible, supporte les commentaires, structure hierarchique naturelle
4. **TOML** - Format moderne, adopte par Python (pyproject.toml), mais moins flexible pour les structures imbriquees

## Decision

Utiliser **YAML** pour definir les standards de conformite dans `standards/defaults/*.yaml`.

## Justification

- Lisibilite superieure pour des definitions de checks avec descriptions
- Support natif des commentaires pour documenter les standards
- Structure hierarchique naturelle pour les listes de checks et leurs proprietes
- Format familier pour les DevOps et les utilisateurs cibles de projinit
- Plus flexible que TOML pour les structures profondement imbriquees

## Consequences

- Dependance a PyYAML pour le parsing
- Pas de validation de schema native (necessite une validation manuelle ou un outil tiers)
- Les utilisateurs doivent connaitre la syntaxe YAML pour personnaliser les standards
