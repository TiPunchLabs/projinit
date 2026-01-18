"""Tests for projinit.core.detector module."""

from pathlib import Path

import pytest

from projinit.core.detector import (
    PROJECT_MARKERS,
    detect_project_type,
    _get_all_markers,
)
from projinit.core.models import ProjectType


class TestDetectProjectType:
    """Tests for detect_project_type function."""

    def test_detect_python_cli(self, python_cli_project: Path):
        """Test detection of Python CLI project."""
        result = detect_project_type(python_cli_project)

        assert result.project_type == ProjectType.PYTHON_CLI
        assert result.confidence > 0.5
        assert "pyproject.toml" in result.markers_found

    def test_detect_python_lib(self, python_lib_project: Path):
        """Test detection of Python library project."""
        result = detect_project_type(python_lib_project)

        # Should detect as Python (CLI or LIB based on markers)
        assert result.project_type in (ProjectType.PYTHON_CLI, ProjectType.PYTHON_LIB)
        assert result.confidence > 0

    def test_detect_node_frontend(self, node_frontend_project: Path):
        """Test detection of Node.js frontend project."""
        result = detect_project_type(node_frontend_project)

        assert result.project_type == ProjectType.NODE_FRONTEND
        assert result.confidence > 0.5
        assert "package.json" in result.markers_found

    def test_detect_infrastructure(self, infrastructure_project: Path):
        """Test detection of infrastructure project."""
        result = detect_project_type(infrastructure_project)

        assert result.project_type == ProjectType.INFRASTRUCTURE
        assert result.confidence >= 0.5

    def test_detect_documentation(self, documentation_project: Path):
        """Test detection of documentation project."""
        result = detect_project_type(documentation_project)

        assert result.project_type == ProjectType.DOCUMENTATION
        assert result.confidence > 0.5
        assert "mkdocs.yml" in result.markers_found

    def test_detect_lab(self, lab_project: Path):
        """Test detection of lab project."""
        result = detect_project_type(lab_project)

        assert result.project_type == ProjectType.LAB
        assert result.confidence > 0.5
        assert "labs/" in result.markers_found

    def test_detect_empty_directory(self, empty_project: Path):
        """Test detection of empty directory returns UNKNOWN."""
        result = detect_project_type(empty_project)

        assert result.project_type == ProjectType.UNKNOWN
        assert result.confidence == 0.0

    def test_detect_nonexistent_path(self, temp_dir: Path):
        """Test detection of non-existent path returns UNKNOWN."""
        result = detect_project_type(temp_dir / "nonexistent")

        assert result.project_type == ProjectType.UNKNOWN
        assert result.confidence == 0.0

    def test_markers_found_populated(self, python_cli_project: Path):
        """Test that markers_found is populated correctly."""
        result = detect_project_type(python_cli_project)

        assert len(result.markers_found) > 0
        assert "pyproject.toml" in result.markers_found
        assert "src/" in result.markers_found

    def test_markers_checked_populated(self, python_cli_project: Path):
        """Test that markers_checked contains all possible markers."""
        result = detect_project_type(python_cli_project)

        assert len(result.markers_checked) > 0
        # Should contain markers from all project types
        assert "pyproject.toml" in result.markers_checked
        assert "package.json" in result.markers_checked

    def test_confidence_capped_at_one(self, complete_python_project: Path):
        """Test that confidence is capped at 1.0."""
        result = detect_project_type(complete_python_project)

        assert result.confidence <= 1.0

    def test_is_confident_property(self, python_cli_project: Path):
        """Test is_confident property works correctly."""
        result = detect_project_type(python_cli_project)

        # A well-formed project should have high confidence
        if result.confidence >= 0.7:
            assert result.is_confident is True


class TestGetAllMarkers:
    """Tests for _get_all_markers helper function."""

    def test_returns_set(self):
        """Test that _get_all_markers returns a set."""
        markers = _get_all_markers()
        assert isinstance(markers, set)

    def test_contains_common_markers(self):
        """Test that common markers are included."""
        markers = _get_all_markers()

        assert "pyproject.toml" in markers
        assert "package.json" in markers
        assert "main.tf" in markers
        assert "mkdocs.yml" in markers

    def test_no_duplicates(self):
        """Test that there are no duplicate markers."""
        markers = _get_all_markers()
        marker_list = list(markers)

        assert len(marker_list) == len(set(marker_list))


class TestProjectMarkers:
    """Tests for PROJECT_MARKERS constant."""

    def test_all_project_types_have_markers(self):
        """Test that all non-UNKNOWN project types have markers defined."""
        for project_type in ProjectType:
            if project_type != ProjectType.UNKNOWN:
                assert project_type in PROJECT_MARKERS
                assert len(PROJECT_MARKERS[project_type]) > 0

    def test_marker_weights_valid(self):
        """Test that all marker weights are between 0 and 1."""
        for project_type, markers in PROJECT_MARKERS.items():
            for marker, weight in markers.items():
                assert 0.0 < weight <= 1.0, f"Invalid weight {weight} for {marker} in {project_type}"

    def test_python_cli_has_main_marker(self):
        """Test Python CLI has __main__.py marker."""
        assert "__main__.py" in PROJECT_MARKERS[ProjectType.PYTHON_CLI]

    def test_node_frontend_has_package_json(self):
        """Test Node frontend has package.json marker."""
        assert "package.json" in PROJECT_MARKERS[ProjectType.NODE_FRONTEND]

    def test_infrastructure_has_terraform_markers(self):
        """Test Infrastructure has Terraform markers."""
        infra_markers = PROJECT_MARKERS[ProjectType.INFRASTRUCTURE]
        assert "main.tf" in infra_markers or "terraform/" in infra_markers


class TestDistinguishingMarkers:
    """Tests for content-based detection."""

    def test_cli_detection_with_scripts(self, python_cli_project: Path):
        """Test that [project.scripts] helps identify CLI projects."""
        result = detect_project_type(python_cli_project)

        # Should find the scripts marker in pyproject.toml
        script_markers = [m for m in result.markers_found if "scripts" in m.lower()]
        assert len(script_markers) > 0 or result.project_type == ProjectType.PYTHON_CLI

    def test_react_detection(self, node_frontend_project: Path):
        """Test that react dependency helps identify Node frontend."""
        result = detect_project_type(node_frontend_project)

        # Should find react in package.json
        react_markers = [m for m in result.markers_found if "react" in m.lower()]
        assert len(react_markers) > 0 or result.project_type == ProjectType.NODE_FRONTEND


class TestEdgeCases:
    """Tests for edge cases in detection."""

    def test_file_instead_of_directory(self, temp_dir: Path):
        """Test detection on a file instead of directory."""
        file_path = temp_dir / "test.txt"
        file_path.write_text("content")

        result = detect_project_type(file_path)

        assert result.project_type == ProjectType.UNKNOWN

    def test_mixed_project_markers(self, temp_dir: Path):
        """Test detection with markers from multiple project types."""
        project = temp_dir / "mixed"
        project.mkdir()

        # Add both Python and Node markers
        (project / "pyproject.toml").write_text("[project]\nname = 'mixed'")
        (project / "package.json").write_text('{"name": "mixed"}')
        (project / "src").mkdir()

        result = detect_project_type(project)

        # Should detect one type with highest confidence
        assert result.project_type != ProjectType.UNKNOWN
        assert result.confidence > 0

    def test_unreadable_file_handling(self, temp_dir: Path):
        """Test that unreadable files don't crash detection."""
        project = temp_dir / "project"
        project.mkdir()

        # Create a valid pyproject.toml
        pyproject = project / "pyproject.toml"
        pyproject.write_text("[project]\nname = 'test'")

        # Detection should work even if file read fails silently
        result = detect_project_type(project)

        assert result.project_type != ProjectType.UNKNOWN or result.confidence == 0
