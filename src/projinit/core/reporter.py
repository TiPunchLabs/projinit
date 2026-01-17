"""Report generation for projinit v2.0."""

import json
from typing import Literal

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from projinit.core.models import AuditReport, CheckLevel, CheckStatus

OutputFormat = Literal["text", "json", "markdown"]


class Reporter:
    """Generates audit reports in various formats."""

    def __init__(self, report: AuditReport, verbose: bool = False):
        """
        Initialize the reporter.

        Args:
            report: The audit report to format.
            verbose: Whether to include detailed information.
        """
        self.report = report
        self.verbose = verbose
        self.console = Console()

    def to_text(self) -> None:
        """Print a rich text report to the console."""
        # Header
        self.console.print()
        self.console.print(
            Panel(
                f"[bold]Project Audit Report[/bold]\n"
                f"Path: {self.report.project_path}\n"
                f"Type: {self.report.project_type.display_name}",
                title="projinit check",
                border_style="blue",
            )
        )

        # Results table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status", width=8)
        table.add_column("Level", width=12)
        table.add_column("Check", width=30)
        table.add_column("Message")

        for check in self.report.checks:
            status_icon = self._get_status_icon(check.status)
            level_style = self._get_level_style(check.level)

            table.add_row(
                status_icon,
                f"[{level_style}]{check.level.value}[/{level_style}]",
                check.id,
                check.message,
            )

            # Show suggestion if verbose and check failed
            if self.verbose and check.suggestion and check.status == CheckStatus.FAILED:
                table.add_row("", "", "", f"[dim]Hint: {check.suggestion}[/dim]")

        self.console.print(table)

        # Summary
        self._print_summary()

    def to_json(self) -> str:
        """Generate a JSON report."""
        data = {
            "project_path": str(self.report.project_path),
            "project_type": self.report.project_type.value,
            "score": round(self.report.score, 1),
            "is_compliant": self.report.is_compliant,
            "summary": {
                "passed": self.report.passed_count,
                "failed": self.report.failed_count,
                "warnings": self.report.warning_count,
                "total": self.report.total_count,
            },
            "checks": [
                {
                    "id": c.id,
                    "status": c.status.value,
                    "level": c.level.value,
                    "message": c.message,
                    "suggestion": c.suggestion,
                    "file_path": str(c.file_path) if c.file_path else None,
                }
                for c in self.report.checks
            ],
        }
        return json.dumps(data, indent=2)

    def to_markdown(self) -> str:
        """Generate a Markdown report."""
        lines = [
            "# Project Audit Report",
            "",
            f"**Path**: `{self.report.project_path}`",
            f"**Type**: {self.report.project_type.display_name}",
            f"**Score**: {self.report.score:.1f}%",
            f"**Status**: {'Compliant' if self.report.is_compliant else 'Non-Compliant'}",
            "",
            "## Results",
            "",
            "| Status | Level | Check | Message |",
            "|--------|-------|-------|---------|",
        ]

        for check in self.report.checks:
            status_emoji = self._get_status_emoji(check.status)
            lines.append(
                f"| {status_emoji} | {check.level.value} | {check.id} | {check.message} |"
            )

        lines.extend(
            [
                "",
                "## Summary",
                "",
                f"- Passed: {self.report.passed_count}",
                f"- Failed: {self.report.failed_count}",
                f"- Warnings: {self.report.warning_count}",
                f"- Total: {self.report.total_count}",
            ]
        )

        return "\n".join(lines)

    def _print_summary(self) -> None:
        """Print the summary panel."""
        score = self.report.score
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"

        status = "COMPLIANT" if self.report.is_compliant else "NON-COMPLIANT"
        status_color = "green" if self.report.is_compliant else "red"

        summary = (
            f"[bold {score_color}]Score: {score:.1f}%[/bold {score_color}]\n\n"
            f"Passed: [green]{self.report.passed_count}[/green] | "
            f"Failed: [red]{self.report.failed_count}[/red] | "
            f"Warnings: [yellow]{self.report.warning_count}[/yellow]\n\n"
            f"Status: [bold {status_color}]{status}[/bold {status_color}]"
        )

        self.console.print()
        self.console.print(Panel(summary, title="Summary", border_style=status_color))

        # Show next steps if non-compliant
        if not self.report.is_compliant:
            self.console.print()
            self.console.print(
                "[dim]Run 'projinit update' to fix issues automatically[/dim]"
            )

    def _get_status_icon(self, status: CheckStatus) -> str:
        """Get a colored icon for the status."""
        icons = {
            CheckStatus.PASSED: "[green]PASS[/green]",
            CheckStatus.FAILED: "[red]FAIL[/red]",
            CheckStatus.WARNING: "[yellow]WARN[/yellow]",
            CheckStatus.SKIPPED: "[dim]SKIP[/dim]",
        }
        return icons.get(status, "[dim]?[/dim]")

    def _get_status_emoji(self, status: CheckStatus) -> str:
        """Get an emoji for the status (for markdown)."""
        emojis = {
            CheckStatus.PASSED: "PASS",
            CheckStatus.FAILED: "FAIL",
            CheckStatus.WARNING: "WARN",
            CheckStatus.SKIPPED: "SKIP",
        }
        return emojis.get(status, "?")

    def _get_level_style(self, level: CheckLevel) -> str:
        """Get a rich style for the level."""
        styles = {
            CheckLevel.REQUIRED: "red",
            CheckLevel.RECOMMENDED: "yellow",
            CheckLevel.OPTIONAL: "dim",
        }
        return styles.get(level, "white")
