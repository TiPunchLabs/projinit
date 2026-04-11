# ADR-0010: CLI uniquement, pas d'API REST

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit pourrait exposer ses fonctionnalites via une API REST, un mode daemon ou un dashboard web en plus de la CLI. Il faut decider du perimetre d'interface.

## Options considerees

1. **CLI uniquement** - Outil en ligne de commande, execution ponctuelle, pas de serveur
2. **CLI + API REST** - Serveur HTTP avec endpoints pour les checks et la generation
3. **CLI + mode daemon** - Processus en arriere-plan avec surveillance continue des projets

## Decision

projinit reste un outil **CLI uniquement**, sans API REST ni mode daemon.

## Justification

- Le cas d'usage est ponctuel (audit, generation) et ne necessite pas un serveur permanent
- Simplicite de deploiement : un `pip install` ou `uv tool install` suffit
- Pas de state a gerer entre les executions
- Integration CI/CD naturelle via la CLI (exit codes, output JSON)

## Consequences

- Pas de dashboard web pour visualiser les resultats de conformite
- Pas de persistence des resultats (sauf export JSON manuel)
- Integration CI/CD via exit codes et parsing de la sortie JSON
- Si un besoin de dashboard emerge, il pourra consommer les exports JSON
