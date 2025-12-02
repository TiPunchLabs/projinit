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

### Structure des Modules
```
src/projinit/
├── cli.py          → Point d'entrée, orchestration du workflow
├── config.py       → Chargement et parsing de la configuration
├── validators.py   → Validation des entrées utilisateur
├── checks.py       → Vérification des dépendances système
├── generator.py    → Génération des fichiers projet
└── templates/      → Templates Jinja2
```

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
- Code modulaire avec responsabilités séparées
- Gestion explicite des erreurs avec messages utilisateur clairs
- Validation des entrées à toutes les frontières
- Échappement approprié pour la génération HCL

### Tests (À Implémenter)
- Tests unitaires pour chaque module (validators, config, generator)
- Tests d'intégration pour le workflow complet
- Tests des templates avec différentes combinaisons de paramètres

## Gouvernance

Cette constitution définit les principes fondateurs de projinit. Toute modification architecturale doit respecter ces principes. Les amendements nécessitent une justification documentée et une mise à jour de ce document.

### Priorités de Décision
1. Sécurité des secrets et tokens
2. Simplicité du code et de l'UX
3. Extensibilité via les templates
4. Compatibilité avec l'écosystème Terraform

**Version**: 1.0.0 | **Ratified**: 2025-12-02 | **Last Amended**: 2025-12-02
