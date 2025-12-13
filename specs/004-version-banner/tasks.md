# Tasks: Version Banner Stylisé

**Input**: Design documents from `/specs/004-version-banner/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, quickstart.md ✓

**Tests**: Non demandés explicitement - tests manuels uniquement via quickstart.md

**Organization**: Tasks groupées par user story pour implémentation et test indépendants.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Peut s'exécuter en parallèle (fichiers différents, pas de dépendances)
- **[Story]**: User story concernée (US1, US2)
- Chemins exacts inclus dans les descriptions

## Path Conventions

- **Projet**: `src/projinit/` (structure single project existante)

---

## Phase 1: Setup

**Purpose**: Aucune initialisation nécessaire - projet existant

*Aucune tâche - le projet est déjà initialisé avec les dépendances requises (rich)*

---

## Phase 2: Foundational

**Purpose**: Aucun prérequis bloquant - les fichiers à modifier existent déjà

*Aucune tâche - les fichiers cli.py et version.py existent*

**Checkpoint**: Prêt pour l'implémentation des user stories

---

## Phase 3: User Story 1 - Affichage de version stylisé (Priority: P1) 🎯 MVP

**Goal**: Afficher un banner complet avec ASCII art, description, features et usage lorsque l'utilisateur exécute `projinit --version`

**Independent Test**: Exécuter `uv run projinit --version` et vérifier que le banner complet s'affiche avec toutes les sections

### Implementation for User Story 1

- [x] T001 [US1] Enrichir la fonction display_version_banner() avec les sections Description, Features et Usage dans src/projinit/version.py
- [x] T002 [US1] Créer la classe VersionAction(argparse.Action) pour intercepter --version dans src/projinit/cli.py
- [x] T003 [US1] Remplacer action="version" par action=VersionAction dans parse_args() de src/projinit/cli.py
- [x] T004 [US1] Tester manuellement `uv run projinit --version` pour valider l'affichage complet

**Checkpoint**: `projinit --version` affiche le banner complet avec toutes les sections

---

## Phase 4: User Story 2 - Cohérence avec sous-commande version (Priority: P2)

**Goal**: Assurer que `projinit version` et `projinit --version` affichent exactement le même contenu

**Independent Test**: Comparer visuellement la sortie de `projinit version` et `projinit --version`

### Implementation for User Story 2

- [x] T005 [US2] Vérifier que la sous-commande version utilise déjà display_version_banner() dans src/projinit/cli.py
- [x] T006 [US2] Tester manuellement `uv run projinit version` pour confirmer la cohérence avec --version

**Checkpoint**: Les deux commandes produisent le même affichage

---

## Phase 5: Polish & Validation

**Purpose**: Validation finale et mise à jour de la version

- [x] T007 Mettre à jour __version__ à "0.2.1" dans src/projinit/__init__.py
- [x] T008 Exécuter la validation complète selon quickstart.md
- [x] T009 Mettre à jour le fichier README.md avec la nouvelle fonctionnalité si nécessaire

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Aucune tâche
- **Foundational (Phase 2)**: Aucune tâche
- **User Story 1 (Phase 3)**: Peut commencer immédiatement
- **User Story 2 (Phase 4)**: Dépend de T001 (même fonction display_version_banner)
- **Polish (Phase 5)**: Dépend de la complétion des US1 et US2

### User Story Dependencies

- **User Story 1 (P1)**: Indépendante - modifie version.py et cli.py
- **User Story 2 (P2)**: Dépend de US1 car elle vérifie la cohérence du résultat

### Within User Story 1

```
T001 (version.py) ──┐
                    ├──→ T003 (intégration) ──→ T004 (test)
T002 (cli.py) ──────┘
```

T001 et T002 peuvent être exécutées en parallèle car elles modifient des fichiers différents, mais T003 dépend des deux.

### Parallel Opportunities

- T001 et T002 peuvent s'exécuter en parallèle (fichiers différents)

---

## Parallel Example: User Story 1

```bash
# Ces deux tâches peuvent être lancées en parallèle:
Task T001: "Enrichir display_version_banner() dans src/projinit/version.py"
Task T002: "Créer VersionAction dans src/projinit/cli.py"

# Puis séquentiellement:
Task T003: "Intégrer VersionAction dans parse_args()"
Task T004: "Test manuel"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Compléter T001: Enrichir version.py avec le nouveau format
2. Compléter T002: Créer VersionAction dans cli.py
3. Compléter T003: Intégrer dans parse_args()
4. **VALIDER**: Tester `projinit --version`
5. ✅ MVP fonctionnel

### Incremental Delivery

1. User Story 1 → Banner complet avec --version
2. User Story 2 → Vérification cohérence avec sous-commande
3. Polish → Mise à jour version et documentation

---

## Notes

- Cette feature est simple: 2 fichiers à modifier
- Pas de tests automatisés demandés - validation manuelle via quickstart.md
- La version sera mise à jour à 0.2.1 pour refléter cette amélioration
- Commit recommandé après chaque phase complétée
