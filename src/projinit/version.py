"""Affichage des informations de version."""

from rich.console import Console
from rich.text import Text

from projinit import __version__

ASCII_ART = """\
██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝"""

TAGLINE = "Project Scaffolding with Terraform + GitHub"

DESCRIPTION = """\
  Générateur de structure projet avec configuration Terraform
  GitHub intégrée. Créez des projets prêts à déployer avec
  infrastructure as code en quelques secondes."""

FEATURES = [
    "Génération de structure projet avec Terraform GitHub",
    "Configuration automatique du provider GitHub",
    "Support direnv + pass pour les secrets",
    "Sélection des technologies (.gitignore adapté)",
    "Génération automatique de .pre-commit-config.yaml",
    "Chemin de sortie personnalisable",
]

USAGE_EXAMPLES = [
    ("projinit", "Menu interactif"),
    ("projinit -p ~/projets", "Spécifier le chemin de sortie"),
    ("projinit --help", "Afficher l'aide"),
]


def display_version_banner() -> None:
    """Affiche le banner de version avec ASCII art, description, features et usage."""
    console = Console()

    # ASCII Art
    console.print()
    console.print(ASCII_ART, style="bold blue")

    # Tagline centrée sous le banner
    tagline_text = Text(f"            {TAGLINE}", style="dim")
    console.print(tagline_text)
    console.print()

    # Version centrée
    version_text = Text(
        f"                        CLI v{__version__}", style="bold cyan"
    )
    console.print(version_text)
    console.print()

    # Section Description
    console.print("Description:", style="bold")
    console.print(DESCRIPTION, style="dim")
    console.print()

    # Section Features
    console.print("Features:", style="bold")
    for feature in FEATURES:
        console.print(f"  - {feature}", style="dim")
    console.print()

    # Section Usage
    console.print("Usage:", style="bold")
    for cmd, desc in USAGE_EXAMPLES:
        # Aligner les commandes et descriptions
        console.print(f"  {cmd:<24} # {desc}", style="dim")
    console.print()
