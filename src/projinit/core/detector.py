"""Project type detection for projinit v2.0."""

from pathlib import Path

from projinit.core.models import DetectionResult, ProjectType

# Markers for each project type with their weight
PROJECT_MARKERS: dict[ProjectType, dict[str, float]] = {
    ProjectType.PYTHON_CLI: {
        "pyproject.toml": 0.3,
        "setup.py": 0.2,
        "src/": 0.2,
        "tests/": 0.1,
        "__main__.py": 0.2,
    },
    ProjectType.PYTHON_LIB: {
        "pyproject.toml": 0.3,
        "setup.py": 0.2,
        "src/": 0.3,
        "tests/": 0.2,
    },
    ProjectType.NODE_FRONTEND: {
        "package.json": 0.4,
        "src/": 0.2,
        "tsconfig.json": 0.2,
        "vite.config.ts": 0.1,
        "vite.config.js": 0.1,
    },
    ProjectType.INFRASTRUCTURE: {
        "main.tf": 0.4,
        "terraform/": 0.3,
        "ansible/": 0.2,
        "playbook.yml": 0.1,
        "inventory/": 0.1,
    },
    ProjectType.DOCUMENTATION: {
        "mkdocs.yml": 0.5,
        "docs/": 0.3,
        "mkdocs.yaml": 0.5,
    },
}

# Files that help distinguish between similar types
DISTINGUISHING_MARKERS: dict[str, tuple[ProjectType, float]] = {
    # CLI indicators
    "[project.scripts]": (ProjectType.PYTHON_CLI, 0.3),
    "click": (ProjectType.PYTHON_CLI, 0.1),
    "argparse": (ProjectType.PYTHON_CLI, 0.1),
    "typer": (ProjectType.PYTHON_CLI, 0.1),
    # Frontend indicators
    "react": (ProjectType.NODE_FRONTEND, 0.2),
    "vue": (ProjectType.NODE_FRONTEND, 0.2),
    "vite": (ProjectType.NODE_FRONTEND, 0.1),
}


def detect_project_type(path: Path) -> DetectionResult:
    """
    Detect the type of project at the given path.

    Args:
        path: Path to the project root directory.

    Returns:
        DetectionResult with the detected type and confidence score.
    """
    if not path.is_dir():
        return DetectionResult(
            project_type=ProjectType.UNKNOWN,
            confidence=0.0,
            markers_found=[],
            markers_checked=list(_get_all_markers()),
        )

    scores: dict[ProjectType, float] = {
        pt: 0.0 for pt in ProjectType if pt != ProjectType.UNKNOWN
    }
    markers_found: list[str] = []
    markers_checked: list[str] = list(_get_all_markers())

    # Check file/directory markers
    for project_type, markers in PROJECT_MARKERS.items():
        for marker, weight in markers.items():
            marker_path = path / marker
            if marker_path.exists():
                scores[project_type] += weight
                if marker not in markers_found:
                    markers_found.append(marker)

    # Check content-based markers in pyproject.toml
    pyproject_path = path / "pyproject.toml"
    if pyproject_path.exists():
        try:
            content = pyproject_path.read_text()
            for pattern, (project_type, weight) in DISTINGUISHING_MARKERS.items():
                if pattern in content:
                    scores[project_type] += weight
                    markers_found.append(f"pyproject.toml:{pattern}")
        except OSError:
            pass

    # Check content-based markers in package.json
    package_json_path = path / "package.json"
    if package_json_path.exists():
        try:
            content = package_json_path.read_text()
            for pattern, (project_type, weight) in DISTINGUISHING_MARKERS.items():
                if pattern in content:
                    scores[project_type] += weight
                    markers_found.append(f"package.json:{pattern}")
        except OSError:
            pass

    # Find the best match
    if not any(scores.values()):
        return DetectionResult(
            project_type=ProjectType.UNKNOWN,
            confidence=0.0,
            markers_found=markers_found,
            markers_checked=markers_checked,
        )

    best_type = max(scores, key=lambda x: scores[x])
    best_score = scores[best_type]

    # Normalize confidence (cap at 1.0)
    confidence = min(best_score, 1.0)

    return DetectionResult(
        project_type=best_type,
        confidence=confidence,
        markers_found=markers_found,
        markers_checked=markers_checked,
    )


def _get_all_markers() -> set[str]:
    """Get all marker names for reporting."""
    markers = set()
    for type_markers in PROJECT_MARKERS.values():
        markers.update(type_markers.keys())
    return markers
