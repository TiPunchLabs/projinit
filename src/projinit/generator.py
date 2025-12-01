"""Génération des fichiers du projet."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, PackageLoader
from rich.console import Console

console = Console()


@dataclass
class ProjectConfig:
    """Configuration du projet à générer."""

    name: str
    description: str
    owner: str
    visibility: str
    use_direnv: bool
    pass_secret_path: str = "github/terraform-token"


def get_template_env() -> Environment:
    """Retourne l'environnement Jinja2 avec les templates."""
    return Environment(
        loader=PackageLoader("projinit", "templates"),
        keep_trailing_newline=True,
    )


def generate_project(config: ProjectConfig, target_dir: Path) -> bool:
    """Génère la structure complète du projet."""
    env = get_template_env()

    # Créer le dossier principal
    target_dir.mkdir(parents=True, exist_ok=True)

    # Créer le dossier terraform
    terraform_dir = target_dir / "terraform"
    terraform_dir.mkdir(exist_ok=True)

    # Contexte pour les templates
    context = {
        "project_name": config.name,
        "description": config.description,
        "owner": config.owner,
        "visibility": config.visibility,
        "use_direnv": config.use_direnv,
        "pass_secret_path": config.pass_secret_path,
    }

    # Générer les fichiers racine
    root_files = [
        ("gitignore.j2", ".gitignore"),
        ("README.md.j2", "README.md"),
        ("LICENSE.j2", "LICENSE"),
    ]

    if config.use_direnv:
        root_files.append(("envrc.j2", ".envrc"))

    for template_name, output_name in root_files:
        template = env.get_template(template_name)
        content = template.render(**context)
        (target_dir / output_name).write_text(content)

    # Générer les fichiers Terraform
    terraform_files = [
        ("main.tf.j2", "main.tf"),
        ("variables.tf.j2", "variables.tf"),
        ("outputs.tf.j2", "outputs.tf"),
        ("versions.tf.j2", "versions.tf"),
        ("terraform.tfvars.j2", "terraform.tfvars"),
    ]

    for template_name, output_name in terraform_files:
        template = env.get_template(template_name)
        content = template.render(**context)
        (terraform_dir / output_name).write_text(content)

    return True


def init_git_repository(target_dir: Path) -> bool:
    """Initialise le dépôt git avec le premier commit."""
    try:
        # git init
        subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=target_dir,
            capture_output=True,
            check=True,
        )

        # git add .
        subprocess.run(
            ["git", "add", "."],
            cwd=target_dir,
            capture_output=True,
            check=True,
        )

        # git commit
        subprocess.run(
            ["git", "commit", "-m", "Initial commit - project scaffolding"],
            cwd=target_dir,
            capture_output=True,
            check=True,
        )

        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erreur lors de l'initialisation git : {e}[/red]")
        return False
