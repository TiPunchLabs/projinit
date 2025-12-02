# Tasks: Version Banner

**Input**: Design documents from `.specify/features/001-version-banner/`
**Prerequisites**: plan.md (required), spec.md (required)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Setup

**Purpose**: Préparation des fichiers

- [ ] T001 [P] Créer src/projinit/version.py avec la constante ASCII_ART
- [ ] T002 [P] Vérifier que __version__ est bien exporté dans src/projinit/__init__.py

---

## Phase 2: User Story 1 - Affichage Version Élégant (Priority: P1)

**Goal**: Implémenter la fonction d'affichage du banner

**Independent Test**: `uv run projinit version`

### Implementation for User Story 1

- [ ] T003 [US1] Implémenter get_system_info() dans version.py (Python, Platform, Architecture, OS)
- [ ] T004 [US1] Implémenter display_version_banner() dans version.py avec Rich Panel
- [ ] T005 [US1] Ajouter le tagline "Project Scaffolding with Terraform + GitHub" sous l'ASCII art

**Checkpoint**: Le module version.py est complet et testable isolément

---

## Phase 3: User Story 2 - Intégration CLI (Priority: P1)

**Goal**: Intégrer la sous-commande dans le CLI existant

**Independent Test**: `uv run projinit version` et `uv run projinit --version`

### Implementation for User Story 2

- [ ] T006 [US2] Modifier parse_args() dans cli.py pour ajouter subparsers
- [ ] T007 [US2] Ajouter la sous-commande "version" au subparser
- [ ] T008 [US2] Modifier main() pour gérer la commande "version"
- [ ] T009 [US2] Vérifier que --version continue de fonctionner (rétrocompatibilité)

**Checkpoint**: Les deux commandes fonctionnent correctement

---

## Phase 4: Polish

**Purpose**: Finalisation

- [ ] T010 [P] Tester l'affichage sur terminal étroit
- [ ] T011 [P] Vérifier les couleurs Rich
- [ ] T012 Mettre à jour le README.md avec la nouvelle commande

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (US1)**: Depends on T001, T002
- **Phase 3 (US2)**: Depends on Phase 2 (T004 must exist)
- **Phase 4 (Polish)**: Depends on Phase 3

### Execution Flow

```
T001, T002 (parallel)
    ↓
T003 → T004 → T005 (sequential)
    ↓
T006 → T007 → T008 → T009 (sequential)
    ↓
T010, T011, T012 (parallel)
```

---

## Notes

- Utiliser `platform` (stdlib) pour les infos système
- Utiliser `rich.panel.Panel` et `rich.table.Table` pour l'affichage
- L'ASCII art doit être centré dans le terminal
- Couleur suggérée: blue pour le style (cohérent avec display_header existant)
