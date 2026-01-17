# Architecture de projinit

## Vue d'Ensemble

projinit est un outil CLI Python qui gere le cycle de vie des projets : creation, audit et mise a jour selon des standards definis.

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Layer                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  check   │ │   new    │ │  update  │ │  config  │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
└───────┼────────────┼────────────┼────────────┼──────────────────┘
        │            │            │            │
┌───────┼────────────┼────────────┼────────────┼──────────────────┐
│       ▼            ▼            ▼            ▼   Core Layer     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ checker │  │generator│  │ updater │  │ config  │            │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │            │                  │
│       └────────────┴─────┬──────┴────────────┘                  │
│                          ▼                                      │
│                    ┌──────────┐                                 │
│                    │ detector │                                 │
│                    └────┬─────┘                                 │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                         ▼         Data Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   standards/ │  │  templates/  │  │   models.py  │          │
│  │   (YAML)     │  │   (Jinja2)   │  │  (dataclass) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Structure des Modules

```
src/projinit/
├── __init__.py              # Version (__version__ = "2.0.0")
├── main_cli.py              # Point d'entree principal
│
├── cli/                     # Couche CLI
│   ├── __init__.py
│   ├── check_cmd.py         # projinit check
│   ├── init_cmd.py          # projinit new
│   ├── update_cmd.py        # projinit update
│   └── config_cmd.py        # projinit config
│
├── core/                    # Couche Metier
│   ├── models.py            # Modeles de donnees (Enum, dataclass)
│   ├── detector.py          # Detection automatique du type
│   ├── checker.py           # Verification de conformite
│   ├── updater.py           # Correction automatique
│   ├── config.py            # Gestion configuration
│   └── reporter.py          # Generation rapports
│
├── standards/               # Standards externalises
│   ├── loader.py            # Chargeur YAML
│   └── defaults/            # Standards par defaut
│       ├── base.yaml        # Checks communs
│       ├── python.yaml      # Python CLI/Lib
│       ├── node.yaml        # Node.js Frontend
│       ├── infra.yaml       # Infrastructure
│       ├── documentation.yaml
│       └── lab.yaml
│
└── templates/               # Templates Jinja2
    ├── README.md.j2
    ├── LICENSE.j2
    ├── CLAUDE.md.j2
    ├── pyproject.toml.j2
    ├── gitignore/           # Par technologie
    ├── precommit/           # Par technologie
    └── commands/            # Commandes Claude Code
```

## Flux de Donnees

### 1. Commande `check` (Audit)

```
Entree: chemin projet
    │
    ▼
┌─────────────────┐
│ detector.detect │ ─────► ProjectType
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  loader.load    │ ─────► List[CheckDefinition]
│  (base + type)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ checker.check   │ ─────► List[CheckResult]
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ reporter.report │ ─────► AuditReport (text/json/markdown)
└─────────────────┘
```

### 2. Commande `new` (Creation)

```
Entree: nom, type, options
    │
    ▼
┌─────────────────────┐
│ Questions interactif│ (questionary)
│ ou arguments CLI    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ _generate_project   │
│  ├─ common files    │ (README, LICENSE, .gitignore...)
│  ├─ type-specific   │ (pyproject.toml, package.json...)
│  └─ .claude/commands│
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ git init + commit   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ direnv allow (opt)  │
└─────────────────────┘
```

### 3. Commande `update` (Correction)

```
Entree: chemin projet
    │
    ▼
┌─────────────────┐
│ checker.check   │ ─────► List[CheckResult] (failed)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ updater.plan    │ ─────► List[UpdateAction]
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Confirmation user   │ (--dry-run / --interactive)
└────────┬────────────┘
         │
         ▼
┌─────────────────┐
│ updater.apply   │ ─────► Fichiers modifies/crees
└─────────────────┘
```

## Choix Techniques

### Python >= 3.10

- **Raison** : Type hints modernes (`list[str]` vs `List[str]`), pattern matching
- **Impact** : Syntaxe plus claire, meilleure maintenabilite

### questionary pour les prompts

- **Alternative consideree** : click, typer, prompt-toolkit
- **Raison du choix** : API simple, beau rendu terminal, support checkbox/select
- **Exemple** :
  ```python
  questionary.select("Type:", choices=[...]).ask()
  questionary.checkbox("Technologies:", choices=[...]).ask()
  ```

### rich pour l'affichage

- **Alternative consideree** : colorama, termcolor
- **Raison du choix** : Panels, tables, progress bars, markup riche
- **Exemple** :
  ```python
  console.print(Panel.fit("[bold]Title[/bold]"))
  console.print("[green]Success[/green]")
  ```

### Jinja2 pour les templates

- **Alternative consideree** : string.Template, mako
- **Raison du choix** : Standard de l'industrie, conditions, boucles, heritage
- **Exemple** :
  ```jinja
  {% if project_type == "python-cli" %}
  [project.scripts]
  {{ project_name }} = "{{ project_name_snake }}.cli:main"
  {% endif %}
  ```

### YAML pour les standards

- **Alternative consideree** : JSON, TOML, Python dict
- **Raison du choix** : Lisibilite humaine, commentaires, structure claire
- **Exemple** :
  ```yaml
  - id: has_readme
    description: README.md must exist
    level: required
    type: file_exists
    path: README.md
  ```

### dataclass pour les modeles

- **Alternative consideree** : attrs, pydantic
- **Raison du choix** : Stdlib Python, pas de dependance, suffisant pour le cas d'usage
- **Exemple** :
  ```python
  @dataclass
  class CheckResult:
      id: str
      status: CheckStatus
      message: str
  ```

## Extensibilite

### Ajouter un nouveau type de projet

1. Ajouter l'enum dans `core/models.py`
2. Ajouter les marqueurs dans `core/detector.py`
3. Creer `standards/defaults/<type>.yaml`
4. Ajouter le mapping dans `standards/loader.py`
5. Ajouter la generation dans `cli/init_cmd.py`

### Ajouter un nouveau check

1. Definir dans le fichier YAML du type concerne
2. Si nouveau type de check : implementer dans `core/checker.py`

### Ajouter un nouveau template

1. Creer le fichier `.j2` dans `templates/`
2. Ajouter la generation dans `cli/init_cmd.py`

## Performance

- **Detection** : O(n) avec n = nombre de marqueurs (< 20)
- **Checks** : O(m) avec m = nombre de checks (< 30)
- **Templates** : Compilation unique par session

## Securite

- Tokens GitHub jamais stockes en clair
- Integration direnv + pass pour les secrets
- Variables sensibles marquees `sensitive` dans Terraform
- Filtre `hcl_escape` pour echapper les valeurs HCL
