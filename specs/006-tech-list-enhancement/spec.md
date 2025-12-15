# Feature Specification: Amélioration de la Liste des Technologies

**Feature Branch**: `006-tech-list-enhancement`
**Created**: 2025-12-15
**Status**: Draft
**Input**: Amélioration de la liste des technologies avec catégorisation par groupes (séparateurs visuels), ajout de nouvelles technologies (Rust, Shell/Bash, React, Vue.js, Angular, Svelte, Next.js/Nuxt.js, GitHub Actions, Kubernetes, Java/Kotlin, Pulumi), organisées par priorité d'implémentation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Navigation facilitée par catégories (Priority: P1)

En tant qu'utilisateur de projinit, je veux voir les technologies organisées par catégories visuellement séparées afin de trouver rapidement la technologie qui m'intéresse sans parcourir une longue liste plate.

**Why this priority**: L'amélioration de l'UX est immédiate et bénéficie à tous les utilisateurs sans nécessiter de nouveaux templates. C'est le fondement sur lequel s'appuient les autres stories.

**Independent Test**: Peut être testé en exécutant `projinit` et en vérifiant que la liste des technologies affiche des séparateurs de catégories (Langages, Front-end, Infrastructure, etc.)

**Acceptance Scenarios**:

1. **Given** l'utilisateur lance projinit, **When** il arrive à la question des technologies, **Then** il voit les technologies organisées en catégories avec des séparateurs visuels
2. **Given** l'utilisateur navigue dans la liste, **When** il passe d'une catégorie à l'autre, **Then** les séparateurs sont clairement visibles et non sélectionnables

---

### User Story 2 - Support des langages Rust et Shell/Bash (Priority: P2)

En tant que développeur, je veux pouvoir sélectionner Rust ou Shell/Bash comme technologies de mon projet afin que le .gitignore et le .pre-commit-config.yaml générés soient adaptés à ces langages.

**Why this priority**: Rust et Shell/Bash sont des langages très répandus. Le support de ces langages répond à un besoin fréquent des utilisateurs.

**Independent Test**: Peut être testé en sélectionnant Rust ou Shell/Bash et en vérifiant que les fichiers générés contiennent les patterns appropriés.

**Acceptance Scenarios**:

1. **Given** l'utilisateur sélectionne Rust, **When** le projet est généré, **Then** le .gitignore contient les patterns Rust (target/, Cargo.lock pour les bibliothèques, etc.)
2. **Given** l'utilisateur sélectionne Rust, **When** le projet est généré, **Then** le .pre-commit-config.yaml contient les hooks pour Rust (clippy, rustfmt)
3. **Given** l'utilisateur sélectionne Shell/Bash, **When** le projet est généré, **Then** le .gitignore contient les patterns Shell appropriés
4. **Given** l'utilisateur sélectionne Shell/Bash, **When** le projet est généré, **Then** le .pre-commit-config.yaml contient les hooks shellcheck et shfmt

---

### User Story 3 - Support des frameworks Front-end (Priority: P3)

En tant que développeur front-end, je veux pouvoir sélectionner React, Vue.js, Angular, Svelte ou Next.js/Nuxt.js afin que les fichiers de configuration générés soient adaptés à mon framework.

**Why this priority**: Les frameworks front-end sont essentiels pour les projets web modernes. Cette story couvre un large éventail de développeurs.

**Independent Test**: Peut être testé en sélectionnant un framework front-end et en vérifiant les fichiers générés.

**Acceptance Scenarios**:

1. **Given** l'utilisateur sélectionne React, **When** le projet est généré, **Then** le .gitignore contient les patterns React/CRA (node_modules, build, .env.local)
2. **Given** l'utilisateur sélectionne Vue.js, **When** le projet est généré, **Then** le .gitignore contient les patterns Vue (dist, .env.local)
3. **Given** l'utilisateur sélectionne Angular, **When** le projet est généré, **Then** le .gitignore contient les patterns Angular (.angular, dist)
4. **Given** l'utilisateur sélectionne Svelte, **When** le projet est généré, **Then** le .gitignore contient les patterns Svelte (.svelte-kit, build)
5. **Given** l'utilisateur sélectionne Next.js/Nuxt.js, **When** le projet est généré, **Then** le .gitignore contient les patterns SSR (.next, .nuxt, .output)

---

### User Story 4 - Support GitHub Actions et Kubernetes (Priority: P4)

En tant que développeur DevOps, je veux pouvoir sélectionner GitHub Actions ou Kubernetes/Helm afin que les fichiers de configuration soient adaptés à ces outils.

**Why this priority**: Ces outils sont complémentaires à l'écosystème existant (Terraform, Docker) et importants pour les workflows CI/CD modernes.

**Independent Test**: Peut être testé en sélectionnant GitHub Actions ou Kubernetes et en vérifiant les fichiers générés.

**Acceptance Scenarios**:

1. **Given** l'utilisateur sélectionne GitHub Actions, **When** le projet est généré, **Then** le .gitignore contient les patterns GitHub Actions appropriés
2. **Given** l'utilisateur sélectionne Kubernetes/Helm, **When** le projet est généré, **Then** le .gitignore contient les patterns Kubernetes (*.kubeconfig, charts/*.tgz)

---

### User Story 5 - Support Java/Kotlin et Pulumi (Priority: P5)

En tant que développeur d'entreprise, je veux pouvoir sélectionner Java/Kotlin ou Pulumi afin que les fichiers de configuration soient adaptés à ces technologies.

**Why this priority**: Technologies de niche mais importantes pour certains contextes d'entreprise. Priorité plus basse car audience plus restreinte.

**Independent Test**: Peut être testé en sélectionnant Java/Kotlin ou Pulumi et en vérifiant les fichiers générés.

**Acceptance Scenarios**:

1. **Given** l'utilisateur sélectionne Java/Kotlin, **When** le projet est généré, **Then** le .gitignore contient les patterns JVM (target/, build/, *.class, *.jar)
2. **Given** l'utilisateur sélectionne Pulumi, **When** le projet est généré, **Then** le .gitignore contient les patterns Pulumi (Pulumi.*.yaml pour les secrets, .pulumi/)

---

### Edge Cases

- Que se passe-t-il si l'utilisateur ne sélectionne aucune technologie ? Le système génère uniquement le .gitignore commun (_common.j2)
- Que se passe-t-il si l'utilisateur sélectionne des technologies incompatibles (ex: React ET Angular) ? Pas de blocage, les deux patterns sont ajoutés au .gitignore
- Comment le système gère-t-il les technologies sans hooks pre-commit ? Seul le .gitignore est impacté, pas de section dans .pre-commit-config.yaml

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher les technologies organisées en catégories avec des séparateurs visuels non sélectionnables
- **FR-002**: Les catégories DOIVENT être : Langages, Front-end, Infrastructure, Conteneurs, Automation, Outils
- **FR-003**: Le système DOIT supporter les nouvelles technologies : Rust, Shell/Bash, React, Vue.js, Angular, Svelte, Next.js/Nuxt.js, GitHub Actions, Kubernetes/Helm, Java/Kotlin, Pulumi
- **FR-004**: Chaque nouvelle technologie DOIT avoir un template .gitignore dédié
- **FR-005**: Les technologies avec des outils de linting/formatting DOIVENT avoir un template pre-commit dédié
- **FR-006**: Le mapping des labels d'affichage DOIT être mis à jour pour inclure toutes les nouvelles technologies
- **FR-007**: Terraform DOIT rester coché par défaut (comportement existant préservé)

### Key Entities

- **Technology**: Représente une technologie sélectionnable (value, label, catégorie, checked par défaut)
- **Category**: Représente un groupe de technologies (label du séparateur, ordre d'affichage)
- **Template gitignore**: Fichier Jinja2 contenant les patterns d'exclusion pour une technologie
- **Template precommit**: Fichier Jinja2 contenant les hooks pre-commit pour une technologie

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'utilisateur peut identifier et sélectionner une technologie en moins de 10 secondes grâce à la catégorisation
- **SC-002**: 100% des nouvelles technologies génèrent un .gitignore fonctionnel sans erreur
- **SC-003**: Les technologies avec linting (Rust, Shell/Bash) génèrent des hooks pre-commit valides et exécutables
- **SC-004**: Le temps de génération du projet reste inférieur à 5 secondes malgré l'ajout de technologies
- **SC-005**: La compatibilité ascendante est maintenue : les projets existants utilisant les technologies actuelles fonctionnent identiquement

## Assumptions

- Les patterns .gitignore sont basés sur les conventions standard de chaque technologie (gitignore.io, documentation officielle)
- Les hooks pre-commit utilisent les outils les plus répandus pour chaque technologie
- L'ordre des catégories reflète la fréquence d'utilisation typique (langages en premier)
- Next.js et Nuxt.js sont regroupés car ils partagent des patterns similaires (SSR)
