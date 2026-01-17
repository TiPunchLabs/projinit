"""Update command for projinit v2.0."""

import argparse
import sys
from pathlib import Path

import questionary
from rich.console import Console
from rich.table import Table

from projinit.core.checker import Checker
from projinit.core.detector import detect_project_type
from projinit.core.models import ActionType, ProjectType
from projinit.core.updater import Updater

console = Console()


def add_update_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the update subcommand to the parser."""
    update_parser = subparsers.add_parser(
        "update",
        help="Update project to conform to standards",
        description="Automatically fix conformity issues by adding missing files and configurations.",
    )
    update_parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Path to the project to update (default: current directory)",
    )
    update_parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[pt.value for pt in ProjectType if pt != ProjectType.UNKNOWN],
        help="Force project type (auto-detected if not specified)",
    )
    update_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    update_parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Confirm each change before applying",
    )
    update_parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files before modifying",
    )
    update_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed information",
    )
    update_parser.set_defaults(func=run_update)


def run_update(args: argparse.Namespace) -> int:
    """
    Run the update command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 = success, 1 = partial success, 2 = error).
    """
    project_path = Path(args.path).resolve()

    # Validate path
    if not project_path.is_dir():
        console.print(f"[red]Error: {project_path} is not a directory[/red]")
        return 2

    # Detect or use specified project type
    if args.type:
        project_type = ProjectType(args.type)
    else:
        detection = detect_project_type(project_path)
        project_type = detection.project_type

        if project_type == ProjectType.UNKNOWN:
            console.print("[yellow]Warning: Could not detect project type[/yellow]")
            console.print("[dim]Use --type to specify the project type manually[/dim]")
            return 2

    if args.verbose:
        console.print(f"[dim]Project type: {project_type.display_name}[/dim]")

    # First, run checks to identify issues
    console.print("[bold]Analyzing project...[/bold]")
    checker = Checker(project_path, project_type)
    report = checker.run_checks()

    if report.is_compliant:
        console.print("[green]Project is already compliant. No updates needed.[/green]")
        return 0

    # Generate update actions
    updater = Updater(
        project_path,
        project_type,
        dry_run=args.dry_run,
        create_backup=not args.no_backup,
    )
    actions = updater.generate_actions(report)

    if not actions:
        console.print("[yellow]No automatic fixes available for the detected issues.[/yellow]")
        console.print("[dim]Some issues may require manual intervention.[/dim]")
        return 1

    # Display planned actions
    _display_actions(actions, args.dry_run)

    if args.dry_run:
        console.print()
        console.print("[dim]Dry run - no changes made[/dim]")
        return 0

    # Interactive mode: confirm each action
    if args.interactive:
        actions = _filter_actions_interactive(actions)
        if not actions:
            console.print("[dim]No actions selected[/dim]")
            return 0

    # Apply actions
    console.print()
    console.print("[bold]Applying updates...[/bold]")

    applied = updater.apply_actions(actions)

    # Report results
    console.print()
    if len(applied) == len(actions):
        console.print(f"[green]Successfully applied {len(applied)} update(s)[/green]")
        return 0
    elif applied:
        console.print(
            f"[yellow]Applied {len(applied)} of {len(actions)} updates[/yellow]"
        )
        return 1
    else:
        console.print("[red]No updates could be applied[/red]")
        return 2


def _display_actions(actions: list, dry_run: bool) -> None:
    """Display the planned actions."""
    title = "Planned updates" if dry_run else "Updates to apply"
    console.print()
    console.print(f"[bold]{title}:[/bold]")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Action", width=10)
    table.add_column("Target")
    table.add_column("Description")

    action_styles = {
        ActionType.CREATE: "[green]CREATE[/green]",
        ActionType.MODIFY: "[yellow]MODIFY[/yellow]",
        ActionType.MERGE: "[blue]MERGE[/blue]",
        ActionType.SKIP: "[dim]SKIP[/dim]",
    }

    for action in actions:
        action_str = action_styles.get(action.action_type, str(action.action_type.value))
        target = str(action.target.relative_to(action.target.parent.parent))
        table.add_row(action_str, target, action.description)

    console.print(table)


def _filter_actions_interactive(actions: list) -> list:
    """Filter actions through interactive confirmation."""
    filtered = []

    console.print()
    for action in actions:
        target = action.target.name
        action_type = action.action_type.value.upper()

        confirm = questionary.confirm(
            f"[{action_type}] {target}: {action.description}?",
            default=True,
        ).ask()

        if confirm is None:
            # User cancelled
            return []
        if confirm:
            filtered.append(action)

    return filtered


def main() -> None:
    """Standalone entry point for update command."""
    parser = argparse.ArgumentParser(
        prog="projinit update",
        description="Update project to conform to standards",
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Path to the project to update (default: current directory)",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[pt.value for pt in ProjectType if pt != ProjectType.UNKNOWN],
        help="Force project type (auto-detected if not specified)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Confirm each change before applying",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files before modifying",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed information",
    )

    args = parser.parse_args()
    sys.exit(run_update(args))


if __name__ == "__main__":
    main()
