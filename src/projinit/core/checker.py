"""Conformity checker for projinit v2.0."""

import time
from pathlib import Path

from projinit.core.models import (
    AuditReport,
    CheckLevel,
    CheckResult,
    CheckStatus,
    ProjectType,
)
from projinit.standards.loader import get_checks_for_type


class Checker:
    """Checks project conformity against standards."""

    def __init__(self, project_path: Path, project_type: ProjectType):
        """
        Initialize the checker.

        Args:
            project_path: Path to the project root.
            project_type: Detected or specified project type.
        """
        self.project_path = project_path
        self.project_type = project_type
        self._files_scanned: set[str] = set()

    def run_checks(self) -> AuditReport:
        """
        Run all applicable checks and return an audit report.

        Returns:
            AuditReport with all check results.
        """
        start_time = time.perf_counter()

        checks = get_checks_for_type(self.project_type)
        results = []

        for check_def in checks:
            result = self._run_single_check(check_def)
            results.append(result)
            # Track scanned files
            if result.file_path:
                self._files_scanned.add(
                    str(result.file_path.relative_to(self.project_path))
                )

        execution_time_ms = (time.perf_counter() - start_time) * 1000

        return AuditReport(
            project_path=self.project_path,
            project_type=self.project_type,
            checks=results,
            execution_time_ms=execution_time_ms,
            files_scanned=sorted(self._files_scanned),
        )

    def _run_single_check(self, check_def: dict) -> CheckResult:
        """
        Run a single check based on its definition.

        Args:
            check_def: Check definition from standards YAML.

        Returns:
            CheckResult with the outcome.
        """
        check_id = check_def.get("id", "unknown")
        check_type = check_def.get("type", "file_exists")
        level = CheckLevel(check_def.get("level", "required"))
        description = check_def.get("description", "")
        template = check_def.get("template")

        try:
            if check_type == "file_exists":
                return self._check_file_exists(
                    check_def, check_id, level, description, template
                )
            elif check_type == "dir_exists":
                return self._check_dir_exists(check_def, check_id, level, description)
            elif check_type == "content_contains":
                return self._check_content_contains(
                    check_def, check_id, level, description
                )
            elif check_type == "any_exists":
                return self._check_any_exists(check_def, check_id, level, description)
            else:
                return CheckResult(
                    id=check_id,
                    status=CheckStatus.SKIPPED,
                    message=f"Unknown check type: {check_type}",
                    level=level,
                )
        except Exception as e:
            return CheckResult(
                id=check_id,
                status=CheckStatus.FAILED,
                message=f"Error running check: {e}",
                level=level,
            )

    def _check_file_exists(
        self,
        check_def: dict,
        check_id: str,
        level: CheckLevel,
        description: str,
        template: str | None,
    ) -> CheckResult:
        """Check if a file exists."""
        path = check_def.get("path", "")
        file_path = self.project_path / path

        # Check alternatives if main path doesn't exist
        alternatives = check_def.get("alternatives", [])
        all_paths = [path] + alternatives

        for p in all_paths:
            if (self.project_path / p).exists():
                return CheckResult(
                    id=check_id,
                    status=CheckStatus.PASSED,
                    message=f"{p} exists",
                    level=level,
                    file_path=self.project_path / p,
                )

        suggestion = None
        if template:
            suggestion = f"Run 'projinit update' to create {path}"

        return CheckResult(
            id=check_id,
            status=CheckStatus.FAILED,
            message=f"{description} - {path} not found",
            level=level,
            suggestion=suggestion,
            file_path=file_path,
        )

    def _check_dir_exists(
        self,
        check_def: dict,
        check_id: str,
        level: CheckLevel,
        description: str,
    ) -> CheckResult:
        """Check if a directory exists."""
        path = check_def.get("path", "")
        dir_path = self.project_path / path

        # Check alternatives
        alternatives = check_def.get("alternatives", [])
        all_paths = [path] + alternatives

        for p in all_paths:
            check_path = self.project_path / p
            if check_path.is_dir():
                return CheckResult(
                    id=check_id,
                    status=CheckStatus.PASSED,
                    message=f"{p} directory exists",
                    level=level,
                    file_path=check_path,
                )

        return CheckResult(
            id=check_id,
            status=CheckStatus.FAILED,
            message=f"{description} - {path} directory not found",
            level=level,
            suggestion=f"Create directory: mkdir -p {path}",
            file_path=dir_path,
        )

    def _check_content_contains(
        self,
        check_def: dict,
        check_id: str,
        level: CheckLevel,
        description: str,
    ) -> CheckResult:
        """Check if a file contains required patterns."""
        path = check_def.get("path", "")
        patterns = check_def.get("patterns", [])
        alternatives = check_def.get("alternatives", [])

        # Find the file (check main path and alternatives)
        all_paths = [path] + alternatives
        file_path = None
        content = None

        for p in all_paths:
            check_path = self.project_path / p
            if check_path.exists():
                file_path = check_path
                try:
                    content = check_path.read_text(encoding="utf-8")
                    break
                except OSError:
                    pass

        if content is None:
            return CheckResult(
                id=check_id,
                status=CheckStatus.SKIPPED,
                message=f"File {path} not found, cannot check content",
                level=level,
                file_path=self.project_path / path,
            )

        # Check all patterns
        missing_patterns = [p for p in patterns if p not in content]

        if not missing_patterns:
            return CheckResult(
                id=check_id,
                status=CheckStatus.PASSED,
                message=f"All required patterns found in {file_path.name}",
                level=level,
                file_path=file_path,
            )

        return CheckResult(
            id=check_id,
            status=CheckStatus.FAILED,
            message=f"{description} - missing: {', '.join(missing_patterns)}",
            level=level,
            suggestion=f"Add missing configuration to {file_path.name if file_path else path}",
            file_path=file_path,
        )

    def _check_any_exists(
        self,
        check_def: dict,
        check_id: str,
        level: CheckLevel,
        description: str,
    ) -> CheckResult:
        """Check if any of the specified paths exist."""
        paths = check_def.get("paths", [])

        for path in paths:
            check_path = self.project_path / path
            if check_path.exists():
                return CheckResult(
                    id=check_id,
                    status=CheckStatus.PASSED,
                    message=f"Found {path}",
                    level=level,
                    file_path=check_path,
                )

        return CheckResult(
            id=check_id,
            status=CheckStatus.FAILED,
            message=f"{description} - none of {paths} found",
            level=level,
            suggestion=f"Create one of: {', '.join(paths)}",
        )
