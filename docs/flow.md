# Flux d'execution

**Derniere mise a jour**: 2026-01-18

Ce document decrit le parcours d'execution de chaque commande CLI.

## Commande: projinit check

### Synopsis

```bash
projinit check [path] [-t TYPE] [-f FORMAT] [-v]
```

### Etapes d'execution

```text
┌──────────────────────────────────────────────────────────────────┐
│ 1. Parsing des arguments                                         │
│    Source: main_cli.py:304                                       │
│    - Valide le path (defaut: ".")                                │
│    - Parse --type, --format, --verbose                           │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Detection du type de projet (si pas --type)                   │
│    Source: cli/check_cmd.py:80                                   │
│    - Appelle detect_project_type(project_path)                   │
│    - Retourne DetectionResult avec confidence                    │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Chargement des checks applicables                             │
│    Source: standards/loader.py                                   │
│    - Charge base.yaml (toujours)                                 │
│    - Charge <type>.yaml selon ProjectType                        │
│    - Applique les overrides de config                            │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. Execution des checks                                          │
│    Source: core/checker.py:31                                    │
│    - Pour chaque check_def:                                      │
│      - Determine le type (file_exists, dir_exists, etc.)         │
│      - Execute le handler approprie                              │
│      - Stocke le CheckResult                                     │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. Generation du rapport                                         │
│    Source: core/reporter.py:31                                   │
│    - Selon --format:                                             │
│      - text: Affichage rich avec tables et progress bar          │
│      - json: Export JSON structure                               │
│      - markdown: Export MD avec badges                           │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 6. Code de sortie                                                │
│    Source: cli/check_cmd.py:113                                  │
│    - 0: Projet conforme (tous les required passes)               │
│    - 1: Projet non-conforme                                      │
│    - 2: Erreur (path invalide, type inconnu)                     │
└──────────────────────────────────────────────────────────────────┘
```

### Diagramme de sequence

```text
User          main_cli     check_cmd     detector      checker      reporter
  │               │             │            │            │            │
  │──check .──────>│             │            │            │            │
  │               │──run_check──>│            │            │            │
  │               │             │            │            │            │
  │               │             │──detect────>│            │            │
  │               │             │<──Result────│            │            │
  │               │             │            │            │            │
  │               │             │──────────────────────────>│            │
  │               │             │            │   Checker() │            │
  │               │             │            │            │            │
  │               │             │<──────────────AuditReport│            │
  │               │             │            │            │            │
  │               │             │────────────────────────────────────────>│
  │               │             │            │            │   to_text() │
  │<──────────────────────────────────────────────────────────────Output│
```

### Points de decision

| Condition | Action | Raison |
|-----------|--------|--------|
| Path n'est pas un repertoire | Return 2 | Impossible d'auditer un fichier |
| --type specifie | Utilise ce type | L'utilisateur sait mieux |
| Detection confidence < 70% | Warning | Detection incertaine |
| Type = UNKNOWN | Return 2 | Pas de checks applicables |

---

## Commande: projinit update

### Synopsis

```bash
projinit update [path] [-t TYPE] [-n] [-i] [--no-backup] [-v]
```

### Etapes d'execution

```text
┌──────────────────────────────────────────────────────────────────┐
│ 1. Parsing et validation                                         │
│    Source: cli/update_cmd.py:76                                  │
│    - Valide le path                                              │
│    - Detecte ou utilise --type                                   │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Audit initial (check)                                         │
│    Source: cli/update_cmd.py:99-101                              │
│    - Execute un check complet                                    │
│    - Identifie les non-conformites                               │
│    - Si deja conforme: exit 0                                    │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Generation des actions                                        │
│    Source: core/updater.py                                       │
│    - Pour chaque check echoue avec template:                     │
│      - Cree une UpdateAction (CREATE, MODIFY, MERGE)             │
│    - Filtre selon MergeStrategy                                  │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. Mode dry-run ou interactif                                    │
│    Source: cli/update_cmd.py:124-136                             │
│    - dry-run: Affiche les actions, exit                          │
│    - interactif: Confirme chaque action                          │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. Application des actions                                       │
│    Source: core/updater.py                                       │
│    - Cree les backups (sauf --no-backup)                         │
│    - Execute les actions                                         │
│    - Rend les templates avec Jinja2                              │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 6. Rapport et code de sortie                                     │
│    Source: cli/update_cmd.py:145-156                             │
│    - 0: Toutes les actions appliquees                            │
│    - 1: Application partielle                                    │
│    - 2: Aucune action possible                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Types d'actions

| ActionType | Description | Exemple |
|------------|-------------|---------|
| CREATE | Cree un nouveau fichier | README.md manquant |
| MODIFY | Modifie un fichier existant | Ajoute section a pyproject.toml |
| MERGE | Fusionne intelligemment | .pre-commit-config.yaml |
| SKIP | Ne fait rien | Fichier deja conforme |

---

## Commande: projinit new

### Synopsis

```bash
projinit new [name] [-t TYPE] [-p PATH] [-d DESC] [--direnv] [-y] [-v]
```

### Etapes d'execution

```text
┌──────────────────────────────────────────────────────────────────┐
│ 1. Collecte des informations                                     │
│    Source: cli/init_cmd.py:110-148                               │
│    - Nom du projet (argument ou prompt)                          │
│    - Type de projet (--type ou prompt)                           │
│    - Description (--description ou prompt)                       │
│    - Direnv (--direnv/--no-direnv ou prompt)                     │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Validations                                                   │
│    Source: cli/init_cmd.py:119-161                               │
│    - Nom valide (slug: lowercase, hyphens)                       │
│    - Repertoire cible n'existe pas                               │
│    - Si direnv: pass et direnv installes                         │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Affichage resume et confirmation                              │
│    Source: cli/init_cmd.py:164-171                               │
│    - Montre la config                                            │
│    - Liste les fichiers qui seront crees                         │
│    - Demande confirmation (sauf -y)                              │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. Generation du projet                                          │
│    Source: cli/init_cmd.py:339-387                               │
│    - Cree le repertoire cible                                    │
│    - Genere les fichiers communs (README, LICENSE, etc.)         │
│    - Genere les fichiers specifiques au type                     │
│    - Genere .envrc si direnv active                              │
│    - Genere .claude/commands/                                    │
│    - Genere doc/                                                 │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 5. Post-generation                                               │
│    Source: cli/init_cmd.py:188-196                               │
│    - git init -b main (sauf --no-git)                            │
│    - git add . && git commit                                     │
│    - direnv allow (si active)                                    │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 6. Affichage des prochaines etapes                               │
│    Source: cli/init_cmd.py:873-905                               │
│    - Instructions specifiques au type de projet                  │
│    - Commandes pour demarrer                                     │
└──────────────────────────────────────────────────────────────────┘
```

### Fichiers generes par type

| Type | Fichiers specifiques |
|------|---------------------|
| python-cli | pyproject.toml, src/<name>/__init__.py, src/<name>/cli.py, tests/ |
| python-lib | pyproject.toml, src/<name>/__init__.py, tests/ |
| node-frontend | package.json, tsconfig.json, vite.config.ts, src/main.tsx |
| infrastructure | terraform/*.tf, ansible/playbook.yml, ansible/inventory/ |
| documentation | mkdocs.yml, pyproject.toml, docs/index.md |
| lab | labs/, solutions/, docs/, mkdocs.yml |

---

## Commande: projinit config

### Synopsis

```bash
projinit config {show|init|paths}
```

### Sous-commandes

#### config show

```text
┌──────────────────────────────────────────────────────────────────┐
│ 1. Chargement de la configuration                                │
│    Source: cli/config_cmd.py:104-107                             │
│    - Charge config globale (~/.config/projinit/config.yaml)      │
│    - Merge avec config locale (.projinit.yaml)                   │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Affichage structure                                           │
│    Source: cli/config_cmd.py:109-171                             │
│    - Author (name, email)                                        │
│    - Defaults (python_version, license)                          │
│    - Standards (overrides, disabled_checks)                      │
│    - Templates (custom_dir, overrides)                           │
└──────────────────────────────────────────────────────────────────┘
```

#### config init

```text
┌──────────────────────────────────────────────────────────────────┐
│ 1. Determine la cible                                            │
│    Source: cli/config_cmd.py:180-188                             │
│    - --global: ~/.config/projinit/config.yaml                    │
│    - --local: ./.projinit.yaml                                   │
│    - default: global                                             │
└──────────────────────┬───────────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Generation et ecriture                                        │
│    Source: cli/config_cmd.py:191-203                             │
│    - Verifie si existe (sauf --force)                            │
│    - Genere contenu exemple                                      │
│    - Ecrit le fichier                                            │
│    - Affiche le contenu avec syntaxe YAML                        │
└──────────────────────────────────────────────────────────────────┘
```

#### config paths

Affiche les chemins de configuration et leur existence.

---

## Gestion des erreurs

### Codes de sortie

| Code | Signification | Commandes |
|------|---------------|-----------|
| 0 | Succes | Toutes |
| 1 | Echec fonctionnel | check (non-conforme), update (partiel) |
| 2 | Erreur | Path invalide, type inconnu, erreur I/O |

### Exceptions gerees

| Exception | Origine | Comportement |
|-----------|---------|--------------|
| `ValueError` | Path vers fichier | Message d'erreur, exit 2 |
| `PermissionError` | Pas de droits ecriture | Message d'erreur, exit 2 |
| `OSError` | Lecture fichier | Skip check, continue |
| `KeyboardInterrupt` | Ctrl+C | "Annule", exit 1 |
