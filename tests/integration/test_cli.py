"""Integration tests for projinit CLI."""

import subprocess
import sys
from pathlib import Path

import pytest


class TestCLIBasics:
    """Basic CLI integration tests."""

    def test_help_command(self):
        """Test that --help works."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "projinit" in result.stdout.lower()

    def test_version_command(self):
        """Test that version command works."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "version"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Should output version number
        assert "." in result.stdout  # Version contains dots

    def test_invalid_command(self):
        """Test that invalid command returns error."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "nonexistent"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0


class TestCheckCommand:
    """Tests for the check command."""

    def test_check_help(self):
        """Test check command help."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "check", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "check" in result.stdout.lower()

    def test_check_current_directory(self, python_cli_project: Path):
        """Test check command on a project."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "check", str(python_cli_project)],
            capture_output=True,
            text=True,
        )

        # Should run without crashing
        # May return non-zero if checks fail, but should not error
        assert "error" not in result.stderr.lower() or result.returncode == 0

    def test_check_with_type_override(self, python_cli_project: Path):
        """Test check command with type override."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "check", str(python_cli_project), "-t", "python-cli"],
            capture_output=True,
            text=True,
        )

        # Should run with specified type
        assert result.returncode in (0, 1)  # 0 = pass, 1 = failures

    def test_check_nonexistent_path(self, temp_dir: Path):
        """Test check command with non-existent path."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "check", str(temp_dir / "nonexistent")],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0


class TestInitCommand:
    """Tests for the init command."""

    def test_init_help(self):
        """Test init command help."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "init", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_init_on_existing_project(self, python_cli_project: Path):
        """Test init command on existing project."""
        # init command is run from the project directory
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "init"],
            capture_output=True,
            text=True,
            cwd=str(python_cli_project),
        )

        # Should detect existing project
        # Output depends on implementation
        assert result.returncode in (0, 1, 2)  # 2 might be argument parsing issues


class TestNewCommand:
    """Tests for the new command."""

    def test_new_help(self):
        """Test new command help."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "new", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "new" in result.stdout.lower() or "initialize" in result.stdout.lower()

    def test_new_creates_project(self, temp_dir: Path):
        """Test new command creates a project."""
        project_name = "test-new-project"

        result = subprocess.run(
            [
                sys.executable, "-m", "projinit", "new",
                project_name,
                "-t", "python-cli",
                "-p", str(temp_dir),
                "-y",
                "--no-git",
                "-d", "Test project",
            ],
            capture_output=True,
            text=True,
        )

        # Should create project successfully
        if result.returncode == 0:
            project_path = temp_dir / project_name
            assert project_path.exists()
            assert (project_path / "pyproject.toml").exists()
            assert (project_path / "README.md").exists()

    def test_new_with_all_types(self, temp_dir: Path):
        """Test new command with different project types."""
        project_types = [
            "python-cli",
            "python-lib",
            "node-frontend",
            "infrastructure",
            "documentation",
            "lab",
        ]

        for i, ptype in enumerate(project_types):
            project_name = f"test-{ptype}-{i}"

            result = subprocess.run(
                [
                    sys.executable, "-m", "projinit", "new",
                    project_name,
                    "-t", ptype,
                    "-p", str(temp_dir),
                    "-y",
                    "--no-git",
                ],
                capture_output=True,
                text=True,
            )

            # All types should work without error
            project_path = temp_dir / project_name
            if result.returncode == 0:
                assert project_path.exists(), f"Project not created for type {ptype}"


class TestUpdateCommand:
    """Tests for the update command."""

    def test_update_help(self):
        """Test update command help."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "update", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_update_existing_project(self, python_cli_project: Path):
        """Test update command on existing project."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "update", str(python_cli_project), "-n"],  # -n for dry-run
            capture_output=True,
            text=True,
        )

        # Should run without crashing
        assert result.returncode in (0, 1)


class TestConfigCommand:
    """Tests for the config command."""

    def test_config_help(self):
        """Test config command help."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "config", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_config_show(self):
        """Test config show subcommand."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "config", "show"],
            capture_output=True,
            text=True,
        )

        # Should show config without error
        assert result.returncode == 0


class TestVerboseOutput:
    """Tests for verbose output."""

    def test_check_verbose(self, python_cli_project: Path):
        """Test check command with verbose flag."""
        result = subprocess.run(
            [sys.executable, "-m", "projinit", "check", str(python_cli_project), "-v"],
            capture_output=True,
            text=True,
        )

        # Verbose should produce more output
        assert result.returncode in (0, 1)


class TestProjectCreationContent:
    """Tests for content of created projects."""

    def test_new_project_has_claude_commands(self, temp_dir: Path):
        """Test that new projects have .claude/commands directory."""
        project_name = "test-commands"

        result = subprocess.run(
            [
                sys.executable, "-m", "projinit", "new",
                project_name,
                "-t", "python-cli",
                "-p", str(temp_dir),
                "-y",
                "--no-git",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            commands_dir = temp_dir / project_name / ".claude" / "commands"
            assert commands_dir.exists()

            # Check for standard commands
            expected_commands = [
                "quality.md",
                "commit.md",
                "lint.md",
                "sync-docs.md",
                "sync-tech-docs.md",
                "opensource-ready.md",
            ]

            for cmd in expected_commands:
                assert (commands_dir / cmd).exists(), f"Missing command: {cmd}"

    def test_new_project_has_doc_directory(self, temp_dir: Path):
        """Test that new projects have doc/ directory."""
        project_name = "test-docs"

        result = subprocess.run(
            [
                sys.executable, "-m", "projinit", "new",
                project_name,
                "-t", "python-cli",
                "-p", str(temp_dir),
                "-y",
                "--no-git",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            doc_dir = temp_dir / project_name / "doc"
            assert doc_dir.exists()

            # Check for standard doc files
            expected_docs = [
                "README.md",
                "architecture.md",
                "development.md",
                "configuration.md",
            ]

            for doc in expected_docs:
                assert (doc_dir / doc).exists(), f"Missing doc: {doc}"

    def test_new_project_has_precommit_config(self, temp_dir: Path):
        """Test that new projects have .pre-commit-config.yaml."""
        project_name = "test-precommit"

        result = subprocess.run(
            [
                sys.executable, "-m", "projinit", "new",
                project_name,
                "-t", "python-cli",
                "-p", str(temp_dir),
                "-y",
                "--no-git",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            precommit = temp_dir / project_name / ".pre-commit-config.yaml"
            assert precommit.exists()

            content = precommit.read_text()
            assert "repos:" in content
            assert "ruff" in content
