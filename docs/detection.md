# Detection Automatique du Type de Projet

## Concept

projinit detecte automatiquement le type d'un projet existant en analysant sa structure. Cette detection utilise un systeme de marqueurs ponderes.

## Algorithme

```
1. Scanner le repertoire projet
2. Pour chaque type de projet :
   a. Verifier la presence des marqueurs
   b. Calculer le score (somme des poids)
3. Retourner le type avec le score le plus eleve
4. Si score < seuil : retourner UNKNOWN
```

## Implementation

### Fichier : `core/detector.py`

```python
from dataclasses import dataclass
from pathlib import Path
from projinit.core.models import ProjectType, DetectionResult

# Marqueurs par type de projet
# Cle = fichier/dossier, Valeur = poids (0.0 a 1.0)
MARKERS: dict[ProjectType, dict[str, float]] = {
    ProjectType.PYTHON_CLI: {
        "pyproject.toml": 0.3,
        "src/": 0.2,
        "tests/": 0.1,
        "cli.py": 0.3,
        "__main__.py": 0.2,
    },
    ProjectType.PYTHON_LIB: {
        "pyproject.toml": 0.3,
        "src/": 0.3,
        "tests/": 0.2,
        "py.typed": 0.3,
    },
    ProjectType.NODE_FRONTEND: {
        "package.json": 0.4,
        "src/": 0.2,
        "tsconfig.json": 0.2,
        "vite.config": 0.2,
        "index.html": 0.1,
    },
    # ... autres types
}

def detect(project_path: Path) -> DetectionResult:
    """Detecte le type de projet."""
    scores: dict[ProjectType, float] = {}
    found_markers: dict[ProjectType, list[str]] = {}

    for project_type, markers in MARKERS.items():
        score = 0.0
        found = []

        for marker, weight in markers.items():
            if _marker_exists(project_path, marker):
                score += weight
                found.append(marker)

        scores[project_type] = score
        found_markers[project_type] = found

    # Trouver le meilleur score
    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    # Seuil de confiance
    if best_score < 0.3:
        return DetectionResult(
            project_type=ProjectType.UNKNOWN,
            confidence=0.0,
            markers_found=[],
        )

    return DetectionResult(
        project_type=best_type,
        confidence=min(best_score, 1.0),
        markers_found=found_markers[best_type],
    )
```

## Marqueurs par Type

### Python CLI

| Marqueur | Poids | Description |
|----------|-------|-------------|
| `pyproject.toml` | 0.3 | Config Python moderne |
| `src/` | 0.2 | Structure src layout |
| `tests/` | 0.1 | Tests unitaires |
| `cli.py` | 0.3 | Point d'entree CLI |
| `__main__.py` | 0.2 | Execution directe |

**Score max** : 1.1 (normalise a 1.0)

### Python Library

| Marqueur | Poids | Description |
|----------|-------|-------------|
| `pyproject.toml` | 0.3 | Config Python |
| `src/` | 0.3 | Structure src layout |
| `tests/` | 0.2 | Tests unitaires |
| `py.typed` | 0.3 | Marker PEP 561 |

### Node.js Frontend

| Marqueur | Poids | Description |
|----------|-------|-------------|
| `package.json` | 0.4 | Config Node.js |
| `src/` | 0.2 | Code source |
| `tsconfig.json` | 0.2 | TypeScript |
| `vite.config.*` | 0.2 | Bundler Vite |
| `index.html` | 0.1 | Point d'entree web |

### Infrastructure

| Marqueur | Poids | Description |
|----------|-------|-------------|
| `main.tf` | 0.4 | Terraform principal |
| `variables.tf` | 0.2 | Variables Terraform |
| `terraform/` | 0.2 | Repertoire Terraform |
| `ansible/` | 0.2 | Repertoire Ansible |
| `playbook.yml` | 0.2 | Playbook Ansible |

### Documentation

| Marqueur | Poids | Description |
|----------|-------|-------------|
| `mkdocs.yml` | 0.5 | Config MkDocs |
| `docs/` | 0.3 | Repertoire docs |
| `docs/index.md` | 0.2 | Page d'accueil |

### Lab/Tutorial

| Marqueur | Poids | Description |
|----------|-------|-------------|
| `labs/` | 0.5 | Repertoire labs |
| `exercises/` | 0.4 | Repertoire exercices |
| `solutions/` | 0.3 | Repertoire solutions |
| `answers/` | 0.3 | Repertoire reponses |
| `mkdocs.yml` | 0.2 | Documentation |
| `docs/` | 0.1 | Docs supplementaires |

## Resultat de Detection

```python
@dataclass
class DetectionResult:
    project_type: ProjectType    # Type detecte
    confidence: float            # Score 0.0 a 1.0
    markers_found: list[str]     # Marqueurs trouves
    markers_checked: list[str]   # Tous les marqueurs verifies

    @property
    def is_confident(self) -> bool:
        """Detection fiable si >= 70%."""
        return self.confidence >= 0.7
```

## Utilisation

### En CLI

```bash
# Detection automatique (pas de -t)
projinit check /path/to/project

# Forcer un type
projinit check /path/to/project -t python-cli
```

### En Code

```python
from projinit.core.detector import detect
from pathlib import Path

result = detect(Path("/path/to/project"))

print(f"Type: {result.project_type.value}")
print(f"Confiance: {result.confidence:.0%}")
print(f"Marqueurs: {result.markers_found}")

if not result.is_confident:
    print("Detection incertaine, verifier manuellement")
```

## Cas Particuliers

### Projets Hybrides

Un projet peut avoir des marqueurs de plusieurs types :

```
my-project/
├── pyproject.toml      # Python
├── package.json        # Node.js
└── mkdocs.yml          # Documentation
```

**Resolution** : Le type avec le score le plus eleve gagne.

Pour forcer un type : `projinit check -t python-cli`

### Projets Non Reconnus

Si aucun type n'atteint le seuil (0.3) :

```python
DetectionResult(
    project_type=ProjectType.UNKNOWN,
    confidence=0.0,
    ...
)
```

Le CLI affiche un message et suggere d'utiliser `-t`.

## Ajouter un Nouveau Type

### 1. Ajouter l'enum

Dans `core/models.py` :

```python
class ProjectType(Enum):
    # ...existants...
    MY_NEW_TYPE = "my-new-type"
```

### 2. Definir les marqueurs

Dans `core/detector.py` :

```python
MARKERS = {
    # ...existants...
    ProjectType.MY_NEW_TYPE: {
        "specific_file.ext": 0.5,
        "specific_dir/": 0.3,
        "another_marker": 0.2,
    },
}
```

### 3. Ajuster les poids

Regles pour les poids :
- **0.4-0.5** : Marqueur tres specifique (fichier unique au type)
- **0.2-0.3** : Marqueur commun mais revelateur
- **0.1** : Marqueur faible, bonus

## Debugging

Voir les scores de detection :

```python
from projinit.core.detector import MARKERS, _marker_exists
from projinit.core.models import ProjectType
from pathlib import Path

project = Path("/path/to/project")

for ptype, markers in MARKERS.items():
    score = sum(
        weight for marker, weight in markers.items()
        if _marker_exists(project, marker)
    )
    print(f"{ptype.value}: {score:.2f}")
```

## Tests

```python
def test_detect_python_cli():
    # Setup
    project = tmp_path / "test-project"
    project.mkdir()
    (project / "pyproject.toml").touch()
    (project / "src").mkdir()
    (project / "src" / "cli.py").touch()

    # Test
    result = detect(project)

    # Assert
    assert result.project_type == ProjectType.PYTHON_CLI
    assert result.confidence >= 0.5
    assert "pyproject.toml" in result.markers_found
```
