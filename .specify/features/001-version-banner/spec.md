# Feature Specification: Version Banner

**Feature Branch**: `001-version-banner`
**Created**: 2025-12-02
**Status**: Draft
**Input**: Affichage élégant des informations de version comme `specify version`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Affichage Version Élégant (Priority: P1)

En tant qu'utilisateur de projinit, je veux pouvoir afficher les informations de version de manière élégante avec un ASCII art et les détails système, pour avoir une vue d'ensemble de mon installation.

**Why this priority**: C'est la fonctionnalité principale demandée. L'affichage actuel `projinit --version` est minimaliste ("projinit 0.1.0").

**Independent Test**: Exécuter `projinit version` et vérifier l'affichage du banner.

**Acceptance Scenarios**:

1. **Given** l'utilisateur exécute `projinit version`, **When** la commande s'exécute, **Then** un ASCII art "PROJINIT" s'affiche suivi d'un panel d'informations
2. **Given** l'utilisateur exécute `projinit version`, **When** la commande s'exécute, **Then** la version du CLI est affichée
3. **Given** l'utilisateur exécute `projinit version`, **When** la commande s'exécute, **Then** la version Python est affichée
4. **Given** l'utilisateur exécute `projinit version`, **When** la commande s'exécute, **Then** la plateforme (Linux/macOS) est affichée
5. **Given** l'utilisateur exécute `projinit version`, **When** la commande s'exécute, **Then** l'architecture (x86_64/arm64) est affichée

---

### User Story 2 - Compatibilité avec --version (Priority: P2)

En tant qu'utilisateur de projinit, je veux que l'option `--version` continue de fonctionner pour les scripts qui parsent la sortie.

**Why this priority**: Rétrocompatibilité avec l'usage existant.

**Independent Test**: Exécuter `projinit --version` et vérifier la sortie simple.

**Acceptance Scenarios**:

1. **Given** l'utilisateur exécute `projinit --version`, **When** la commande s'exécute, **Then** la sortie reste "projinit X.Y.Z" (format simple pour parsing)
2. **Given** l'utilisateur exécute `projinit -v`, **When** la commande s'exécute, **Then** la sortie reste "projinit X.Y.Z"

---

### Edge Cases

- Que se passe-t-il si le terminal ne supporte pas les couleurs ? (fallback gracieux)
- Que se passe-t-il sur un terminal très étroit ? (ASCII art potentiellement cassé)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher un ASCII art "PROJINIT" lors de `projinit version`
- **FR-002**: Le système DOIT afficher la version du CLI dans un panel Rich
- **FR-003**: Le système DOIT afficher la version Python utilisée
- **FR-004**: Le système DOIT afficher la plateforme (Linux, Darwin, Windows)
- **FR-005**: Le système DOIT afficher l'architecture du processeur
- **FR-006**: Le système DOIT afficher la version de l'OS
- **FR-007**: L'option `--version` DOIT conserver son comportement actuel (sortie simple)
- **FR-008**: La sous-commande `version` DOIT être ajoutée au CLI

### Informations à Afficher

| Champ | Source | Exemple |
|-------|--------|---------|
| CLI Version | `projinit.__version__` | 0.1.0 |
| Python | `sys.version_info` | 3.12.3 |
| Platform | `platform.system()` | Linux |
| Architecture | `platform.machine()` | x86_64 |
| OS Version | `platform.release()` | 6.14.0-36-generic |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `projinit version` affiche le banner complet avec toutes les informations
- **SC-002**: `projinit --version` continue d'afficher le format simple
- **SC-003**: L'affichage utilise les couleurs Rich pour une présentation élégante
- **SC-004**: Le banner s'affiche en moins de 100ms
