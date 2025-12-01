"""Validation des inputs utilisateur."""

import re


def validate_slug(value: str) -> bool | str:
    """Valide que la valeur est en slug-case (kebab-case)."""
    if not value:
        return "Le nom du projet est obligatoire"

    pattern = r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$"
    if not re.match(pattern, value):
        return "Le nom doit être en slug-case (ex: mon-projet, api-v2)"

    if len(value) > 100:
        return "Le nom ne doit pas dépasser 100 caractères"

    return True


def validate_description(value: str) -> bool:
    """Valide la description (toujours valide, peut être vide)."""
    return True
