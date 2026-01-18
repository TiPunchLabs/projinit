"""Shared fixtures for projinit tests."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def python_cli_project(temp_dir: Path) -> Path:
    """Create a minimal Python CLI project structure."""
    project = temp_dir / "my-cli"
    project.mkdir()

    # Create pyproject.toml with CLI entry point
    pyproject = project / "pyproject.toml"
    pyproject.write_text("""[project]
name = "my-cli"
version = "0.1.0"

[project.scripts]
my-cli = "my_cli.cli:main"
""")

    # Create src structure
    src = project / "src" / "my_cli"
    src.mkdir(parents=True)
    (src / "__init__.py").write_text('__version__ = "0.1.0"')
    (src / "cli.py").write_text("def main(): pass")
    (src / "__main__.py").write_text("from .cli import main; main()")

    # Create tests directory
    tests = project / "tests"
    tests.mkdir()
    (tests / "__init__.py").write_text("")

    return project


@pytest.fixture
def python_lib_project(temp_dir: Path) -> Path:
    """Create a minimal Python library project structure."""
    project = temp_dir / "my-lib"
    project.mkdir()

    # Create pyproject.toml (no scripts)
    pyproject = project / "pyproject.toml"
    pyproject.write_text("""[project]
name = "my-lib"
version = "0.1.0"
""")

    # Create src structure
    src = project / "src" / "my_lib"
    src.mkdir(parents=True)
    (src / "__init__.py").write_text('__version__ = "0.1.0"')

    # Create tests directory
    tests = project / "tests"
    tests.mkdir()

    return project


@pytest.fixture
def node_frontend_project(temp_dir: Path) -> Path:
    """Create a minimal Node.js frontend project structure."""
    project = temp_dir / "my-frontend"
    project.mkdir()

    # Create package.json
    package_json = project / "package.json"
    package_json.write_text("""{
  "name": "my-frontend",
  "version": "0.1.0",
  "dependencies": {
    "react": "^18.0.0"
  }
}
""")

    # Create tsconfig.json
    tsconfig = project / "tsconfig.json"
    tsconfig.write_text('{"compilerOptions": {"strict": true}}')

    # Create src directory
    src = project / "src"
    src.mkdir()
    (src / "main.tsx").write_text("// Main entry")

    return project


@pytest.fixture
def infrastructure_project(temp_dir: Path) -> Path:
    """Create a minimal infrastructure project structure."""
    project = temp_dir / "my-infra"
    project.mkdir()

    # Create terraform directory
    terraform = project / "terraform"
    terraform.mkdir()
    (terraform / "main.tf").write_text('provider "aws" {}')
    (terraform / "variables.tf").write_text('variable "region" {}')

    # Create ansible directory
    ansible = project / "ansible"
    ansible.mkdir()
    (ansible / "playbook.yml").write_text("---\n- hosts: all")

    return project


@pytest.fixture
def documentation_project(temp_dir: Path) -> Path:
    """Create a minimal documentation project structure."""
    project = temp_dir / "my-docs"
    project.mkdir()

    # Create mkdocs.yml
    mkdocs = project / "mkdocs.yml"
    mkdocs.write_text("site_name: My Docs")

    # Create docs directory
    docs = project / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Welcome")

    return project


@pytest.fixture
def lab_project(temp_dir: Path) -> Path:
    """Create a minimal lab/tutorial project structure."""
    project = temp_dir / "my-lab"
    project.mkdir()

    # Create labs directory
    labs = project / "labs"
    labs.mkdir()
    (labs / "01-intro").mkdir()
    (labs / "01-intro" / "README.md").write_text("# Lab 1: Introduction")

    # Create exercises directory (important for LAB detection)
    exercises = project / "exercises"
    exercises.mkdir()
    (exercises / "01-basics.md").write_text("# Exercise 1")

    # Create solutions directory
    solutions = project / "solutions"
    solutions.mkdir()
    (solutions / "01-basics.md").write_text("# Solution 1")

    # Create docs directory
    docs = project / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Lab Documentation")

    # Create mkdocs.yml
    mkdocs = project / "mkdocs.yml"
    mkdocs.write_text("site_name: My Lab")

    return project


@pytest.fixture
def empty_project(temp_dir: Path) -> Path:
    """Create an empty project directory."""
    project = temp_dir / "empty-project"
    project.mkdir()
    return project


@pytest.fixture
def complete_python_project(python_cli_project: Path) -> Path:
    """Create a complete Python project with all standard files."""
    project = python_cli_project

    # Add README
    (project / "README.md").write_text("# My CLI\n\nA CLI tool.")

    # Add LICENSE
    (project / "LICENSE").write_text("MIT License")

    # Add .gitignore
    (project / ".gitignore").write_text("__pycache__/\n.venv/\n")

    # Add CLAUDE.md
    (project / "CLAUDE.md").write_text("# Project Guidelines")

    # Add .pre-commit-config.yaml
    (project / ".pre-commit-config.yaml").write_text("""repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
""")

    # Add doc directory
    doc = project / "doc"
    doc.mkdir()
    (doc / "README.md").write_text("# Technical Documentation")

    # Add .claude/commands directory
    claude_commands = project / ".claude" / "commands"
    claude_commands.mkdir(parents=True)
    (claude_commands / "quality.md").write_text("# Quality Check")

    return project
