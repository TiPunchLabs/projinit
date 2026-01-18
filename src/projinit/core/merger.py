"""Intelligent file merging for projinit v2.0."""

from pathlib import Path

import yaml


def merge_yaml(existing: dict, template: dict) -> dict:
    """
    Merge a template YAML into existing YAML content.

    Preserves existing values while adding missing keys from template.
    Lists are concatenated (avoiding duplicates by key fields).

    Args:
        existing: The existing YAML content as dict.
        template: The template content to merge.

    Returns:
        Merged dictionary.
    """
    result = existing.copy()

    for key, value in template.items():
        if key not in result:
            # Key doesn't exist, add it
            result[key] = value
        elif isinstance(value, dict) and isinstance(result[key], dict):
            # Both are dicts, merge recursively
            result[key] = merge_yaml(result[key], value)
        elif isinstance(value, list) and isinstance(result[key], list):
            # Both are lists, merge intelligently
            result[key] = _merge_lists(result[key], value)
        # else: keep existing value (don't overwrite)

    return result


def _merge_lists(existing: list, template: list) -> list:
    """
    Merge two lists, avoiding duplicates.

    For lists of dicts, uses 'id', 'name', or 'repo' as unique key.
    For lists of primitives, adds missing items.
    """
    result = existing.copy()

    # Try to find a unique key for dict items
    key_fields = ["id", "name", "repo"]

    for item in template:
        if isinstance(item, dict):
            # Find unique key
            unique_key = None
            unique_value = None
            for kf in key_fields:
                if kf in item:
                    unique_key = kf
                    unique_value = item[kf]
                    break

            if unique_key:
                # Check if already exists
                exists = any(
                    isinstance(e, dict) and e.get(unique_key) == unique_value
                    for e in result
                )
                if not exists:
                    result.append(item)
            else:
                # No unique key, add if not equal to any existing
                if item not in result:
                    result.append(item)
        else:
            # Primitive value
            if item not in result:
                result.append(item)

    return result


def merge_precommit_config(existing_path: Path, hooks_to_add: list[dict]) -> str:
    """
    Merge pre-commit hooks into an existing config file.

    Args:
        existing_path: Path to existing .pre-commit-config.yaml
        hooks_to_add: List of repo definitions to add

    Returns:
        Merged YAML content as string.
    """
    try:
        content = existing_path.read_text(encoding="utf-8")
        existing = yaml.safe_load(content) or {}
    except (OSError, yaml.YAMLError):
        existing = {}

    if "repos" not in existing:
        existing["repos"] = []

    for hook_def in hooks_to_add:
        repo_url = hook_def.get("repo")
        if not repo_url:
            continue

        # Check if repo already exists
        existing_repo = None
        for repo in existing["repos"]:
            if repo.get("repo") == repo_url:
                existing_repo = repo
                break

        if existing_repo:
            # Merge hooks into existing repo
            existing_hooks = existing_repo.get("hooks", [])
            for hook in hook_def.get("hooks", []):
                hook_id = hook.get("id")
                if hook_id and not any(h.get("id") == hook_id for h in existing_hooks):
                    existing_hooks.append(hook)
            existing_repo["hooks"] = existing_hooks
            # Update rev if newer
            if hook_def.get("rev"):
                existing_repo["rev"] = hook_def["rev"]
        else:
            # Add new repo
            existing["repos"].append(hook_def)

    return yaml.dump(
        existing, default_flow_style=False, allow_unicode=True, sort_keys=False
    )


def merge_toml_section(existing_content: str, section: str, values: dict) -> str:
    """
    Add or update a TOML section in existing content.

    Simple implementation that appends section if not present.

    Args:
        existing_content: Existing TOML file content.
        section: Section name (e.g., "[tool.ruff]").
        values: Dict of values to set in section.

    Returns:
        Updated TOML content.
    """
    # Check if section exists
    if section in existing_content:
        # Section exists, don't modify
        return existing_content

    # Append section
    lines = [existing_content.rstrip(), "", section]
    for key, value in values.items():
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        elif isinstance(value, list):
            list_str = ", ".join(
                f'"{v}"' if isinstance(v, str) else str(v) for v in value
            )
            lines.append(f"{key} = [{list_str}]")
        else:
            lines.append(f"{key} = {value}")

    return "\n".join(lines) + "\n"
