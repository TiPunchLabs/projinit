# Module: core/reporter.py

**Derniere mise a jour**: 2026-01-18

**Source**: [src/projinit/core/reporter.py](../../src/projinit/core/reporter.py)

## Responsabilite

Generation de rapports d'audit dans differents formats (text, JSON, Markdown).

## Classe: Reporter

```python
class Reporter:
    def __init__(self, report: AuditReport, verbose: bool = False):
        ...
```

### Parametres du constructeur

| Parametre | Type | Description |
|-----------|------|-------------|
| `report` | `AuditReport` | Rapport d'audit a formater |
| `verbose` | `bool` | Inclure les details techniques |

### Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `report` | `AuditReport` | Rapport source |
| `verbose` | `bool` | Mode verbeux |
| `console` | `Console` | Instance rich.Console |

---

## Fonctions publiques

### to_text()

Affiche le rapport en texte riche dans le terminal.

```python
def to_text(self) -> None:
```

**Source**: [reporter.py:31](../../src/projinit/core/reporter.py#L31)

**Affiche**:
1. Header (path, type)
2. Checks groupes par niveau
3. Barre de progression du score
4. Panel de resume
5. Suggestions de fix (si echecs)
6. Infos techniques (si verbose)

**Exemple**:
```python
from projinit.core.reporter import Reporter

reporter = Reporter(report, verbose=True)
reporter.to_text()
```

---

### to_json()

Genere un rapport JSON.

```python
def to_json(self) -> str:
```

**Source**: [reporter.py:198](../../src/projinit/core/reporter.py#L198)

**Retourne**: String JSON formatee

**Structure**:
```json
{
  "project_path": "/path/to/project",
  "project_type": "python-cli",
  "score": 85.0,
  "is_compliant": true,
  "execution_time_ms": 42.5,
  "summary": {
    "passed": 8,
    "failed": 1,
    "warnings": 0,
    "total": 9
  },
  "checks": [
    {
      "id": "has_readme",
      "status": "passed",
      "level": "required",
      "message": "README.md exists",
      "suggestion": null,
      "file_path": "/path/to/project/README.md"
    }
  ],
  "files_scanned": ["README.md", "pyproject.toml"]
}
```

**Exemple**:
```python
json_output = reporter.to_json()
print(json_output)

# Ou pour CI
import json
data = json.loads(reporter.to_json())
if not data["is_compliant"]:
    sys.exit(1)
```

---

### to_markdown()

Genere un rapport Markdown avec badges.

```python
def to_markdown(self) -> str:
```

**Source**: [reporter.py:230](../../src/projinit/core/reporter.py#L230)

**Retourne**: String Markdown

**Structure**:
```markdown
# Project Audit Report

![Status](https://img.shields.io/badge/status-passing-brightgreen)
![Score](https://img.shields.io/badge/score-85%25-brightgreen)

## Overview

| Property | Value |
|----------|-------|
| **Path** | `/path/to/project` |
| **Type** | Python CLI Application |
| **Score** | 85.0% |

## Required Checks

| Status | Check | Message |
|--------|-------|---------|
| PASS | `has_readme` | README.md exists |
...
```

**Exemple**:
```python
md_output = reporter.to_markdown()
Path("AUDIT.md").write_text(md_output)
```

---

## Fonctions internes

### _print_header()

Affiche le header du rapport.

**Source**: [reporter.py:54](../../src/projinit/core/reporter.py#L54)

### _print_checks_by_level()

Affiche les checks groupes par niveau (required, recommended, optional).

**Source**: [reporter.py:66](../../src/projinit/core/reporter.py#L66)

### _print_score_bar()

Affiche la barre de progression du score.

**Source**: [reporter.py:97](../../src/projinit/core/reporter.py#L97)

**Couleurs**:
- >= 80%: vert
- >= 60%: jaune
- < 60%: rouge

### _print_summary()

Affiche le panel de resume.

**Source**: [reporter.py:117](../../src/projinit/core/reporter.py#L117)

### _print_suggestions()

Affiche les suggestions de correction.

**Source**: [reporter.py:147](../../src/projinit/core/reporter.py#L147)

### _print_verbose_info()

Affiche les informations techniques (temps, fichiers scannes).

**Source**: [reporter.py:175](../../src/projinit/core/reporter.py#L175)

### _get_status_icon()

Retourne l'icone coloree pour un status.

**Source**: [reporter.py:333](../../src/projinit/core/reporter.py#L333)

```python
{
    CheckStatus.PASSED: "[green]PASS[/green]",
    CheckStatus.FAILED: "[red]FAIL[/red]",
    CheckStatus.WARNING: "[yellow]WARN[/yellow]",
    CheckStatus.SKIPPED: "[dim]SKIP[/dim]",
}
```

### _get_status_emoji()

Retourne le texte status pour Markdown.

**Source**: [reporter.py:343](../../src/projinit/core/reporter.py#L343)

---

## Dependances

```python
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from projinit.core.models import AuditReport, CheckLevel, CheckResult, CheckStatus
```
