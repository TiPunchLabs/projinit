"""Init command for projinit v2.0 - Create new projects from standards."""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import questionary
from jinja2 import Environment, PackageLoader
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from projinit.core.models import ProjectType

console = Console()

# Default path for secrets in pass
DEFAULT_PASS_SECRET_PATH = "projects/secrets"


def add_init_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the init subcommand to the parser."""
    init_parser = subparsers.add_parser(
        "new",
        help="Create a new project from standards (v2.0)",
        description="Initialize a new project with standard structure and configurations.",
    )
    init_parser.add_argument(
        "name",
        type=str,
        nargs="?",
        help="Project name (will be prompted if not provided)",
    )
    init_parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[pt.value for pt in ProjectType if pt != ProjectType.UNKNOWN],
        help="Project type (will be prompted if not provided)",
    )
    init_parser.add_argument(
        "-p",
        "--path",
        type=str,
        default=".",
        help="Parent directory for the new project (default: current directory)",
    )
    init_parser.add_argument(
        "--no-git",
        action="store_true",
        help="Don't initialize git repository",
    )
    init_parser.add_argument(
        "-d",
        "--description",
        type=str,
        default=None,
        help="Project description",
    )
    init_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompts",
    )
    init_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed information",
    )
    init_parser.add_argument(
        "--direnv",
        action="store_true",
        default=None,
        help="Enable direnv + pass for secrets management",
    )
    init_parser.add_argument(
        "--no-direnv",
        action="store_true",
        help="Disable direnv + pass",
    )
    init_parser.set_defaults(func=run_init)


def run_init(args: argparse.Namespace) -> int:
    """
    Run the init command.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 = success, 1 = error).
    """
    # Display header
    console.print()
    console.print(
        Panel.fit(
            "[bold]projinit new[/bold]\n[dim]Create a new project from standards[/dim]",
            border_style="blue",
        )
    )
    console.print()

    # Get project name
    project_name = args.name
    if not project_name:
        project_name = _ask_project_name()
        if not project_name:
            console.print("[dim]Cancelled[/dim]")
            return 1

    # Validate project name
    if not _is_valid_slug(project_name):
        console.print(f"[red]Invalid project name: {project_name}[/red]")
        console.print("[dim]Use lowercase letters, numbers, and hyphens only[/dim]")
        return 1

    # Get project type
    if args.type:
        project_type = ProjectType(args.type)
    else:
        project_type = _ask_project_type()
        if not project_type:
            console.print("[dim]Cancelled[/dim]")
            return 1

    # Get description
    if args.description:
        description = args.description
    elif args.yes:
        description = f"Project {project_name}"
    else:
        description = _ask_description(project_name)

    # Get direnv preference
    use_direnv = False
    if args.no_direnv:
        use_direnv = False
    elif args.direnv:
        use_direnv = True
    elif not args.yes:
        use_direnv = _ask_direnv()

    # Validate direnv requirements if enabled
    if use_direnv and not _check_direnv_requirements():
        return 1

    # Determine target directory
    parent_path = Path(args.path).resolve()
    target_dir = parent_path / project_name

    # Check if directory exists
    if target_dir.exists():
        console.print(f"[red]Directory already exists: {target_dir}[/red]")
        return 1

    # Show summary
    _display_summary(project_name, project_type, description, target_dir, use_direnv)

    # Confirm (skip if --yes)
    if not args.yes:
        confirm = questionary.confirm("Create project?", default=True).ask()
        if not confirm:
            console.print("[dim]Cancelled[/dim]")
            return 1

    # Generate project
    console.print()
    with console.status("[bold blue]Creating project...[/bold blue]"):
        success = _generate_project(
            project_name=project_name,
            project_type=project_type,
            description=description,
            target_dir=target_dir,
            use_direnv=use_direnv,
        )

    if not success:
        console.print("[red]Failed to create project[/red]")
        return 1

    # Initialize git
    if not args.no_git:
        with console.status("[bold blue]Initializing git...[/bold blue]"):
            _init_git(target_dir)

    # Allow direnv if enabled
    if use_direnv:
        with console.status("[bold blue]Configuring direnv...[/bold blue]"):
            _allow_direnv(target_dir)

    console.print()
    console.print(f"[green]Project '{project_name}' created successfully![/green]")
    _display_next_steps(project_name, project_type, use_direnv)

    return 0


def _ask_project_name() -> str | None:
    """Prompt for project name."""
    return questionary.text(
        "Project name:",
        validate=lambda val: _is_valid_slug(val)
        or "Use lowercase letters, numbers, and hyphens",
    ).ask()


def _ask_project_type() -> ProjectType | None:
    """Prompt for project type."""
    choices = [
        questionary.Choice("Python CLI Application", value=ProjectType.PYTHON_CLI),
        questionary.Choice("Python Library", value=ProjectType.PYTHON_LIB),
        questionary.Choice(
            "Node.js Frontend (React/Vue)", value=ProjectType.NODE_FRONTEND
        ),
        questionary.Choice(
            "Infrastructure (Terraform + Ansible)", value=ProjectType.INFRASTRUCTURE
        ),
        questionary.Choice("Documentation (MkDocs)", value=ProjectType.DOCUMENTATION),
        questionary.Choice("Lab/Tutorial/Dojo", value=ProjectType.LAB),
    ]
    return questionary.select("Project type:", choices=choices).ask()


def _ask_description(project_name: str) -> str:
    """Prompt for project description."""
    description = questionary.text("Description:", default="").ask()
    return description if description else f"Project {project_name}"


def _ask_direnv() -> bool:
    """Prompt for direnv + pass activation."""
    return (
        questionary.confirm(
            "Enable direnv + pass for secrets management?",
            default=False,
        ).ask()
        or False
    )


def _check_direnv_requirements() -> bool:
    """Check if direnv and pass are installed."""
    # Check direnv
    if shutil.which("direnv") is None:
        console.print("[red]direnv is not installed[/red]")
        console.print("[dim]Install with: sudo apt install direnv[/dim]")
        console.print('[dim]Then add to your shell: eval "$(direnv hook bash)"[/dim]')
        return False

    # Check pass
    if shutil.which("pass") is None:
        console.print("[red]pass (password-store) is not installed[/red]")
        console.print("[dim]Install with: sudo apt install pass[/dim]")
        return False

    return True


def _is_valid_slug(name: str) -> bool:
    """Check if name is a valid project slug."""
    return bool(re.match(r"^[a-z][a-z0-9-]*$", name))


def _display_summary(
    project_name: str,
    project_type: ProjectType,
    description: str,
    target_dir: Path,
    use_direnv: bool = False,
) -> None:
    """Display project summary before creation."""
    console.print()
    console.print("[bold]Project Summary:[/bold]")
    console.print(f"  Name: [cyan]{project_name}[/cyan]")
    console.print(f"  Type: [cyan]{project_type.display_name}[/cyan]")
    console.print(f"  Path: [cyan]{target_dir}[/cyan]")
    console.print(f"  Description: [cyan]{description}[/cyan]")
    console.print(f"  Direnv: [cyan]{'yes' if use_direnv else 'no'}[/cyan]")
    console.print()

    # Show files that will be created
    files = _get_files_for_type(project_type)
    table = Table(title="Files to create", show_header=False)
    table.add_column("File")
    for f in files:
        table.add_row(f"  {f}")
    console.print(table)
    console.print()


def _get_files_for_type(project_type: ProjectType) -> list[str]:
    """Get list of files that will be created for a project type."""
    common = [
        "README.md",
        "LICENSE",
        ".gitignore",
        "CLAUDE.md",
        ".pre-commit-config.yaml",
        ".claude/commands/quality.md",
        ".claude/commands/commit.md",
        ".claude/commands/lint.md",
        "doc/README.md",
        "doc/architecture.md",
        "doc/development.md",
        "doc/configuration.md",
    ]

    type_specific = {
        ProjectType.PYTHON_CLI: [
            "pyproject.toml",
            "src/<name>/__init__.py",
            "src/<name>/cli.py",
            "tests/",
        ],
        ProjectType.PYTHON_LIB: ["pyproject.toml", "src/<name>/__init__.py", "tests/"],
        ProjectType.NODE_FRONTEND: ["package.json", "tsconfig.json", "src/", "public/"],
        ProjectType.INFRASTRUCTURE: [
            "terraform/main.tf",
            "terraform/variables.tf",
            "ansible/playbook.yml",
        ],
        ProjectType.DOCUMENTATION: ["mkdocs.yml", "pyproject.toml", "docs/index.md"],
        ProjectType.LAB: ["labs/", "docs/index.md", "mkdocs.yml"],
    }

    return common + type_specific.get(project_type, [])


def _generate_project(
    project_name: str,
    project_type: ProjectType,
    description: str,
    target_dir: Path,
    use_direnv: bool = False,
) -> bool:
    """Generate project files based on type."""
    try:
        env = Environment(
            loader=PackageLoader("projinit", "templates"),
            keep_trailing_newline=True,
        )

        # Common context
        project_name_snake = project_name.replace("-", "_")
        context = {
            "project_name": project_name,
            "project_name_snake": project_name_snake,
            "project_type": project_type.value,
            "project_type_display": project_type.display_name,
            "description": description,
            "year": datetime.now().year,
            "python_version": "3.10",
            "use_direnv": use_direnv,
        }

        # Create base directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Generate common files
        _generate_common_files(env, target_dir, context, project_type, use_direnv)

        # Generate type-specific files
        if project_type in (ProjectType.PYTHON_CLI, ProjectType.PYTHON_LIB):
            _generate_python_project(env, target_dir, context, project_type)
        elif project_type == ProjectType.NODE_FRONTEND:
            _generate_node_project(env, target_dir, context)
        elif project_type == ProjectType.INFRASTRUCTURE:
            _generate_infra_project(env, target_dir, context)
        elif project_type == ProjectType.DOCUMENTATION:
            _generate_docs_project(env, target_dir, context)
        elif project_type == ProjectType.LAB:
            _generate_lab_project(env, target_dir, context)

        return True
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False


def _generate_common_files(
    env: Environment,
    target_dir: Path,
    context: dict,
    project_type: ProjectType,
    use_direnv: bool = False,
) -> None:
    """Generate files common to all project types."""
    # README.md
    template = env.get_template("README.md.j2")
    (target_dir / "README.md").write_text(template.render(**context))

    # LICENSE
    template = env.get_template("LICENSE.j2")
    (target_dir / "LICENSE").write_text(template.render(**context))

    # CLAUDE.md
    template = env.get_template("CLAUDE.md.j2")
    (target_dir / "CLAUDE.md").write_text(template.render(**context))

    # .gitignore - select appropriate technologies
    tech_map = {
        ProjectType.PYTHON_CLI: ["python"],
        ProjectType.PYTHON_LIB: ["python"],
        ProjectType.NODE_FRONTEND: ["node"],
        ProjectType.INFRASTRUCTURE: ["terraform", "ansible"],
        ProjectType.DOCUMENTATION: ["python"],
    }
    technologies = tech_map.get(project_type, []) + ["ide"]

    gitignore_content = env.get_template("gitignore/_common.j2").render()
    for tech in technologies:
        try:
            gitignore_content += env.get_template(f"gitignore/{tech}.j2").render()
        except Exception:
            pass
    (target_dir / ".gitignore").write_text(gitignore_content)

    # .pre-commit-config.yaml
    precommit_content = env.get_template("precommit/_header.j2").render()
    for tech in technologies:
        if tech == "ide":
            continue
        try:
            precommit_content += env.get_template(f"precommit/{tech}.j2").render()
        except Exception:
            pass
    (target_dir / ".pre-commit-config.yaml").write_text(precommit_content)

    # .envrc for direnv + pass
    if use_direnv:
        _generate_envrc(target_dir, context)

    # .claude/commands/
    _generate_claude_commands(env, target_dir, context, project_type)

    # doc/ technical documentation
    _generate_technical_docs(env, target_dir, context, project_type)


def _generate_python_project(
    env: Environment,
    target_dir: Path,
    context: dict,
    project_type: ProjectType,
) -> None:
    """Generate Python project files."""
    project_name_snake = context["project_name_snake"]

    # pyproject.toml
    template = env.get_template("pyproject.toml.j2")
    (target_dir / "pyproject.toml").write_text(template.render(**context))

    # Create src directory structure
    src_dir = target_dir / "src" / project_name_snake
    src_dir.mkdir(parents=True, exist_ok=True)

    # __init__.py
    (src_dir / "__init__.py").write_text(
        f'"""{context["project_name"]} package."""\n\n__version__ = "0.1.0"\n'
    )

    # cli.py for CLI projects
    if project_type == ProjectType.PYTHON_CLI:
        cli_content = '''"""Command-line interface."""

import argparse


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="{name}",
        description="{description}",
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()

    print("Hello from {name}!")


if __name__ == "__main__":
    main()
'''.format(name=context["project_name"], description=context["description"])
        (src_dir / "cli.py").write_text(cli_content)

    # Create tests directory
    tests_dir = target_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / f"test_{project_name_snake}.py").write_text(
        f'''"""Tests for {context["project_name"]}."""

def test_import():
    """Test that the package can be imported."""
    import {project_name_snake}
    assert {project_name_snake}.__version__ == "0.1.0"
'''
    )


def _generate_node_project(env: Environment, target_dir: Path, context: dict) -> None:
    """Generate Node.js frontend project files."""
    context["framework"] = "react"  # Default to React

    # package.json
    template = env.get_template("package.json.j2")
    (target_dir / "package.json").write_text(template.render(**context))

    # tsconfig.json
    tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""
    (target_dir / "tsconfig.json").write_text(tsconfig)

    # Create src directory
    src_dir = target_dir / "src"
    src_dir.mkdir(exist_ok=True)

    # Basic index.tsx
    project_name = context["project_name"]
    (src_dir / "main.tsx").write_text(f"""import React from 'react'
import ReactDOM from 'react-dom/client'

function App() {{
  return (
    <div>
      <h1>Hello from {project_name}!</h1>
    </div>
  )
}}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""")

    # Create public directory
    public_dir = target_dir / "public"
    public_dir.mkdir(exist_ok=True)

    # index.html
    (target_dir / "index.html").write_text(f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{context["project_name"]}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""")

    # vite.config.ts
    (target_dir / "vite.config.ts").write_text("""import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
""")


def _generate_infra_project(env: Environment, target_dir: Path, context: dict) -> None:
    """Generate Infrastructure project files."""
    # Create terraform directory
    tf_dir = target_dir / "terraform"
    tf_dir.mkdir(exist_ok=True)

    # Generate terraform files using existing templates
    tf_templates = [
        ("main.tf.j2", "main.tf"),
        ("variables.tf.j2", "variables.tf"),
        ("outputs.tf.j2", "outputs.tf"),
        ("versions.tf.j2", "versions.tf"),
    ]
    for template_name, output_name in tf_templates:
        try:
            template = env.get_template(template_name)
            (tf_dir / output_name).write_text(template.render(**context))
        except Exception:
            # Create minimal file if template not available
            (tf_dir / output_name).write_text(f"# {output_name}\n")

    # Create ansible directory
    ansible_dir = target_dir / "ansible"
    ansible_dir.mkdir(exist_ok=True)
    (ansible_dir / "inventory").mkdir(exist_ok=True)

    # Basic playbook
    (ansible_dir / "playbook.yml").write_text(f"""---
- name: {context["project_name"]} playbook
  hosts: all
  become: true

  tasks:
    - name: Example task
      ansible.builtin.debug:
        msg: "Hello from {context["project_name"]}!"
""")

    # Inventory file
    (ansible_dir / "inventory" / "hosts.yml").write_text("""---
all:
  hosts:
    localhost:
      ansible_connection: local
""")


def _generate_docs_project(env: Environment, target_dir: Path, context: dict) -> None:
    """Generate Documentation project files."""
    # pyproject.toml for docs
    template = env.get_template("pyproject-docs.toml.j2")
    (target_dir / "pyproject.toml").write_text(template.render(**context))

    # mkdocs.yml
    template = env.get_template("mkdocs.yml.j2")
    (target_dir / "mkdocs.yml").write_text(template.render(**context))

    # Create docs directory
    docs_dir = target_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    # index.md
    (docs_dir / "index.md").write_text(f"""# {context["project_name"]}

{context["description"]}

## Getting Started

Welcome to the {context["project_name"]} documentation.

## Quick Start

```bash
# Install dependencies
uv sync

# Serve documentation locally
uv run mkdocs serve
```

## Structure

- `docs/` - Documentation source files
- `mkdocs.yml` - MkDocs configuration
""")


def _generate_lab_project(env: Environment, target_dir: Path, context: dict) -> None:
    """Generate Lab/Tutorial/Dojo project files."""
    # pyproject.toml for docs
    template = env.get_template("pyproject-docs.toml.j2")
    (target_dir / "pyproject.toml").write_text(template.render(**context))

    # mkdocs.yml
    template = env.get_template("mkdocs.yml.j2")
    (target_dir / "mkdocs.yml").write_text(template.render(**context))

    # Create labs directory structure
    labs_dir = target_dir / "labs"
    labs_dir.mkdir(exist_ok=True)

    # Create example lab
    lab01_dir = labs_dir / "01-getting-started"
    lab01_dir.mkdir(exist_ok=True)

    (lab01_dir / "README.md").write_text(f"""# Lab 01: Getting Started

## Objectives

- Understand the basics of {context["project_name"]}
- Complete your first exercise

## Prerequisites

- Basic knowledge required (list here)

## Exercises

### Exercise 1: Hello World

**Task**: Create a simple hello world example.

**Expected outcome**: A working hello world program.

## Solutions

See the `solutions/` directory for reference implementations.
""")

    # Create solutions directory
    solutions_dir = target_dir / "solutions"
    solutions_dir.mkdir(exist_ok=True)
    (solutions_dir / "01-getting-started" / ".gitkeep").parent.mkdir(
        parents=True, exist_ok=True
    )
    (solutions_dir / "01-getting-started" / ".gitkeep").write_text("")

    # Create docs directory for mkdocs
    docs_dir = target_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    (docs_dir / "index.md").write_text(f"""# {context["project_name"]}

{context["description"]}

## Overview

This is a lab/tutorial project for hands-on learning.

## Getting Started

1. Read the lab instructions in `labs/`
2. Complete the exercises
3. Check your work against `solutions/`

## Labs

- [Lab 01: Getting Started](labs/01-getting-started/README.md)

## Prerequisites

List prerequisites here.
""")


def _generate_envrc(target_dir: Path, context: dict) -> None:
    """Generate .envrc file for direnv + pass integration."""
    project_name = context["project_name"]
    secret_path = f"{DEFAULT_PASS_SECRET_PATH}/{project_name}"

    envrc_content = f"""# Environment variables managed by direnv + pass
# Secrets are stored in pass at: {secret_path}

# Example: Load a secret from pass
# export API_KEY=$(pass show {secret_path}/api-key)

# Project-specific environment
export PROJECT_NAME="{project_name}"

# Add project bin to PATH (if applicable)
# PATH_add bin

# Python virtual environment (uncomment if using venv)
# layout python3
"""
    (target_dir / ".envrc").write_text(envrc_content)


def _generate_claude_commands(
    env: Environment,
    target_dir: Path,
    context: dict,
    project_type: ProjectType,
) -> None:
    """Generate .claude/commands/ directory with standard commands."""
    commands_dir = target_dir / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)

    # Commands common to all project types
    common_commands = ["quality.md", "commit.md", "lint.md"]

    for cmd in common_commands:
        template_name = f"commands/{cmd}.j2"
        try:
            template = env.get_template(template_name)
            (commands_dir / cmd).write_text(template.render(**context))
        except Exception:
            pass


def _generate_technical_docs(
    env: Environment,
    target_dir: Path,
    context: dict,
    project_type: ProjectType,
) -> None:
    """Generate doc/ directory with technical documentation."""
    doc_dir = target_dir / "doc"
    doc_dir.mkdir(parents=True, exist_ok=True)

    # Documentation files to generate
    doc_files = ["README.md", "architecture.md", "development.md", "configuration.md"]

    for doc_file in doc_files:
        template_name = f"doc/{doc_file}.j2"
        try:
            template = env.get_template(template_name)
            (doc_dir / doc_file).write_text(template.render(**context))
        except Exception:
            pass


def _allow_direnv(target_dir: Path) -> bool:
    """Allow direnv for the project directory."""
    try:
        subprocess.run(
            ["direnv", "allow"],
            cwd=target_dir,
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[yellow]Warning: direnv allow failed: {e}[/yellow]")
        return False


def _init_git(target_dir: Path) -> bool:
    """Initialize git repository."""
    try:
        subprocess.run(
            ["git", "init", "-b", "main"],
            cwd=target_dir,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "add", "."], cwd=target_dir, capture_output=True, check=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit - project scaffolding"],
            cwd=target_dir,
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def _display_next_steps(
    project_name: str, project_type: ProjectType, use_direnv: bool = False
) -> None:
    """Display next steps after project creation."""
    console.print()
    console.print("[bold]Next steps:[/bold]")
    console.print()
    console.print(f"  [dim]1.[/dim] cd {project_name}")

    step = 2
    if use_direnv:
        console.print(
            f"  [dim]{step}.[/dim] Configure secrets in pass: "
            f"pass insert {DEFAULT_PASS_SECRET_PATH}/{project_name}/api-key"
        )
        step += 1

    if project_type in (ProjectType.PYTHON_CLI, ProjectType.PYTHON_LIB):
        console.print(f"  [dim]{step}.[/dim] uv sync")
        console.print(f"  [dim]{step + 1}.[/dim] uv run pytest")
    elif project_type == ProjectType.NODE_FRONTEND:
        console.print(f"  [dim]{step}.[/dim] npm install")
        console.print(f"  [dim]{step + 1}.[/dim] npm run dev")
    elif project_type == ProjectType.INFRASTRUCTURE:
        console.print(f"  [dim]{step}.[/dim] cd terraform && terraform init")
        console.print(f"  [dim]{step + 1}.[/dim] terraform plan")
    elif project_type == ProjectType.DOCUMENTATION:
        console.print(f"  [dim]{step}.[/dim] uv sync")
        console.print(f"  [dim]{step + 1}.[/dim] uv run mkdocs serve")
    elif project_type == ProjectType.LAB:
        console.print(f"  [dim]{step}.[/dim] uv sync")
        console.print(f"  [dim]{step + 1}.[/dim] uv run mkdocs serve")
        console.print(f"  [dim]{step + 2}.[/dim] Start with labs/01-getting-started/")

    console.print()


def main() -> None:
    """Standalone entry point."""
    parser = argparse.ArgumentParser(
        prog="projinit new", description="Create a new project"
    )
    parser.add_argument("name", type=str, nargs="?", help="Project name")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[pt.value for pt in ProjectType if pt != ProjectType.UNKNOWN],
        help="Project type",
    )
    parser.add_argument("-p", "--path", type=str, default=".", help="Parent directory")
    parser.add_argument("--no-git", action="store_true", help="Don't initialize git")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()
    sys.exit(run_init(args))


if __name__ == "__main__":
    main()
