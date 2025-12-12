# Tasks: Chemin de Destination Personnalisé

**Input**: Design documents from `/specs/003-output-path/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Non demandés explicitement - pas de tâches de tests incluses.

**Organization**: Tâches groupées par user story pour permettre une implémentation et des tests indépendants.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Peut s'exécuter en parallèle (fichiers différents, pas de dépendances)
- **[Story]**: User story associée (US1, US2, US3)
- Chemins exacts inclus dans les descriptions

---

## Phase 1: Setup (Infrastructure Partagée)

**Purpose**: Préparation de l'environnement - import nécessaire

- [x] T001 Ajouter l'import `os` dans src/projinit/cli.py

**Checkpoint**: Import disponible pour os.access().

---

## Phase 2: Foundational (Prérequis Bloquants)

**Purpose**: Fonctions helper et argument CLI qui servent à toutes les user stories

**⚠️ CRITICAL**: Les user stories ne peuvent pas commencer avant cette phase.

- [x] T002 Ajouter l'argument `--path` / `-p` dans parse_args() de src/projinit/cli.py
- [x] T003 Créer la fonction _get_first_existing_parent(path) dans src/projinit/cli.py
- [x] T004 Créer la fonction resolve_output_path(path_arg) dans src/projinit/cli.py

**Checkpoint**: L'argument CLI est parsé et les fonctions de résolution sont disponibles.

---

## Phase 3: User Story 1 - Génération dans le dossier courant (Priority: P1) 🎯 MVP

**Goal**: Garantir la rétrocompatibilité - sans argument `--path`, le projet est créé dans le dossier courant.

**Independent Test**: Exécuter `uv run projinit` sans argument et vérifier que le projet est créé dans le dossier courant.

### Implementation for User Story 1

- [x] T005 [US1] Modifier main() pour appeler resolve_output_path(args.path) dans src/projinit/cli.py
- [x] T006 [US1] Modifier main() pour utiliser base_path au lieu de Path.cwd() pour target_dir dans src/projinit/cli.py
- [x] T007 [US1] Vérifier que resolve_output_path(None) retourne Path.cwd() dans src/projinit/cli.py

**Checkpoint**: Sans argument --path, le comportement est identique à l'existant.

---

## Phase 4: User Story 2 - Spécification du chemin via argument CLI (Priority: P1)

**Goal**: Permettre à l'utilisateur de spécifier un chemin de destination via `--path` ou `-p`.

**Independent Test**: Exécuter `uv run projinit --path /tmp/custom` et vérifier que le projet est créé dans `/tmp/custom/nom-projet`.

### Implementation for User Story 2

- [x] T008 [US2] Implémenter la résolution du tilde (~) avec Path.expanduser() dans resolve_output_path() de src/projinit/cli.py
- [x] T009 [US2] Implémenter la résolution des chemins relatifs avec Path.resolve() dans resolve_output_path() de src/projinit/cli.py
- [x] T010 [US2] Modifier display_summary() pour accepter target_dir en paramètre dans src/projinit/cli.py
- [x] T011 [US2] Afficher le chemin complet résolu dans display_summary() de src/projinit/cli.py
- [x] T012 [US2] Mettre à jour l'appel à display_summary() dans main() pour passer target_dir dans src/projinit/cli.py

**Checkpoint**: L'utilisateur peut spécifier un chemin absolu, relatif ou avec tilde.

---

## Phase 5: User Story 3 - Validation et création du chemin (Priority: P2)

**Goal**: Valider le chemin fourni et afficher des messages d'erreur clairs avant la génération.

**Independent Test**: Fournir un chemin non accessible en écriture et vérifier qu'un message d'erreur clair est affiché.

### Implementation for User Story 3

- [x] T013 [US3] Ajouter la vérification is_file() dans resolve_output_path() de src/projinit/cli.py
- [x] T014 [US3] Ajouter la vérification os.access(W_OK) dans resolve_output_path() de src/projinit/cli.py
- [x] T015 [US3] Ajouter la gestion du chemin vide (fallback vers cwd) dans resolve_output_path() de src/projinit/cli.py
- [x] T016 [US3] Ajouter le try/except pour ValueError et PermissionError dans main() de src/projinit/cli.py

**Checkpoint**: Toutes les erreurs de chemin sont détectées avant la génération.

---

## Phase 6: Polish & Validation Finale

**Purpose**: Vérifications et documentation

- [x] T017 Vérifier que --help affiche correctement l'option --path
- [x] T018 Exécuter les scénarios 1-9 de quickstart.md manuellement
- [x] T019 Mettre à jour le README.md pour documenter l'option --path dans la section Options

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Pas de dépendances - peut commencer immédiatement
- **Foundational (Phase 2)**: Dépend de Setup - BLOQUE toutes les user stories
- **User Story 1 (Phase 3)**: Dépend de Foundational
- **User Story 2 (Phase 4)**: Dépend de Foundational (peut être en parallèle avec US1)
- **User Story 3 (Phase 5)**: Dépend de Foundational (peut être en parallèle avec US1/US2)
- **Polish (Phase 6)**: Dépend de toutes les user stories

### User Story Dependencies

- **User Story 1 (P1)**: Indépendante après Phase 2 - MVP minimal
- **User Story 2 (P1)**: Indépendante après Phase 2 - Peut se faire en parallèle avec US1
- **User Story 3 (P2)**: Indépendante après Phase 2 - Peut se faire en parallèle avec US1/US2

**Note**: Les 3 user stories modifient le même fichier (cli.py), donc en pratique elles doivent être implémentées séquentiellement pour éviter les conflits.

### Within Each User Story

- Modifications de resolve_output_path() avant modifications de main()
- Modifications de display_summary() avant modifications de main()
- Vérifier le fonctionnement après chaque tâche

### Parallel Opportunities

**Phase 2 (Foundational)**:
```bash
# T003 et T004 peuvent être écrits en parallèle (fonctions indépendantes)
# mais T004 utilise T003, donc séquentiel recommandé
```

**Phases 3-5 (User Stories)**:
```bash
# En théorie parallélisables, mais même fichier = séquentiel en pratique
# Recommandé: US1 → US2 → US3
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Compléter Phase 1: Setup (import os)
2. Compléter Phase 2: Foundational (argument + fonctions)
3. Compléter Phase 3: User Story 1 (comportement par défaut)
4. **STOP et VALIDER**: Tester avec quickstart.md scénario 1
5. Compléter Phase 4: User Story 2 (chemins personnalisés)
6. **STOP et VALIDER**: Tester avec quickstart.md scénarios 2-4
7. Compléter Phase 5: User Story 3 (validation)
8. **STOP et VALIDER**: Tester avec quickstart.md scénarios 5-9
9. Compléter Phase 6: Polish

### Incremental Delivery

1. Setup + Foundational → Infrastructure prête
2. Ajouter US1 → Tester → Rétrocompatibilité OK
3. Ajouter US2 → Tester → Chemins personnalisés fonctionnels
4. Ajouter US3 → Tester → Validation robuste
5. Chaque story ajoute de la valeur sans casser les précédentes

---

## Notes

- Toutes les modifications sont dans `src/projinit/cli.py`
- Aucune modification requise dans `generator.py` (target_dir déjà paramétrable)
- Messages d'erreur en français pour cohérence avec l'UX existante
- Commit après chaque phase ou groupe logique de tâches
