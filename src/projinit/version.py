"""Affichage des informations de version."""

import platform
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from projinit import __version__

ASCII_ART = """\
██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   """

TAGLINE = "Project Scaffolding with Terraform + GitHub"


def get_system_info() -> dict[str, str]:
    """Récupère les informations système."""
    return {
        "CLI Version": __version__,
        "Python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Platform": platform.system(),
        "Architecture": platform.machine(),
        "OS Version": platform.release(),
    }


def display_version_banner() -> None:
    """Affiche le banner de version avec ASCII art et informations système."""
    console = Console()

    # ASCII Art sans centrage (les caractères Unicode ne sont pas bien gérés)
    console.print()
    console.print(ASCII_ART.strip(), style="bold blue")
    console.print(f"  {TAGLINE}", style="dim")
    console.print()

    # Table des informations
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="dim", justify="right")
    table.add_column("Value", style="cyan")

    for key, value in get_system_info().items():
        table.add_row(key, value)

    # Panel contenant la table
    panel = Panel(
        table,
        title="projinit CLI Information",
        border_style="blue",
        padding=(1, 4),
    )

    console.print(panel)
    console.print()
