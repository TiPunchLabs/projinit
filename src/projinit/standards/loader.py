"""Standards loader for projinit v2.0."""

from pathlib import Path

import yaml

from projinit.core.models import ProjectType

# Path to default standards
DEFAULTS_DIR = Path(__file__).parent / "defaults"


def load_standards(project_type: ProjectType) -> dict:
    """
    Load standards for a given project type.

    Loads base standards plus type-specific standards.
    Supports hierarchy: defaults < global (~/.config/projinit) < local (.projinit.yaml)

    Args:
        project_type: The detected or specified project type.

    Returns:
        Merged standards dictionary with all applicable checks.
    """
    standards = {"checks": [], "precommit_hooks": []}

    # Load base standards (always)
    base_path = DEFAULTS_DIR / "base.yaml"
    if base_path.exists():
        base_standards = _load_yaml(base_path)
        standards = _merge_standards(standards, base_standards)

    # Load type-specific standards
    type_mapping = {
        ProjectType.PYTHON_CLI: "python.yaml",
        ProjectType.PYTHON_LIB: "python.yaml",
        ProjectType.NODE_FRONTEND: "node.yaml",
        ProjectType.INFRASTRUCTURE: "infra.yaml",
        ProjectType.DOCUMENTATION: "documentation.yaml",
    }

    if project_type in type_mapping:
        type_path = DEFAULTS_DIR / type_mapping[project_type]
        if type_path.exists():
            type_standards = _load_yaml(type_path)
            standards = _merge_standards(standards, type_standards)

    # TODO: Load global config from ~/.config/projinit/standards.yaml
    # TODO: Load local config from .projinit.yaml

    return standards


def load_all_standards() -> dict[str, dict]:
    """
    Load all available standard files.

    Returns:
        Dictionary mapping standard names to their content.
    """
    standards = {}
    for yaml_file in DEFAULTS_DIR.glob("*.yaml"):
        standards[yaml_file.stem] = _load_yaml(yaml_file)
    return standards


def get_checks_for_type(project_type: ProjectType) -> list[dict]:
    """
    Get all checks applicable to a project type.

    Args:
        project_type: The project type to get checks for.

    Returns:
        List of check definitions.
    """
    standards = load_standards(project_type)
    checks = standards.get("checks", [])

    # Filter checks by applies_to if specified
    filtered_checks = []
    for check in checks:
        applies_to = check.get("applies_to")
        if applies_to is None:
            # No restriction, applies to all
            filtered_checks.append(check)
        elif project_type.value in applies_to:
            filtered_checks.append(check)

    return filtered_checks


def _load_yaml(path: Path) -> dict:
    """Load a YAML file and return its content."""
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError) as e:
        raise RuntimeError(f"Failed to load standards from {path}: {e}") from e


def _merge_standards(base: dict, overlay: dict) -> dict:
    """
    Merge two standards dictionaries.

    Lists (checks, hooks) are concatenated, other values are overwritten.
    """
    result = base.copy()

    for key, value in overlay.items():
        if key in ("checks", "precommit_hooks") and isinstance(value, list):
            # Concatenate lists, avoiding duplicates by id
            existing_ids = {item.get("id") for item in result.get(key, [])}
            for item in value:
                if item.get("id") not in existing_ids:
                    result.setdefault(key, []).append(item)
                    existing_ids.add(item.get("id"))
        else:
            result[key] = value

    return result
