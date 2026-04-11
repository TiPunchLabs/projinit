# ADR-0006: rich pour l'affichage terminal

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit affiche des resultats de conformite avec des tables, des barres de progression et des couleurs. L'affichage terminal doit etre lisible, esthetique et compatible multi-plateformes.

## Options considerees

1. **ANSI codes manuels** - Codes d'echappement directement dans le code, zero dependance mais fragile et non portable
2. **colorama** - Librairie legere pour les couleurs ANSI, compatible Windows, mais limitee aux couleurs
3. **rich** - Librairie complete pour le terminal (tables, panels, progress bars, markdown, syntax highlighting)

## Decision

Utiliser **rich** pour tous les affichages terminal de projinit.

## Justification

- Tables, panels et progress bars disponibles out-of-the-box
- Gestion automatique des terminaux sans support couleur (fallback gracieux)
- Rendu markdown integre pour les descriptions de checks
- Activement maintenue avec une large communaute
- API intuitive et bien documentee

## Consequences

- Dependance significative en termes de taille (rich + ses dependances)
- API specifique a apprendre pour les contributeurs
- Excellent support Windows via la gestion automatique des codes ANSI
- Permet une evolution rapide de l'interface CLI sans reimplementer les composants
