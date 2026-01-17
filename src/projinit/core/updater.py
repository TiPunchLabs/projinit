"""Project updater for projinit v2.0."""

import shutil
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from projinit.core.merger import merge_precommit_config, merge_toml_section
from projinit.core.models import (
    ActionType,
    AuditReport,
    CheckLevel,
    CheckStatus,
    MergeStrategy,
    ProjectType,
    UpdateAction,
)
from projinit.standards.loader import load_standards

# Path to templates
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class Updater:
    """Applies updates to make a project conform to standards."""

    def __init__(
        self,
        project_path: Path,
        project_type: ProjectType,
        dry_run: bool = False,
        create_backup: bool = True,
    ):
        """
        Initialize the updater.

        Args:
            project_path: Path to the project root.
            project_type: Detected or specified project type.
            dry_run: If True, don't actually modify files.
            create_backup: If True, create .bak files before modifying.
        """
        self.project_path = project_path
        self.project_type = project_type
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.actions_taken: list[UpdateAction] = []

        # Setup Jinja2 environment
        if TEMPLATES_DIR.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(TEMPLATES_DIR)),
                keep_trailing_newline=True,
            )
        else:
            self.jinja_env = None

    def generate_actions(self, report: AuditReport) -> list[UpdateAction]:
        """
        Generate update actions based on an audit report.

        Args:
            report: The audit report with failed checks.

        Returns:
            List of UpdateAction to perform.
        """
        actions = []
        standards = load_standards(self.project_type)

        for check in report.checks:
            if check.status != CheckStatus.FAILED:
                continue

            # Find the check definition in standards
            check_def = self._find_check_definition(standards, check.id)
            if not check_def:
                continue

            action = self._create_action_for_check(check_def, check)
            if action:
                actions.append(action)

        return actions

    def apply_actions(self, actions: list[UpdateAction]) -> list[UpdateAction]:
        """
        Apply a list of update actions.

        Args:
            actions: List of actions to apply.

        Returns:
            List of actions that were successfully applied.
        """
        applied = []

        for action in actions:
            success = self._apply_single_action(action)
            if success:
                applied.append(action)
                self.actions_taken.append(action)

        return applied

    def _find_check_definition(self, standards: dict, check_id: str) -> dict | None:
        """Find a check definition by ID in standards."""
        for check in standards.get("checks", []):
            if check.get("id") == check_id:
                return check
        return None

    def _create_action_for_check(self, check_def: dict, check_result) -> UpdateAction | None:
        """Create an update action for a failed check."""
        check_type = check_def.get("type")
        path = check_def.get("path", "")
        template = check_def.get("template")
        target_path = self.project_path / path

        if check_type == "file_exists" and template:
            # Create missing file from template
            return UpdateAction(
                action_type=ActionType.CREATE,
                source=Path(template) if template else None,
                target=target_path,
                merge_strategy=MergeStrategy.SKIP_EXISTING,
                description=f"Create {path} from template",
                template_vars=self._get_template_vars(),
            )

        elif check_type == "dir_exists":
            # Create missing directory
            return UpdateAction(
                action_type=ActionType.CREATE,
                source=None,
                target=target_path,
                merge_strategy=MergeStrategy.SKIP_EXISTING,
                description=f"Create directory {path}",
            )

        elif check_type == "content_contains":
            # Check if we can fix this
            patterns = check_def.get("patterns", [])

            # Special handling for pre-commit hooks
            if "pre-commit" in path.lower() and ".yaml" in path:
                precommit_hooks = self._get_precommit_hooks_for_patterns(patterns)
                if precommit_hooks:
                    return UpdateAction(
                        action_type=ActionType.MERGE,
                        source=None,
                        target=target_path,
                        merge_strategy=MergeStrategy.SMART,
                        description=f"Add missing hooks to {path}",
                        template_vars={"hooks": precommit_hooks},
                    )

            # Special handling for pyproject.toml sections
            if "pyproject.toml" in path:
                section = self._get_toml_section_for_patterns(patterns)
                if section:
                    return UpdateAction(
                        action_type=ActionType.MERGE,
                        source=None,
                        target=target_path,
                        merge_strategy=MergeStrategy.SMART,
                        description=f"Add {section['name']} section to {path}",
                        template_vars={"section": section},
                    )

        return None

    def _apply_single_action(self, action: UpdateAction) -> bool:
        """Apply a single update action."""
        if self.dry_run:
            return True

        try:
            if action.action_type == ActionType.CREATE:
                return self._apply_create(action)
            elif action.action_type == ActionType.MERGE:
                return self._apply_merge(action)
            elif action.action_type == ActionType.MODIFY:
                return self._apply_modify(action)
            else:
                return False
        except Exception:
            return False

    def _apply_create(self, action: UpdateAction) -> bool:
        """Apply a create action."""
        target = action.target

        # Check if it's a directory creation
        if action.source is None and not str(target).endswith(('.yaml', '.yml', '.toml', '.md', '.txt', '.json')):
            # Probably a directory
            target.mkdir(parents=True, exist_ok=True)
            return True

        # Skip if file exists
        if target.exists() and action.merge_strategy == MergeStrategy.SKIP_EXISTING:
            return False

        # Create parent directory
        target.parent.mkdir(parents=True, exist_ok=True)

        # Render template if available
        if action.source and self.jinja_env:
            try:
                template = self.jinja_env.get_template(str(action.source))
                content = template.render(**action.template_vars)
                target.write_text(content, encoding="utf-8")
                return True
            except TemplateNotFound:
                pass

        # Create minimal file if no template
        return self._create_minimal_file(target, action.template_vars)

    def _apply_merge(self, action: UpdateAction) -> bool:
        """Apply a merge action."""
        target = action.target

        if not target.exists():
            return False

        # Backup if needed
        if self.create_backup:
            self._backup_file(target)

        # Handle pre-commit hooks merge
        if "hooks" in action.template_vars:
            hooks = action.template_vars["hooks"]
            content = merge_precommit_config(target, hooks)
            target.write_text(content, encoding="utf-8")
            return True

        # Handle TOML section merge
        if "section" in action.template_vars:
            section = action.template_vars["section"]
            existing = target.read_text(encoding="utf-8")
            content = merge_toml_section(existing, section["name"], section["values"])
            target.write_text(content, encoding="utf-8")
            return True

        return False

    def _apply_modify(self, action: UpdateAction) -> bool:
        """Apply a modify action."""
        # Not implemented yet - would require more complex logic
        return False

    def _backup_file(self, path: Path) -> None:
        """Create a backup of a file."""
        if path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = path.with_suffix(f"{path.suffix}.{timestamp}.bak")
            shutil.copy2(path, backup_path)

    def _get_template_vars(self) -> dict:
        """Get template variables for rendering."""
        return {
            "project_name": self.project_path.name,
            "project_type": self.project_type.value,
            "year": datetime.now().year,
        }

    def _get_precommit_hooks_for_patterns(self, patterns: list[str]) -> list[dict]:
        """Get pre-commit hook definitions for missing patterns."""
        standards = load_standards(self.project_type)
        hooks_to_add = []

        for hook_def in standards.get("precommit_hooks", []):
            # Check if any hook in this repo matches the patterns
            for hook in hook_def.get("hooks", []):
                hook_id = hook.get("id", "")
                if any(p in hook_id or hook_id in p for p in patterns):
                    # Add the whole repo definition
                    if hook_def not in hooks_to_add:
                        hooks_to_add.append(hook_def)
                    break

        return hooks_to_add

    def _get_toml_section_for_patterns(self, patterns: list[str]) -> dict | None:
        """Get TOML section definition for missing patterns."""
        for pattern in patterns:
            if "[tool.ruff]" in pattern:
                return {
                    "name": "[tool.ruff]",
                    "values": {
                        "line-length": 100,
                        "target-version": "py310",
                    },
                }
        return None

    def _create_minimal_file(self, path: Path, vars: dict) -> bool:
        """Create a minimal file when no template is available."""
        name = path.name.lower()
        project_name = vars.get("project_name", "Project")

        if name == "readme.md":
            content = f"# {project_name}\n\nProject description.\n"
        elif name == "license":
            year = vars.get("year", datetime.now().year)
            content = f"MIT License\n\nCopyright (c) {year}\n"
        elif name == ".gitignore":
            content = self._get_minimal_gitignore()
        elif name == "claude.md":
            content = f"# {project_name}\n\nInstructions for Claude Code.\n"
        elif name == ".pre-commit-config.yaml":
            content = self._get_minimal_precommit()
        else:
            content = ""

        path.write_text(content, encoding="utf-8")
        return True

    def _get_minimal_gitignore(self) -> str:
        """Get minimal .gitignore content."""
        return """# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.envrc
"""

    def _get_minimal_precommit(self) -> str:
        """Get minimal pre-commit config."""
        return """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
"""
