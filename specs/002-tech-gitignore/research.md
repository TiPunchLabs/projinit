# Research: Sélection de Technologies pour .gitignore Adapté

**Feature**: 002-tech-gitignore
**Date**: 2025-12-09

## Research Tasks

### 1. questionary.checkbox() - Multi-select Implementation

**Decision**: Utiliser `questionary.checkbox()` avec l'option `checked` pour présélectionner Terraform.

**Rationale**:
- API native de questionary, déjà une dépendance du projet
- Supporte les valeurs présélectionnées via le paramètre `checked`
- Retourne une liste de valeurs, compatible avec notre besoin

**Alternatives Considered**:
- `questionary.select()` avec multi=True : N'existe pas dans l'API
- Prompt texte libre avec parsing : Mauvaise UX, erreurs possibles
- Bibliothèque tierce (inquirer, etc.) : Dépendance inutile

**Example**:
```python
technologies = questionary.checkbox(
    "Technologies du projet :",
    choices=[
        questionary.Choice("Python", value="python"),
        questionary.Choice("Node.js", value="node"),
        questionary.Choice("Go", value="go"),
        questionary.Choice("Terraform", value="terraform", checked=True),
        questionary.Choice("Docker", value="docker"),
        questionary.Choice("IDE (VSCode/JetBrains)", value="ide"),
    ]
).ask()
```

### 2. Jinja2 Fragment Loading - Best Practices

**Decision**: Utiliser `PackageLoader` existant avec sous-répertoire, charger les fragments individuellement.

**Rationale**:
- Cohérent avec l'architecture existante (`get_template_env()`)
- Pas besoin de modifier la configuration Jinja2
- Chemin relatif : `gitignore/python.j2`

**Alternatives Considered**:
- FileSystemLoader séparé : Incohérent avec le reste du projet
- Inline templates : Moins maintenable, pas de séparation
- YAML avec patterns : Over-engineering

**Implementation Pattern**:
```python
def generate_gitignore_content(env: Environment, technologies: list[str]) -> str:
    content = env.get_template("gitignore/_common.j2").render()
    for tech in sorted(technologies):
        template_path = f"gitignore/{tech}.j2"
        content += "\n" + env.get_template(template_path).render()
    return content
```

### 3. Standard .gitignore Patterns per Technology

**Decision**: Utiliser les patterns standards de gitignore.io comme référence, mais embarqués localement.

**Rationale**:
- Pas de dépendance réseau (principe de simplicité)
- Patterns stables et bien connus
- Maintenable manuellement pour 6 technologies

**Sources de référence**:
- https://github.com/github/gitignore (templates officiels GitHub)
- https://www.toptal.com/developers/gitignore (gitignore.io)

**Patterns par technologie**:

| Technology | Key Patterns |
|------------|--------------|
| _common | .DS_Store, Thumbs.db, *.log, .direnv/, *~ |
| python | __pycache__/, *.py[cod], .venv/, .env, dist/, *.egg-info/ |
| node | node_modules/, dist/, .npm, *.tgz, .env.local |
| go | /bin/, *.exe, vendor/, go.work |
| terraform | .terraform/, *.tfstate*, *.tfvars.backup, .terraform.lock.hcl |
| docker | .docker/, docker-compose.override.yml |
| ide | .idea/, .vscode/, *.swp, *.swo, .project, .settings/ |

## Resolved Clarifications

Aucune clarification nécessaire - la feature est suffisamment spécifiée dans la spec.

## Open Questions

Aucune question ouverte - prêt pour l'implémentation.
