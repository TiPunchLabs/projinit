"""Tests for projinit.core.models module."""

from pathlib import Path

import pytest

from projinit.core.models import (
    ActionType,
    AuditReport,
    CheckLevel,
    CheckResult,
    CheckStatus,
    DetectionResult,
    MergeStrategy,
    ProjectType,
    UpdateAction,
)


class TestProjectType:
    """Tests for ProjectType enum."""

    def test_all_values_exist(self):
        """Verify all expected project types exist."""
        assert ProjectType.PYTHON_CLI.value == "python-cli"
        assert ProjectType.PYTHON_LIB.value == "python-lib"
        assert ProjectType.NODE_FRONTEND.value == "node-frontend"
        assert ProjectType.INFRASTRUCTURE.value == "infrastructure"
        assert ProjectType.DOCUMENTATION.value == "documentation"
        assert ProjectType.LAB.value == "lab"
        assert ProjectType.UNKNOWN.value == "unknown"

    def test_display_name_property(self):
        """Verify display names are human-readable."""
        assert ProjectType.PYTHON_CLI.display_name == "Python CLI Application"
        assert ProjectType.PYTHON_LIB.display_name == "Python Library"
        assert ProjectType.NODE_FRONTEND.display_name == "Node.js Frontend"
        assert ProjectType.INFRASTRUCTURE.display_name == "Infrastructure (Terraform/Ansible)"
        assert ProjectType.DOCUMENTATION.display_name == "Documentation (MkDocs)"
        assert ProjectType.LAB.display_name == "Lab/Tutorial"
        assert ProjectType.UNKNOWN.display_name == "Unknown"

    def test_can_create_from_value(self):
        """Verify enum can be created from string value."""
        assert ProjectType("python-cli") == ProjectType.PYTHON_CLI
        assert ProjectType("infrastructure") == ProjectType.INFRASTRUCTURE


class TestCheckStatus:
    """Tests for CheckStatus enum."""

    def test_all_statuses(self):
        """Verify all check statuses exist."""
        assert CheckStatus.PASSED.value == "passed"
        assert CheckStatus.FAILED.value == "failed"
        assert CheckStatus.WARNING.value == "warning"
        assert CheckStatus.SKIPPED.value == "skipped"


class TestCheckLevel:
    """Tests for CheckLevel enum."""

    def test_all_levels(self):
        """Verify all check levels exist."""
        assert CheckLevel.REQUIRED.value == "required"
        assert CheckLevel.RECOMMENDED.value == "recommended"
        assert CheckLevel.OPTIONAL.value == "optional"


class TestCheckResult:
    """Tests for CheckResult dataclass."""

    def test_basic_creation(self):
        """Test creating a basic check result."""
        result = CheckResult(
            id="test_check",
            status=CheckStatus.PASSED,
            message="Test passed",
        )
        assert result.id == "test_check"
        assert result.status == CheckStatus.PASSED
        assert result.message == "Test passed"
        assert result.level == CheckLevel.REQUIRED  # default

    def test_is_passed_property(self):
        """Test is_passed property."""
        passed = CheckResult(id="t1", status=CheckStatus.PASSED, message="ok")
        failed = CheckResult(id="t2", status=CheckStatus.FAILED, message="fail")

        assert passed.is_passed is True
        assert failed.is_passed is False

    def test_is_critical_property(self):
        """Test is_critical property."""
        critical = CheckResult(
            id="t1",
            status=CheckStatus.FAILED,
            message="fail",
            level=CheckLevel.REQUIRED,
        )
        non_critical = CheckResult(
            id="t2",
            status=CheckStatus.FAILED,
            message="fail",
            level=CheckLevel.RECOMMENDED,
        )

        assert critical.is_critical is True
        assert non_critical.is_critical is False

    def test_with_file_path(self):
        """Test check result with file path."""
        result = CheckResult(
            id="test",
            status=CheckStatus.PASSED,
            message="ok",
            file_path=Path("/tmp/test.txt"),
        )
        assert result.file_path == Path("/tmp/test.txt")

    def test_with_suggestion(self):
        """Test check result with suggestion."""
        result = CheckResult(
            id="test",
            status=CheckStatus.FAILED,
            message="fail",
            suggestion="Run: pip install package",
        )
        assert result.suggestion == "Run: pip install package"


class TestDetectionResult:
    """Tests for DetectionResult dataclass."""

    def test_basic_creation(self):
        """Test creating a detection result."""
        result = DetectionResult(
            project_type=ProjectType.PYTHON_CLI,
            confidence=0.85,
            markers_found=["pyproject.toml", "src/"],
        )
        assert result.project_type == ProjectType.PYTHON_CLI
        assert result.confidence == 0.85
        assert "pyproject.toml" in result.markers_found

    def test_is_confident_high(self):
        """Test is_confident with high confidence."""
        result = DetectionResult(
            project_type=ProjectType.PYTHON_CLI,
            confidence=0.8,
        )
        assert result.is_confident is True

    def test_is_confident_low(self):
        """Test is_confident with low confidence."""
        result = DetectionResult(
            project_type=ProjectType.PYTHON_CLI,
            confidence=0.5,
        )
        assert result.is_confident is False

    def test_is_confident_threshold(self):
        """Test is_confident at threshold (0.7)."""
        at_threshold = DetectionResult(project_type=ProjectType.PYTHON_CLI, confidence=0.7)
        below = DetectionResult(project_type=ProjectType.PYTHON_CLI, confidence=0.69)

        assert at_threshold.is_confident is True
        assert below.is_confident is False


class TestUpdateAction:
    """Tests for UpdateAction dataclass."""

    def test_basic_creation(self):
        """Test creating an update action."""
        action = UpdateAction(
            action_type=ActionType.CREATE,
            source=Path("templates/readme.md"),
            target=Path("README.md"),
        )
        assert action.action_type == ActionType.CREATE
        assert action.merge_strategy == MergeStrategy.SMART  # default

    def test_is_destructive(self):
        """Test is_destructive property."""
        create = UpdateAction(
            action_type=ActionType.CREATE,
            source=None,
            target=Path("test"),
        )
        modify = UpdateAction(
            action_type=ActionType.MODIFY,
            source=None,
            target=Path("test"),
        )
        merge = UpdateAction(
            action_type=ActionType.MERGE,
            source=None,
            target=Path("test"),
        )

        assert create.is_destructive is False
        assert modify.is_destructive is True
        assert merge.is_destructive is True


class TestAuditReport:
    """Tests for AuditReport dataclass."""

    @pytest.fixture
    def sample_checks(self) -> list[CheckResult]:
        """Create a sample list of check results."""
        return [
            CheckResult(id="c1", status=CheckStatus.PASSED, message="ok", level=CheckLevel.REQUIRED),
            CheckResult(id="c2", status=CheckStatus.PASSED, message="ok", level=CheckLevel.REQUIRED),
            CheckResult(id="c3", status=CheckStatus.FAILED, message="fail", level=CheckLevel.REQUIRED),
            CheckResult(id="c4", status=CheckStatus.WARNING, message="warn", level=CheckLevel.RECOMMENDED),
            CheckResult(id="c5", status=CheckStatus.SKIPPED, message="skip", level=CheckLevel.OPTIONAL),
        ]

    def test_basic_creation(self, sample_checks):
        """Test creating an audit report."""
        report = AuditReport(
            project_path=Path("/tmp/project"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        assert report.project_path == Path("/tmp/project")
        assert len(report.checks) == 5

    def test_passed_count(self, sample_checks):
        """Test passed_count property."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        assert report.passed_count == 2

    def test_failed_count(self, sample_checks):
        """Test failed_count property."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        assert report.failed_count == 1

    def test_warning_count(self, sample_checks):
        """Test warning_count property."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        assert report.warning_count == 1

    def test_total_count_excludes_skipped(self, sample_checks):
        """Test total_count excludes skipped checks."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        # 2 passed + 1 failed + 1 warning = 4 (skipped not counted)
        assert report.total_count == 4

    def test_score(self, sample_checks):
        """Test score calculation."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        # 2 passed out of 4 total = 50%
        assert report.score == 50.0

    def test_score_empty_report(self):
        """Test score with no checks."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=[],
        )
        assert report.score == 100.0

    def test_is_compliant_true(self):
        """Test is_compliant when all required checks pass."""
        checks = [
            CheckResult(id="c1", status=CheckStatus.PASSED, message="ok", level=CheckLevel.REQUIRED),
            CheckResult(id="c2", status=CheckStatus.FAILED, message="fail", level=CheckLevel.RECOMMENDED),
        ]
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=checks,
        )
        assert report.is_compliant is True

    def test_is_compliant_false(self):
        """Test is_compliant when a required check fails."""
        checks = [
            CheckResult(id="c1", status=CheckStatus.FAILED, message="fail", level=CheckLevel.REQUIRED),
        ]
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=checks,
        )
        assert report.is_compliant is False

    def test_checks_by_level(self, sample_checks):
        """Test checks_by_level grouping."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        by_level = report.checks_by_level

        assert len(by_level[CheckLevel.REQUIRED]) == 3
        assert len(by_level[CheckLevel.RECOMMENDED]) == 1
        assert len(by_level[CheckLevel.OPTIONAL]) == 1

    def test_failed_checks(self, sample_checks):
        """Test failed_checks property."""
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=sample_checks,
        )
        failed = report.failed_checks

        assert len(failed) == 1
        assert failed[0].id == "c3"

    def test_actionable_suggestions(self):
        """Test actionable_suggestions property."""
        checks = [
            CheckResult(
                id="c1",
                status=CheckStatus.FAILED,
                message="fail",
                suggestion="Run: fix command",
            ),
            CheckResult(
                id="c2",
                status=CheckStatus.FAILED,
                message="fail",
                suggestion=None,  # No suggestion
            ),
        ]
        report = AuditReport(
            project_path=Path("/tmp"),
            project_type=ProjectType.PYTHON_CLI,
            checks=checks,
        )
        suggestions = report.actionable_suggestions

        assert len(suggestions) == 1
        assert suggestions[0] == ("c1", "Run: fix command")
