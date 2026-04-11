# Module: core/detector.py

**Derniere mise a jour**: 2026-01-18

**Source**: [src/projinit/core/detector.py](../../src/projinit/core/detector.py)

## Responsabilite

Detection automatique du type de projet base sur les fichiers presents.

## Constantes

### PROJECT_MARKERS

Dictionnaire des markers et leurs poids par type de projet.

```python
PROJECT_MARKERS: dict[ProjectType, dict[str, float]]
```

**Source**: [detector.py:8](../../src/projinit/core/detector.py#L8)

**Structure**:
```python
{
    ProjectType.PYTHON_CLI: {
        "pyproject.toml": 0.3,
        "setup.py": 0.2,
        "src/": 0.2,
        "tests/": 0.1,
        "__main__.py": 0.2,
    },
    # ...
}
```

### DISTINGUISHING_MARKERS

Markers basés sur le contenu des fichiers de config.

```python
DISTINGUISHING_MARKERS: dict[str, tuple[ProjectType, float]]
```

**Source**: [detector.py:52](../../src/projinit/core/detector.py#L52)

**Structure**:
```python
{
    "[project.scripts]": (ProjectType.PYTHON_CLI, 0.3),
    "click": (ProjectType.PYTHON_CLI, 0.1),
    "react": (ProjectType.NODE_FRONTEND, 0.2),
    # ...
}
```

---

## Fonctions publiques

### detect_project_type()

Detecte le type de projet.

```python
def detect_project_type(path: Path) -> DetectionResult:
```

**Source**: [detector.py:65](../../src/projinit/core/detector.py#L65)

**Parametres**:
| Parametre | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Chemin vers le repertoire du projet |

**Retourne**: `DetectionResult` avec:
- `project_type`: Type detecte
- `confidence`: Score de confiance (0.0 - 1.0)
- `markers_found`: Liste des markers trouves
- `markers_checked`: Liste de tous les markers verifies

**Exemple**:
```python
from projinit.core.detector import detect_project_type
from pathlib import Path

result = detect_project_type(Path("/home/user/my-project"))

print(f"Type: {result.project_type.display_name}")
print(f"Confidence: {result.confidence:.0%}")
print(f"Markers: {', '.join(result.markers_found)}")

if result.is_confident:
    print("Detection fiable")
else:
    print("Verification manuelle recommandee")
```

**Implementation**:

```text
1. Initialise scores a 0 pour chaque type
2. Pour chaque type dans PROJECT_MARKERS:
   - Pour chaque marker:
     - Si path/marker existe: score[type] += weight
3. Si pyproject.toml existe:
   - Lit le contenu
   - Pour chaque pattern dans DISTINGUISHING_MARKERS:
     - Si pattern dans contenu: score[type] += weight
4. Meme logique pour package.json
5. Trouve le type avec le score max
6. Normalise confidence = min(score, 1.0)
7. Retourne DetectionResult
```

**Cas speciaux**:
- Path n'est pas un repertoire: retourne UNKNOWN avec confidence 0.0
- Aucun marker trouve: retourne UNKNOWN avec confidence 0.0

---

## Fonctions internes

### _get_all_markers()

Retourne l'ensemble de tous les markers.

```python
def _get_all_markers() -> set[str]:
```

**Source**: [detector.py:145](../../src/projinit/core/detector.py#L145)

**Utilisation**: Pour remplir `markers_checked` dans le resultat.

---

## Diagramme de flux

```text
                    ┌─────────────┐
                    │    path     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ is_dir()?   │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │ No                      │ Yes
              ▼                         ▼
    ┌─────────────────┐      ┌─────────────────┐
    │ Return UNKNOWN  │      │ Init scores = 0 │
    │ confidence = 0  │      └────────┬────────┘
    └─────────────────┘               │
                                      ▼
                           ┌─────────────────────┐
                           │ For each type:      │
                           │   For each marker:  │
                           │     if exists:      │
                           │       score += wt   │
                           └────────┬────────────┘
                                    │
                                    ▼
                           ┌─────────────────────┐
                           │ Check pyproject.toml│
                           │ for patterns        │
                           └────────┬────────────┘
                                    │
                                    ▼
                           ┌─────────────────────┐
                           │ Check package.json  │
                           │ for patterns        │
                           └────────┬────────────┘
                                    │
                                    ▼
                           ┌─────────────────────┐
                           │ best = max(scores)  │
                           │ conf = min(best,1.0)│
                           └────────┬────────────┘
                                    │
                                    ▼
                           ┌─────────────────────┐
                           │ Return              │
                           │ DetectionResult     │
                           └─────────────────────┘
```

---

## Dependances

```python
from pathlib import Path
from projinit.core.models import DetectionResult, ProjectType
```
