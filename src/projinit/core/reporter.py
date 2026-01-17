"""Report generation for projinit v2.0."""

import json
from typing import Literal

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

from projinit.core.models import AuditReport, CheckLevel, CheckResult, CheckStatus

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
        self._print_header()

        # Group checks by level
        self._print_checks_by_level()

        # Score progress bar
        self._print_score_bar()

        # Summary
        self._print_summary()

        # Suggestions panel (if there are failures)
        if self.report.failed_checks:
            self._print_suggestions()

        # Verbose info
        if self.verbose:
            self._print_verbose_info()

    def _print_header(self) -> None:
        """Print the report header."""
        self.console.print(
            Panel(
                f"[bold]Project Audit Report[/bold]\n"
                f"Path: {self.report.project_path}\n"
                f"Type: {self.report.project_type.display_name}",
                title="projinit check",
                border_style="blue",
            )
        )

    def _print_checks_by_level(self) -> None:
        """Print checks grouped by level."""
        checks_by_level = self.report.checks_by_level

        level_info = [
            (CheckLevel.REQUIRED, "Required", "red"),
            (CheckLevel.RECOMMENDED, "Recommended", "yellow"),
            (CheckLevel.OPTIONAL, "Optional", "dim"),
        ]

        for level, title, style in level_info:
            checks = checks_by_level.get(level, [])
            if not checks:
                continue

            self.console.print()
            self.console.print(f"[bold {style}]{title} Checks[/bold {style}]")

            table = Table(
                show_header=True, header_style="bold", box=None, padding=(0, 1)
            )
            table.add_column("", width=6)
            table.add_column("Check", width=28)
            table.add_column("Result")

            for check in checks:
                status_icon = self._get_status_icon(check.status)
                table.add_row(status_icon, check.id, check.message)

            self.console.print(table)

    def _print_score_bar(self) -> None:
        """Print a visual progress bar for the score."""
        score = self.report.score
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"

        self.console.print()

        # Create progress bar
        with Progress(
            TextColumn("[bold]Conformity Score"),
            BarColumn(
                bar_width=40, complete_style=score_color, finished_style=score_color
            ),
            TextColumn(f"[bold {score_color}]{score:.1f}%[/bold {score_color}]"),
            console=self.console,
            transient=False,
        ) as progress:
            task = progress.add_task("", total=100)
            progress.update(task, completed=score)

    def _print_summary(self) -> None:
        """Print the summary panel."""
        status = "COMPLIANT" if self.report.is_compliant else "NON-COMPLIANT"
        status_color = "green" if self.report.is_compliant else "red"

        # Count by level
        checks_by_level = self.report.checks_by_level

        def count_passed(checks: list[CheckResult]) -> tuple[int, int]:
            passed = sum(1 for c in checks if c.status == CheckStatus.PASSED)
            total = sum(1 for c in checks if c.status != CheckStatus.SKIPPED)
            return passed, total

        req_passed, req_total = count_passed(checks_by_level[CheckLevel.REQUIRED])
        rec_passed, rec_total = count_passed(checks_by_level[CheckLevel.RECOMMENDED])
        opt_passed, opt_total = count_passed(checks_by_level[CheckLevel.OPTIONAL])

        summary_lines = [
            f"[bold {status_color}]Status: {status}[/bold {status_color}]",
            "",
            f"[red]Required:[/red]    {req_passed}/{req_total} passed",
            f"[yellow]Recommended:[/yellow] {rec_passed}/{rec_total} passed",
            f"[dim]Optional:[/dim]    {opt_passed}/{opt_total} passed",
        ]

        self.console.print()
        self.console.print(
            Panel("\n".join(summary_lines), title="Summary", border_style=status_color)
        )

    def _print_suggestions(self) -> None:
        """Print actionable suggestions panel."""
        suggestions = self.report.actionable_suggestions
        if not suggestions:
            return

        self.console.print()
        self.console.print("[bold cyan]Quick Fixes[/bold cyan]")
        self.console.print()

        # Main suggestion: run update
        self.console.print("  [green]projinit update[/green]")
        self.console.print(
            "  [dim]Auto-fix all issues that can be automatically resolved[/dim]"
        )
        self.console.print()

        # Individual suggestions
        if self.verbose and suggestions:
            self.console.print("  [dim]Or fix manually:[/dim]")
            for check_id, suggestion in suggestions[:5]:  # Limit to 5
                self.console.print(f"    [dim]{check_id}:[/dim] {suggestion}")

            if len(suggestions) > 5:
                self.console.print(
                    f"    [dim]... and {len(suggestions) - 5} more[/dim]"
                )

    def _print_verbose_info(self) -> None:
        """Print verbose technical information."""
        self.console.print()
        self.console.print("[dim]Technical Details:[/dim]")
        self.console.print(
            f"  [dim]Execution time: {self.report.execution_time_ms:.1f}ms[/dim]"
        )
        self.console.print(f"  [dim]Checks run: {self.report.total_count}[/dim]")

        if self.report.files_scanned:
            self.console.print(
                f"  [dim]Files checked: {len(self.report.files_scanned)}[/dim]"
            )
            if len(self.report.files_scanned) <= 10:
                for f in self.report.files_scanned:
                    self.console.print(f"    [dim]- {f}[/dim]")
            else:
                for f in self.report.files_scanned[:5]:
                    self.console.print(f"    [dim]- {f}[/dim]")
                self.console.print(
                    f"    [dim]... and {len(self.report.files_scanned) - 5} more[/dim]"
                )

    def to_json(self) -> str:
        """Generate a JSON report."""
        data = {
            "project_path": str(self.report.project_path),
            "project_type": self.report.project_type.value,
            "score": round(self.report.score, 1),
            "is_compliant": self.report.is_compliant,
            "execution_time_ms": round(self.report.execution_time_ms, 2),
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

        if self.verbose:
            data["files_scanned"] = self.report.files_scanned

        return json.dumps(data, indent=2)

    def to_markdown(self) -> str:
        """Generate a Markdown report with badges."""
        score = self.report.score
        status = "passing" if self.report.is_compliant else "failing"
        status_color = "brightgreen" if self.report.is_compliant else "red"
        score_color = (
            "brightgreen" if score >= 80 else "yellow" if score >= 60 else "red"
        )

        # Generate shields.io badge URLs
        status_badge = (
            f"![Status](https://img.shields.io/badge/status-{status}-{status_color})"
        )
        score_badge = (
            f"![Score](https://img.shields.io/badge/score-{score:.0f}%25-{score_color})"
        )

        lines = [
            "# Project Audit Report",
            "",
            f"{status_badge} {score_badge}",
            "",
            "## Overview",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| **Path** | `{self.report.project_path}` |",
            f"| **Type** | {self.report.project_type.display_name} |",
            f"| **Score** | {score:.1f}% |",
            f"| **Status** | {'Compliant' if self.report.is_compliant else 'Non-Compliant'} |",
            "",
        ]

        # Group checks by level
        checks_by_level = self.report.checks_by_level

        level_info = [
            (CheckLevel.REQUIRED, "Required Checks"),
            (CheckLevel.RECOMMENDED, "Recommended Checks"),
            (CheckLevel.OPTIONAL, "Optional Checks"),
        ]

        for level, title in level_info:
            checks = checks_by_level.get(level, [])
            if not checks:
                continue

            lines.extend(
                [
                    f"## {title}",
                    "",
                    "| Status | Check | Message |",
                    "|--------|-------|---------|",
                ]
            )

            for check in checks:
                status_emoji = self._get_status_emoji(check.status)
                # Escape pipe characters in message
                message = check.message.replace("|", "\\|")
                lines.append(f"| {status_emoji} | `{check.id}` | {message} |")

            lines.append("")

        # Summary
        lines.extend(
            [
                "## Summary",
                "",
                f"- **Passed**: {self.report.passed_count}",
                f"- **Failed**: {self.report.failed_count}",
                f"- **Warnings**: {self.report.warning_count}",
                f"- **Total**: {self.report.total_count}",
                "",
            ]
        )

        # Quick fix section
        if self.report.failed_checks:
            lines.extend(
                [
                    "## Quick Fix",
                    "",
                    "Run the following command to automatically fix issues:",
                    "",
                    "```bash",
                    "projinit update",
                    "```",
                    "",
                ]
            )

        # Footer
        lines.extend(
            [
                "---",
                "",
                f"*Generated by projinit in {self.report.execution_time_ms:.1f}ms*",
            ]
        )

        return "\n".join(lines)

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
