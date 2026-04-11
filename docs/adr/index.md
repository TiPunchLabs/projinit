# Architecture Decision Records (ADR)

Ce dossier contient les decisions architecturales prises pour le projet **projinit**.

## Liste des ADR

| # | Titre | Date | Statut |
|---|-------|------|--------|
| [ADR-0001](0001-argparse-vs-click.md) | argparse vs click pour le framework CLI | 2024-12 | Accepte |
| [ADR-0002](0002-src-layout.md) | Organisation src/ layout | 2024-12 | Accepte |
| [ADR-0003](0003-yaml-standards.md) | YAML pour les standards de conformite | 2024-12 | Accepte |
| [ADR-0004](0004-scoring-detection.md) | Detection par scoring avec poids | 2024-12 | Accepte |
| [ADR-0005](0005-jinja2-templates.md) | Jinja2 pour la generation de templates | 2024-12 | Accepte |
| [ADR-0006](0006-rich-terminal.md) | rich pour l'affichage terminal | 2024-12 | Accepte |
| [ADR-0007](0007-config-hierarchy.md) | Hierarchie de configuration a 3 niveaux | 2024-12 | Accepte |
| [ADR-0008](0008-direnv-pass-secrets.md) | direnv + pass pour la gestion des secrets | 2024-12 | Accepte |
| [ADR-0009](0009-check-levels.md) | 3 niveaux de checks (required, recommended, optional) | 2024-12 | Accepte |
| [ADR-0010](0010-cli-only.md) | CLI uniquement, pas d'API REST | 2024-12 | Accepte |

------

## Template ADR

Pour creer une nouvelle ADR, copier le template ci-dessous dans un nouveau fichier `NNNN-short-title.md` :

```markdown
# ADR-NNNN: Titre

**Date**: YYYY-MM
**Statut**: Propose | Accepte | Deprecie | Remplace par [ADR-XXXX](XXXX-title.md)

## Contexte

Quel est le probleme ou la question a resoudre ?

## Options considerees

1. **Option 1** - Description
2. **Option 2** - Description
3. **Option 3** - Description

## Decision

Quelle option a ete choisie ?

## Justification

- Raison 1
- Raison 2

## Consequences

- Consequence positive ou negative 1
- Consequence positive ou negative 2
```
