# Commandes CLI

## Vue d'Ensemble

projinit expose 4 commandes principales :

| Commande | Description |
|----------|-------------|
| `projinit check` | Auditer la conformite d'un projet |
| `projinit new` | Creer un nouveau projet |
| `projinit update` | Corriger les non-conformites |
| `projinit config` | Gerer la configuration |

## Architecture CLI

```
main_cli.py                 # Point d'entree, dispatch
├── parse_args()            # Parser argparse principal
└── main()                  # Logique de dispatch

cli/
├── check_cmd.py            # projinit check
│   ├── add_check_parser()
│   └── run_check()
├── init_cmd.py             # projinit new
│   ├── add_init_parser()
│   └── run_init()
├── update_cmd.py           # projinit update
│   ├── add_update_parser()
│   └── run_update()
└── config_cmd.py           # projinit config
    ├── add_config_parser()
    └── run_config()
```

## Commande `check`

### Usage

```bash
# Audit du projet courant
projinit check

# Audit d'un projet specifique
projinit check /path/to/project

# Forcer le type
projinit check -t python-cli

# Format de sortie
projinit check -f json
projinit check -f markdown > report.md

# Mode verbose
projinit check -v
```

### Arguments

| Argument | Description |
|----------|-------------|
| `path` | Chemin du projet (defaut: `.`) |
| `-t, --type` | Type de projet (auto-detecte si omis) |
| `-f, --format` | Format: text, json, markdown |
| `-v, --verbose` | Afficher details (temps, fichiers) |

### Implementation

```python
# cli/check_cmd.py

def add_check_parser(subparsers):
    parser = subparsers.add_parser("check", help="Audit project")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("-t", "--type", choices=[...])
    parser.add_argument("-f", "--format", default="text")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.set_defaults(func=run_check)

def run_check(args) -> int:
    project_path = Path(args.path).resolve()

    # Detection ou type force
    if args.type:
        project_type = ProjectType(args.type)
    else:
        result = detect(project_path)
        project_type = result.project_type

    # Charger standards
    checks = load_standards(project_type)

    # Executer checks
    results = checker.run_checks(project_path, checks)

    # Generer rapport
    report = AuditReport(
        project_path=project_path,
        project_type=project_type,
        checks=results,
    )

    # Afficher selon format
    if args.format == "json":
        print(reporter.to_json(report))
    elif args.format == "markdown":
        print(reporter.to_markdown(report))
    else:
        reporter.display(report)

    return 0 if report.is_compliant else 1
```

## Commande `new`

### Usage

```bash
# Creation interactive
projinit new mon-projet

# Non-interactif
projinit new mon-projet -t python-cli -d "Description" -y

# Avec direnv
projinit new mon-projet --direnv

# Dans un dossier specifique
projinit new mon-projet -p /path/to/parent
```

### Arguments

| Argument | Description |
|----------|-------------|
| `name` | Nom du projet (slug-case) |
| `-t, --type` | Type de projet |
| `-d, --description` | Description |
| `-p, --path` | Repertoire parent |
| `-y, --yes` | Skip confirmations |
| `--direnv` | Activer direnv + pass |
| `--no-direnv` | Desactiver direnv |
| `--no-git` | Ne pas initialiser git |

### Flux

```
1. Collecter infos (args ou questions)
   ├── Nom du projet
   ├── Type de projet
   ├── Description
   └── Options (direnv, etc.)

2. Valider
   ├── Nom valide (slug-case)
   ├── Repertoire n'existe pas
   └── Prerequis (direnv, pass si active)

3. Afficher resume + confirmation

4. Generer
   ├── Fichiers communs (README, LICENSE, etc.)
   ├── Fichiers specifiques au type
   ├── .claude/commands/
   └── .envrc si direnv

5. Initialiser git

6. Afficher next steps
```

### Implementation

```python
# cli/init_cmd.py

def run_init(args) -> int:
    # Collecter
    project_name = args.name or _ask_project_name()
    project_type = ProjectType(args.type) if args.type else _ask_project_type()
    description = args.description or _ask_description(project_name)
    use_direnv = args.direnv or (not args.no_direnv and _ask_direnv())

    # Valider
    if not _is_valid_slug(project_name):
        console.print("[red]Invalid name[/red]")
        return 1

    target_dir = Path(args.path).resolve() / project_name
    if target_dir.exists():
        console.print("[red]Directory exists[/red]")
        return 1

    # Confirmer
    _display_summary(...)
    if not args.yes and not questionary.confirm("Create?").ask():
        return 1

    # Generer
    _generate_project(project_name, project_type, description, target_dir, use_direnv)

    # Git
    if not args.no_git:
        _init_git(target_dir)

    # direnv
    if use_direnv:
        _allow_direnv(target_dir)

    _display_next_steps(...)
    return 0
```

## Commande `update`

### Usage

```bash
# Correction automatique
projinit update

# Mode dry-run
projinit update --dry-run

# Mode interactif
projinit update --interactive

# Sans backup
projinit update --no-backup
```

### Arguments

| Argument | Description |
|----------|-------------|
| `path` | Chemin du projet |
| `--dry-run` | Afficher sans appliquer |
| `--interactive` | Confirmer chaque action |
| `--no-backup` | Ne pas creer de backup |

### Flux

```
1. Executer check
2. Collecter les checks echoues
3. Pour chaque check avec template:
   a. Planifier l'action (CREATE/MODIFY)
   b. Si --dry-run: afficher seulement
   c. Si --interactive: demander confirmation
   d. Appliquer la correction
4. Afficher resume
```

## Commande `config`

### Usage

```bash
# Voir configuration
projinit config show

# Voir chemins
projinit config paths

# Initialiser configuration
projinit config init --global
projinit config init --local
```

### Sous-commandes

| Sous-commande | Description |
|---------------|-------------|
| `show` | Afficher configuration fusionnee |
| `paths` | Afficher chemins des fichiers config |
| `init` | Creer fichier de configuration |

## Ajouter une Nouvelle Commande

### 1. Creer le module

```python
# cli/my_cmd.py

import argparse
from rich.console import Console

console = Console()

def add_my_parser(subparsers):
    """Ajouter la sous-commande."""
    parser = subparsers.add_parser(
        "mycommand",
        help="Description courte",
        description="Description longue",
    )
    parser.add_argument("arg1", help="Premier argument")
    parser.add_argument("-o", "--option", help="Une option")
    parser.set_defaults(func=run_my_command)

def run_my_command(args) -> int:
    """Executer la commande."""
    console.print(f"Running with {args.arg1}")

    # Logique...

    return 0  # Code de sortie
```

### 2. Enregistrer dans main_cli.py

```python
from projinit.cli.my_cmd import add_my_parser, run_my_command

def parse_args():
    # ...
    subparsers = parser.add_subparsers(dest="command")

    # Commandes existantes
    add_check_parser(subparsers)
    add_init_parser(subparsers)
    # ...

    # Nouvelle commande
    add_my_parser(subparsers)

def main():
    args = parse_args()

    if args.command == "mycommand":
        exit_code = run_my_command(args)
        sys.exit(exit_code)
```

## Conventions

### Codes de Sortie

| Code | Signification |
|------|---------------|
| 0 | Succes |
| 1 | Erreur generale |
| 2 | Erreur d'arguments |

### Affichage

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Messages
console.print("[green]Success[/green]")
console.print("[red]Error[/red]")
console.print("[yellow]Warning[/yellow]")
console.print("[dim]Info[/dim]")

# Panel
console.print(Panel.fit("[bold]Title[/bold]"))

# Status
with console.status("[bold blue]Processing...[/bold blue]"):
    do_work()
```

### Questions Interactives

```python
import questionary

# Texte
name = questionary.text("Project name:").ask()

# Selection
type = questionary.select(
    "Type:",
    choices=[
        questionary.Choice("Option A", value="a"),
        questionary.Choice("Option B", value="b"),
    ]
).ask()

# Confirmation
ok = questionary.confirm("Proceed?", default=True).ask()

# Checkbox
techs = questionary.checkbox(
    "Technologies:",
    choices=["Python", "Node.js", "Go"]
).ask()
```

## Tests

```python
def test_check_command(tmp_path, monkeypatch):
    # Setup projet
    project = tmp_path / "test-project"
    project.mkdir()
    (project / "README.md").touch()

    # Mock sys.argv
    monkeypatch.setattr(
        sys, "argv",
        ["projinit", "check", str(project)]
    )

    # Run
    from projinit.main_cli import main
    main()

    # Assertions via capfd pour stdout
```
