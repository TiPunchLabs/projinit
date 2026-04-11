# ADR-0009: 3 niveaux de checks (required, recommended, optional)

**Date**: 2024-12
**Statut**: Accepte

## Contexte

Tous les checks de conformite n'ont pas la meme importance. Un fichier LICENSE manquant est plus critique qu'un fichier CONTRIBUTING.md absent. Il faut un systeme de severite pour refleter cette realite.

## Options considerees

1. **Binaire (pass/fail)** - Tous les checks ont le meme poids, pas de nuance
2. **Poids numerique** - Score de 1 a 10 par check, trop granulaire et difficile a calibrer
3. **Niveaux categoriques** - Categories nommees avec semantique claire

## Decision

3 niveaux de severite :

| Niveau | Signification | Impact |
|--------|---------------|--------|
| required | Doit passer | Bloque la conformite |
| recommended | Devrait passer | Warning, compte dans le score |
| optional | Nice to have | Informatif seulement |

## Justification

- Permet de distinguer les echecs bloquants des ameliorations suggerees
- Le score global reflete la realite du projet (pas juste un pass/fail binaire)
- L'utilisateur peut override les niveaux via la configuration locale
- Trois niveaux suffisent sans complexite excessive

## Consequences

- Logique de scoring plus complexe (ponderation par niveau)
- L'interface utilisateur doit montrer clairement les niveaux (couleurs, icones)
