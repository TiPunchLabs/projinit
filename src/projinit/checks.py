"""Vérifications système (direnv, pass, etc.)."""

import shutil
import subprocess
from pathlib import Path

from rich.console import Console

console = Console()


def check_directory_not_exists(path: Path) -> bool:
    """Vérifie que le dossier cible n'existe pas déjà."""
    if path.exists():
        console.print(f"[red]Le dossier '{path}' existe déjà[/red]")
        return False
    return True


def check_direnv_installed() -> bool:
    """Vérifie que direnv est installé."""
    if shutil.which("direnv") is None:
        console.print("[red]direnv n'est pas installé[/red]")
        console.print("[dim]Installez-le avec : sudo apt install direnv[/dim]")
        return False
    return True


def check_pass_installed() -> bool:
    """Vérifie que pass est installé."""
    if shutil.which("pass") is None:
        console.print("[red]pass n'est pas installé[/red]")
        console.print("[dim]Installez-le avec : sudo apt install pass[/dim]")
        return False
    return True


def check_pass_secret_exists(secret_path: str) -> bool:
    """Vérifie que le secret existe dans pass."""
    try:
        result = subprocess.run(
            ["pass", secret_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            console.print(f"[red]Le secret '{secret_path}' n'existe pas dans pass[/red]")
            console.print(f"[dim]Créez-le avec : pass insert {secret_path}[/dim]")
            return False
        return True
    except Exception:
        console.print("[red]Erreur lors de la vérification du secret pass[/red]")
        return False


def run_direnv_checks(pass_secret_path: str = "github/terraform-token") -> bool:
    """Exécute toutes les vérifications pour direnv."""
    if not check_direnv_installed():
        return False
    if not check_pass_installed():
        return False
    if not check_pass_secret_exists(pass_secret_path):
        return False
    return True
