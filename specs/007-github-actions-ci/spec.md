# Feature Specification: Pipeline CI/CD GitHub Actions

**Feature Branch**: `007-github-actions-ci`
**Created**: 2025-12-18
**Status**: Draft
**Input**: Mettre en place un pipeline GitHub Actions pour effectuer le lint et des tests pour le CLI afin de maintenir la cohérence du projet.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validation automatique du code à chaque push (Priority: P1)

En tant que développeur, je veux que le code soit automatiquement validé (lint) à chaque push sur une branche afin de détecter les erreurs de style et de qualité avant la revue de code.

**Why this priority**: Le linting est la base de la qualité du code et doit être vérifié en premier pour garantir la cohérence du projet.

**Independent Test**: Pousser du code avec des erreurs de linting et vérifier que le pipeline échoue avec un message clair.

**Acceptance Scenarios**:

1. **Given** un développeur pousse du code sur une branche, **When** le pipeline s'exécute, **Then** le linting (ruff check) est exécuté automatiquement
2. **Given** le code contient des erreurs de linting, **When** le pipeline s'exécute, **Then** le workflow échoue avec un message indiquant les erreurs trouvées
3. **Given** le code est conforme aux règles de linting, **When** le pipeline s'exécute, **Then** le workflow réussit

---

### User Story 2 - Vérification du formatage du code (Priority: P2)

En tant que développeur, je veux que le formatage du code soit vérifié automatiquement afin de maintenir une cohérence visuelle dans tout le projet.

**Why this priority**: Le formatage est complémentaire au linting et assure la lisibilité du code.

**Independent Test**: Pousser du code mal formaté et vérifier que le pipeline signale les fichiers à reformater.

**Acceptance Scenarios**:

1. **Given** un développeur pousse du code, **When** le pipeline s'exécute, **Then** la vérification du formatage (ruff format --check) est exécutée
2. **Given** le code n'est pas correctement formaté, **When** le pipeline s'exécute, **Then** le workflow échoue en listant les fichiers mal formatés

---

### User Story 3 - Exécution des tests unitaires (Priority: P3)

En tant que développeur, je veux que les tests unitaires soient exécutés automatiquement à chaque push afin de détecter les régressions le plus tôt possible.

**Why this priority**: Les tests garantissent que les fonctionnalités existantes ne sont pas cassées par les nouvelles modifications.

**Independent Test**: Pousser du code qui casse un test existant et vérifier que le pipeline échoue.

**Acceptance Scenarios**:

1. **Given** un développeur pousse du code, **When** le pipeline s'exécute, **Then** les tests sont exécutés avec pytest
2. **Given** un test échoue, **When** le pipeline s'exécute, **Then** le workflow échoue avec le rapport des tests en erreur
3. **Given** tous les tests passent, **When** le pipeline s'exécute, **Then** le workflow réussit

---

### User Story 4 - Validation sur les Pull Requests (Priority: P4)

En tant que mainteneur, je veux que toutes les validations soient exécutées sur les Pull Requests vers la branche principale afin de garantir que seul du code de qualité est fusionné.

**Why this priority**: Les PR sont le point d'entrée pour le code en production, elles doivent être particulièrement surveillées.

**Independent Test**: Créer une PR avec du code non conforme et vérifier que le merge est bloqué.

**Acceptance Scenarios**:

1. **Given** une PR est ouverte vers main, **When** le pipeline s'exécute, **Then** lint, format et tests sont tous exécutés
2. **Given** une validation échoue sur une PR, **When** le développeur consulte la PR, **Then** il voit clairement quelle étape a échoué

---

### Edge Cases

- Que se passe-t-il si aucun fichier Python n'est modifié ? Le pipeline s'exécute quand même pour garantir la cohérence
- Que se passe-t-il si pytest n'est pas installé ou aucun test n'existe ? Le pipeline doit gérer gracieusement l'absence de tests
- Que se passe-t-il si le workflow échoue pour une raison externe (timeout, erreur GitHub) ? Les erreurs doivent être distinguables des erreurs de qualité du code

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT exécuter le linting (ruff check) sur tous les fichiers Python du dossier src/
- **FR-002**: Le système DOIT vérifier le formatage (ruff format --check) sur tous les fichiers Python du dossier src/
- **FR-003**: Le système DOIT exécuter les tests avec pytest si des tests existent
- **FR-004**: Le workflow DOIT s'exécuter automatiquement sur chaque push
- **FR-005**: Le workflow DOIT s'exécuter automatiquement sur chaque Pull Request vers main
- **FR-006**: Le workflow DOIT afficher clairement les erreurs rencontrées pour faciliter le débogage
- **FR-007**: Le workflow DOIT utiliser la même version de Python que celle spécifiée dans le projet (>= 3.10)
- **FR-008**: Le workflow DOIT installer les dépendances du projet avant d'exécuter les validations

### Key Entities

- **Workflow CI**: Configuration YAML définissant les étapes de validation (lint, format, test)
- **Job**: Unité d'exécution dans le workflow (peut être parallélisé)
- **Step**: Action individuelle dans un job (checkout, setup, lint, test)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chaque push déclenche une exécution du pipeline en moins de 30 secondes après le push
- **SC-002**: Le pipeline complet (lint + format + tests) s'exécute en moins de 5 minutes
- **SC-003**: 100% des erreurs de linting sont détectées et reportées avant le merge
- **SC-004**: Les développeurs peuvent identifier la cause d'un échec en moins de 1 minute grâce aux logs clairs
- **SC-005**: Le pipeline fonctionne sur toutes les branches du repository

## Assumptions

- Le projet utilise uv comme gestionnaire de packages Python
- ruff est utilisé comme linter et formateur (via uvx)
- pytest est le framework de test (à installer si non présent)
- Le repository est hébergé sur GitHub
- Les développeurs ont les droits de pusher sur leurs branches
