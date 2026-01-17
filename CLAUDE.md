# projinit Development Guidelines

Version: 2.0.0 | Last updated: 2025-01

## Overview

projinit is a project lifecycle management CLI tool that:
- **Audits** project conformity against defined standards
- **Updates** projects to fix non-conformities automatically
- **Creates** new projects following best practices
- **Configures** standards through YAML configuration

## Project Structure

```text
src/projinit/
├── __init__.py           # Version info
├── main_cli.py           # Main CLI entry point
├── cli/                  # Command implementations
│   ├── check_cmd.py      # projinit check
│   ├── update_cmd.py     # projinit update
│   ├── init_cmd.py       # projinit new
│   └── config_cmd.py     # projinit config
├── core/                 # Business logic
│   ├── models.py         # Data models (ProjectType, CheckResult, etc.)
│   ├── detector.py       # Project type auto-detection
│   ├── checker.py        # Conformity checking
│   ├── reporter.py       # Report generation (text, json, markdown)
│   ├── updater.py        # Automatic fixes
│   ├── merger.py         # YAML/TOML smart merging
│   └── config.py         # Configuration loading
├── standards/            # Standards definitions
│   ├── loader.py         # Standards loading with config overrides
│   └── defaults/         # Default standards YAML files
│       ├── base.yaml
│       ├── python.yaml
│       ├── node.yaml
│       ├── infra.yaml
│       └── documentation.yaml
└── templates/            # Jinja2 templates for project generation
    ├── README.md.j2
    ├── CLAUDE.md.j2
    ├── pyproject.toml.j2
    └── ...
```

## Commands

```bash
# Development
uv sync                           # Install dependencies
uv run projinit --version         # Run CLI

# Testing
uv run projinit check .           # Check this project
uv run projinit check -v          # Verbose mode

# Linting
uvx ruff check src/               # Run linter
uvx ruff format src/              # Format code
```

## Technologies

- **Python**: >= 3.10
- **CLI Framework**: argparse (stdlib) + questionary (interactive)
- **Output**: rich (tables, panels, progress bars)
- **Templates**: Jinja2
- **Data**: PyYAML, toml
- **Package Manager**: uv

## Code Style

- Follow PEP 8 with ruff enforcement
- Type hints required for all public APIs
- Docstrings in Google format
- Maximum line length: 100 characters

## Key Concepts

### Project Types
- `python-cli`: CLI applications with src/ layout
- `python-lib`: Libraries with py.typed marker
- `node-frontend`: React/Vue/vanilla TypeScript
- `infrastructure`: Terraform + Ansible
- `documentation`: MkDocs sites

### Check Levels
- `required`: Must pass for compliance
- `recommended`: Best practices
- `optional`: Nice to have

### Configuration Hierarchy
1. Defaults (built-in)
2. Global: `~/.config/projinit/config.yaml`
3. Local: `.projinit.yaml` (project root)

## Adding New Checks

1. Add check definition to `standards/defaults/*.yaml`:
```yaml
- id: my_new_check
  type: file_exists  # or dir_exists, content_contains, any_exists
  path: some/file.txt
  level: recommended
  description: "Description of the check"
  template: some-template.j2  # Optional: for auto-fix
```

2. If new check type needed, add handler in `core/checker.py`

3. If template needed for auto-fix, add to `templates/`

## Adding New Project Types

1. Create `standards/defaults/<type>.yaml` with checks
2. Add enum value in `core/models.py::ProjectType`
3. Update detection markers in `core/detector.py`
4. Add templates to `templates/`
