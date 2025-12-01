"""Gestion de la configuration."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class OwnerConfig:
    """Configuration d'un owner GitHub."""

    name: str
    label: str


@dataclass
class DefaultsConfig:
    """Valeurs par défaut."""

    visibility: str = "public"
    use_direnv: bool = False


@dataclass
class Config:
    """Configuration complète de projinit."""

    owners: list[OwnerConfig] = field(default_factory=list)
    pass_secret_path: str = "github/terraform-token"
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)

    @classmethod
    def get_default(cls) -> "Config":
        """Retourne la configuration par défaut."""
        return cls(
            owners=[
                OwnerConfig(name="owner", label="owner (personnel)"),
            ],
            pass_secret_path="github/terraform-token",
            defaults=DefaultsConfig(),
        )


def find_config_file() -> Path | None:
    """Cherche le fichier de configuration (local puis global)."""
    # 1. Fichier local
    local_config = Path.cwd() / "config.yaml"
    if local_config.exists():
        return local_config

    # 2. Fichier global XDG
    xdg_config_home = Path.home() / ".config"
    global_config = xdg_config_home / "projinit" / "config.yaml"
    if global_config.exists():
        return global_config

    return None


def parse_config(data: dict[str, Any]) -> Config:
    """Parse les données de configuration."""
    owners = []
    for owner_data in data.get("owners", []):
        owners.append(
            OwnerConfig(
                name=owner_data.get("name", ""),
                label=owner_data.get("label", owner_data.get("name", "")),
            )
        )

    defaults_data = data.get("defaults", {})
    defaults = DefaultsConfig(
        visibility=defaults_data.get("visibility", "public"),
        use_direnv=defaults_data.get("use_direnv", False),
    )

    return Config(
        owners=owners if owners else Config.get_default().owners,
        pass_secret_path=data.get("pass_secret_path", "github/terraform-token"),
        defaults=defaults,
    )


def load_config() -> Config:
    """Charge la configuration depuis le fichier ou retourne les valeurs par défaut."""
    config_path = find_config_file()

    if config_path is None:
        return Config.get_default()

    try:
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
        return parse_config(data)
    except Exception:
        return Config.get_default()
