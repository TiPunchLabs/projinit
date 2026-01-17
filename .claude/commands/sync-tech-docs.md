---
description: Synchronize technical documentation (doc/) with current codebase
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Update the technical documentation in `doc/` to reflect the current state of the codebase. This command analyzes the source code and updates documentation accordingly.

## Scope

This command updates the following files in `doc/`:

| File | Source Analysis |
|------|-----------------|
| `architecture.md` | Module structure in `src/` |
| `standards.md` | YAML files in `standards/defaults/` |
| `templates.md` | Templates in `templates/` |
| `detection.md` | Markers in `core/detector.py` |
| `cli.md` | Commands in `cli/*.py` |
| `configuration.md` | Config options in `core/config.py` |
| `models.md` | Enums and dataclasses in `core/models.py` |

## Execution Steps

1. **Analyze current codebase**:
   - Read `src/projinit/core/models.py` for ProjectType enum and dataclasses
   - Read `src/projinit/core/detector.py` for detection markers
   - Read `src/projinit/standards/defaults/*.yaml` for all check definitions
   - Read `src/projinit/templates/` structure for available templates
   - Read `src/projinit/cli/*.py` for CLI commands

2. **Compare with existing documentation**:
   - Check if `doc/` directory exists
   - Compare documented items vs actual code
   - Identify missing or outdated sections

3. **Update documentation**:
   - For each doc file, update relevant sections:
     - Add new project types to architecture.md and detection.md
     - Add new checks to standards.md
     - Add new templates to templates.md
     - Add new CLI commands to cli.md
     - Add new models to models.md
   - Preserve existing explanations and examples
   - Add TODO markers for sections needing manual review

4. **Report changes**:
   - List files updated
   - List new items added
   - Suggest manual review areas

## Guidelines

- **Preserve manual content**: Only update structured sections (tables, code blocks)
- **Add, don't remove**: Flag outdated content instead of deleting
- **French comments**: Keep documentation style consistent (currently ASCII-safe French)
- **Code examples**: Update code examples if API changed

## Output

After execution, display:
```
Technical Documentation Sync Complete

Updated files:
- doc/standards.md (added 2 new checks)
- doc/models.md (added LAB project type)

No changes needed:
- doc/architecture.md
- doc/cli.md

Manual review suggested:
- doc/detection.md: verify marker weights
```

## When to Run

- After adding new project types
- After adding new checks to standards
- After adding new CLI commands
- After modifying data models
- Before major releases
