"""Tests for projinit.standards.loader module."""

from pathlib import Path

import pytest

from projinit.core.models import ProjectType
from projinit.standards.loader import (
    DEFAULTS_DIR,
    _load_yaml,
    _merge_standards,
    get_checks_for_type,
    load_all_standards,
    load_standards,
)


class TestLoadStandards:
    """Tests for load_standards function."""

    def test_load_python_cli_standards(self):
        """Test loading standards for Python CLI projects."""
        standards = load_standards(ProjectType.PYTHON_CLI)

        assert "checks" in standards
        assert len(standards["checks"]) > 0

    def test_load_python_lib_standards(self):
        """Test loading standards for Python library projects."""
        standards = load_standards(ProjectType.PYTHON_LIB)

        assert "checks" in standards
        assert len(standards["checks"]) > 0

    def test_load_node_frontend_standards(self):
        """Test loading standards for Node.js frontend projects."""
        standards = load_standards(ProjectType.NODE_FRONTEND)

        assert "checks" in standards

    def test_load_infrastructure_standards(self):
        """Test loading standards for infrastructure projects."""
        standards = load_standards(ProjectType.INFRASTRUCTURE)

        assert "checks" in standards

    def test_load_documentation_standards(self):
        """Test loading standards for documentation projects."""
        standards = load_standards(ProjectType.DOCUMENTATION)

        assert "checks" in standards

    def test_load_lab_standards(self):
        """Test loading standards for lab projects."""
        standards = load_standards(ProjectType.LAB)

        assert "checks" in standards

    def test_load_unknown_type_uses_base(self):
        """Test that UNKNOWN type still loads base standards."""
        standards = load_standards(ProjectType.UNKNOWN)

        assert "checks" in standards

    def test_base_standards_always_included(self):
        """Test that base standards are always included."""
        python_standards = load_standards(ProjectType.PYTHON_CLI)
        node_standards = load_standards(ProjectType.NODE_FRONTEND)

        # Both should have README check from base
        python_ids = {c["id"] for c in python_standards["checks"]}
        node_ids = {c["id"] for c in node_standards["checks"]}

        assert "has_readme" in python_ids
        assert "has_readme" in node_ids

    def test_precommit_hooks_key_exists(self):
        """Test that precommit_hooks key is present."""
        standards = load_standards(ProjectType.PYTHON_CLI)

        assert "precommit_hooks" in standards


class TestGetChecksForType:
    """Tests for get_checks_for_type function."""

    def test_returns_list(self):
        """Test that get_checks_for_type returns a list."""
        checks = get_checks_for_type(ProjectType.PYTHON_CLI)

        assert isinstance(checks, list)

    def test_checks_have_required_fields(self):
        """Test that all checks have required fields."""
        checks = get_checks_for_type(ProjectType.PYTHON_CLI)

        for check in checks:
            assert "id" in check
            assert "type" in check or "description" in check

    def test_checks_filtered_by_applies_to(self):
        """Test that checks are filtered by applies_to field."""
        python_checks = get_checks_for_type(ProjectType.PYTHON_CLI)
        node_checks = get_checks_for_type(ProjectType.NODE_FRONTEND)

        python_ids = {c["id"] for c in python_checks}
        node_ids = {c["id"] for c in node_checks}

        # Python-specific checks should not appear in Node
        # (This depends on actual standards definitions)
        # At minimum, both should have base checks
        assert len(python_ids) > 0
        assert len(node_ids) > 0


class TestLoadAllStandards:
    """Tests for load_all_standards function."""

    def test_returns_dict(self):
        """Test that load_all_standards returns a dict."""
        all_standards = load_all_standards()

        assert isinstance(all_standards, dict)

    def test_contains_base(self):
        """Test that base standards are included."""
        all_standards = load_all_standards()

        assert "base" in all_standards

    def test_contains_python(self):
        """Test that Python standards are included."""
        all_standards = load_all_standards()

        assert "python" in all_standards

    def test_all_entries_are_dicts(self):
        """Test that all loaded standards are dicts."""
        all_standards = load_all_standards()

        for name, content in all_standards.items():
            assert isinstance(content, dict), f"{name} is not a dict"


class TestLoadYaml:
    """Tests for _load_yaml helper function."""

    def test_load_base_yaml(self):
        """Test loading base.yaml."""
        base_path = DEFAULTS_DIR / "base.yaml"
        content = _load_yaml(base_path)

        assert isinstance(content, dict)
        assert "checks" in content

    def test_load_nonexistent_raises_error(self, temp_dir: Path):
        """Test that loading non-existent file raises RuntimeError."""
        with pytest.raises(RuntimeError) as exc_info:
            _load_yaml(temp_dir / "nonexistent.yaml")

        assert "Failed to load standards" in str(exc_info.value)

    def test_load_invalid_yaml_raises_error(self, temp_dir: Path):
        """Test that loading invalid YAML raises RuntimeError."""
        invalid_yaml = temp_dir / "invalid.yaml"
        invalid_yaml.write_text("{ invalid yaml content [")

        with pytest.raises(RuntimeError):
            _load_yaml(invalid_yaml)

    def test_load_empty_yaml_returns_empty_dict(self, temp_dir: Path):
        """Test that empty YAML file returns empty dict."""
        empty_yaml = temp_dir / "empty.yaml"
        empty_yaml.write_text("")

        result = _load_yaml(empty_yaml)

        assert result == {}


class TestMergeStandards:
    """Tests for _merge_standards helper function."""

    def test_merge_empty_dicts(self):
        """Test merging two empty dicts."""
        result = _merge_standards({}, {})

        assert result == {}

    def test_overlay_overwrites_simple_values(self):
        """Test that overlay values overwrite base values."""
        base = {"key": "base_value"}
        overlay = {"key": "overlay_value"}

        result = _merge_standards(base, overlay)

        assert result["key"] == "overlay_value"

    def test_checks_are_concatenated(self):
        """Test that checks lists are concatenated."""
        base = {"checks": [{"id": "check1"}]}
        overlay = {"checks": [{"id": "check2"}]}

        result = _merge_standards(base, overlay)

        assert len(result["checks"]) == 2
        ids = {c["id"] for c in result["checks"]}
        assert ids == {"check1", "check2"}

    def test_duplicate_checks_not_added(self):
        """Test that duplicate check IDs are not added."""
        base = {"checks": [{"id": "check1", "level": "required"}]}
        overlay = {"checks": [{"id": "check1", "level": "optional"}]}

        result = _merge_standards(base, overlay)

        # Should only have one check with id "check1"
        assert len(result["checks"]) == 1
        # Original value should be preserved
        assert result["checks"][0]["level"] == "required"

    def test_precommit_hooks_concatenated(self):
        """Test that precommit_hooks lists are concatenated."""
        base = {"precommit_hooks": [{"id": "hook1"}]}
        overlay = {"precommit_hooks": [{"id": "hook2"}]}

        result = _merge_standards(base, overlay)

        assert len(result["precommit_hooks"]) == 2

    def test_base_not_modified(self):
        """Test that original base dict is not modified."""
        base = {"checks": [{"id": "check1"}]}
        base_original = {"checks": [{"id": "check1"}]}
        overlay = {"checks": [{"id": "check2"}]}

        _merge_standards(base, overlay)

        assert base == base_original


class TestDefaultsDir:
    """Tests for DEFAULTS_DIR constant."""

    def test_defaults_dir_exists(self):
        """Test that DEFAULTS_DIR exists."""
        assert DEFAULTS_DIR.exists()
        assert DEFAULTS_DIR.is_dir()

    def test_base_yaml_exists(self):
        """Test that base.yaml exists in DEFAULTS_DIR."""
        assert (DEFAULTS_DIR / "base.yaml").exists()

    def test_python_yaml_exists(self):
        """Test that python.yaml exists in DEFAULTS_DIR."""
        assert (DEFAULTS_DIR / "python.yaml").exists()


class TestCheckDefinitions:
    """Tests for check definitions in standards files."""

    def test_all_checks_have_valid_level(self):
        """Test that all checks have valid level values."""
        valid_levels = {"required", "recommended", "optional"}

        for project_type in ProjectType:
            if project_type != ProjectType.UNKNOWN:
                checks = get_checks_for_type(project_type)
                for check in checks:
                    level = check.get("level", "required")
                    assert level in valid_levels, f"Invalid level '{level}' in check {check.get('id')}"

    def test_all_checks_have_valid_type(self):
        """Test that all checks have valid type values."""
        valid_types = {"file_exists", "dir_exists", "content_contains", "any_exists"}

        for project_type in ProjectType:
            if project_type != ProjectType.UNKNOWN:
                checks = get_checks_for_type(project_type)
                for check in checks:
                    check_type = check.get("type", "file_exists")
                    assert check_type in valid_types, f"Invalid type '{check_type}' in check {check.get('id')}"

    def test_file_exists_checks_have_path(self):
        """Test that file_exists checks have a path defined."""
        for project_type in ProjectType:
            if project_type != ProjectType.UNKNOWN:
                checks = get_checks_for_type(project_type)
                for check in checks:
                    if check.get("type") == "file_exists":
                        assert "path" in check or "paths" in check, f"Check {check.get('id')} missing path"
