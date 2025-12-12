# Feature Specification: Chemin de Destination Personnalisé

**Feature Branch**: `003-output-path`
**Created**: 2025-12-09
**Status**: Draft
**Input**: Ajouter la possibilité de spécifier le chemin de destination où générer le projet. Par défaut, le projet est généré dans le dossier courant.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Génération dans le dossier courant (Priority: P1)

En tant que développeur, je veux pouvoir générer un projet dans le dossier courant sans avoir à spécifier de chemin, afin de conserver le comportement actuel simple et rapide.

**Why this priority**: C'est le comportement par défaut qui doit fonctionner. La rétrocompatibilité est essentielle - les utilisateurs existants ne doivent pas voir de changement dans leur workflow habituel.

**Independent Test**: Exécuter `projinit` sans argument de chemin et vérifier que le projet est créé dans le dossier courant.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est dans le dossier `/home/user/projects`, **When** il exécute `projinit` et nomme son projet "mon-projet", **Then** le projet est créé dans `/home/user/projects/mon-projet`
2. **Given** l'utilisateur ne fournit pas d'argument de chemin, **When** le questionnaire se termine, **Then** aucune question sur le chemin de destination n'est posée

---

### User Story 2 - Spécification du chemin via argument CLI (Priority: P1)

En tant que développeur, je veux pouvoir spécifier un chemin de destination via un argument en ligne de commande, afin de générer le projet dans un dossier spécifique sans interaction supplémentaire.

**Why this priority**: Permet l'automatisation et les scripts. Les utilisateurs avancés ont besoin de cette flexibilité.

**Independent Test**: Exécuter `projinit --path /tmp/mes-projets` et vérifier que le projet est créé dans ce dossier.

**Acceptance Scenarios**:

1. **Given** l'utilisateur fournit `--path /tmp/projets`, **When** il nomme son projet "test-app", **Then** le projet est créé dans `/tmp/projets/test-app`
2. **Given** l'utilisateur fournit un chemin relatif `--path ../autres-projets`, **When** il est dans `/home/user/dev`, **Then** le projet est créé dans `/home/user/autres-projets/nom-projet`
3. **Given** l'utilisateur fournit un chemin avec `~`, **When** le projet est généré, **Then** le tilde est correctement résolu vers le home directory

---

### User Story 3 - Validation et création du chemin (Priority: P2)

En tant que développeur, je veux que le système valide le chemin fourni et crée les dossiers intermédiaires si nécessaire, afin d'éviter les erreurs de génération.

**Why this priority**: Améliore la robustesse mais n'est pas bloquant pour le MVP si la validation basique fonctionne.

**Independent Test**: Fournir un chemin inexistant et vérifier qu'il est créé automatiquement.

**Acceptance Scenarios**:

1. **Given** le chemin `/tmp/nouveau/dossier` n'existe pas, **When** l'utilisateur le spécifie comme destination, **Then** les dossiers intermédiaires sont créés automatiquement
2. **Given** le chemin parent `/readonly` n'est pas accessible en écriture, **When** l'utilisateur le spécifie, **Then** un message d'erreur clair est affiché avant la génération
3. **Given** le chemin fourni est un fichier existant (pas un dossier), **When** l'utilisateur le spécifie, **Then** un message d'erreur indique que le chemin doit être un dossier

---

### Edge Cases

- Que se passe-t-il si le chemin contient des caractères spéciaux ? Le système doit les accepter si le système de fichiers les supporte.
- Que se passe-t-il si le chemin pointe vers un montage réseau lent ? Le système doit fonctionner normalement, la latence est acceptable.
- Que se passe-t-il si le chemin est vide (`--path ""`) ? Le système utilise le dossier courant par défaut.
- Que se passe-t-il si le projet existe déjà dans le chemin cible ? Le système affiche une erreur comme actuellement.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT accepter un argument optionnel `--path` ou `-p` pour spécifier le chemin de destination
- **FR-002**: Le système DOIT utiliser le dossier courant comme destination par défaut si aucun chemin n'est spécifié
- **FR-003**: Le système DOIT accepter les chemins absolus (commençant par `/`)
- **FR-004**: Le système DOIT accepter les chemins relatifs et les résoudre par rapport au dossier courant
- **FR-005**: Le système DOIT résoudre le caractère `~` vers le répertoire home de l'utilisateur
- **FR-006**: Le système DOIT créer les dossiers intermédiaires si le chemin n'existe pas
- **FR-007**: Le système DOIT vérifier que le chemin parent est accessible en écriture avant de commencer la génération
- **FR-008**: Le système DOIT afficher un message d'erreur clair si le chemin n'est pas valide ou accessible
- **FR-009**: Le système DOIT afficher le chemin complet résolu dans le récapitulatif avant confirmation
- **FR-010**: Le système DOIT conserver la rétrocompatibilité avec le comportement actuel (aucun argument = dossier courant)

### Key Entities

- **OutputPath**: Représente le chemin de destination (brut, résolu, existence, permissions)
- **ProjectConfig**: Configuration du projet étendue pour inclure le chemin de destination

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% des utilisateurs existants peuvent continuer à utiliser projinit sans changer leur workflow
- **SC-002**: L'utilisateur peut spécifier un chemin de destination en moins de 5 secondes (un seul argument)
- **SC-003**: Le chemin résolu est affiché dans le récapitulatif pour validation visuelle
- **SC-004**: 100% des erreurs de chemin sont détectées avant la génération (pas d'échec en cours de génération)
- **SC-005**: Les chemins relatifs, absolus et avec tilde fonctionnent de manière cohérente

## Assumptions

- Les utilisateurs comprennent la notion de chemin absolu vs relatif
- Le système de fichiers cible supporte les opérations standard (création de dossiers, écriture)
- Les permissions du système de fichiers sont vérifiables avant la génération
- Le caractère `~` représente toujours le home directory de l'utilisateur courant
