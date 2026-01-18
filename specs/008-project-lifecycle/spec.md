# Feature Specification: Project Lifecycle Management

**Feature Branch**: `008-project-lifecycle`
**Created**: 2026-01-17
**Status**: Draft
**Target Version**: v2.0.0 (version majeure)
**Input**: Analyse de 7 projets existants pour extraire une méthodologie unifiée de structuration, initialisation et mise à jour de projets.

## Contexte

Cette évolution majeure transforme projinit d'un simple générateur de projets en un **gestionnaire de cycle de vie de projets** capable de :
- Initialiser de nouveaux projets selon des standards définis
- Auditer la conformité des projets existants
- Mettre à jour les projets pour les aligner sur les standards

### Projets analysés

| Projet | Type | Technologies |
|--------|------|--------------|
| cv-converter | Python CLI | Python, ruff, pre-commit |
| good-points | PWA Frontend | React, TypeScript, Vite, Tailwind |
| proxmox-vm-neutron | Infrastructure | Terraform, Ansible |
| proxmox-vm-kubebeast | Infrastructure | Terraform, Ansible |
| k8s-dojo | Documentation | MkDocs Material |
| ckad-dojo | Documentation | MkDocs Material |
| projinit | Python CLI | Python, ruff, pre-commit |

### Méthodologie extraite - 3 niveaux

**Niveau 1 - Obligatoire (tous projets)**
- `README.md`, `LICENSE`, `.gitignore`
- `.pre-commit-config.yaml` (hooks de base)
- `CLAUDE.md` (instructions pour Claude Code)

**Niveau 2 - Recommandé (selon écosystème)**
- Python: `pyproject.toml`, `src/`, `tests/`
- Node.js: `package.json`, `src/`, `tsconfig.json`
- Infrastructure: `terraform/`, `ansible/`

**Niveau 3 - Spécifique projet**
- `.github/workflows/` (CI/CD)
- `.specify/` (spécifications)
- `docs/` (documentation)

---

## User Scenarios & Testing

### User Story 1 - Audit de conformité (Priority: P1)

En tant que développeur, je veux auditer un projet existant pour identifier les écarts avec les standards de mon organisation, afin de savoir exactement ce qui doit être corrigé.

**Why this priority**: C'est la fonctionnalité la plus demandée - comprendre l'état actuel avant toute modification. Sans audit, impossible de prioriser les corrections.

**Independent Test**: Peut être testé en exécutant `projinit check` sur n'importe quel projet et en vérifiant que le rapport identifie correctement les fichiers manquants/non conformes.

**Acceptance Scenarios**:

1. **Given** un projet Python existant sans `.pre-commit-config.yaml`, **When** j'exécute `projinit check`, **Then** le rapport indique que `.pre-commit-config.yaml` est manquant avec une priorité "obligatoire".

2. **Given** un projet avec un `pyproject.toml` incomplet (pas de section `[tool.ruff]`), **When** j'exécute `projinit check`, **Then** le rapport indique que la configuration ruff est manquante avec les recommandations.

3. **Given** un projet entièrement conforme aux standards, **When** j'exécute `projinit check`, **Then** le rapport affiche un score de conformité de 100% avec un message de succès.

4. **Given** un projet, **When** j'exécute `projinit check --format json`, **Then** le résultat est exporté en JSON pour intégration CI.

---

### User Story 2 - Mise à jour automatique (Priority: P1)

En tant que développeur, je veux mettre à jour automatiquement un projet existant pour le rendre conforme aux standards, afin de gagner du temps sur les corrections manuelles.

**Why this priority**: Complémentaire à l'audit - après avoir identifié les écarts, il faut pouvoir les corriger. Ensemble, ces deux fonctionnalités forment le coeur de la v2.0.

**Independent Test**: Peut être testé en exécutant `projinit update` sur un projet non conforme et en vérifiant que les fichiers sont ajoutés/modifiés correctement.

**Acceptance Scenarios**:

1. **Given** un projet sans `CLAUDE.md`, **When** j'exécute `projinit update`, **Then** un fichier `CLAUDE.md` est généré avec les instructions appropriées au type de projet.

2. **Given** un projet avec un `.pre-commit-config.yaml` incomplet, **When** j'exécute `projinit update`, **Then** les hooks manquants sont ajoutés sans supprimer les existants.

3. **Given** un projet, **When** j'exécute `projinit update --dry-run`, **Then** les modifications prévues sont affichées sans être appliquées.

4. **Given** un projet, **When** j'exécute `projinit update --interactive`, **Then** chaque modification est proposée avec confirmation (y/n/a pour all).

5. **Given** un fichier existant qui serait modifié, **When** j'exécute `projinit update`, **Then** une sauvegarde `.bak` est créée avant modification (sauf si `--no-backup`).

---

### User Story 3 - Initialisation enrichie (Priority: P2)

En tant que développeur, je veux initialiser un nouveau projet avec tous les standards de mon organisation appliqués automatiquement, afin de démarrer avec une base solide.

**Why this priority**: L'initialisation existe déjà dans projinit v1.x. Cette story l'enrichit mais n'est pas critique car les projets existants sont plus nombreux que les nouveaux.

**Independent Test**: Peut être testé en exécutant `projinit init` dans un répertoire vide et en vérifiant la structure générée.

**Acceptance Scenarios**:

1. **Given** un répertoire vide, **When** j'exécute `projinit init --type python-cli`, **Then** une structure complète Python CLI est générée (pyproject.toml, src/, tests/, .pre-commit-config.yaml, CLAUDE.md, etc.).

2. **Given** un répertoire vide, **When** j'exécute `projinit init` sans arguments, **Then** un assistant interactif me guide pour choisir le type de projet.

3. **Given** un répertoire avec des fichiers existants, **When** j'exécute `projinit init`, **Then** je reçois un avertissement et une demande de confirmation.

4. **Given** un répertoire, **When** j'exécute `projinit init --type infrastructure`, **Then** une structure Terraform + Ansible est générée avec les bonnes pratiques.

---

### User Story 4 - Configuration externalisée (Priority: P2)

En tant que lead technique, je veux définir mes propres standards dans un fichier de configuration, afin d'adapter projinit aux conventions de mon équipe.

**Why this priority**: Permet la personnalisation sans modifier le code. Important pour l'adoption mais pas bloquant pour une première version.

**Independent Test**: Peut être testé en créant un fichier `.projinit.yaml` personnalisé et en vérifiant que les commandes l'utilisent.

**Acceptance Scenarios**:

1. **Given** un fichier `~/.config/projinit/standards.yaml` définissant des hooks pre-commit personnalisés, **When** j'exécute `projinit update`, **Then** ces hooks sont utilisés à la place des défauts.

2. **Given** un fichier `.projinit.yaml` à la racine du projet, **When** j'exécute `projinit check`, **Then** les standards locaux ont priorité sur les globaux.

3. **Given** une configuration avec des templates personnalisés, **When** j'exécute `projinit init`, **Then** mes templates sont utilisés pour la génération.

---

### User Story 5 - Rapport détaillé (Priority: P3)

En tant que développeur, je veux un rapport visuel clair avec des suggestions de correction, afin de comprendre facilement ce qui doit être fait.

**Why this priority**: Améliore l'expérience utilisateur mais n'est pas fonctionnellement critique.

**Independent Test**: Peut être testé en exécutant `projinit check` et en vérifiant la qualité du formatage du rapport.

**Acceptance Scenarios**:

1. **Given** un projet non conforme, **When** j'exécute `projinit check`, **Then** le rapport affiche un tableau coloré avec icônes (✓/✗), catégories, et score global.

2. **Given** un élément manquant, **When** le rapport est affiché, **Then** une suggestion de commande `projinit update` est proposée.

3. **Given** un projet, **When** j'exécute `projinit check --verbose`, **Then** des détails supplémentaires sont affichés pour chaque vérification.

---

### Edge Cases

- **Projet sans gestionnaire de dépendances détecté**: Proposer de choisir manuellement le type ou utiliser un mode "generic".
- **Conflit de fusion lors de l'update**: Afficher le diff et demander résolution manuelle.
- **Fichier verrouillé ou en lecture seule**: Afficher une erreur claire et continuer avec les autres fichiers.
- **Standards contradictoires** (local vs global): Le local a toujours priorité, afficher un warning.
- **Projet dans un monorepo**: Détecter et traiter chaque sous-projet indépendamment ou le projet racine.

---

## Requirements

### Functional Requirements

- **FR-001**: Le système DOIT détecter automatiquement le type de projet (Python, Node.js, Infrastructure, Documentation) basé sur les fichiers présents.
- **FR-002**: Le système DOIT supporter 3 commandes principales : `init`, `check`, `update`.
- **FR-003**: Le système DOIT charger les standards depuis des fichiers YAML externalisés.
- **FR-004**: Le système DOIT supporter une hiérarchie de configuration : défaut < global < local.
- **FR-005**: Le système DOIT générer des rapports en plusieurs formats : texte, JSON, markdown.
- **FR-006**: Le système DOIT créer des sauvegardes avant modification de fichiers existants (par défaut).
- **FR-007**: Le système DOIT supporter un mode `--dry-run` pour prévisualiser les changements.
- **FR-008**: Le système DOIT supporter un mode `--interactive` pour confirmation individuelle.
- **FR-009**: Le système DOIT intégrer les hooks pre-commit de manière additive (sans supprimer les existants).
- **FR-010**: Le système DOIT respecter les templates Jinja2 existants pour la génération de fichiers.
- **FR-011**: Le système DOIT retourner un code de sortie approprié (0 = conforme, 1 = non conforme, 2 = erreur).

### Key Entities

- **Standard**: Définition d'une règle de conformité (fichier requis, contenu attendu, hooks).
- **ProjectType**: Catégorie de projet (python-cli, python-lib, node-frontend, infrastructure, documentation).
- **CheckResult**: Résultat d'une vérification (passed, failed, warning, skipped).
- **UpdateAction**: Action de mise à jour (create, modify, merge, skip).

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: L'audit d'un projet de taille moyenne (< 1000 fichiers) s'exécute en moins de 5 secondes.
- **SC-002**: La mise à jour d'un projet génère 0 régression sur les fichiers existants (tests automatisés).
- **SC-003**: 100% des projets analysés (cv-converter, good-points, etc.) peuvent être audités avec succès.
- **SC-004**: Le rapport d'audit identifie correctement au moins 95% des écarts manuellement vérifiés.
- **SC-005**: La documentation couvre 100% des commandes et options disponibles.
