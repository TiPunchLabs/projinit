# Modeles de Donnees

## Vue d'Ensemble

Les modeles sont definis dans `core/models.py` et utilisent les `Enum` et `dataclass` de la stdlib Python.

```python
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
```

## Enumerations

### ProjectType

Types de projets supportes par projinit.

```python
class ProjectType(Enum):
    """Type of project detected or specified."""

    PYTHON_CLI = "python-cli"
    PYTHON_LIB = "python-lib"
    NODE_FRONTEND = "node-frontend"
    INFRASTRUCTURE = "infrastructure"
    DOCUMENTATION = "documentation"
    LAB = "lab"
    UNKNOWN = "unknown"

    @property
    def display_name(self) -> str:
        """Human-readable name for the project type."""
        names = {
            ProjectType.PYTHON_CLI: "Python CLI Application",
            ProjectType.PYTHON_LIB: "Python Library",
            ProjectType.NODE_FRONTEND: "Node.js Frontend",
            ProjectType.INFRASTRUCTURE: "Infrastructure (Terraform/Ansible)",
            ProjectType.DOCUMENTATION: "Documentation (MkDocs)",
            ProjectType.LAB: "Lab/Tutorial",
            ProjectType.UNKNOWN: "Unknown",
        }
        return names.get(self, self.value)
```

**Usage** :
```python
project_type = ProjectType.PYTHON_CLI
print(project_type.value)         # "python-cli"
print(project_type.display_name)  # "Python CLI Application"
```

### CheckStatus

Resultat d'un check de conformite.

```python
class CheckStatus(Enum):
    """Status of a conformity check."""

    PASSED = "passed"    # Check reussi
    FAILED = "failed"    # Check echoue
    WARNING = "warning"  # Check partiel
    SKIPPED = "skipped"  # Check ignore (desactive)
```

### CheckLevel

Niveau de severite d'un check.

```python
class CheckLevel(Enum):
    """Importance level of a check."""

    REQUIRED = "required"        # Obligatoire pour compliance
    RECOMMENDED = "recommended"  # Recommande, affecte le score
    OPTIONAL = "optional"        # Informatif seulement
```

### ActionType

Type d'action de mise a jour.

```python
class ActionType(Enum):
    """Type of update action."""

    CREATE = "create"  # Creer nouveau fichier
    MODIFY = "modify"  # Modifier fichier existant
    MERGE = "merge"    # Fusionner avec existant
    SKIP = "skip"      # Ne rien faire
```

### MergeStrategy

Strategie de fusion pour les mises a jour.

```python
class MergeStrategy(Enum):
    """Strategy for merging files."""

    OVERWRITE = "overwrite"       # Remplacer completement
    SMART = "smart"               # Fusion intelligente
    SKIP_EXISTING = "skip_existing"  # Garder l'existant
```

## Dataclasses

### CheckResult

Resultat d'un check individuel.

```python
@dataclass
class CheckResult:
    """Result of a single conformity check."""

    id: str                           # Identifiant unique (ex: "has_readme")
    status: CheckStatus               # PASSED, FAILED, WARNING, SKIPPED
    message: str                      # Message descriptif
    level: CheckLevel = CheckLevel.REQUIRED
    suggestion: str | None = None     # Commande pour corriger
    file_path: Path | None = None     # Fichier concerne

    @property
    def is_passed(self) -> bool:
        """Check if the result indicates success."""
        return self.status == CheckStatus.PASSED

    @property
    def is_critical(self) -> bool:
        """Check if this is a critical failure."""
        return self.status == CheckStatus.FAILED and self.level == CheckLevel.REQUIRED
```

**Exemple** :
```python
result = CheckResult(
    id="has_readme",
    status=CheckStatus.FAILED,
    message="README.md not found",
    level=CheckLevel.REQUIRED,
    suggestion="Create README.md with project documentation",
    file_path=Path("README.md"),
)

if result.is_critical:
    print("Critical issue!")
```

### UpdateAction

Action de correction a effectuer.

```python
@dataclass
class UpdateAction:
    """Action to perform during project update."""

    action_type: ActionType           # CREATE, MODIFY, MERGE, SKIP
    source: Path | None               # Template source
    target: Path                      # Fichier cible
    merge_strategy: MergeStrategy = MergeStrategy.SMART
    description: str = ""             # Description de l'action
    template_vars: dict = field(default_factory=dict)

    @property
    def is_destructive(self) -> bool:
        """Check if this action modifies existing files."""
        return self.action_type in (ActionType.MODIFY, ActionType.MERGE)
```

**Exemple** :
```python
action = UpdateAction(
    action_type=ActionType.CREATE,
    source=Path("templates/README.md.j2"),
    target=Path("README.md"),
    description="Create README.md from template",
    template_vars={"project_name": "my-project"},
)

if action.is_destructive:
    print("Warning: this will modify existing files")
```

### DetectionResult

Resultat de la detection de type de projet.

```python
@dataclass
class DetectionResult:
    """Result of project type detection."""

    project_type: ProjectType         # Type detecte
    confidence: float                 # Score 0.0 a 1.0
    markers_found: list[str] = field(default_factory=list)
    markers_checked: list[str] = field(default_factory=list)

    @property
    def is_confident(self) -> bool:
        """Check if detection has high confidence."""
        return self.confidence >= 0.7
```

**Exemple** :
```python
result = DetectionResult(
    project_type=ProjectType.PYTHON_CLI,
    confidence=0.85,
    markers_found=["pyproject.toml", "src/", "cli.py"],
    markers_checked=["pyproject.toml", "src/", "tests/", "cli.py"],
)

print(f"Type: {result.project_type.display_name}")
print(f"Confidence: {result.confidence:.0%}")
print(f"Confident: {result.is_confident}")
```

### AuditReport

Rapport complet d'audit.

```python
@dataclass
class AuditReport:
    """Complete audit report for a project."""

    project_path: Path
    project_type: ProjectType
    checks: list[CheckResult] = field(default_factory=list)
    execution_time_ms: float = 0.0
    files_scanned: list[str] = field(default_factory=list)

    @property
    def passed_count(self) -> int:
        """Number of passed checks."""
        return sum(1 for c in self.checks if c.status == CheckStatus.PASSED)

    @property
    def failed_count(self) -> int:
        """Number of failed checks."""
        return sum(1 for c in self.checks if c.status == CheckStatus.FAILED)

    @property
    def warning_count(self) -> int:
        """Number of warnings."""
        return sum(1 for c in self.checks if c.status == CheckStatus.WARNING)

    @property
    def total_count(self) -> int:
        """Total number of checks (excluding skipped)."""
        return sum(1 for c in self.checks if c.status != CheckStatus.SKIPPED)

    @property
    def score(self) -> float:
        """Conformity score as percentage."""
        if self.total_count == 0:
            return 100.0
        return (self.passed_count / self.total_count) * 100

    @property
    def is_compliant(self) -> bool:
        """Check if project passes all required checks."""
        return all(
            c.status != CheckStatus.FAILED
            for c in self.checks
            if c.level == CheckLevel.REQUIRED
        )

    @property
    def checks_by_level(self) -> dict[CheckLevel, list[CheckResult]]:
        """Group checks by their level."""
        result: dict[CheckLevel, list[CheckResult]] = {
            CheckLevel.REQUIRED: [],
            CheckLevel.RECOMMENDED: [],
            CheckLevel.OPTIONAL: [],
        }
        for check in self.checks:
            result[check.level].append(check)
        return result

    @property
    def failed_checks(self) -> list[CheckResult]:
        """Get all failed checks."""
        return [c for c in self.checks if c.status == CheckStatus.FAILED]

    @property
    def actionable_suggestions(self) -> list[tuple[str, str]]:
        """Get actionable suggestions with commands."""
        suggestions = []
        for check in self.failed_checks:
            if check.suggestion:
                suggestions.append((check.id, check.suggestion))
        return suggestions
```

**Exemple** :
```python
report = AuditReport(
    project_path=Path("/path/to/project"),
    project_type=ProjectType.PYTHON_CLI,
    checks=[
        CheckResult("has_readme", CheckStatus.PASSED, "OK"),
        CheckResult("has_license", CheckStatus.PASSED, "OK"),
        CheckResult("has_tests", CheckStatus.FAILED, "Missing tests/"),
    ],
    execution_time_ms=150.5,
)

print(f"Score: {report.score:.1f}%")
print(f"Compliant: {report.is_compliant}")
print(f"Failed: {report.failed_count}")

for level, checks in report.checks_by_level.items():
    print(f"{level.value}: {len(checks)} checks")
```

## Diagramme de Relations

```
┌──────────────┐
│ ProjectType  │ ◄─────────────────────┐
└──────────────┘                       │
       ▲                               │
       │                               │
       │                        ┌──────┴───────┐
┌──────┴───────────┐            │ AuditReport  │
│ DetectionResult  │            │              │
│  - project_type  │            │ - checks[]   │
│  - confidence    │            │ - score      │
└──────────────────┘            └──────┬───────┘
                                       │
                                       │ contains
                                       ▼
┌─────────────┐              ┌─────────────────┐
│ CheckLevel  │◄─────────────│  CheckResult    │
└─────────────┘              │                 │
                             │ - id            │
┌─────────────┐              │ - status        │
│ CheckStatus │◄─────────────│ - message       │
└─────────────┘              └─────────────────┘


┌─────────────┐              ┌─────────────────┐
│ ActionType  │◄─────────────│  UpdateAction   │
└─────────────┘              │                 │
                             │ - action_type   │
┌───────────────┐            │ - source        │
│ MergeStrategy │◄───────────│ - target        │
└───────────────┘            └─────────────────┘
```

## Bonnes Pratiques

### Immutabilite

Les dataclasses sont immuables par defaut (pas de `@dataclass(frozen=True)` ici mais recommande pour les modeles de domaine).

### Type Hints

Tous les champs ont des type hints explicites :
```python
id: str
status: CheckStatus
file_path: Path | None = None  # Python 3.10+ syntax
```

### Proprietes Calculees

Utiliser `@property` pour les valeurs derivees :
```python
@property
def score(self) -> float:
    return (self.passed_count / self.total_count) * 100
```

### Default Factory

Pour les listes/dicts mutables, utiliser `field(default_factory=...)` :
```python
checks: list[CheckResult] = field(default_factory=list)
template_vars: dict = field(default_factory=dict)
```
