# Feature Specification: Version Banner Stylisé

**Feature Branch**: `004-version-banner`
**Created**: 2025-12-12
**Status**: Draft
**Input**: User description: "Ajouter un affichage de version stylisé avec ASCII art pour la commande projinit --version"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Affichage de version stylisé (Priority: P1)

En tant qu'utilisateur du CLI projinit, je veux voir un affichage de version complet et stylisé lorsque j'exécute `projinit --version`, afin de connaître rapidement les capacités de l'outil et comment l'utiliser.

**Why this priority**: C'est la fonctionnalité principale demandée. L'affichage de version est souvent le premier point de contact de l'utilisateur avec le CLI.

**Independent Test**: Peut être testé en exécutant `projinit --version` et en vérifiant que l'affichage contient le banner ASCII, la description, les features et l'usage.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a installé projinit, **When** il exécute `projinit --version`, **Then** il voit le banner ASCII art "PROJINIT" en couleur
2. **Given** l'utilisateur exécute `projinit --version`, **When** l'affichage se termine, **Then** il voit la description du projet, la liste des fonctionnalités et les exemples d'usage
3. **Given** l'utilisateur exécute `projinit -v`, **When** l'affichage se termine, **Then** il voit le même affichage complet que `--version`

---

### User Story 2 - Cohérence avec la sous-commande version (Priority: P2)

En tant qu'utilisateur, je veux que `projinit version` et `projinit --version` affichent le même contenu stylisé, pour une expérience utilisateur cohérente.

**Why this priority**: Assure la cohérence de l'interface utilisateur et évite la confusion.

**Independent Test**: Exécuter les deux commandes et comparer visuellement les sorties.

**Acceptance Scenarios**:

1. **Given** l'utilisateur connaît la sous-commande `version`, **When** il exécute `projinit version` ou `projinit --version`, **Then** il obtient le même affichage stylisé

---

### Edge Cases

- Que se passe-t-il si le terminal ne supporte pas les couleurs ? L'affichage reste lisible en mode texte brut grâce à Rich qui détecte automatiquement les capacités du terminal.
- Que se passe-t-il si le terminal est très étroit ? Le banner ASCII déborde mais reste fonctionnel (largeur minimale recommandée: 80 caractères).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher un banner ASCII art "PROJINIT" lorsque l'utilisateur exécute `projinit --version`
- **FR-002**: Le système DOIT afficher une tagline sous le banner: "Project Scaffolding with Terraform + GitHub"
- **FR-003**: Le système DOIT afficher le numéro de version du CLI (format: "CLI vX.Y.Z")
- **FR-004**: Le système DOIT afficher une section "Description" expliquant le but de l'outil
- **FR-005**: Le système DOIT afficher une section "Features" listant les fonctionnalités principales:
  - Génération de structure projet avec Terraform GitHub
  - Configuration automatique du provider GitHub
  - Support direnv + pass pour les secrets
  - Sélection des technologies (.gitignore adapté)
  - Choix du chemin de sortie personnalisé
- **FR-006**: Le système DOIT afficher une section "Usage" avec des exemples de commandes typiques:
  - `projinit` pour le menu interactif
  - `projinit --help` pour l'aide
  - `projinit -p /chemin` pour spécifier le chemin de sortie
- **FR-007**: Le système DOIT utiliser des couleurs pour améliorer la lisibilité (banner en bleu, sections stylisées)
- **FR-008**: L'option `-v` DOIT être un alias de `--version` et produire le même affichage
- **FR-009**: La sous-commande `projinit version` DOIT produire le même affichage que `projinit --version`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'exécution de `projinit --version` affiche le banner complet en moins de 1 seconde
- **SC-002**: Le banner inclut les 5 sections obligatoires: ASCII art, tagline avec version, description, features, usage
- **SC-003**: Les exemples d'usage correspondent aux commandes réellement supportées par le CLI
- **SC-004**: L'affichage est lisible et fonctionnel sur un terminal de 80 caractères de large

## Assumptions

- Le terminal de l'utilisateur supporte l'affichage de caractères Unicode (pour l'ASCII art bloc)
- La bibliothèque Rich est disponible pour le formatage des couleurs (déjà une dépendance du projet)
- Le numéro de version est défini dans `__version__` du module projinit
- L'utilisateur utilise un terminal moderne capable d'afficher les couleurs ANSI
