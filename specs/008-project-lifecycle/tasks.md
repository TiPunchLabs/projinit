# Tasks: Project Lifecycle Management

**Input**: Design documents from `/specs/008-project-lifecycle/`
**Prerequisites**: plan.md (required), spec.md (required)
**Target Version**: v2.0.0

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Restructuration du projet et préparation pour v2.0.0

- [ ] T001 Créer la branche `008-project-lifecycle` depuis main
- [ ] T002 Mettre à jour la version dans pyproject.toml vers 2.0.0-dev
- [ ] T003 [P] Créer la structure de répertoires `src/projinit/cli/`
- [ ] T004 [P] Créer la structure de répertoires `src/projinit/core/`
- [ ] T005 [P] Créer la structure de répertoires `src/projinit/standards/`
- [ ] T006 [P] Créer la structure de répertoires `src/projinit/standards/defaults/`
- [ ] T007 [P] Créer la structure de répertoires `tests/fixtures/`
- [ ] T008 Ajouter PyYAML aux dépendances dans pyproject.toml

---

## Phase 2: Foundational (Core Infrastructure)

**Purpose**: Composants de base nécessaires à toutes les commandes

**⚠️ CRITICAL**: Aucune commande ne peut être implémentée avant cette phase

- [ ] T009 [P] Créer `src/projinit/core/__init__.py` avec exports
- [ ] T010 [P] Créer modèles de données dans `src/projinit/core/models.py`:
  - ProjectType (enum: python_cli, python_lib, node_frontend, infrastructure, documentation)
  - CheckResult (dataclass: id, status, message, level, suggestion)
  - UpdateAction (dataclass: action_type, source, target, merge_strategy)
- [ ] T011 Implémenter `src/projinit/core/detector.py`:
  - Fonction `detect_project_type(path: Path) -> ProjectType`
  - Recherche de fichiers marqueurs (pyproject.toml, package.json, main.tf, mkdocs.yml)
  - Score de confiance pour les types ambigus
- [ ] T012 [P] Créer schéma YAML pour standards dans `src/projinit/standards/schema.py`
- [ ] T013 Implémenter `src/projinit/standards/loader.py`:
  - Fonction `load_standards(project_type: ProjectType) -> dict`
  - Support de la hiérarchie: defaults < global < local
  - Validation du schéma YAML
- [ ] T014 [P] Créer `src/projinit/standards/defaults/base.yaml` (standards obligatoires):
  - README.md, LICENSE, .gitignore
  - CLAUDE.md
  - .pre-commit-config.yaml (hooks de base)
- [ ] T015 [P] Créer `src/projinit/standards/defaults/python.yaml`:
  - pyproject.toml avec sections requises
  - Structure src/, tests/
  - Configuration ruff
  - Hooks pre-commit Python (ruff, ruff-format)
- [ ] T016 [P] Créer `src/projinit/standards/defaults/node.yaml`:
  - package.json avec scripts requis
  - Configuration TypeScript/ESLint
  - Hooks pre-commit Node
- [ ] T017 [P] Créer `src/projinit/standards/defaults/infra.yaml`:
  - Structure terraform/, ansible/
  - Hooks terraform_fmt, terraform_validate, ansible-lint
- [ ] T018 [P] Tests unitaires pour detector dans `tests/unit/test_detector.py`
- [ ] T019 [P] Tests unitaires pour loader dans `tests/unit/test_loader.py`

**Checkpoint**: Infrastructure de base prête - implémentation des commandes possible

---

## Phase 3: User Story 1 - Audit de conformité (Priority: P1) 🎯 MVP

**Goal**: Permettre l'audit de conformité d'un projet existant avec rapport clair

**Independent Test**: `projinit check` sur un projet retourne un rapport avec les écarts identifiés

### Tests for User Story 1

- [ ] T020 [P] [US1] Test d'intégration pour check dans `tests/integration/test_check_cmd.py`:
  - Test check sur projet conforme
  - Test check sur projet avec fichiers manquants
  - Test check avec --format json

### Implementation for User Story 1

- [ ] T021 [US1] Implémenter `src/projinit/core/checker.py`:
  - Classe `Checker` avec méthode `run_checks(path: Path) -> list[CheckResult]`
  - Types de vérifications: file_exists, content_contains, content_matches_pattern
  - Support des niveaux: required, recommended, optional
- [ ] T022 [US1] Implémenter `src/projinit/core/reporter.py`:
  - Classe `Reporter` avec méthodes `to_text()`, `to_json()`, `to_markdown()`
  - Affichage coloré avec rich (✓ vert, ✗ rouge, ⚠ jaune)
  - Score de conformité global (pourcentage)
- [ ] T023 [US1] Implémenter `src/projinit/cli/check_cmd.py`:
  - Commande `check` avec options: --format, --verbose, --path
  - Intégration avec detector, checker, reporter
  - Code de sortie: 0 (conforme), 1 (non conforme), 2 (erreur)
- [ ] T024 [US1] Intégrer check dans `src/projinit/main.py`:
  - Ajouter sous-commande `projinit check`
  - Documentation help
- [ ] T025 [P] [US1] Créer fixtures de test dans `tests/fixtures/`:
  - `project_python_complete/` (projet conforme)
  - `project_python_incomplete/` (fichiers manquants)
- [ ] T026 [US1] Tests unitaires checker dans `tests/unit/test_checker.py`
- [ ] T027 [US1] Tests unitaires reporter dans `tests/unit/test_reporter.py`

**Checkpoint**: `projinit check` fonctionnel - MVP audit disponible

---

## Phase 4: User Story 2 - Mise à jour automatique (Priority: P1)

**Goal**: Permettre la mise à jour automatique d'un projet pour le rendre conforme

**Independent Test**: `projinit update` ajoute les fichiers manquants sans casser l'existant

### Tests for User Story 2

- [ ] T028 [P] [US2] Test d'intégration pour update dans `tests/integration/test_update_cmd.py`:
  - Test update crée fichiers manquants
  - Test update avec --dry-run
  - Test update avec --interactive (mock)
  - Test update préserve fichiers existants

### Implementation for User Story 2

- [ ] T029 [US2] Implémenter `src/projinit/core/updater.py`:
  - Classe `Updater` avec méthode `apply_updates(path: Path, actions: list[UpdateAction])`
  - Stratégies de merge: create, merge_yaml, merge_toml, skip_existing
  - Gestion des sauvegardes (.bak)
- [ ] T030 [US2] Implémenter merge intelligent YAML dans `src/projinit/core/merger.py`:
  - Fonction `merge_yaml(existing: dict, template: dict) -> dict`
  - Préserve les valeurs existantes, ajoute les manquantes
  - Cas spécial: pre-commit hooks (additif)
- [ ] T031 [US2] Implémenter `src/projinit/cli/update_cmd.py`:
  - Commande `update` avec options: --dry-run, --interactive, --no-backup, --path
  - Affichage des actions prévues avant exécution
  - Confirmation utilisateur en mode interactif
- [ ] T032 [US2] Intégrer update dans `src/projinit/main.py`:
  - Ajouter sous-commande `projinit update`
  - Documentation help
- [ ] T033 [US2] Tests unitaires updater dans `tests/unit/test_updater.py`
- [ ] T034 [US2] Tests unitaires merger dans `tests/unit/test_merger.py`

**Checkpoint**: `projinit update` fonctionnel - mise à jour automatique disponible

---

## Phase 5: User Story 3 - Initialisation enrichie (Priority: P2)

**Goal**: Enrichir la commande init existante avec les nouveaux standards

**Independent Test**: `projinit init --type python-cli` crée un projet complet avec tous les standards

### Tests for User Story 3

- [ ] T035 [P] [US3] Test d'intégration pour init dans `tests/integration/test_init_cmd.py`:
  - Test init crée structure complète
  - Test init avec --type spécifié
  - Test init dans répertoire non vide (warning)

### Implementation for User Story 3

- [ ] T036 [US3] Refactorer `src/projinit/cli/init_cmd.py`:
  - Réutiliser les standards et templates
  - Ajouter option --type pour forcer le type de projet
  - Intégrer la génération CLAUDE.md
- [ ] T037 [US3] Créer templates enrichis:
  - `templates/CLAUDE.md.j2` (générique + spécifique au type)
  - Vérifier/enrichir templates existants
- [ ] T038 [US3] Mettre à jour assistant interactif:
  - Choix du type de projet avec descriptions
  - Preview des fichiers qui seront créés
- [ ] T039 [US3] Tests unitaires pour init refactoré

**Checkpoint**: `projinit init` utilise les nouveaux standards

---

## Phase 6: User Story 4 - Configuration externalisée (Priority: P2)

**Goal**: Permettre la personnalisation des standards via fichiers de configuration

**Independent Test**: Un fichier `.projinit.yaml` local modifie le comportement de check/update

### Implementation for User Story 4

- [ ] T040 [US4] Implémenter chargement config dans `src/projinit/core/config.py`:
  - Recherche `~/.config/projinit/config.yaml` (global)
  - Recherche `.projinit.yaml` (local)
  - Fusion avec priorité: defaults < global < local
- [ ] T041 [US4] Étendre le schéma standards pour templates personnalisés:
  - Section `custom_templates:` pointant vers répertoire local
  - Section `overrides:` pour modifier les checks par défaut
- [ ] T042 [US4] Mettre à jour loader pour utiliser la config
- [ ] T043 [P] [US4] Tests unitaires config dans `tests/unit/test_config.py`
- [ ] T044 [US4] Test d'intégration avec config personnalisée

**Checkpoint**: Configuration externalisée fonctionnelle

---

## Phase 7: User Story 5 - Rapport détaillé (Priority: P3)

**Goal**: Améliorer l'expérience utilisateur avec des rapports visuels riches

### Implementation for User Story 5

- [ ] T045 [US5] Enrichir Reporter avec tableaux rich:
  - Groupement par catégorie (obligatoire/recommandé/optionnel)
  - Barre de progression pour le score
  - Panel de suggestions avec commandes à copier
- [ ] T046 [US5] Ajouter option --verbose avec détails techniques:
  - Patterns recherchés
  - Fichiers scannés
  - Temps d'exécution
- [ ] T047 [US5] Ajouter export markdown pour documentation/CI:
  - Format compatible GitHub
  - Badges de conformité

**Checkpoint**: Rapports visuellement riches et informatifs

---

## Phase 8: Polish & Documentation

**Purpose**: Finalisation et documentation

- [ ] T048 [P] Mettre à jour README.md avec nouvelles commandes
- [ ] T049 [P] Créer documentation utilisateur dans `docs/`:
  - Guide d'utilisation check/update/init
  - Guide de personnalisation standards
  - Exemples de configuration
- [ ] T050 [P] Mettre à jour CLAUDE.md du projet
- [ ] T051 Validation finale sur les 7 projets analysés
- [ ] T052 Mettre à jour version vers 2.0.0 (release)
- [ ] T053 Tag et release

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──────────────────────────────────────────┐
                                                          │
Phase 2 (Foundational) ◄──────────────────────────────────┘
    │
    ├─► Phase 3 (US1: Check) ──────────────────► MVP!
    │
    ├─► Phase 4 (US2: Update) ─────────────────► v2.0 Core
    │
    ├─► Phase 5 (US3: Init) ───────────────────► v2.0 Complete
    │
    ├─► Phase 6 (US4: Config) ─────────────────► v2.1 (peut être différé)
    │
    └─► Phase 7 (US5: Reports) ────────────────► v2.1 (peut être différé)

Phase 8 (Polish) ◄─────────────────── All phases complete
```

### Parallel Opportunities

**Phase 1**: T003, T004, T005, T006, T007 peuvent être en parallèle
**Phase 2**: T014, T015, T016, T017, T018, T019 peuvent être en parallèle
**Phase 3-7**: Les tests peuvent être écrits en parallèle avec l'implémentation

### Milestones

| Milestone | Phases | Livrable |
|-----------|--------|----------|
| MVP | 1-3 | `projinit check` fonctionnel |
| v2.0-alpha | 1-4 | check + update |
| v2.0-beta | 1-5 | check + update + init enrichi |
| v2.0 | 1-5 + polish | Release complète |
| v2.1 | 6-7 | Configuration externe + rapports riches |

---

## Notes

- Prioriser US1 (check) et US2 (update) car ils forment le coeur de la v2.0
- US3 (init) est une évolution de l'existant, moins critique
- US4 et US5 peuvent être différés à une v2.1 si nécessaire
- Chaque phase a un checkpoint pour valider avant de continuer
- Commits atomiques après chaque tâche (ou groupe logique)
