# Algorithme de detection de type

**Derniere mise a jour**: 2026-01-18

**Source**: [src/projinit/core/detector.py](../../src/projinit/core/detector.py)

## Vue d'ensemble

La detection de type utilise un **systeme de scoring pondere** plutot qu'une approche rules-based simple. Cela permet de gerer les projets hybrides et les ambiguites.

## Pourquoi le scoring?

| Approche | Avantages | Inconvenients |
|----------|-----------|---------------|
| Rules-based | Simple, deterministe | Echoue sur projets hybrides |
| ML/Classification | Flexible | Overhead, donnees necessaires |
| **Scoring** | Gere ambiguites, debuggable | Necessite calibration |

Le scoring a ete choisi car il:
- Gere naturellement les projets multi-technos
- Est facilement debuggable (on peut voir les scores)
- Ne necessite pas de dataset d'entrainement
- Peut etre ajuste finement par marker

## Algorithme detaille

### Phase 1: Scoring des markers fichiers/repertoires

```python
scores = {type: 0.0 for type in ProjectType}

for project_type, markers in PROJECT_MARKERS.items():
    for marker, weight in markers.items():
        if (path / marker).exists():
            scores[project_type] += weight
            markers_found.append(marker)
```

**Exemple concret**:

```text
Projet avec: pyproject.toml, src/, tests/, __main__.py

Scores apres Phase 1:
- PYTHON_CLI:  0.3 + 0.2 + 0.1 + 0.2 = 0.8
- PYTHON_LIB:  0.3 + 0.3 + 0.2       = 0.8
- NODE_FRONTEND: 0                    = 0.0
- INFRASTRUCTURE: 0                   = 0.0
```

### Phase 2: Scoring du contenu (pyproject.toml)

```python
if (path / "pyproject.toml").exists():
    content = read(path / "pyproject.toml")
    for pattern, (type, weight) in DISTINGUISHING_MARKERS.items():
        if pattern in content:
            scores[type] += weight
```

**Exemple avec pyproject.toml contenant `[project.scripts]`**:

```text
Scores apres Phase 2:
- PYTHON_CLI:  0.8 + 0.3 = 1.1  <-- Gagnant
- PYTHON_LIB:  0.8             = 0.8
```

### Phase 3: Scoring du contenu (package.json)

Meme logique pour les projets Node.js.

```python
if (path / "package.json").exists():
    content = read(path / "package.json")
    for pattern, (type, weight) in DISTINGUISHING_MARKERS.items():
        if pattern in content:
            scores[type] += weight
```

### Phase 4: Selection du gagnant

```python
if not any(scores.values()):
    return UNKNOWN, 0.0

best_type = max(scores, key=lambda x: scores[x])
confidence = min(scores[best_type], 1.0)
```

## Poids et calibration

### Principes de calibration

1. **Markers specifiques**: Poids plus eleve (0.4-0.5)
   - `mkdocs.yml` pour documentation
   - `main.tf` pour infrastructure

2. **Markers partages**: Poids plus faible (0.1-0.3)
   - `src/` est commun a plusieurs types
   - `tests/` aussi

3. **Markers distinctifs**: Pour departager
   - `[project.scripts]` indique CLI (pas lib)
   - `react` dans package.json indique frontend

### Table des poids actuels

#### Python CLI

| Marker | Poids | Justification |
|--------|-------|---------------|
| `pyproject.toml` | 0.3 | Commun mais important |
| `setup.py` | 0.2 | Legacy mais valide |
| `src/` | 0.2 | Layout moderne |
| `tests/` | 0.1 | Commun a tous |
| `__main__.py` | 0.2 | Specifique CLI |
| `[project.scripts]` (contenu) | 0.3 | Tres specifique |
| `click/argparse/typer` (contenu) | 0.1 | Frameworks CLI |

#### Node.js Frontend

| Marker | Poids | Justification |
|--------|-------|---------------|
| `package.json` | 0.4 | Tres specifique |
| `src/` | 0.2 | Commun |
| `tsconfig.json` | 0.2 | TypeScript |
| `vite.config.*` | 0.1 | Build tool |
| `react/vue` (contenu) | 0.2 | Framework |

## Gestion des ambiguites

### Egalite de scores

Actuellement: le premier dans l'ordre d'iteration gagne.

**Amelioration possible**: Ajouter des tie-breakers specifiques.

### Projets hybrides

Exemple: Python CLI + Terraform

```text
my-infra-tool/
├── pyproject.toml     # Python: +0.3
├── src/               # Python: +0.2
│   └── tool/
├── terraform/         # Infra: +0.3
│   └── main.tf        # Infra: +0.4
└── tests/             # Python: +0.1

Scores:
- PYTHON_CLI:     0.6
- INFRASTRUCTURE: 0.7  <-- Gagnant
```

**Solution**: L'utilisateur peut forcer avec `--type python-cli`.

### Projet vide

```text
empty-project/
└── (rien)

Scores: tous a 0.0
Resultat: UNKNOWN, confidence 0.0
```

## Debug de detection

Pour comprendre pourquoi un type a ete detecte:

```bash
projinit check -v
```

Output:
```text
Detected project type: Python CLI Application (confidence: 85%)
Markers found: pyproject.toml, src/, __main__.py, tests/
```

## Ajouter des markers

### Nouveau marker pour type existant

```python
# detector.py
PROJECT_MARKERS[ProjectType.PYTHON_CLI]["new_marker.txt"] = 0.2
```

### Marker distinctif

```python
# detector.py
DISTINGUISHING_MARKERS["specific-pattern"] = (ProjectType.PYTHON_CLI, 0.15)
```

### Recommandations

- Poids total d'un type: viser ~1.0 max avec markers communs
- Markers distinctifs: 0.2-0.3 pour bien departager
- Tester avec plusieurs projets apres modification
