# ADR-0007: Hierarchie de configuration a 3 niveaux

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit doit permettre la personnalisation des standards et du comportement a differents niveaux : valeurs par defaut raisonnables, preferences globales de l'utilisateur, et overrides specifiques par projet.

## Options considerees

1. **Fichier unique** - Un seul fichier de configuration global
2. **Hierarchie a 2 niveaux** - Global + local
3. **Hierarchie a 3 niveaux** - Defaults + global + local

## Decision

Hierarchie a 3 niveaux :

```text
1. Defaults (built-in)           <- Toujours present
      |
2. Global (~/.config/projinit/)  <- Preferences utilisateur
      |
3. Local (.projinit.yaml)        <- Override par projet
```

## Justification

- Pattern standard utilise par git, npm, eslint et d'autres outils familiers
- Permet des defaults raisonnables sans configuration initiale
- Override granulaire par projet sans modifier la config globale
- Familier pour les developpeurs

## Consequences

- Complexite de merge entre les niveaux de configuration
- Debugging plus difficile pour determiner quel niveau s'applique
- Ajout de la commande `projinit config paths` pour clarifier la resolution
