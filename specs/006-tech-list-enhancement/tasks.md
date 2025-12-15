# Tasks: Amélioration de la Liste des Technologies

**Input**: Design documents from `/specs/006-tech-list-enhancement/`
**Prerequisites**: spec.md (user stories P1-P5)

**Tests**: Tests NOT explicitly requested - implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/projinit/` at repository root
- Templates: `src/projinit/templates/gitignore/`, `src/projinit/templates/precommit/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No setup required - existing project structure is already in place

- [x] T001 Verify existing project structure and templates directory layout

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update core CLI structure to support categorized technology list

**Note**: This phase modifies the ask_technologies() function which is required by ALL user stories

- [x] T002 Update ask_technologies() with questionary.Separator for categories in src/projinit/cli.py
- [x] T003 Reorganize existing technologies under appropriate category separators in src/projinit/cli.py

**Checkpoint**: Foundation ready - category separators in place, user stories can add new technologies

---

## Phase 3: User Story 1 - Navigation facilitée par catégories (Priority: P1)

**Goal**: Technologies organisées en catégories avec séparateurs visuels questionary

**Independent Test**: Exécuter `uv run projinit` et vérifier que les catégories (Langages, Front-end, Infrastructure, etc.) sont affichées avec des séparateurs

### Implementation for User Story 1

- [x] T004 [US1] Add category separator "Langages" before Python in src/projinit/cli.py
- [x] T005 [US1] Add category separator "Front-end" after Go (empty for now) in src/projinit/cli.py
- [x] T006 [US1] Add category separator "Infrastructure" before Terraform in src/projinit/cli.py
- [x] T007 [US1] Add category separator "Conteneurs" before Docker in src/projinit/cli.py
- [x] T008 [US1] Add category separator "Automation" before Ansible in src/projinit/cli.py
- [x] T009 [US1] Add category separator "Outils" before IDE in src/projinit/cli.py
- [x] T010 [US1] Test category display by running projinit interactively

**Checkpoint**: User Story 1 complete - categories visually separated, existing technologies organized

---

## Phase 4: User Story 2 - Support Rust et Shell/Bash (Priority: P2)

**Goal**: Ajouter Rust et Shell/Bash comme technologies sélectionnables avec templates gitignore et precommit

**Independent Test**: Sélectionner Rust ou Shell/Bash et vérifier les fichiers .gitignore et .pre-commit-config.yaml générés

### Implementation for User Story 2

- [x] T011 [P] [US2] Create gitignore template for Rust in src/projinit/templates/gitignore/rust.j2
- [x] T012 [P] [US2] Create gitignore template for Shell/Bash in src/projinit/templates/gitignore/shell.j2
- [x] T013 [P] [US2] Create precommit template for Rust (clippy, rustfmt) in src/projinit/templates/precommit/rust.j2
- [x] T014 [P] [US2] Create precommit template for Shell (shellcheck, shfmt) in src/projinit/templates/precommit/shell.j2
- [x] T015 [US2] Add Rust choice to ask_technologies() under Langages category in src/projinit/cli.py
- [x] T016 [US2] Add Shell/Bash choice to ask_technologies() under Automation category in src/projinit/cli.py
- [x] T017 [US2] Update tech_labels mapping in display_summary() for rust and shell in src/projinit/cli.py
- [x] T018 [US2] Test Rust and Shell/Bash generation by creating a test project

**Checkpoint**: User Story 2 complete - Rust and Shell/Bash fully supported

---

## Phase 5: User Story 3 - Support frameworks Front-end (Priority: P3)

**Goal**: Ajouter React, Vue.js, Angular, Svelte, Next.js/Nuxt.js comme technologies front-end

**Independent Test**: Sélectionner un framework front-end et vérifier le .gitignore généré

### Implementation for User Story 3

- [x] T019 [P] [US3] Create gitignore template for React in src/projinit/templates/gitignore/react.j2
- [x] T020 [P] [US3] Create gitignore template for Vue.js in src/projinit/templates/gitignore/vue.j2
- [x] T021 [P] [US3] Create gitignore template for Angular in src/projinit/templates/gitignore/angular.j2
- [x] T022 [P] [US3] Create gitignore template for Svelte in src/projinit/templates/gitignore/svelte.j2
- [x] T023 [P] [US3] Create gitignore template for Next.js/Nuxt.js in src/projinit/templates/gitignore/nextjs.j2
- [x] T024 [US3] Add React choice to ask_technologies() under Front-end category in src/projinit/cli.py
- [x] T025 [US3] Add Vue.js choice to ask_technologies() under Front-end category in src/projinit/cli.py
- [x] T026 [US3] Add Angular choice to ask_technologies() under Front-end category in src/projinit/cli.py
- [x] T027 [US3] Add Svelte choice to ask_technologies() under Front-end category in src/projinit/cli.py
- [x] T028 [US3] Add Next.js/Nuxt.js choice to ask_technologies() under Front-end category in src/projinit/cli.py
- [x] T029 [US3] Update tech_labels mapping for all front-end frameworks in src/projinit/cli.py
- [x] T030 [US3] Test front-end frameworks generation by creating test projects

**Checkpoint**: User Story 3 complete - All front-end frameworks supported

---

## Phase 6: User Story 4 - Support GitHub Actions et Kubernetes (Priority: P4)

**Goal**: Ajouter GitHub Actions et Kubernetes/Helm comme technologies DevOps

**Independent Test**: Sélectionner GitHub Actions ou Kubernetes et vérifier le .gitignore généré

### Implementation for User Story 4

- [x] T031 [P] [US4] Create gitignore template for GitHub Actions in src/projinit/templates/gitignore/github-actions.j2
- [x] T032 [P] [US4] Create gitignore template for Kubernetes/Helm in src/projinit/templates/gitignore/kubernetes.j2
- [x] T033 [US4] Add GitHub Actions choice to ask_technologies() under Outils category in src/projinit/cli.py
- [x] T034 [US4] Add Kubernetes/Helm choice to ask_technologies() under Infrastructure category in src/projinit/cli.py
- [x] T035 [US4] Update tech_labels mapping for github-actions and kubernetes in src/projinit/cli.py
- [x] T036 [US4] Test GitHub Actions and Kubernetes generation

**Checkpoint**: User Story 4 complete - DevOps tools supported

---

## Phase 7: User Story 5 - Support Java/Kotlin et Pulumi (Priority: P5)

**Goal**: Ajouter Java/Kotlin et Pulumi comme technologies d'entreprise

**Independent Test**: Sélectionner Java/Kotlin ou Pulumi et vérifier le .gitignore généré

### Implementation for User Story 5

- [x] T037 [P] [US5] Create gitignore template for Java/Kotlin in src/projinit/templates/gitignore/java.j2
- [x] T038 [P] [US5] Create gitignore template for Pulumi in src/projinit/templates/gitignore/pulumi.j2
- [x] T039 [P] [US5] Create precommit template for Java (checkstyle, spotless) in src/projinit/templates/precommit/java.j2
- [x] T040 [US5] Add Java/Kotlin choice to ask_technologies() under Langages category in src/projinit/cli.py
- [x] T041 [US5] Add Pulumi choice to ask_technologies() under Infrastructure category in src/projinit/cli.py
- [x] T042 [US5] Update tech_labels mapping for java and pulumi in src/projinit/cli.py
- [x] T043 [US5] Test Java/Kotlin and Pulumi generation

**Checkpoint**: User Story 5 complete - Enterprise technologies supported

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation updates

- [x] T044 Run full integration test with multiple technologies selected
- [x] T045 Update README.md with new technologies list in src/../README.md
- [x] T046 Update constitution.md if needed in .specify/memory/constitution.md
- [x] T047 Verify backward compatibility with existing technology selections
- [x] T048 Final code review and cleanup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verification only
- **Foundational (Phase 2)**: Depends on Setup - creates category structure
- **User Story 1 (Phase 3)**: Depends on Foundational - implements visual separators
- **User Story 2-5 (Phase 4-7)**: Depend on User Story 1 - add technologies to categorized list
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundational prerequisite for all other stories (category structure)
- **User Story 2 (P2)**: Independent after US1 - can run parallel with US3-5
- **User Story 3 (P3)**: Independent after US1 - can run parallel with US2, US4-5
- **User Story 4 (P4)**: Independent after US1 - can run parallel with US2-3, US5
- **User Story 5 (P5)**: Independent after US1 - can run parallel with US2-4

### Within Each User Story

- Templates (gitignore, precommit) can be created in parallel [P]
- CLI updates must be done after templates exist
- Label mapping update after CLI choices added
- Test after all components in place

### Parallel Opportunities

- All gitignore templates within a story marked [P] can run in parallel
- All precommit templates within a story marked [P] can run in parallel
- User Stories 2-5 can be worked on in parallel after US1 completes
- Different developers can work on different stories simultaneously

---

## Parallel Example: User Story 2

```bash
# Launch all templates for User Story 2 together:
Task: "Create gitignore template for Rust in src/projinit/templates/gitignore/rust.j2"
Task: "Create gitignore template for Shell/Bash in src/projinit/templates/gitignore/shell.j2"
Task: "Create precommit template for Rust in src/projinit/templates/precommit/rust.j2"
Task: "Create precommit template for Shell in src/projinit/templates/precommit/shell.j2"

# Then sequentially:
Task: "Add Rust and Shell choices to ask_technologies()"
Task: "Update tech_labels mapping"
Task: "Test generation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup verification
2. Complete Phase 2: Foundational (category structure)
3. Complete Phase 3: User Story 1 (visual separators)
4. **STOP and VALIDATE**: Test category display with `uv run projinit`
5. Commit and validate UX improvement

### Incremental Delivery

1. Complete Setup + Foundational + US1 → Categories working (MVP!)
2. Add User Story 2 → Rust/Shell supported → Commit
3. Add User Story 3 → Front-end frameworks → Commit
4. Add User Story 4 → DevOps tools → Commit
5. Add User Story 5 → Enterprise tech → Commit
6. Polish → Documentation updated → Final commit

### Recommended Order

For single developer, follow priority order: P1 → P2 → P3 → P4 → P5

---

## Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Setup | 1 | 0 |
| Foundational | 2 | 0 |
| US1 (P1) | 7 | 0 |
| US2 (P2) | 8 | 4 |
| US3 (P3) | 12 | 5 |
| US4 (P4) | 6 | 2 |
| US5 (P5) | 7 | 3 |
| Polish | 5 | 0 |
| **Total** | **48** | **14** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable after US1
- Commit after each user story completion
- Templates follow existing naming convention (lowercase, .j2 extension)
