# Data Model: Sélection de Technologies pour .gitignore Adapté

**Feature**: 002-tech-gitignore
**Date**: 2025-12-09

## Entities

### ProjectConfig (Extended)

Extension de la dataclass existante pour inclure les technologies sélectionnées.

```text
ProjectConfig
├── name: str                    # Nom du projet (existant)
├── description: str             # Description (existant)
├── owner: str                   # Owner GitHub (existant)
├── visibility: str              # public/private (existant)
├── use_direnv: bool             # Activation direnv (existant)
├── pass_secret_path: str        # Chemin pass (existant)
└── technologies: list[str]      # [NEW] Technologies sélectionnées
```

**Validation Rules**:
- `technologies` ne peut pas être None (liste vide acceptable)
- Chaque valeur doit correspondre à un fragment existant
- Valeurs valides : `python`, `node`, `go`, `terraform`, `docker`, `ide`

### Technology Choice

Représente une option de technologie dans le questionnaire.

```text
TechnologyChoice (conceptuel, pas une classe)
├── value: str      # Identifiant interne (ex: "python")
├── label: str      # Label affiché (ex: "Python")
└── checked: bool   # Présélectionné par défaut (True pour terraform)
```

**Note**: Pas besoin d'une classe dédiée - utilisation directe de `questionary.Choice`.

### GitignoreFragment

Représente un fichier template de patterns .gitignore.

```text
GitignoreFragment (fichier template)
├── path: str           # templates/gitignore/{name}.j2
├── header: str         # Commentaire identifiant (ex: "# Python")
└── patterns: list[str] # Lignes de patterns
```

**Naming Convention**: `{technology_value}.j2` (ex: `python.j2`, `node.j2`)

**Special**: `_common.j2` est toujours inclus en premier.

## Relationships

```text
┌─────────────────┐      selects      ┌──────────────────┐
│  User           │─────────────────▶ │  TechnologyChoice │
└─────────────────┘                   └──────────────────┘
                                              │
                                              │ maps to
                                              ▼
┌─────────────────┐    contains       ┌──────────────────┐
│  ProjectConfig  │◀──────────────────│  technologies[]  │
└─────────────────┘                   └──────────────────┘
        │
        │ uses
        ▼
┌─────────────────┐    concatenates   ┌──────────────────┐
│  Generator      │──────────────────▶│ GitignoreFragment │
└─────────────────┘                   └──────────────────┘
        │
        │ produces
        ▼
┌─────────────────┐
│  .gitignore     │
└─────────────────┘
```

## State Transitions

Pas de transitions d'état complexes. Le flux est linéaire :

1. **Selection** → User sélectionne technologies via checkbox
2. **Storage** → Technologies stockées dans ProjectConfig.technologies
3. **Generation** → Fragments concaténés en .gitignore final

## Data Defaults

| Field | Default Value |
|-------|---------------|
| `technologies` | `["terraform"]` (Terraform présélectionné) |

## Constraints

- Un fragment doit exister pour chaque technologie supportée
- Le fragment `_common.j2` DOIT toujours exister
- Aucune validation des patterns eux-mêmes (contenu libre dans les templates)
