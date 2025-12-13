# Quickstart: Génération automatique de pre-commit config

## Test Manuel

### Scénario 1: Projet avec Python uniquement

```bash
cd /tmp
uv run projinit -p /tmp/test-projects
# Sélectionner: Python uniquement
# Vérifier le contenu de /tmp/test-projects/<nom>/.pre-commit-config.yaml
```

**Résultat attendu**:
- Fichier `.pre-commit-config.yaml` présent
- Contient les hooks communs (pre-commit-hooks, yamllint, shfmt, shellcheck)
- Contient les hooks Python (ruff)

### Scénario 2: Projet avec plusieurs technologies

```bash
cd /tmp
uv run projinit -p /tmp/test-projects
# Sélectionner: Python, Terraform, Docker
```

**Résultat attendu**:
- Hooks communs présents
- Hooks Python (ruff)
- Hooks Terraform (terraform_fmt, terraform_validate, terraform_tflint)
- Hooks Docker (hadolint)

### Scénario 3: Projet avec Ansible

```bash
cd /tmp
uv run projinit -p /tmp/test-projects
# Sélectionner: Ansible
```

**Résultat attendu**:
- Ansible apparaît dans la liste des technologies
- Fichier `.pre-commit-config.yaml` contient ansible-lint
- Fichier `.gitignore` contient les patterns Ansible (*.retry, .vault_pass)

### Scénario 4: Projet sans technologie spécifique

```bash
cd /tmp
uv run projinit -p /tmp/test-projects
# Ne sélectionner aucune technologie (ou juste IDE)
```

**Résultat attendu**:
- Fichier `.pre-commit-config.yaml` présent
- Contient uniquement les hooks communs

## Validation du fichier généré

```bash
cd /tmp/test-projects/<nom>
pre-commit validate-config
```

**Résultat attendu**: Pas d'erreur de validation

## Checklist de validation

- [ ] Ansible apparaît dans la liste des technologies
- [ ] Le fichier `.pre-commit-config.yaml` est généré pour tous les projets
- [ ] Les hooks communs sont toujours présents
- [ ] Les hooks technologiques correspondent aux sélections
- [ ] Le fichier passe `pre-commit validate-config`
- [ ] Le `.gitignore` inclut les patterns Ansible si sélectionné
