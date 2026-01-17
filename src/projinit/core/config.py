"""Configuration management for projinit v2.0.

Supports hierarchical configuration:
1. Built-in defaults (lowest priority)
2. Global config: ~/.config/projinit/config.yaml
3. Local config: .projinit.yaml in project root (highest priority)
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Default config locations
GLOBAL_CONFIG_DIR = Path.home() / ".config" / "projinit"
GLOBAL_CONFIG_FILE = GLOBAL_CONFIG_DIR / "config.yaml"
LOCAL_CONFIG_FILE = ".projinit.yaml"


@dataclass
class AuthorConfig:
    """Author information for project templates."""

    name: str | None = None
    email: str | None = None


@dataclass
class StandardsConfig:
    """Standards customization configuration."""

    # Override check levels (id -> level)
    check_overrides: dict[str, str] = field(default_factory=dict)
    # Additional checks to add
    extra_checks: list[dict] = field(default_factory=list)
    # Checks to disable
    disabled_checks: list[str] = field(default_factory=list)
    # Custom pre-commit hooks to add
    extra_precommit_hooks: list[dict] = field(default_factory=list)


@dataclass
class TemplatesConfig:
    """Custom templates configuration."""

    # Path to custom templates directory
    templates_dir: Path | None = None
    # Template overrides (template_name -> custom_path)
    overrides: dict[str, str] = field(default_factory=dict)


@dataclass
class ProjInitConfig:
    """Main projinit configuration."""

    # Author information
    author: AuthorConfig = field(default_factory=AuthorConfig)
    # Default Python version
    python_version: str = "3.10"
    # Default license
    default_license: str = "MIT"
    # Standards configuration
    standards: StandardsConfig = field(default_factory=StandardsConfig)
    # Templates configuration
    templates: TemplatesConfig = field(default_factory=TemplatesConfig)
    # Source of this config (for debugging)
    _source: str = "defaults"


def load_config(project_path: Path | None = None) -> ProjInitConfig:
    """
    Load configuration with hierarchy: defaults < global < local.

    Args:
        project_path: Path to project root for local config. If None, uses cwd.

    Returns:
        Merged configuration.
    """
    config = ProjInitConfig()

    # Load global config
    if GLOBAL_CONFIG_FILE.exists():
        global_config = _load_yaml_config(GLOBAL_CONFIG_FILE)
        config = _merge_config(config, global_config)
        config._source = f"global ({GLOBAL_CONFIG_FILE})"

    # Load local config
    if project_path is None:
        project_path = Path.cwd()

    local_config_path = project_path / LOCAL_CONFIG_FILE
    if local_config_path.exists():
        local_config = _load_yaml_config(local_config_path)
        config = _merge_config(config, local_config)
        config._source = f"local ({local_config_path})"

    return config


def save_global_config(config: ProjInitConfig) -> None:
    """
    Save configuration to global config file.

    Args:
        config: Configuration to save.
    """
    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    data = _config_to_dict(config)
    with open(GLOBAL_CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_config_paths() -> dict[str, Path]:
    """Get paths to configuration files."""
    return {
        "global": GLOBAL_CONFIG_FILE,
        "local": Path.cwd() / LOCAL_CONFIG_FILE,
    }


def _load_yaml_config(path: Path) -> dict:
    """Load configuration from YAML file."""
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _merge_config(base: ProjInitConfig, overlay: dict) -> ProjInitConfig:
    """Merge overlay dict into base config."""
    # Author
    if "author" in overlay:
        author = overlay["author"]
        if isinstance(author, dict):
            base.author.name = author.get("name", base.author.name)
            base.author.email = author.get("email", base.author.email)

    # Simple values
    if "python_version" in overlay:
        base.python_version = str(overlay["python_version"])
    if "default_license" in overlay:
        base.default_license = overlay["default_license"]

    # Standards
    if "standards" in overlay:
        standards = overlay["standards"]
        if isinstance(standards, dict):
            if "check_overrides" in standards:
                base.standards.check_overrides.update(standards["check_overrides"])
            if "extra_checks" in standards:
                base.standards.extra_checks.extend(standards["extra_checks"])
            if "disabled_checks" in standards:
                base.standards.disabled_checks.extend(standards["disabled_checks"])
            if "extra_precommit_hooks" in standards:
                base.standards.extra_precommit_hooks.extend(standards["extra_precommit_hooks"])

    # Templates
    if "templates" in overlay:
        templates = overlay["templates"]
        if isinstance(templates, dict):
            if "templates_dir" in templates:
                base.templates.templates_dir = Path(templates["templates_dir"])
            if "overrides" in templates:
                base.templates.overrides.update(templates["overrides"])

    return base


def _config_to_dict(config: ProjInitConfig) -> dict:
    """Convert config to dictionary for saving."""
    data = {}

    # Author
    if config.author.name or config.author.email:
        data["author"] = {}
        if config.author.name:
            data["author"]["name"] = config.author.name
        if config.author.email:
            data["author"]["email"] = config.author.email

    # Simple values
    if config.python_version != "3.10":
        data["python_version"] = config.python_version
    if config.default_license != "MIT":
        data["default_license"] = config.default_license

    # Standards
    standards_data = {}
    if config.standards.check_overrides:
        standards_data["check_overrides"] = config.standards.check_overrides
    if config.standards.extra_checks:
        standards_data["extra_checks"] = config.standards.extra_checks
    if config.standards.disabled_checks:
        standards_data["disabled_checks"] = config.standards.disabled_checks
    if config.standards.extra_precommit_hooks:
        standards_data["extra_precommit_hooks"] = config.standards.extra_precommit_hooks
    if standards_data:
        data["standards"] = standards_data

    # Templates
    templates_data = {}
    if config.templates.templates_dir:
        templates_data["templates_dir"] = str(config.templates.templates_dir)
    if config.templates.overrides:
        templates_data["overrides"] = config.templates.overrides
    if templates_data:
        data["templates"] = templates_data

    return data


def generate_example_config() -> str:
    """Generate an example configuration file content."""
    return '''# projinit configuration
# Place this file at ~/.config/projinit/config.yaml (global)
# or .projinit.yaml in your project root (local override)

# Author information for generated files
author:
  name: "Your Name"
  email: "your.email@example.com"

# Default Python version for new projects
python_version: "3.10"

# Default license
default_license: "MIT"

# Standards customization
standards:
  # Override check levels (id: level)
  # Levels: required, recommended, optional
  check_overrides:
    # has_claude_md: required  # Make CLAUDE.md mandatory

  # Disable specific checks
  disabled_checks: []
    # - has_py_typed  # Don't check for py.typed marker

  # Add custom pre-commit hooks
  extra_precommit_hooks: []
    # - repo: https://github.com/example/hook
    #   rev: v1.0.0
    #   hooks:
    #     - id: example-hook

# Custom templates
templates:
  # Path to custom templates directory
  # templates_dir: ~/.config/projinit/templates

  # Override specific templates
  overrides: {}
    # README.md.j2: ~/.config/projinit/templates/my-readme.j2
'''
