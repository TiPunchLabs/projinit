"""Config command for projinit v2.0."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from projinit.core.config import (
    GLOBAL_CONFIG_DIR,
    GLOBAL_CONFIG_FILE,
    LOCAL_CONFIG_FILE,
    generate_example_config,
    get_config_paths,
    load_config,
)

console = Console()


def add_config_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the config subcommand to the parser."""
    config_parser = subparsers.add_parser(
        "config",
        help="Manage projinit configuration",
        description="View and manage projinit configuration files.",
    )

    config_subparsers = config_parser.add_subparsers(dest="config_command")

    # config show
    show_parser = config_subparsers.add_parser(
        "show",
        help="Show current configuration",
    )
    show_parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=".",
        help="Project path for local config (default: current directory)",
    )

    # config init
    init_parser = config_subparsers.add_parser(
        "init",
        help="Create example configuration file",
    )
    init_parser.add_argument(
        "--global",
        dest="global_config",
        action="store_true",
        help="Create global config (~/.config/projinit/config.yaml)",
    )
    init_parser.add_argument(
        "--local",
        dest="local_config",
        action="store_true",
        help="Create local config (.projinit.yaml)",
    )
    init_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite existing config file",
    )

    # config paths
    config_subparsers.add_parser(
        "paths",
        help="Show configuration file paths",
    )

    config_parser.set_defaults(func=run_config)


def run_config(args: argparse.Namespace) -> int:
    """
    Run the config command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 = success, 1 = error).
    """
    if not hasattr(args, "config_command") or args.config_command is None:
        # No subcommand, show help
        console.print("[yellow]Usage: projinit config {show|init|paths}[/yellow]")
        return 1

    if args.config_command == "show":
        return _show_config(args)
    elif args.config_command == "init":
        return _init_config(args)
    elif args.config_command == "paths":
        return _show_paths()

    return 1


def _show_config(args: argparse.Namespace) -> int:
    """Show current configuration."""
    project_path = Path(args.path).resolve()
    config = load_config(project_path)

    console.print()
    console.print(
        Panel.fit(
            "[bold]Current Configuration[/bold]",
            border_style="blue",
        )
    )
    console.print()

    console.print(f"[dim]Source:[/dim] {config._source}")
    console.print()

    # Author
    console.print("[bold]Author:[/bold]")
    console.print(f"  Name:  {config.author.name or '[dim]not set[/dim]'}")
    console.print(f"  Email: {config.author.email or '[dim]not set[/dim]'}")
    console.print()

    # Defaults
    console.print("[bold]Defaults:[/bold]")
    console.print(f"  Python version: {config.python_version}")
    console.print(f"  License:        {config.default_license}")
    console.print()

    # Standards
    console.print("[bold]Standards customization:[/bold]")
    if config.standards.check_overrides:
        console.print("  Check overrides:")
        for check_id, level in config.standards.check_overrides.items():
            console.print(f"    {check_id}: {level}")
    else:
        console.print("  Check overrides: [dim]none[/dim]")

    if config.standards.disabled_checks:
        console.print(f"  Disabled checks: {', '.join(config.standards.disabled_checks)}")
    else:
        console.print("  Disabled checks: [dim]none[/dim]")

    if config.standards.extra_precommit_hooks:
        console.print(f"  Extra hooks: {len(config.standards.extra_precommit_hooks)} configured")
    else:
        console.print("  Extra hooks: [dim]none[/dim]")
    console.print()

    # Templates
    console.print("[bold]Templates:[/bold]")
    if config.templates.templates_dir:
        console.print(f"  Custom dir: {config.templates.templates_dir}")
    else:
        console.print("  Custom dir: [dim]not set[/dim]")

    if config.templates.overrides:
        console.print("  Overrides:")
        for template, path in config.templates.overrides.items():
            console.print(f"    {template}: {path}")
    else:
        console.print("  Overrides: [dim]none[/dim]")

    console.print()
    return 0


def _init_config(args: argparse.Namespace) -> int:
    """Create example configuration file."""
    example_content = generate_example_config()

    # Determine target
    if args.global_config:
        target_path = GLOBAL_CONFIG_FILE
        GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    elif args.local_config:
        target_path = Path.cwd() / LOCAL_CONFIG_FILE
    else:
        # Default to global
        target_path = GLOBAL_CONFIG_FILE
        GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Check if file exists
    if target_path.exists() and not args.force:
        console.print(f"[yellow]Config file already exists: {target_path}[/yellow]")
        console.print("[dim]Use --force to overwrite[/dim]")
        return 1

    # Write file
    target_path.write_text(example_content, encoding="utf-8")
    console.print(f"[green]Created config file: {target_path}[/green]")

    # Show content
    console.print()
    syntax = Syntax(example_content, "yaml", theme="monokai", line_numbers=True)
    console.print(syntax)

    return 0


def _show_paths() -> int:
    """Show configuration file paths."""
    paths = get_config_paths()

    console.print()
    console.print("[bold]Configuration file paths:[/bold]")
    console.print()

    for name, path in paths.items():
        exists = "[green]exists[/green]" if path.exists() else "[dim]not found[/dim]"
        console.print(f"  {name}: {path} ({exists})")

    console.print()
    console.print("[dim]Hint: Use 'projinit config init --global' to create global config[/dim]")
    console.print("[dim]      Use 'projinit config init --local' to create local config[/dim]")
    console.print()

    return 0


def main() -> None:
    """Standalone entry point."""
    parser = argparse.ArgumentParser(prog="projinit config", description="Manage configuration")
    subparsers = parser.add_subparsers(dest="config_command")

    show_parser = subparsers.add_parser("show", help="Show configuration")
    show_parser.add_argument("-p", "--path", type=str, default=".")

    init_parser = subparsers.add_parser("init", help="Create config file")
    init_parser.add_argument("--global", dest="global_config", action="store_true")
    init_parser.add_argument("--local", dest="local_config", action="store_true")
    init_parser.add_argument("-f", "--force", action="store_true")

    subparsers.add_parser("paths", help="Show config paths")

    args = parser.parse_args()
    sys.exit(run_config(args))


if __name__ == "__main__":
    main()
