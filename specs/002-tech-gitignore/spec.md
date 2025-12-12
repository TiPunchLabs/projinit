# Feature Specification: Sélection de Technologies pour .gitignore Adapté

**Feature Branch**: `002-tech-gitignore`
**Created**: 2025-12-09
**Status**: Draft
**Input**: Ajouter la sélection de technologies au questionnaire projinit pour générer un .gitignore adapté via des fragments Jinja2 modulaires.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sélection des technologies du projet (Priority: P1)

En tant que développeur, je veux sélectionner les technologies que mon projet utilise lors de l'initialisation, afin que le fichier .gitignore généré contienne les patterns d'exclusion appropriés pour chaque technologie.

**Why this priority**: C'est la fonctionnalité core de cette feature. Sans la sélection des technologies, aucun .gitignore adapté ne peut être généré. Cette story délivre la valeur principale demandée.

**Independent Test**: Peut être testé en exécutant `projinit`, en sélectionnant différentes combinaisons de technologies, et en vérifiant que le questionnaire enregistre correctement les choix.

**Acceptance Scenarios**:

1. **Given** l'utilisateur lance projinit, **When** il atteint l'étape de sélection des technologies, **Then** il voit une liste à choix multiples avec les options : Python, Node.js, Go, Terraform, Docker, IDE
2. **Given** la liste des technologies est affichée, **When** l'utilisateur utilise la barre espace pour sélectionner plusieurs options, **Then** chaque option sélectionnée est marquée visuellement
3. **Given** Terraform est une technologie core du projet, **When** la liste s'affiche, **Then** Terraform est présélectionné par défaut
4. **Given** l'utilisateur a fait ses sélections, **When** il valide avec Entrée, **Then** les choix sont enregistrés pour la génération

---

### User Story 2 - Génération du .gitignore adapté (Priority: P1)

En tant que développeur, je veux que le .gitignore généré contienne les patterns d'exclusion correspondant aux technologies sélectionnées, afin de ne pas avoir à configurer manuellement ces exclusions.

**Why this priority**: Cette story est indissociable de la première - elle représente le résultat tangible de la sélection. Sans génération adaptée, la sélection n'a pas de valeur.

**Independent Test**: Peut être testé en générant un projet avec différentes combinaisons de technologies et en vérifiant le contenu du .gitignore résultant.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a sélectionné Python et Terraform, **When** le projet est généré, **Then** le .gitignore contient les patterns Python (__pycache__, *.pyc, .venv/) ET les patterns Terraform (.terraform/, *.tfstate)
2. **Given** l'utilisateur a sélectionné uniquement Terraform, **When** le projet est généré, **Then** le .gitignore contient les patterns Terraform et les patterns communs (.DS_Store, *.log)
3. **Given** l'utilisateur a sélectionné toutes les technologies disponibles, **When** le projet est généré, **Then** le .gitignore contient tous les patterns sans doublons
4. **Given** le projet est généré, **When** l'utilisateur ouvre le .gitignore, **Then** chaque section de patterns est identifiée par un commentaire indiquant la technologie

---

### User Story 3 - Patterns communs automatiques (Priority: P2)

En tant que développeur, je veux que les patterns d'exclusion universels (fichiers système, logs, etc.) soient toujours inclus dans le .gitignore, indépendamment des technologies sélectionnées.

**Why this priority**: Améliore l'expérience utilisateur en évitant les oublis courants, mais n'est pas bloquant pour la fonctionnalité principale.

**Independent Test**: Peut être testé en générant un projet avec n'importe quelle combinaison de technologies et en vérifiant la présence des patterns communs.

**Acceptance Scenarios**:

1. **Given** l'utilisateur génère un projet avec n'importe quelle sélection, **When** le .gitignore est créé, **Then** il contient les patterns pour .DS_Store, Thumbs.db, *.log, et .direnv/
2. **Given** l'utilisateur n'a sélectionné aucune technologie additionnelle, **When** le projet est généré, **Then** le .gitignore contient au minimum les patterns communs et Terraform

---

### Edge Cases

- Que se passe-t-il si l'utilisateur désélectionne Terraform ? Le système doit permettre cette action car l'utilisateur peut vouloir un projet sans infrastructure Terraform.
- Que se passe-t-il si l'utilisateur ne sélectionne aucune technologie ? Le .gitignore contient uniquement les patterns communs.
- Comment gérer les patterns en doublon entre technologies ? Les patterns sont dédupliqués lors de la concaténation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher une question à choix multiples pour la sélection des technologies après la question sur direnv
- **FR-002**: Le système DOIT proposer les technologies suivantes : Python, Node.js, Go, Terraform, Docker, IDE (VSCode/JetBrains)
- **FR-003**: Le système DOIT présélectionner Terraform par défaut dans la liste des technologies
- **FR-004**: Le système DOIT permettre à l'utilisateur de désélectionner n'importe quelle technologie, y compris Terraform
- **FR-005**: Le système DOIT générer le .gitignore en concaténant les fragments correspondant aux technologies sélectionnées
- **FR-006**: Le système DOIT toujours inclure les patterns communs (fichiers système, logs) dans le .gitignore généré
- **FR-007**: Le système DOIT identifier chaque section du .gitignore avec un commentaire indiquant la technologie source
- **FR-008**: Le système DOIT afficher les technologies sélectionnées dans le résumé avant confirmation
- **FR-009**: Le système DOIT stocker les fragments de .gitignore dans un répertoire dédié aux templates

### Key Entities

- **Technology**: Représente une technologie sélectionnable (nom, label affiché, fichier fragment associé)
- **GitignoreFragment**: Contenu des patterns d'exclusion pour une technologie spécifique
- **ProjectConfig**: Configuration du projet étendue pour inclure la liste des technologies sélectionnées

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'utilisateur peut sélectionner ses technologies en moins de 10 secondes (interaction simple et intuitive)
- **SC-002**: Le .gitignore généré contient 100% des patterns pertinents pour les technologies sélectionnées
- **SC-003**: Aucun pattern en doublon n'apparaît dans le .gitignore final
- **SC-004**: Le temps de génération du projet reste sous 2 secondes malgré l'ajout de cette fonctionnalité
- **SC-005**: 100% des utilisateurs comprennent la question de sélection sans documentation additionnelle

## Assumptions

- Les patterns de chaque technologie sont stables et maintenus manuellement dans les fragments
- La liste des technologies proposées (6 options) couvre les cas d'usage majoritaires des utilisateurs de projinit
- L'ordre d'insertion des fragments dans le .gitignore n'a pas d'importance fonctionnelle
- Les utilisateurs de projinit ont une connaissance de base des technologies qu'ils utilisent
