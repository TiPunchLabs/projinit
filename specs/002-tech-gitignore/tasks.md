# Tasks: Sélection de Technologies pour .gitignore Adapté

**Input**: Design documents from `/specs/002-tech-gitignore/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Non demandés explicitement - pas de tâches de tests incluses.

**Organization**: Tâches groupées par user story pour permettre une implémentation et des tests indépendants.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Peut s'exécuter en parallèle (fichiers différents, pas de dépendances)
- **[Story]**: User story associée (US1, US2, US3)
- Chemins exacts inclus dans les descriptions

---

## Phase 1: Setup (Infrastructure Partagée)

**Purpose**: Création de la structure des templates gitignore

- [x] T001 Créer le répertoire templates/gitignore/ dans src/projinit/templates/gitignore/
- [x] T002 [P] Créer le fragment _common.j2 avec patterns universels dans src/projinit/templates/gitignore/_common.j2
- [x] T003 [P] Créer le fragment terraform.j2 (migration de l'existant) dans src/projinit/templates/gitignore/terraform.j2
- [x] T004 [P] Créer le fragment python.j2 dans src/projinit/templates/gitignore/python.j2
- [x] T005 [P] Créer le fragment node.j2 dans src/projinit/templates/gitignore/node.j2
- [x] T006 [P] Créer le fragment go.j2 dans src/projinit/templates/gitignore/go.j2
- [x] T007 [P] Créer le fragment docker.j2 dans src/projinit/templates/gitignore/docker.j2
- [x] T008 [P] Créer le fragment ide.j2 dans src/projinit/templates/gitignore/ide.j2

**Checkpoint**: Tous les fragments .gitignore sont créés et prêts à être utilisés.

---

## Phase 2: Foundational (Prérequis Bloquants)

**Purpose**: Extension du modèle de données pour supporter les technologies

**⚠️ CRITICAL**: Les user stories ne peuvent pas commencer avant cette phase.

- [x] T009 Étendre la dataclass ProjectConfig avec le champ technologies: list[str] dans src/projinit/generator.py
- [x] T010 Ajouter la valeur par défaut technologies=None avec field(default_factory=list) dans src/projinit/generator.py

**Checkpoint**: Le modèle ProjectConfig supporte les technologies - l'implémentation des user stories peut commencer.

---

## Phase 3: User Story 1 - Sélection des technologies (Priority: P1) 🎯 MVP

**Goal**: Permettre à l'utilisateur de sélectionner les technologies via un multi-select dans le questionnaire.

**Independent Test**: Exécuter `uv run projinit`, vérifier que la question technologies apparaît après direnv avec Terraform présélectionné.

### Implementation for User Story 1

- [x] T011 [US1] Créer la fonction ask_technologies() avec questionary.checkbox() dans src/projinit/cli.py
- [x] T012 [US1] Définir les 6 choix de technologies avec labels et valeurs dans src/projinit/cli.py
- [x] T013 [US1] Configurer Terraform comme présélectionné (checked=True) dans src/projinit/cli.py
- [x] T014 [US1] Appeler ask_technologies() après ask_direnv() dans la fonction main() de src/projinit/cli.py
- [x] T015 [US1] Gérer le cas d'annulation (None) pour ask_technologies() dans src/projinit/cli.py
- [x] T016 [US1] Passer les technologies au constructeur ProjectConfig dans src/projinit/cli.py
- [x] T017 [US1] Afficher les technologies sélectionnées dans display_summary() de src/projinit/cli.py

**Checkpoint**: L'utilisateur peut sélectionner les technologies, elles apparaissent dans le résumé.

---

## Phase 4: User Story 2 - Génération du .gitignore adapté (Priority: P1)

**Goal**: Générer un .gitignore contenant les patterns des technologies sélectionnées.

**Independent Test**: Générer un projet avec Python+Terraform, vérifier que le .gitignore contient les deux sections.

### Implementation for User Story 2

- [x] T018 [US2] Créer la fonction generate_gitignore_content(env, technologies) dans src/projinit/generator.py
- [x] T019 [US2] Implémenter le chargement du fragment _common.j2 dans generate_gitignore_content() de src/projinit/generator.py
- [x] T020 [US2] Implémenter la boucle de concaténation des fragments par technologie dans src/projinit/generator.py
- [x] T021 [US2] Modifier generate_project() pour utiliser generate_gitignore_content() au lieu de gitignore.j2 dans src/projinit/generator.py
- [x] T022 [US2] Supprimer l'ancien template gitignore.j2 de src/projinit/templates/gitignore.j2

**Checkpoint**: Le .gitignore généré contient les patterns de toutes les technologies sélectionnées.

---

## Phase 5: User Story 3 - Patterns communs automatiques (Priority: P2)

**Goal**: Garantir que les patterns communs sont toujours inclus, quelle que soit la sélection.

**Independent Test**: Générer un projet sans sélectionner de technologies, vérifier que .DS_Store et *.log sont présents.

### Implementation for User Story 3

- [x] T023 [US3] Vérifier que _common.j2 est toujours chargé en premier dans generate_gitignore_content() de src/projinit/generator.py
- [x] T024 [US3] Ajouter les patterns .direnv/ au fragment _common.j2 dans src/projinit/templates/gitignore/_common.j2

**Checkpoint**: Les patterns communs sont présents dans tous les .gitignore générés.

---

## Phase 6: Polish & Validation Finale

**Purpose**: Vérifications et nettoyage

- [x] T025 Vérifier que chaque fragment a un commentaire header identifiant la technologie dans src/projinit/templates/gitignore/*.j2
- [x] T026 Exécuter les scénarios de test de quickstart.md manuellement
- [x] T027 Mettre à jour le README.md si nécessaire pour documenter la nouvelle fonctionnalité

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Pas de dépendances - peut commencer immédiatement
- **Foundational (Phase 2)**: Dépend de Setup - BLOQUE toutes les user stories
- **User Story 1 (Phase 3)**: Dépend de Foundational
- **User Story 2 (Phase 4)**: Dépend de Foundational + T001-T008 (fragments)
- **User Story 3 (Phase 5)**: Dépend de User Story 2
- **Polish (Phase 6)**: Dépend de toutes les user stories

### User Story Dependencies

- **User Story 1 (P1)**: Indépendante après Phase 2
- **User Story 2 (P1)**: Dépend des fragments (T002-T008) et du modèle (T009-T010)
- **User Story 3 (P2)**: Dépend de US2 (vérifie le comportement de génération)

### Within Each User Story

- Modèles avant services
- Services avant génération
- Vérifier le fonctionnement après chaque tâche

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# Lancer en parallèle après T001:
T002, T003, T004, T005, T006, T007, T008
```

**Phase 2 (Foundational)**:
```bash
# Séquentiel - T010 dépend de T009
T009 → T010
```

**Phase 3 (US1) - Séquentiel**:
```bash
T011 → T012 → T013 → T014 → T015 → T016 → T017
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Compléter Phase 1: Setup (créer tous les fragments)
2. Compléter Phase 2: Foundational (étendre ProjectConfig)
3. Compléter Phase 3: User Story 1 (question multi-select)
4. Compléter Phase 4: User Story 2 (génération .gitignore)
5. **STOP et VALIDER**: Tester avec quickstart.md scénarios 1-3
6. Déployer/démo si prêt

### Incremental Delivery

1. Setup + Foundational → Infrastructure prête
2. Ajouter US1 → Tester → La question apparaît
3. Ajouter US2 → Tester → Le .gitignore est correct
4. Ajouter US3 → Tester → Les patterns communs sont toujours présents
5. Chaque story ajoute de la valeur sans casser les précédentes

---

## Notes

- Tous les fragments doivent avoir un header `# TechnologyName` comme première ligne
- L'ordre des fragments dans le .gitignore: _common → technologies triées alphabétiquement
- Pas de déduplication automatique des patterns (accepté dans la spec)
- Commit après chaque phase ou groupe logique de tâches
