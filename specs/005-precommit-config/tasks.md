# Tasks: Génération automatique de pre-commit config

**Input**: Design documents from `/specs/005-precommit-config/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, quickstart.md ✓

**Tests**: Non demandés explicitement - tests manuels uniquement via quickstart.md

**Organization**: Tasks groupées par user story pour implémentation et test indépendants.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Peut s'exécuter en parallèle (fichiers différents, pas de dépendances)
- **[Story]**: User story concernée (US1, US2)
- Chemins exacts inclus dans les descriptions

## Path Conventions

- **Projet**: `src/projinit/` (structure single project existante)
- **Templates**: `src/projinit/templates/`

---

## Phase 1: Setup

**Purpose**: Création de la structure des templates pre-commit

- [ ] T001 Créer le dossier src/projinit/templates/precommit/

---

## Phase 2: Foundational - Templates communs

**Purpose**: Créer les templates de base utilisés par toutes les user stories

- [ ] T002 [P] Créer le template _header.j2 avec hooks communs dans src/projinit/templates/precommit/_header.j2
- [ ] T003 [P] Créer le template python.j2 avec hooks ruff dans src/projinit/templates/precommit/python.j2
- [ ] T004 [P] Créer le template node.j2 avec hooks eslint/prettier dans src/projinit/templates/precommit/node.j2
- [ ] T005 [P] Créer le template go.j2 avec hooks gofmt/golangci-lint dans src/projinit/templates/precommit/go.j2
- [ ] T006 [P] Créer le template terraform.j2 avec hooks terraform dans src/projinit/templates/precommit/terraform.j2
- [ ] T007 [P] Créer le template docker.j2 avec hook hadolint dans src/projinit/templates/precommit/docker.j2

**Checkpoint**: Tous les templates de base sont créés

---

## Phase 3: User Story 1 - Génération automatique du fichier pre-commit (Priority: P1) 🎯 MVP

**Goal**: Générer le fichier `.pre-commit-config.yaml` automatiquement basé sur les technologies sélectionnées

**Independent Test**: Créer un projet avec `uv run projinit`, sélectionner des technologies et vérifier que le fichier `.pre-commit-config.yaml` contient les hooks appropriés

### Implementation for User Story 1

- [ ] T008 [US1] Ajouter la fonction generate_precommit_content() dans src/projinit/generator.py
- [ ] T009 [US1] Modifier generate_project() pour appeler generate_precommit_content() et écrire .pre-commit-config.yaml dans src/projinit/generator.py
- [ ] T010 [US1] Tester manuellement la génération avec différentes combinaisons de technologies

**Checkpoint**: `projinit` génère le fichier `.pre-commit-config.yaml` avec les hooks appropriés

---

## Phase 4: User Story 2 - Ajout d'Ansible aux technologies (Priority: P2)

**Goal**: Ajouter Ansible comme technologie sélectionnable avec ses hooks pre-commit et patterns .gitignore

**Independent Test**: Sélectionner Ansible lors de la création d'un projet et vérifier la présence des hooks ansible-lint et des patterns .gitignore

### Implementation for User Story 2

- [ ] T011 [P] [US2] Créer le template ansible.j2 avec hook ansible-lint dans src/projinit/templates/precommit/ansible.j2
- [ ] T012 [P] [US2] Créer le template gitignore/ansible.j2 avec patterns Ansible dans src/projinit/templates/gitignore/ansible.j2
- [ ] T013 [US2] Ajouter Ansible à la liste des technologies dans ask_technologies() de src/projinit/cli.py
- [ ] T014 [US2] Tester manuellement la sélection Ansible et vérifier les fichiers générés

**Checkpoint**: Ansible est sélectionnable et génère les hooks/gitignore appropriés

---

## Phase 5: Polish & Validation

**Purpose**: Validation finale et mises à jour

- [ ] T015 Mettre à jour __version__ à "0.3.0" dans src/projinit/__init__.py
- [ ] T016 Mettre à jour pyproject.toml avec la version 0.3.0
- [ ] T017 Exécuter la validation complète selon quickstart.md
- [ ] T018 Mettre à jour le fichier README.md avec la nouvelle fonctionnalité
- [ ] T019 Mettre à jour version.py pour ajouter "Génération pre-commit" aux Features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Aucune dépendance - créer le dossier
- **Foundational (Phase 2)**: Dépend de Phase 1 - créer les templates
- **User Story 1 (Phase 3)**: Dépend de Phase 2 - implémenter la génération
- **User Story 2 (Phase 4)**: Peut commencer après Phase 2 (parallèle avec US1 possible)
- **Polish (Phase 5)**: Dépend de US1 et US2

### User Story Dependencies

- **User Story 1 (P1)**: Dépend des templates de base (Phase 2)
- **User Story 2 (P2)**: Dépend des templates de base (Phase 2), indépendante de US1

### Parallel Opportunities

**Phase 2** - Tous les templates peuvent être créés en parallèle:
```
T002, T003, T004, T005, T006, T007 → peuvent s'exécuter en parallèle
```

**Phase 4** - Les templates Ansible peuvent être créés en parallèle:
```
T011, T012 → peuvent s'exécuter en parallèle
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Compléter Phase 1: Setup (T001)
2. Compléter Phase 2: Templates (T002-T007)
3. Compléter Phase 3: User Story 1 (T008-T010)
4. **VALIDER**: Tester avec `uv run projinit` et vérifier le fichier généré
5. ✅ MVP fonctionnel

### Incremental Delivery

1. Phase 1 + Phase 2 → Templates prêts
2. User Story 1 → Génération pre-commit fonctionnelle
3. User Story 2 → Support Ansible ajouté
4. Polish → Version 0.3.0 et documentation

---

## Notes

- Cette feature suit le même pattern que la génération du .gitignore (fragments Jinja2)
- Les versions des hooks sont définies dans research.md
- La version sera incrémentée à 0.3.0 (nouvelle fonctionnalité majeure)
- Commit recommandé après chaque phase complétée
