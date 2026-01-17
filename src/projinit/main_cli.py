"""Logique interactive CLI."""

import argparse
import os
import sys
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel

from projinit import __version__
from projinit.checks import check_directory_not_exists, run_direnv_checks
from projinit.config import Config, load_config
from projinit.generator import (
    ProjectConfig,
    allow_direnv,
    generate_project,
    init_git_repository,
)
from projinit.cli.check_cmd import add_check_parser, run_check
from projinit.validators import validate_slug
from projinit.version import display_version_banner

console = Console()


class VersionAction(argparse.Action):
    """Action personnalisée pour afficher le banner de version stylisé."""

    def __init__(
        self,
        option_strings: list[str],
        dest: str = argparse.SUPPRESS,
        default: str = argparse.SUPPRESS,
        help: str = "Affiche les informations de version détaillées",  # noqa: A002
    ) -> None:
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | None,
        option_string: str | None = None,
    ) -> None:
        display_version_banner()
        parser.exit()


def parse_args() -> argparse.Namespace:
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        prog="projinit",
        description="CLI pour initialiser, auditer et mettre à jour des projets selon des standards définis",
    )
    parser.add_argument(
        "-v",
        "--version",
        action=VersionAction,
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=None,
        metavar="PATH",
        help="Chemin de destination pour le projet (défaut: dossier courant)",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "version", help="Affiche les informations de version détaillées"
    )
    subparsers.add_parser(
        "init", help="Initialise un nouveau projet (mode interactif)"
    )
    add_check_parser(subparsers)

    return parser.parse_args()


def _get_first_existing_parent(path: Path) -> Path:
    """Trouve le premier parent existant pour vérifier les permissions."""
    current = path.resolve()
    while not current.exists():
        current = current.parent
    return current


def resolve_output_path(path_arg: str | None) -> Path:
    """Résout et valide le chemin de destination.

    Args:
        path_arg: Le chemin fourni via --path, ou None pour le dossier courant.

    Returns:
        Le chemin résolu et validé.

    Raises:
        ValueError: Si le chemin pointe vers un fichier existant.
        PermissionError: Si pas de permission d'écriture.
    """
    if not path_arg or path_arg.strip() == "":
        return Path.cwd()

    resolved = Path(path_arg).expanduser().resolve()

    if resolved.is_file():
        raise ValueError(f"Le chemin '{resolved}' est un fichier, pas un dossier")

    first_existing = _get_first_existing_parent(resolved)
    if not os.access(first_existing, os.W_OK):
        raise PermissionError(f"Pas de permission d'écriture sur '{first_existing}'")

    return resolved


def display_header() -> None:
    """Affiche l'en-tête du CLI."""
    console.print()
    console.print(
        Panel.fit(
            f"[bold]projinit[/bold] [dim]v{__version__}[/dim]\n"
            "[dim]Générateur de projet avec Terraform GitHub[/dim]",
            border_style="blue",
        )
    )
    console.print()


def ask_project_name() -> str | None:
    """Demande le nom du projet."""
    return questionary.text(
        "Nom du projet :",
        validate=lambda val: validate_slug(val)
        if isinstance(validate_slug(val), bool)
        else validate_slug(val),
    ).ask()


def ask_description(project_name: str) -> str:
    """Demande la description du projet."""
    description = questionary.text(
        "Description :",
        default="",
    ).ask()

    if description is None:
        return ""

    return description if description.strip() else f"Projet {project_name}"


def ask_owner(config: Config) -> str | None:
    """Demande le propriétaire GitHub."""
    choices = [
        questionary.Choice(owner.label, value=owner.name) for owner in config.owners
    ]

    if not choices:
        console.print("[red]Aucun owner configuré[/red]")
        return None

    return questionary.select(
        "Owner GitHub :",
        choices=choices,
        default=config.owners[0].name if config.owners else None,
    ).ask()


def ask_visibility(config: Config) -> str | None:
    """Demande la visibilité du dépôt."""
    return questionary.select(
        "Visibilité :",
        choices=[
            questionary.Choice("public", value="public"),
            questionary.Choice("private", value="private"),
        ],
        default=config.defaults.visibility,
    ).ask()


def ask_direnv(config: Config) -> bool | None:
    """Demande si direnv doit être activé."""
    return questionary.confirm(
        "Activer direnv + pass ?",
        default=config.defaults.use_direnv,
    ).ask()


def ask_technologies() -> list[str] | None:
    """Demande les technologies utilisées dans le projet."""
    return questionary.checkbox(
        "Technologies du projet :",
        choices=[
            # Langages
            questionary.Separator("── Langages ──"),
            questionary.Choice("Python", value="python"),
            questionary.Choice("Node.js", value="node"),
            questionary.Choice("Go", value="go"),
            questionary.Choice("Rust", value="rust"),
            questionary.Choice("Java/Kotlin", value="java"),
            # Front-end
            questionary.Separator("── Front-end ──"),
            questionary.Choice("HTML/CSS", value="html"),
            questionary.Choice("React", value="react"),
            questionary.Choice("Vue.js", value="vue"),
            questionary.Choice("Angular", value="angular"),
            questionary.Choice("Svelte", value="svelte"),
            questionary.Choice("Next.js/Nuxt.js", value="nextjs"),
            # Infrastructure
            questionary.Separator("── Infrastructure ──"),
            questionary.Choice("Terraform", value="terraform", checked=True),
            questionary.Choice("Pulumi", value="pulumi"),
            questionary.Choice("Kubernetes/Helm", value="kubernetes"),
            # Conteneurs
            questionary.Separator("── Conteneurs ──"),
            questionary.Choice("Docker", value="docker"),
            # Automation
            questionary.Separator("── Automation ──"),
            questionary.Choice("Ansible", value="ansible"),
            questionary.Choice("Shell/Bash", value="shell"),
            # Outils
            questionary.Separator("── Outils ──"),
            questionary.Choice("IDE (VSCode/JetBrains)", value="ide"),
            questionary.Choice("GitHub Actions", value="github-actions"),
        ],
    ).ask()


def display_summary(project_config: ProjectConfig, target_dir: Path) -> None:
    """Affiche le récapitulatif de la configuration."""
    console.print()
    console.print("[bold]Récapitulatif :[/bold]")
    console.print(f"  Nom        : [cyan]{project_config.name}[/cyan]")
    console.print(f"  Chemin     : [cyan]{target_dir}[/cyan]")
    console.print(f"  Description: [cyan]{project_config.description}[/cyan]")
    console.print(f"  Owner      : [cyan]{project_config.owner}[/cyan]")
    console.print(f"  Visibilité : [cyan]{project_config.visibility}[/cyan]")
    console.print(
        f"  Direnv     : [cyan]{'oui' if project_config.use_direnv else 'non'}[/cyan]"
    )
    if project_config.technologies:
        tech_labels = {
            "python": "Python",
            "node": "Node.js",
            "go": "Go",
            "rust": "Rust",
            "java": "Java/Kotlin",
            "html": "HTML/CSS",
            "react": "React",
            "vue": "Vue.js",
            "angular": "Angular",
            "svelte": "Svelte",
            "nextjs": "Next.js/Nuxt.js",
            "terraform": "Terraform",
            "pulumi": "Pulumi",
            "kubernetes": "Kubernetes/Helm",
            "docker": "Docker",
            "ansible": "Ansible",
            "shell": "Shell/Bash",
            "ide": "IDE",
            "github-actions": "GitHub Actions",
        }
        tech_display = ", ".join(
            tech_labels.get(t, t) for t in project_config.technologies
        )
        console.print(f"  Technologies: [cyan]{tech_display}[/cyan]")
    console.print()


def display_next_steps(project_name: str, use_direnv: bool) -> None:
    """Affiche les prochaines étapes."""
    console.print()
    console.print("[bold]Prochaines étapes :[/bold]")
    console.print()
    console.print(f"  [dim]1.[/dim] cd {project_name}")
    if use_direnv:
        console.print("  [dim]2.[/dim] cd terraform && terraform init")
        console.print("  [dim]3.[/dim] terraform plan")
        console.print("  [dim]4.[/dim] terraform apply")
    else:
        console.print("  [dim]2.[/dim] export TF_VAR_github_token=<votre-token>")
        console.print("  [dim]3.[/dim] cd terraform && terraform init")
        console.print("  [dim]4.[/dim] terraform plan")
        console.print("  [dim]5.[/dim] terraform apply")
    console.print()


def main() -> None:
    """Point d'entrée principal du CLI."""
    # Parser les arguments (gère --version automatiquement)
    args = parse_args()

    # Gérer la sous-commande version
    if args.command == "version":
        display_version_banner()
        return

    # Gérer la sous-commande check
    if args.command == "check":
        exit_code = run_check(args)
        sys.exit(exit_code)

    # Si init explicite ou pas de commande, lancer le mode interactif
    # Résoudre le chemin de destination
    try:
        base_path = resolve_output_path(args.path)
    except ValueError as e:
        console.print(f"[red]Erreur: {e}[/red]")
        sys.exit(1)
    except PermissionError as e:
        console.print(f"[red]Erreur: {e}[/red]")
        sys.exit(1)

    # Charger la configuration
    config = load_config()

    display_header()

    # Questions interactives
    project_name = ask_project_name()
    if project_name is None:
        console.print("[dim]Annulé[/dim]")
        sys.exit(1)

    description = ask_description(project_name)

    owner = ask_owner(config)
    if owner is None:
        console.print("[dim]Annulé[/dim]")
        sys.exit(1)

    visibility = ask_visibility(config)
    if visibility is None:
        console.print("[dim]Annulé[/dim]")
        sys.exit(1)

    use_direnv = ask_direnv(config)
    if use_direnv is None:
        console.print("[dim]Annulé[/dim]")
        sys.exit(1)

    technologies = ask_technologies()
    if technologies is None:
        console.print("[dim]Annulé[/dim]")
        sys.exit(1)

    # Vérifications
    target_dir = base_path / project_name

    if not check_directory_not_exists(target_dir):
        sys.exit(1)

    if use_direnv and not run_direnv_checks(config.pass_secret_path):
        sys.exit(1)

    # Créer la configuration du projet
    project_config = ProjectConfig(
        name=project_name,
        description=description,
        owner=owner,
        visibility=visibility,
        use_direnv=use_direnv,
        pass_secret_path=config.pass_secret_path,
        technologies=technologies,
    )

    display_summary(project_config, target_dir)

    # Confirmation
    confirm = questionary.confirm("Générer le projet ?", default=True).ask()
    if not confirm:
        console.print("[dim]Annulé[/dim]")
        sys.exit(1)

    # Génération
    console.print()
    with console.status("[bold blue]Génération du projet...[/bold blue]"):
        if not generate_project(project_config, target_dir):
            console.print("[red]Erreur lors de la génération du projet[/red]")
            sys.exit(1)

        if not init_git_repository(target_dir):
            console.print("[red]Erreur lors de l'initialisation git[/red]")
            sys.exit(1)

        if use_direnv and not allow_direnv(target_dir):
            console.print("[red]Erreur lors de l'autorisation direnv[/red]")
            sys.exit(1)

    console.print(f"[green]Projet '{project_name}' créé avec succès[/green]")

    display_next_steps(project_name, use_direnv)
