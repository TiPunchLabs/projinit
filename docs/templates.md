# Systeme de Templates Jinja2

## Concept

Les templates Jinja2 definissent le contenu des fichiers generes. Ils permettent une personnalisation dynamique basee sur le contexte du projet.

## Structure des Templates

```
templates/
├── README.md.j2           # README generique
├── LICENSE.j2             # Licence MIT
├── CLAUDE.md.j2           # Instructions Claude Code
├── pyproject.toml.j2      # Config Python standard
├── pyproject-docs.toml.j2 # Config Python pour docs
├── package.json.j2        # Config Node.js
├── mkdocs.yml.j2          # Config MkDocs
├── envrc.j2               # Template .envrc
│
├── gitignore/             # .gitignore par technologie
│   ├── _common.j2         # Base commune
│   ├── python.j2
│   ├── node.j2
│   ├── terraform.j2
│   ├── ansible.j2
│   ├── docker.j2
│   ├── go.j2
│   ├── rust.j2
│   ├── java.j2
│   └── ide.j2
│
├── precommit/             # pre-commit par technologie
│   ├── _header.j2         # En-tete YAML
│   ├── python.j2
│   ├── node.j2
│   ├── terraform.j2
│   ├── ansible.j2
│   ├── go.j2
│   ├── rust.j2
│   └── java.j2
│
└── commands/              # Commandes Claude Code
    ├── quality.md.j2
    ├── commit.md.j2
    └── lint.md.j2
```

## Contexte de Template

Variables disponibles dans tous les templates :

```python
context = {
    "project_name": "my-project",           # Nom du projet (slug)
    "project_name_snake": "my_project",     # Nom en snake_case
    "project_type": "python-cli",           # Type de projet
    "project_type_display": "Python CLI",   # Nom affichable
    "description": "Description du projet",
    "year": 2024,                           # Annee courante
    "python_version": "3.10",               # Version Python
    "use_direnv": True,                     # direnv active
}
```

## Syntaxe Jinja2

### Variables

```jinja
Nom du projet : {{ project_name }}
Description : {{ description }}
```

### Conditions

```jinja
{% if project_type == "python-cli" %}
[project.scripts]
{{ project_name }} = "{{ project_name_snake }}.cli:main"
{% endif %}

{% if use_direnv %}
# Variables chargees via direnv
{% endif %}
```

### Boucles

```jinja
{% for tech in technologies %}
- {{ tech }}
{% endfor %}
```

### Filtres

```jinja
{{ project_name | upper }}        # MY-PROJECT
{{ project_name | replace("-", "_") }}  # my_project
```

## Exemples de Templates

### README.md.j2

```jinja
# {{ project_name }}

{{ description }}

## Installation

{% if project_type in ["python-cli", "python-lib"] %}
```bash
uv sync
```
{% elif project_type == "node-frontend" %}
```bash
npm install
```
{% endif %}

## Usage

{% if project_type == "python-cli" %}
```bash
uv run {{ project_name }} --help
```
{% elif project_type == "node-frontend" %}
```bash
npm run dev
```
{% endif %}
```

### pyproject.toml.j2

```jinja
[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
readme = "README.md"
requires-python = ">={{ python_version }}"

{% if project_type == "python-cli" %}
[project.scripts]
{{ project_name }} = "{{ project_name_snake }}.cli:main"
{% endif %}

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{{ project_name_snake }}"]

[tool.ruff]
line-length = 88
target-version = "py{{ python_version | replace('.', '') }}"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP"]
```

### commands/quality.md.j2

```jinja
---
description: Quality Check
---

## Quality Check

Run quality checks for {{ project_name }}.

{% if project_type == "python-cli" or project_type == "python-lib" %}
```bash
uvx ruff check src/
uvx ruff format --check src/
uv run pytest
```
{% elif project_type == "node-frontend" %}
```bash
npm run lint
npm run format:check
npm test
```
{% endif %}
```

## Composition de Templates

### .gitignore

Le `.gitignore` est compose de plusieurs templates :

```python
# Dans init_cmd.py
gitignore_content = env.get_template("gitignore/_common.j2").render()

for tech in technologies:
    gitignore_content += env.get_template(f"gitignore/{tech}.j2").render()
```

### .pre-commit-config.yaml

```python
precommit_content = env.get_template("precommit/_header.j2").render()

for tech in technologies:
    if tech != "ide":
        precommit_content += env.get_template(f"precommit/{tech}.j2").render()
```

## Chargement des Templates

projinit utilise `PackageLoader` de Jinja2 :

```python
from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader("projinit", "templates"),
    keep_trailing_newline=True,  # Conserve les newlines finales
)

template = env.get_template("README.md.j2")
content = template.render(**context)
```

## Ajouter un Nouveau Template

### 1. Creer le fichier .j2

```bash
# templates/my_new_file.j2
```

```jinja
# {{ project_name }}

Contenu genere pour {{ project_type }}
```

### 2. Ajouter la generation

Dans `cli/init_cmd.py` :

```python
def _generate_common_files(...):
    # ...existant...

    # Mon nouveau fichier
    template = env.get_template("my_new_file.j2")
    (target_dir / "my_new_file.txt").write_text(template.render(**context))
```

### 3. Mettre a jour _get_files_for_type

```python
def _get_files_for_type(project_type: ProjectType) -> list[str]:
    common = [
        "README.md",
        "LICENSE",
        # ...
        "my_new_file.txt",  # Ajouter ici
    ]
```

## Templates Conditionnels par Type

Pour generer un fichier seulement pour certains types :

```python
def _generate_common_files(env, target_dir, context, project_type, ...):
    # ...

    # Fichier specifique Python
    if project_type in (ProjectType.PYTHON_CLI, ProjectType.PYTHON_LIB):
        template = env.get_template("python_specific.j2")
        (target_dir / "python_specific.txt").write_text(template.render(**context))
```

## Personnalisation Utilisateur

Via configuration :

```yaml
# ~/.config/projinit/config.yaml
templates:
  templates_dir: ~/.config/projinit/templates
  overrides:
    README.md.j2: ~/.config/projinit/templates/my-readme.j2
```

Les templates utilisateur sont prioritaires sur les templates par defaut.

## Bonnes Pratiques

1. **Nommage** : `nom_fichier.extension.j2` (ex: `README.md.j2`)

2. **Indentation** : Respecter l'indentation du format cible
   ```jinja
   [project]
   name = "{{ project_name }}"
   {% if project_type == "python-cli" %}
   [project.scripts]
   {{ project_name }} = "..."
   {% endif %}
   ```

3. **Whitespace** : Utiliser `{%-` et `-%}` pour controler les espaces
   ```jinja
   {%- if condition -%}
   contenu sans espaces avant/apres
   {%- endif -%}
   ```

4. **Commentaires** : Documenter les sections complexes
   ```jinja
   {# Configuration specifique aux projets CLI #}
   {% if project_type == "python-cli" %}
   ```

## Debugging

Tester un template :

```python
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("projinit", "templates"))
template = env.get_template("pyproject.toml.j2")

context = {
    "project_name": "test-project",
    "project_name_snake": "test_project",
    "project_type": "python-cli",
    "description": "Test description",
    "python_version": "3.10",
}

print(template.render(**context))
```
