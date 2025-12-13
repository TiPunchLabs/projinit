# Feature Specification: Génération automatique de pre-commit config

**Feature Branch**: `005-precommit-config`
**Created**: 2025-12-12
**Status**: Draft
**Input**: User description: "Générer automatiquement un fichier .pre-commit-config.yaml basé sur les technologies sélectionnées"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Génération automatique du fichier pre-commit (Priority: P1)

En tant qu'utilisateur de projinit, je veux que le fichier `.pre-commit-config.yaml` soit généré automatiquement lors de la création du projet, en fonction des technologies que j'ai sélectionnées, afin d'avoir des hooks de qualité de code prêts à l'emploi.

**Why this priority**: C'est la fonctionnalité principale demandée. Sans cette génération automatique, la feature n'a pas de valeur.

**Independent Test**: Créer un projet avec différentes technologies et vérifier que le fichier `.pre-commit-config.yaml` contient les hooks appropriés.

**Acceptance Scenarios**:

1. **Given** l'utilisateur crée un projet avec Python sélectionné, **When** le projet est généré, **Then** le fichier `.pre-commit-config.yaml` contient les hooks Python (ruff)
2. **Given** l'utilisateur crée un projet avec Terraform sélectionné, **When** le projet est généré, **Then** le fichier contient les hooks Terraform (fmt, validate, tflint)
3. **Given** l'utilisateur crée un projet sans aucune technologie sélectionnée, **When** le projet est généré, **Then** le fichier contient uniquement les hooks communs

---

### User Story 2 - Ajout d'Ansible aux technologies disponibles (Priority: P2)

En tant qu'utilisateur travaillant avec Ansible, je veux pouvoir sélectionner Ansible comme technologie dans projinit, afin de bénéficier des hooks de linting Ansible et du .gitignore approprié.

**Why this priority**: Étend les capacités du CLI pour supporter un cas d'usage fréquent (Infrastructure as Code avec Ansible).

**Independent Test**: Sélectionner Ansible lors de la création d'un projet et vérifier la présence des hooks ansible-lint et des patterns .gitignore Ansible.

**Acceptance Scenarios**:

1. **Given** l'utilisateur lance projinit, **When** il arrive à la question des technologies, **Then** Ansible apparaît dans la liste des choix
2. **Given** l'utilisateur sélectionne Ansible, **When** le projet est généré, **Then** le fichier `.pre-commit-config.yaml` contient ansible-lint
3. **Given** l'utilisateur sélectionne Ansible, **When** le projet est généré, **Then** le fichier `.gitignore` contient les patterns Ansible

---

### Edge Cases

- Que se passe-t-il si aucune technologie n'est sélectionnée ? Le fichier `.pre-commit-config.yaml` contient uniquement les hooks communs (formatage, sécurité, shell).
- Que se passe-t-il si plusieurs technologies sont sélectionnées ? Toutes les sections de hooks correspondantes sont incluses dans le fichier.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT générer un fichier `.pre-commit-config.yaml` valide à la racine du projet créé
- **FR-002**: Le système DOIT toujours inclure les hooks communs dans le fichier généré:
  - end-of-file-fixer, trailing-whitespace, check-merge-conflict, check-yaml, detect-private-key
  - yamllint
  - shfmt, shellcheck (hooks shell)
- **FR-003**: Le système DOIT inclure les hooks spécifiques pour chaque technologie sélectionnée:
  - Python → ruff
  - Node.js → eslint, prettier
  - Go → gofmt, golangci-lint
  - Terraform → terraform_fmt, terraform_validate, terraform_tflint
  - Docker → hadolint
  - Ansible → ansible-lint
- **FR-004**: Le système DOIT ajouter Ansible à la liste des technologies sélectionnables dans le CLI
- **FR-005**: Le système DOIT générer un fichier `.gitignore` avec les patterns Ansible lorsque cette technologie est sélectionnée
- **FR-006**: Le fichier `.pre-commit-config.yaml` généré DOIT être syntaxiquement valide et prêt à l'usage avec `pre-commit install`

### Key Entities

- **Hook commun**: Vérification de base appliquée à tous les projets (formatage, sécurité)
- **Hook technologique**: Vérification spécifique liée à une technologie (linter, formatter)
- **Technologie**: Option sélectionnable qui déclenche l'ajout de hooks et patterns .gitignore spécifiques

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Le fichier `.pre-commit-config.yaml` est généré pour 100% des projets créés avec projinit
- **SC-002**: Les hooks générés correspondent exactement aux technologies sélectionnées par l'utilisateur
- **SC-003**: Le fichier généré passe la validation `pre-commit validate-config` sans erreur
- **SC-004**: Ansible est visible et sélectionnable dans la liste des technologies du CLI

## Assumptions

- L'utilisateur connaît l'outil pre-commit et l'installera séparément si nécessaire
- Les versions des hooks utilisées sont des versions stables récentes
- Le pattern de génération par fragments (comme pour .gitignore) est applicable
- L'ordre des sections dans le fichier YAML n'impacte pas le fonctionnement
