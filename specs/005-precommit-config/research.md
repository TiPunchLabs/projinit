# Research: Génération automatique de pre-commit config

**Feature**: 005-precommit-config
**Date**: 2025-12-12

## Décision 1: Structure des templates pre-commit

**Décision**: Utiliser le même pattern de fragments que pour .gitignore

**Rationale**:
- Pattern déjà établi et testé dans le projet
- Facilite la maintenance (une structure cohérente)
- Permet l'ajout facile de nouvelles technologies

**Alternatives considérées**:
1. **Un seul template avec conditions Jinja2**: Plus complexe, difficile à maintenir
2. **Fichier de configuration YAML externe**: Sur-ingénierie pour ce cas d'usage

## Décision 2: Versions des hooks pre-commit

**Décision**: Utiliser des versions fixes et récentes pour chaque repo

| Repo | Version |
|------|---------|
| pre-commit-hooks | v5.0.0 |
| yamllint | v1.35.1 |
| shfmt | v3.11.0-1 |
| shellcheck | v0.10.0 |
| ruff-pre-commit | v0.8.3 |
| mirrors-eslint | v9.17.0 |
| mirrors-prettier | v3.4.2 |
| golangci-lint | v1.62.2 |
| pre-commit-terraform | v1.99.0 |
| hadolint | v2.12.0 |
| ansible-lint | v25.1.1 |

**Rationale**: Versions stables récentes au moment de l'implémentation. L'utilisateur peut les mettre à jour manuellement.

## Décision 3: Hooks communs (toujours inclus)

**Décision**: Inclure dans le header les hooks de base + shell

**Hooks communs**:
- `end-of-file-fixer`: Assure une ligne vide en fin de fichier
- `trailing-whitespace`: Supprime les espaces en fin de ligne
- `check-merge-conflict`: Détecte les marqueurs de conflit git
- `check-yaml`: Valide la syntaxe YAML
- `detect-private-key`: Prévient les fuites de clés privées
- `yamllint`: Linting YAML
- `shfmt`: Formatage des scripts shell
- `shellcheck`: Analyse statique des scripts shell

**Rationale**: Ces hooks sont utiles pour tous les projets, indépendamment des technologies sélectionnées.

## Décision 4: Patterns .gitignore pour Ansible

**Décision**: Créer un nouveau fragment `gitignore/ansible.j2`

**Patterns à inclure**:
```
# Ansible
*.retry
.vault_pass
inventory/**/host_vars/**/vault.yml
inventory/**/group_vars/**/vault.yml
```

**Rationale**: Patterns standards pour ignorer les fichiers retry et protéger les vaults.
