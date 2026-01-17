---
description: Synchronize README.md and constitution.md with current project state after feature implementation
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command ensures documentation coherence after implementing a feature or making significant changes.
It should be called:
- At the end of a feature implementation
- After adding new project types or standards
- After modifying CLI commands
- After updating the technology stack

## Outline

### 1. Analyze Current Project State

Read and analyze the following files to understand current capabilities:

**Core Files:**
- `src/projinit/__init__.py` - Current version
- `src/projinit/core/models.py` - Project types enum
- `src/projinit/core/detector.py` - Detection markers
- `src/projinit/cli/*.py` - Available CLI commands

**Standards:**
- `src/projinit/standards/defaults/*.yaml` - All standard files

**Configuration:**
- `pyproject.toml` - Dependencies and project metadata

### 2. README.md Update

Read `README.md` and update the following sections to reflect current state:

**Version Banner:**
- Update version number if changed

**Features Table:**
- List all available commands from CLI
- Include any new commands added

**Project Types:**
- Update list of supported project types from `ProjectType` enum
- Include display names

**Standards Table:**
- Update required/recommended checks from base.yaml
- Add any new checks

**Configuration Options:**
- Ensure configuration examples reflect current capabilities

**Development Section:**
- Update development commands if changed

### 3. Constitution Update

Read `.specify/memory/constitution.md` and synchronize:

**Stack Technique:**
- Verify dependencies match `pyproject.toml`
- Add new technologies if introduced

**Architecture:**
- Update module structure if files were added/removed
- Update supported technologies list

**Version and Date:**
- Increment version (PATCH for docs sync, MINOR for new features)
- Update `Last Amended` date to today

### 4. Generate Sync Report

Create a summary of changes:

| File | Section | Change |
|------|---------|--------|
| README.md | Version | 2.0.0 -> 2.1.0 |
| README.md | Project Types | Added LAB |
| constitution.md | Stack | Added LAB standards |
| constitution.md | Version | 1.2.0 -> 1.3.0 |

### 5. Validation

Before writing changes:
- Ensure no placeholder tokens remain
- Verify all links are valid
- Check markdown formatting
- Confirm version consistency between files

### 6. Write Changes

- Write updated README.md
- Write updated constitution.md
- Provide git diff summary

### 7. Suggest Commit

Output a suggested commit message:
```
docs: sync documentation with current project state

- Update README.md with new features/types
- Update constitution.md version and stack
```

## Arguments

- `readme-only`: Only update README.md
- `constitution-only`: Only update constitution.md
- `dry-run`: Show what would be changed without writing
- `verbose`: Show detailed analysis

## Integration with Feature Workflow

This command should be invoked:

1. **After `/speckit.implement`** - Automatic documentation sync
2. **After manual implementation** - Run `/sync-docs`
3. **Before merge/PR** - Ensure docs are current

## Example Usage

```bash
# Full sync after feature implementation
/sync-docs

# Preview changes without writing
/sync-docs dry-run

# Only update README
/sync-docs readme-only

# Verbose mode with full analysis
/sync-docs verbose
```
