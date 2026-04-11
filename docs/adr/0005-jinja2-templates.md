# ADR-0005: Jinja2 pour la generation de templates

**Date**: 2024-12
**Statut**: Accepte

## Contexte

projinit genere des fichiers (README, pyproject.toml, CI workflows, etc.) lors de la creation de nouveaux projets. Le systeme de templating doit etre flexible, maintenable et supporter la logique conditionnelle.

## Options considerees

1. **String formatting** - `str.format()` ou f-strings, simple mais limite pour les templates complexes
2. **Jinja2** - Moteur de templates standard Python, supporte boucles, conditions, filtres, heritage
3. **Cookiecutter** - Outil complet de scaffolding avec Jinja2, mais impose sa propre structure et workflow

## Decision

Utiliser **Jinja2** directement comme moteur de templates, avec `PackageLoader` pour charger les templates depuis le package.

## Justification

- Flexibilite maximale pour les templates avec logique conditionnelle
- Standard de l'industrie pour le templating Python (Flask, Ansible, etc.)
- Integration native avec `PackageLoader` pour distribuer les templates dans le package
- Plus leger que Cookiecutter qui impose un workflow et une structure specifiques
- Support de l'heritage de templates pour factoriser les parties communes

## Consequences

- Dependance a Jinja2 (largement adoptee et maintenue)
- Syntaxe Jinja2 a connaitre pour creer ou modifier des templates
- Les templates peuvent devenir complexes avec trop de logique conditionnelle
- Necessite une bonne organisation des templates pour rester maintenable
