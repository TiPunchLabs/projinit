# Module: core/checker.py

**Derniere mise a jour**: 2026-01-18

**Source**: [src/projinit/core/checker.py](../../src/projinit/core/checker.py)

## Responsabilite

Execute les verifications de conformite sur un projet.

## Classe: Checker

```python
class Checker:
    def __init__(self, project_path: Path, project_type: ProjectType):
        ...
```

### Parametres du constructeur

| Parametre | Type | Description |
|-----------|------|-------------|
| `project_path` | `Path` | Chemin absolu vers le projet |
| `project_type` | `ProjectType` | Type de projet detecte ou specifie |

### Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `project_path` | `Path` | Chemin du projet |
| `project_type` | `ProjectType` | Type de projet |
| `_files_scanned` | `set[str]` | Fichiers analyses (interne) |

---

## Fonctions publiques

### run_checks()

Execute tous les checks applicables et retourne un rapport d'audit.

```python
def run_checks(self) -> AuditReport:
```

**Retourne**: `AuditReport` avec tous les resultats de checks

**Exemple**:
```python
from projinit.core.checker import Checker
from projinit.core.models import ProjectType
from pathlib import Path

checker = Checker(Path("/home/user/my-project"), ProjectType.PYTHON_CLI)
report = checker.run_checks()

print(f"Score: {report.score:.1f}%")
print(f"Conforme: {report.is_compliant}")

for check in report.failed_checks:
    print(f"- {check.id}: {check.message}")
```

**Implementation** ([checker.py:31](../../src/projinit/core/checker.py#L31)):
1. Charge les checks via `get_checks_for_type()`
2. Execute chaque check via `_run_single_check()`
3. Mesure le temps d'execution
4. Retourne un `AuditReport`

---

## Fonctions internes

### _run_single_check()

Execute un check individuel.

```python
def _run_single_check(self, check_def: dict) -> CheckResult:
```

**Source**: [checker.py:62](../../src/projinit/core/checker.py#L62)

**Parametres**:
- `check_def`: Definition du check depuis le YAML

**Retourne**: `CheckResult`

**Dispatch par type**:
- `file_exists` -> `_check_file_exists()`
- `dir_exists` -> `_check_dir_exists()`
- `content_contains` -> `_check_content_contains()`
- `any_exists` -> `_check_any_exists()`

---

### _check_file_exists()

Verifie l'existence d'un fichier.

```python
def _check_file_exists(
    self,
    check_def: dict,
    check_id: str,
    level: CheckLevel,
    description: str,
    template: str | None,
) -> CheckResult:
```

**Source**: [checker.py:106](../../src/projinit/core/checker.py#L106)

**Logique**:
1. Verifie le path principal
2. Verifie les alternatives si definies
3. Retourne PASSED si trouve, FAILED sinon
4. Inclut suggestion de fix si template disponible

---

### _check_dir_exists()

Verifie l'existence d'un repertoire.

```python
def _check_dir_exists(
    self,
    check_def: dict,
    check_id: str,
    level: CheckLevel,
    description: str,
) -> CheckResult:
```

**Source**: [checker.py:145](../../src/projinit/core/checker.py#L145)

---

### _check_content_contains()

Verifie qu'un fichier contient des patterns.

```python
def _check_content_contains(
    self,
    check_def: dict,
    check_id: str,
    level: CheckLevel,
    description: str,
) -> CheckResult:
```

**Source**: [checker.py:180](../../src/projinit/core/checker.py#L180)

**Logique**:
1. Lit le fichier (path ou alternatives)
2. Verifie chaque pattern
3. PASSED si tous trouves, FAILED si patterns manquants
4. SKIPPED si fichier inexistant

---

### _check_any_exists()

Verifie qu'au moins un path existe.

```python
def _check_any_exists(
    self,
    check_def: dict,
    check_id: str,
    level: CheckLevel,
    description: str,
) -> CheckResult:
```

**Source**: [checker.py:237](../../src/projinit/core/checker.py#L237)

---

## Diagramme de sequence

```text
Client           Checker            Standards          FileSystem
   │                │                   │                   │
   │ run_checks()   │                   │                   │
   │───────────────>│                   │                   │
   │                │ get_checks_for_type()                 │
   │                │──────────────────>│                   │
   │                │<─────checks[]─────│                   │
   │                │                   │                   │
   │                │ for check in checks:                  │
   │                │   _run_single_check()                 │
   │                │                   │                   │
   │                │   if file_exists: │                   │
   │                │───────────────────────exists()───────>│
   │                │<─────────────────────bool────────────│
   │                │                   │                   │
   │                │   if content_contains:                │
   │                │───────────────────────read_text()────>│
   │                │<─────────────────────content─────────│
   │                │                   │                   │
   │<──AuditReport──│                   │                   │
```

## Dependances

```python
from projinit.core.models import (
    AuditReport,
    CheckLevel,
    CheckResult,
    CheckStatus,
    ProjectType,
)
from projinit.standards.loader import get_checks_for_type
```
