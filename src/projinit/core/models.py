"""Data models for projinit v2.0."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ProjectType(Enum):
    """Type of project detected or specified."""

    PYTHON_CLI = "python-cli"
    PYTHON_LIB = "python-lib"
    NODE_FRONTEND = "node-frontend"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION = "documentation"
    LAB = "lab"
    UNKNOWN = "unknown"

    @property
    def display_name(self) -> str:
        """Human-readable name for the project type."""
        names = {
            ProjectType.PYTHON_CLI: "Python CLI Application",
            ProjectType.PYTHON_LIB: "Python Library",
            ProjectType.NODE_FRONTEND: "Node.js Frontend",
            ProjectType.INFRASTRUCTURE: "Infrastructure (Terraform/Ansible)",
            ProjectType.DOCUMENTATION: "Documentation (MkDocs)",
            ProjectType.LAB: "Lab/Tutorial",
            ProjectType.UNKNOWN: "Unknown",
        }
        return names.get(self, self.value)


class CheckStatus(Enum):
    """Status of a conformity check."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


class CheckLevel(Enum):
    """Importance level of a check."""

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class ActionType(Enum):
    """Type of update action."""

    CREATE = "create"
    MODIFY = "modify"
    MERGE = "merge"
    SKIP = "skip"


class MergeStrategy(Enum):
    """Strategy for merging files."""

    OVERWRITE = "overwrite"
    SMART = "smart"
    SKIP_EXISTING = "skip_existing"


@dataclass
class CheckResult:
    """Result of a single conformity check."""

    id: str
    status: CheckStatus
    message: str
    level: CheckLevel = CheckLevel.REQUIRED
    suggestion: str | None = None
    file_path: Path | None = None

    @property
    def is_passed(self) -> bool:
        """Check if the result indicates success."""
        return self.status == CheckStatus.PASSED

    @property
    def is_critical(self) -> bool:
        """Check if this is a critical failure."""
        return self.status == CheckStatus.FAILED and self.level == CheckLevel.REQUIRED


@dataclass
class UpdateAction:
    """Action to perform during project update."""

    action_type: ActionType
    source: Path | None
    target: Path
    merge_strategy: MergeStrategy = MergeStrategy.SMART
    description: str = ""
    template_vars: dict = field(default_factory=dict)

    @property
    def is_destructive(self) -> bool:
        """Check if this action modifies existing files."""
        return self.action_type in (ActionType.MODIFY, ActionType.MERGE)


@dataclass
class DetectionResult:
    """Result of project type detection."""

    project_type: ProjectType
    confidence: float  # 0.0 to 1.0
    markers_found: list[str] = field(default_factory=list)
    markers_checked: list[str] = field(default_factory=list)

    @property
    def is_confident(self) -> bool:
        """Check if detection has high confidence."""
        return self.confidence >= 0.7


@dataclass
class AuditReport:
    """Complete audit report for a project."""

    project_path: Path
    project_type: ProjectType
    checks: list[CheckResult] = field(default_factory=list)
    execution_time_ms: float = 0.0
    files_scanned: list[str] = field(default_factory=list)

    @property
    def passed_count(self) -> int:
        """Number of passed checks."""
        return sum(1 for c in self.checks if c.status == CheckStatus.PASSED)

    @property
    def failed_count(self) -> int:
        """Number of failed checks."""
        return sum(1 for c in self.checks if c.status == CheckStatus.FAILED)

    @property
    def warning_count(self) -> int:
        """Number of warnings."""
        return sum(1 for c in self.checks if c.status == CheckStatus.WARNING)

    @property
    def total_count(self) -> int:
        """Total number of checks (excluding skipped)."""
        return sum(1 for c in self.checks if c.status != CheckStatus.SKIPPED)

    @property
    def score(self) -> float:
        """Conformity score as percentage."""
        if self.total_count == 0:
            return 100.0
        return (self.passed_count / self.total_count) * 100

    @property
    def is_compliant(self) -> bool:
        """Check if project passes all required checks."""
        return all(
            c.status != CheckStatus.FAILED
            for c in self.checks
            if c.level == CheckLevel.REQUIRED
        )

    @property
    def checks_by_level(self) -> dict[CheckLevel, list[CheckResult]]:
        """Group checks by their level."""
        result: dict[CheckLevel, list[CheckResult]] = {
            CheckLevel.REQUIRED: [],
            CheckLevel.RECOMMENDED: [],
            CheckLevel.OPTIONAL: [],
        }
        for check in self.checks:
            result[check.level].append(check)
        return result

    @property
    def failed_checks(self) -> list[CheckResult]:
        """Get all failed checks."""
        return [c for c in self.checks if c.status == CheckStatus.FAILED]

    @property
    def actionable_suggestions(self) -> list[tuple[str, str]]:
        """Get actionable suggestions with commands."""
        suggestions = []
        for check in self.failed_checks:
            if check.suggestion:
                suggestions.append((check.id, check.suggestion))
        return suggestions
