"""Check command for projinit v2.0."""

import argparse
import sys
from pathlib import Path

from rich.console import Console

from projinit.core.checker import Checker
from projinit.core.detector import detect_project_type
from projinit.core.models import ProjectType
from projinit.core.reporter import Reporter

console = Console()


def add_check_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the check subcommand to the parser."""
    check_parser = subparsers.add_parser(
        "check",
        help="Audit project conformity against standards",
        description="Check if a project conforms to defined standards and best practices.",
    )
    check_parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Path to the project to check (default: current directory)",
    )
    check_parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[pt.value for pt in ProjectType if pt != ProjectType.UNKNOWN],
        help="Force project type (auto-detected if not specified)",
    )
    check_parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)",
    )
    check_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed information and suggestions",
    )
    check_parser.set_defaults(func=run_check)


def run_check(args: argparse.Namespace) -> int:
    """
    Run the check command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 = compliant, 1 = non-compliant, 2 = error).
    """
    project_path = Path(args.path).resolve()

    # Validate path
    if not project_path.is_dir():
        console.print(f"[red]Error: {project_path} is not a directory[/red]")
        return 2

    # Detect or use specified project type
    if args.type:
        project_type = ProjectType(args.type)
        if args.verbose:
            console.print(
                f"[dim]Using specified project type: {project_type.display_name}[/dim]"
            )
    else:
        detection = detect_project_type(project_path)
        project_type = detection.project_type

        if args.verbose:
            console.print(
                f"[dim]Detected project type: {project_type.display_name} "
                f"(confidence: {detection.confidence:.0%})[/dim]"
            )
            if detection.markers_found:
                console.print(
                    f"[dim]Markers found: {', '.join(detection.markers_found)}[/dim]"
                )

        if project_type == ProjectType.UNKNOWN:
            console.print("[yellow]Warning: Could not detect project type[/yellow]")
            console.print("[dim]Use --type to specify the project type manually[/dim]")
            return 2

    # Run checks
    checker = Checker(project_path, project_type)
    report = checker.run_checks()

    # Generate output
    reporter = Reporter(report, verbose=args.verbose)

    if args.format == "json":
        print(reporter.to_json())
    elif args.format == "markdown":
        print(reporter.to_markdown())
    else:
        reporter.to_text()

    # Return appropriate exit code
    return 0 if report.is_compliant else 1


def main() -> None:
    """Standalone entry point for check command."""
    parser = argparse.ArgumentParser(
        prog="projinit check",
        description="Check project conformity against standards",
    )
    # Add arguments directly (without subparser)
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=".",
        help="Path to the project to check (default: current directory)",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[pt.value for pt in ProjectType if pt != ProjectType.UNKNOWN],
        help="Force project type (auto-detected if not specified)",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed information and suggestions",
    )

    args = parser.parse_args()
    sys.exit(run_check(args))


if __name__ == "__main__":
    main()
