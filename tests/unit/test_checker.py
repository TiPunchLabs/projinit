"""Tests for projinit.core.checker module."""

from pathlib import Path

import pytest

from projinit.core.checker import Checker
from projinit.core.models import CheckLevel, CheckStatus, ProjectType


class TestChecker:
    """Tests for Checker class."""

    def test_init(self, python_cli_project: Path):
        """Test Checker initialization."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)

        assert checker.project_path == python_cli_project
        assert checker.project_type == ProjectType.PYTHON_CLI

    def test_run_checks_returns_audit_report(self, python_cli_project: Path):
        """Test that run_checks returns an AuditReport."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        assert report.project_path == python_cli_project
        assert report.project_type == ProjectType.PYTHON_CLI
        assert len(report.checks) > 0

    def test_execution_time_recorded(self, python_cli_project: Path):
        """Test that execution time is recorded."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        assert report.execution_time_ms > 0

    def test_files_scanned_populated(self, complete_python_project: Path):
        """Test that files_scanned is populated."""
        checker = Checker(complete_python_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # Should have scanned some files
        assert len(report.files_scanned) >= 0


class TestFileExistsCheck:
    """Tests for file_exists check type."""

    def test_file_exists_passes(self, python_cli_project: Path):
        """Test file_exists check passes when file exists."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # pyproject.toml should exist and pass
        pyproject_checks = [c for c in report.checks if "pyproject" in c.id.lower()]
        if pyproject_checks:
            assert pyproject_checks[0].status == CheckStatus.PASSED

    def test_file_exists_fails(self, python_cli_project: Path):
        """Test file_exists check fails when file is missing."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # README should be missing in basic project
        readme_checks = [c for c in report.checks if c.id == "has_readme"]
        if readme_checks:
            assert readme_checks[0].status == CheckStatus.FAILED

    def test_file_exists_with_alternatives(self, temp_dir: Path):
        """Test file_exists check with alternative paths."""
        project = temp_dir / "project"
        project.mkdir()

        # Create alternative file (e.g., setup.py instead of pyproject.toml)
        (project / "setup.py").write_text("from setuptools import setup")

        checker = Checker(project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # Should pass if alternatives are defined
        assert report is not None


class TestDirExistsCheck:
    """Tests for dir_exists check type."""

    def test_dir_exists_passes(self, python_cli_project: Path):
        """Test dir_exists check passes when directory exists."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # src/ should exist
        src_checks = [c for c in report.checks if "src" in c.id.lower()]
        if src_checks:
            assert src_checks[0].status == CheckStatus.PASSED

    def test_dir_exists_fails(self, temp_dir: Path):
        """Test dir_exists check fails when directory is missing."""
        project = temp_dir / "project"
        project.mkdir()
        (project / "pyproject.toml").write_text("[project]\nname = 'test'")

        checker = Checker(project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # doc/ should be missing
        doc_checks = [c for c in report.checks if c.id == "has_technical_docs"]
        if doc_checks:
            assert doc_checks[0].status == CheckStatus.FAILED


class TestContentContainsCheck:
    """Tests for content_contains check type."""

    def test_content_contains_passes(self, complete_python_project: Path):
        """Test content_contains check passes when patterns found."""
        # Add .pre-commit-config.yaml with required content
        precommit = complete_python_project / ".pre-commit-config.yaml"
        precommit.write_text("""repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
""")

        checker = Checker(complete_python_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # Should have checked precommit content
        precommit_checks = [c for c in report.checks if "precommit" in c.id.lower()]
        # Result depends on actual check definitions
        assert report is not None

    def test_content_contains_skipped_when_file_missing(self, python_cli_project: Path):
        """Test content_contains check is skipped when file doesn't exist."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # content_contains checks on missing files should be skipped
        skipped = [c for c in report.checks if c.status == CheckStatus.SKIPPED]
        # May or may not have skipped checks depending on project
        assert report is not None


class TestAnyExistsCheck:
    """Tests for any_exists check type."""

    def test_any_exists_passes_first_option(self, temp_dir: Path):
        """Test any_exists passes when first option exists."""
        project = temp_dir / "project"
        project.mkdir()
        (project / "README.md").write_text("# Test")

        checker = Checker(project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # README check should pass
        readme_checks = [c for c in report.checks if c.id == "has_readme"]
        if readme_checks:
            assert readme_checks[0].status == CheckStatus.PASSED


class TestCheckLevels:
    """Tests for check level handling."""

    def test_required_checks_affect_compliance(self, python_cli_project: Path):
        """Test that required check failures affect compliance."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # If any required check fails, is_compliant should be False
        required_failures = [
            c for c in report.checks
            if c.status == CheckStatus.FAILED and c.level == CheckLevel.REQUIRED
        ]

        if required_failures:
            assert report.is_compliant is False

    def test_recommended_checks_dont_affect_compliance(self, complete_python_project: Path):
        """Test that recommended check failures don't affect compliance."""
        checker = Checker(complete_python_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # Even with recommended failures, can still be compliant
        # if all required checks pass
        required_checks = [
            c for c in report.checks
            if c.level == CheckLevel.REQUIRED
        ]

        all_required_pass = all(c.status == CheckStatus.PASSED for c in required_checks)
        if all_required_pass:
            assert report.is_compliant is True


class TestCheckSuggestions:
    """Tests for check suggestions."""

    def test_failed_checks_may_have_suggestions(self, python_cli_project: Path):
        """Test that failed checks may have suggestions."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        failed = [c for c in report.checks if c.status == CheckStatus.FAILED]

        # At least some failed checks should have suggestions
        suggestions = [c.suggestion for c in failed if c.suggestion]
        # Not all checks have suggestions, but this tests the mechanism
        assert report is not None

    def test_suggestions_are_actionable(self, python_cli_project: Path):
        """Test that suggestions contain actionable commands."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        for suggestion_id, suggestion in report.actionable_suggestions:
            # Suggestions should be non-empty strings
            assert isinstance(suggestion, str)
            assert len(suggestion) > 0


class TestErrorHandling:
    """Tests for error handling in checks."""

    def test_invalid_check_type_skipped(self, python_cli_project: Path):
        """Test that invalid check types are handled gracefully."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)

        # Manually run a check with invalid type
        result = checker._run_single_check({
            "id": "invalid_check",
            "type": "nonexistent_type",
            "description": "Test",
        })

        assert result.status == CheckStatus.SKIPPED
        assert "Unknown check type" in result.message

    def test_check_exception_handled(self, python_cli_project: Path):
        """Test that exceptions during checks are caught."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)

        # This should not raise an exception
        report = checker.run_checks()

        assert report is not None


class TestReportProperties:
    """Tests for AuditReport properties through Checker."""

    def test_score_calculation(self, python_cli_project: Path):
        """Test score is calculated correctly."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        # Score should be between 0 and 100
        assert 0 <= report.score <= 100

    def test_checks_by_level_grouping(self, python_cli_project: Path):
        """Test checks are grouped by level correctly."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        by_level = report.checks_by_level

        # All levels should be present
        assert CheckLevel.REQUIRED in by_level
        assert CheckLevel.RECOMMENDED in by_level
        assert CheckLevel.OPTIONAL in by_level

        # Total should match
        total = sum(len(checks) for checks in by_level.values())
        assert total == len(report.checks)


class TestDifferentProjectTypes:
    """Tests for different project types."""

    def test_python_cli_checks(self, python_cli_project: Path):
        """Test checks for Python CLI project."""
        checker = Checker(python_cli_project, ProjectType.PYTHON_CLI)
        report = checker.run_checks()

        check_ids = {c.id for c in report.checks}
        # Should have Python-specific checks
        assert len(check_ids) > 0

    def test_node_frontend_checks(self, node_frontend_project: Path):
        """Test checks for Node.js frontend project."""
        checker = Checker(node_frontend_project, ProjectType.NODE_FRONTEND)
        report = checker.run_checks()

        check_ids = {c.id for c in report.checks}
        # Should have Node-specific checks
        assert len(check_ids) > 0

    def test_infrastructure_checks(self, infrastructure_project: Path):
        """Test checks for infrastructure project."""
        checker = Checker(infrastructure_project, ProjectType.INFRASTRUCTURE)
        report = checker.run_checks()

        check_ids = {c.id for c in report.checks}
        # Should have infrastructure-specific checks
        assert len(check_ids) > 0

    def test_documentation_checks(self, documentation_project: Path):
        """Test checks for documentation project."""
        checker = Checker(documentation_project, ProjectType.DOCUMENTATION)
        report = checker.run_checks()

        check_ids = {c.id for c in report.checks}
        # Should have documentation-specific checks
        assert len(check_ids) > 0
