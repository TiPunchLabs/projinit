# projinit Constitution

## Core Principles

### I. Simplicité et Minimalisme
Le code doit rester simple et focalisé. Chaque module a une responsabilité unique et claire. Pas de sur-ingénierie : seules les fonctionnalités explicitement demandées sont implémentées. YAGNI (You Aren't Gonna Need It) est le principe directeur.

### II. Configuration-Driven
Le comportement de l'application est entièrement contrôlé par la configuration YAML. La hiérarchie de configuration (local → global → défauts) permet une flexibilité maximale. Les valeurs par défaut sensées permettent un démarrage rapide.

### III. Template-Based Generation
La génération de fichiers utilise exclusivement Jinja2 pour la templating. Les templates sont isolés dans un répertoire dédié et peuvent être personnalisés. Le filtre `hcl_escape` garantit la sécurité des valeurs injectées dans Terraform.

### IV. Expérience Utilisateur Interactive
L'interface CLI est interactive avec un questionnaire guidé. Rich fournit un formatage visuel élégant (panels, status, couleurs). Les validations sont effectuées en temps réel avec des messages d'erreur clairs.

### V. Sécurité First
Les tokens GitHub ne sont jamais stockés en clair dans le projet. L'intégration optionnelle direnv + pass offre une gestion sécurisée des secrets. Les variables sensibles sont marquées comme `sensitive` dans Terraform.

## Stack Technique

### Technologies Mandatées
| Composant | Technologie | Version |
|-----------|-------------|---------|
| Langage | Python | >= 3.10 |
| Package Manager | uv | Latest |
| CLI Prompts | questionary | >= 2.0.0 |
| Terminal UI | rich | >= 13.0.0 |
| Templating | Jinja2 | >= 3.1.0 |
| Configuration | PyYAML | >= 6.0 |
| Build System | Hatchling | Latest |

### Infrastructure Générée
| Composant | Technologie | Version |
|-----------|-------------|---------|
| IaC | Terraform | >= 1.0 |
| Provider | GitHub Provider | ~> 6.0 |
| Secrets (optionnel) | pass + direnv | Latest |

## Architecture

### Structure des Modules (v2.0)
```
src/projinit/
├── __init__.py         → Version et metadata
├── cli/                → Commandes CLI
│   ├── main.py         → Point d'entrée principal
│   ├── check_cmd.py    → Commande audit (projinit check)
│   ├── update_cmd.py   → Commande correction (projinit update)
│   ├── init_cmd.py     → Commande création (projinit new)
│   └── config_cmd.py   → Commande configuration (projinit config)
├── core/               → Logique métier
│   ├── models.py       → Modèles de données (ProjectType, CheckResult, etc.)
│   ├── detector.py     → Détection automatique du type de projet
│   ├── checker.py      → Vérification de conformité
│   ├── updater.py      → Correction automatique
│   ├── config.py       → Gestion de la configuration
│   └── reporter.py     → Génération des rapports
├── standards/          → Standards externalisés
│   ├── loader.py       → Chargeur de standards YAML
│   └── defaults/       → Standards par défaut
│       ├── base.yaml   → Checks communs à tous les types
│       ├── python.yaml → Standards Python (CLI/Lib)
│       ├── node.yaml   → Standards Node.js (React/Vite/PWA)
│       ├── infra.yaml  → Standards Infrastructure (Terraform/Ansible)
│       ├── documentation.yaml → Standards Documentation (MkDocs)
│       └── lab.yaml    → Standards Lab/Tutorial
└── templates/          → Templates Jinja2
    ├── gitignore/      → Templates .gitignore par technologie
    └── precommit/      → Templates pre-commit par technologie
```

### Types de Projets Supportés (v2.0)

| Type | Description | Standards |
|------|-------------|-----------|
| `python-cli` | Application CLI Python | pyproject.toml, src/, tests/, ruff |
| `python-lib` | Bibliothèque Python | pyproject.toml, src/, tests/, py.typed |
| `node-frontend` | Frontend Node.js (React/Vue/Vite/PWA) | package.json, src/, tsconfig, eslint |
| `infrastructure` | IaC Terraform + Ansible | main.tf, variables.tf, playbook.yml |
| `documentation` | Documentation MkDocs | mkdocs.yml, docs/, pyproject.toml |
| `lab` | Lab/Tutorial/Dojo | labs/, exercises/, solutions/, README |

### Technologies Supportées
La sélection des technologies est organisée en catégories pour une meilleure UX :

| Catégorie | Technologies |
|-----------|--------------|
| Langages | Python, Node.js, Go, Rust, Java/Kotlin |
| Front-end | HTML/CSS, React, Vue.js, Angular, Svelte, Next.js/Nuxt.js |
| Infrastructure | Terraform, Pulumi, Kubernetes/Helm |
| Conteneurs | Docker |
| Automation | Ansible, Shell/Bash |
| Outils | IDE (VSCode/JetBrains), GitHub Actions |

Chaque technologie dispose d'un template `.gitignore` dédié. Les technologies avec outils de linting (Python, Node.js, Go, Rust, Shell/Bash, Java, Terraform, Docker, Ansible) disposent également d'un template pre-commit.

### Flux de Données
1. **Entrée CLI** → Questionnaire interactif
2. **Configuration** → Chargement YAML (local/global/défaut)
3. **Validation** → Vérification des entrées et prérequis
4. **Génération** → Rendu des templates Jinja2
5. **Initialisation** → Git init + commit initial

## Conventions de Développement

### Naming Conventions
- **Modules Python**: snake_case (`my_module.py`)
- **Classes**: PascalCase (`ProjectConfig`)
- **Fonctions/Variables**: snake_case (`generate_project`)
- **Templates**: nom_fichier.extension.j2 (`main.tf.j2`)
- **Noms de projet générés**: slug-case (`my-project`)

### Patterns Appliqués
- **Dataclass**: Pour les structures de configuration type-safe
- **Factory Pattern**: `Config.get_default()` pour la création d'instances
- **Template Method**: Algorithme de génération extensible
- **Validation Pipeline**: Vérifications composables et chaînées

### Règles de Code
- Documentation en français pour le README utilisateur
- Docstrings en anglais dans le code source
- Type hints obligatoires pour les signatures de fonctions
- Pas de dépendances non déclarées dans pyproject.toml

## Qualité et Tests

### Standards de Qualité

#### Analyse Statique (automatisée, bloquante)
- **Linting**: `ruff check` — zéro erreur, zéro warning
- **Formatage**: `ruff format` — code formaté avant commit
- **Type checking**: type hints validés (mypy optionnel mais recommandé)

#### Limites de Complexité
- Complexité cyclomatique: < 10 par fonction
- Longueur fonction: < 50 lignes (hors docstrings/commentaires)
- Longueur fichier: < 300 lignes (découper si dépassement)
- Profondeur d'imbrication: < 4 niveaux

#### DRY & Maintenabilité
- Aucun bloc dupliqué > 5 lignes — extraire en fonction/module
- Single Responsibility: une fonction = une tâche
- Pas de magic numbers/strings — utiliser des constantes nommées
- Docstrings obligatoires pour les fonctions publiques

#### Sécurité
- Aucun secret dans le code (tokens, mots de passe)
- Variables sensibles via environnement ou pass/direnv
- Validation des entrées utilisateur à toutes les frontières
- Échappement systématique pour la génération HCL (`hcl_escape`)

#### Gestion de la Dette Technique
- TODO interdit sans format: `TODO(#issue): description`
- Code mort supprimé, jamais commenté
- Pas de `# type: ignore` sans justification

### Tests

#### Couverture Requise
- Minimum: 80% lignes, 70% branches
- Modules critiques (validators, generator): 90%+

#### Types de Tests
| Type | Scope | Outils |
|------|-------|--------|
| Unitaires | Chaque module isolé | pytest |
| Intégration | Workflow CLI complet | pytest + tmp_path |
| Templates | Combinaisons de paramètres | pytest + snapshots |

#### Bonnes Pratiques Tests
- Nommage: `test_<fonction>_<scenario>_<resultat_attendu>`
- Fixtures partagées dans `conftest.py`
- Pas de tests skippés sans issue liée
- Mocks limités aux frontières externes (GitHub API, filesystem)

### Quality Gate Checklist

Avant de marquer une tâche comme terminée, vérifier :

- [ ] `ruff check` passe sans erreur
- [ ] `ruff format --check` passe
- [ ] Tests écrits et passants (`pytest`)
- [ ] Aucun warning nouveau introduit
- [ ] Docstrings ajoutées si fonction publique
- [ ] Pas de secrets ou valeurs hardcodées
- [ ] Type hints présents sur les signatures

## Intégration Continue (CI)

### Pipeline GitHub Actions
Un workflow CI automatisé valide la qualité du code à chaque push et Pull Request :

| Job | Outil | Description |
|-----|-------|-------------|
| lint | ruff check | Vérification des règles de linting Python |
| format | ruff format --check | Vérification du formatage du code |
| test | pytest | Exécution des tests unitaires et d'intégration |

### Matrice de Tests
Le pipeline s'exécute sur Python 3.10, 3.11 et 3.12 pour garantir la compatibilité.

### Standards de Validation
- Tout push déclenche le pipeline
- Les PRs vers `main` doivent passer tous les checks
- Aucun code ne doit être fusionné avec des erreurs de linting ou de formatage

## Gouvernance

Cette constitution définit les principes fondateurs de projinit. Toute modification architecturale doit respecter ces principes. Les amendements nécessitent une justification documentée et une mise à jour de ce document.

### Priorités de Décision
1. Sécurité des secrets et tokens
2. Simplicité du code et de l'UX
3. Extensibilité via les templates
4. Compatibilité avec l'écosystème Terraform

**Version**: 1.3.0 | **Ratified**: 2025-12-02 | **Last Amended**: 2026-01-17
