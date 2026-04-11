---
description: Generate and synchronize technical documentation (doc/) with current codebase
handoffs:
  - label: Sync User Docs
    agent: sync-docs
    prompt: Synchronize README and constitution
    send: true
  - label: Run Quality Check
    agent: quality
    prompt: Run quality checks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

**Supported arguments:**
- `--generate` or `-g`: Force full documentation generation (even if files exist)
- `--sync-only` or `-s`: Only synchronize existing documentation
- `--section <name>`: Generate/sync a specific section (overview, architecture, flow, decisions, api, internals, standards, cli, extending)
- No argument: Generate missing files and synchronize existing ones

## Purpose

**Generate and synchronize** technical documentation in `doc/` to help developers quickly understand:
- Project architecture and the rationale behind design choices
- Data flow and execution paths
- Patterns and conventions used
- Technical decisions and their justifications
- How to contribute and extend the project

## Outline

1. **Setup**: Verify `doc/` directory exists, create if missing
2. **Analyze**: Deep scan of codebase for modules, functions, patterns
3. **Generate**: Create missing documentation files from analysis
4. **Synchronize**: Update existing files with new code elements
5. **Validate**: Check internal links and code references
6. **Report**: Display summary of changes and suggestions

## Documentation Structure

Technical documentation is organized in two levels:

### Level 1: Overview (Quick Onboarding)

| File | Purpose | Content |
|------|---------|---------|
| `doc/overview.md` | Documentation entry point | Table of contents, reading guide, quick links |
| `doc/architecture.md` | System architecture | Diagrams, main components, module dependencies |
| `doc/flow.md` | Execution flow | Command path from A to Z, sequence diagrams |
| `doc/decisions.md` | Architecture Decision Records | ADRs documenting important choices and rationale |

### Level 2: Detailed Documentation (For Contributors)

| File | Purpose | Content |
|------|---------|---------|
| `doc/api/` | Internal API | Public function documentation per module |
| `doc/internals/` | Internal mechanisms | Algorithms, data structures, edge cases |
| `doc/cli.md` | CLI interface | Commands, options, usage examples |
| `doc/configuration.md` | Configuration | Options, hierarchy, examples |
| `doc/standards.md` | Standards & Checks | All available checks, how to add new ones |
| `doc/templates.md` | Template system | Available templates, variables, customization |
| `doc/models.md` | Data models | Enums, dataclasses, relationships |
| `doc/detection.md` | Auto-detection | Detection algorithm, markers, weights |
| `doc/extending.md` | Extension guide | How to add types, checks, commands |

## Phases

### Phase 1: Deep Codebase Analysis

1. **Module mapping**:
   - Scan `src/projinit/` recursively
   - Identify imports between modules (internal dependencies)
   - List public exports of each module
   - Detect patterns used (factory, strategy, etc.)

2. **Key function analysis**:
   - Identify entry points (main_cli.py, commands)
   - Trace execution flow for each command
   - Document public function signatures
   - Identify hooks and extension points

3. **Architectural choices extraction**:
   - Analyze existing docstrings and comments
   - Identify recurring patterns (error handling, configuration, etc.)
   - Spot constants and magic numbers with their justifications

4. **Data model analysis**:
   - Parse `core/models.py` for enums and dataclasses
   - Document relationships between models
   - Identify invariants and constraints

5. **Standards and checks analysis**:
   - Read all `standards/defaults/*.yaml` files
   - Categorize by check type and level
   - Document logic for each check type in `checker.py`

### Phase 2: Documentation Generation

For each documentation file, generate content following these templates:

#### `doc/overview.md`

```markdown
# Technical Documentation projinit

## Quick Navigation
- New to the project? Start with [Architecture](architecture.md)
- Understanding a command? See [Execution Flow](flow.md)
- Why this choice? Check [Decisions](decisions.md)
- Contributing? Read [Extension Guide](extending.md)

## Project Structure
[Directory tree with descriptions]

## Tech Stack
[Technologies, versions, justifications]
```

#### `doc/architecture.md`

```markdown
# Architecture

## Overview
[ASCII or Mermaid diagram of components]

## Main Components
For each module:
- Single responsibility
- Exposed interfaces
- Dependencies
- Patterns used

## Data Flow
[Diagram showing data circulation]

## Extension Points
[Where and how to extend the system]
```

#### `doc/flow.md`

```markdown
# Execution Flow

For each CLI command (check, update, new, config):

## Command: projinit check

### Steps
1. Argument parsing (main_cli.py:XX)
2. Config loading (core/config.py:XX)
3. Project type detection (core/detector.py:XX)
4. ...

### Sequence Diagram
[Mermaid or ASCII diagram]

### Decision Points
- If X then Y because Z
- Error handling: ...
```

#### `doc/decisions.md` (ADRs)

```markdown
# Architecture Decision Records

## ADR-001: Choice of argparse vs click

**Context**: Need for a CLI framework
**Decision**: argparse (stdlib) + questionary
**Rationale**:
- No external dependency for basic parsing
- questionary only for interactive mode
**Consequences**: ...
**Date**: YYYY-MM-DD

## ADR-002: src/ layout structure
...
```

#### `doc/api/*.md`

For each important module:

```markdown
# Module: core/checker.py

## Responsibility
Execute conformity checks

## Public Functions

### check_project(path, project_type, config) -> List[CheckResult]
Execute all applicable checks.

**Parameters:**
- path: Project path
- project_type: Detected or specified type
- config: Loaded configuration

**Returns:** List of check results

**Example:**
\`\`\`python
results = check_project(Path("."), ProjectType.PYTHON_CLI, config)
\`\`\`

## Internal Functions (For Contributors)
[Documentation of important private functions]
```

#### `doc/internals/`

For complex algorithms:

```markdown
# Type Detection Algorithm

## Overview
Detection uses a scoring system based on markers.

## Markers and Weights
[Table of markers with weights]

## Algorithm
1. Scan files at root
2. For each marker found, add weight to type score
3. Highest score wins
4. In case of tie: [tie-breaking rule]

## Edge Cases
- Empty project: returns UNKNOWN
- Conflicting markers: [behavior]
```

### Phase 3: Synchronization

1. **Compare with existing**:
   - Identify auto-generated sections (marked `<!-- AUTO-GENERATED-START -->`)
   - Preserve manual sections
   - Detect inconsistencies

2. **Smart update**:
   - Update auto-generated tables and lists
   - Add new elements
   - Mark obsolete elements with `[DEPRECATED]`
   - Never delete manual content

3. **Validation**:
   - Check internal links
   - Verify code references (file:line) exist
   - Report inconsistencies

### Phase 4: Report

Display structured summary with changes, warnings, and suggestions.

## Key Rules

### Generation

- **Extract, don't invent**: Documentation must reflect code, not guess
- **Cite sources**: Each statement must reference file:line
- **Mermaid diagrams**: Prefer Mermaid for diagrams (GitHub rendered)
- **Executable examples**: Code examples must be testable

### Style

- **Technical French**: Documentation in French, English technical terms accepted
- **Concise but complete**: No verbosity, but cover all cases
- **Progressive disclosure**: From general to specific, simple to complex
- **Cross-links**: Connect concepts between documents

### Maintenance

- **Auto-generated sections**: Wrap with `<!-- AUTO-GENERATED-START -->` and `<!-- AUTO-GENERATED-END -->`
- **Manual sections**: Preserved during updates
- **Versioning**: Include last update date in each file

## Output

Display a structured summary:

```text
╭─────────────────────────────────────────────────────────╮
│           Technical Documentation Sync                   │
╰─────────────────────────────────────────────────────────╯

Generated (3 new files):
   • doc/overview.md
   • doc/flow.md
   • doc/decisions.md

Updated (2 files):
   • doc/architecture.md
     └─ Added: merger component
     └─ Updated: dependency diagram
   • doc/standards.md
     └─ Added: 3 new checks (yaml_valid, has_tests, ci_configured)

Unchanged (4 files):
   • doc/cli.md, doc/configuration.md, doc/models.md, doc/detection.md

Warnings (1):
   • doc/api/detector.md:23 - Function `detect_by_files` renamed

Suggested:
   • Consider adding ADR for the new merger algorithm
   • doc/flow.md needs sequence diagram for `update` command

Documentation coverage: 87% of public API documented
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--generate` | `-g` | Force full generation (overwrite existing) |
| `--sync-only` | `-s` | Only update existing files |
| `--section <name>` | | Target specific section |
| `--dry-run` | `-n` | Show changes without writing |
| `--verbose` | `-v` | Show detailed analysis |

## Example Usage

```bash
# Full generation and sync
/sync-tech-docs

# Force regenerate all documentation
/sync-tech-docs --generate

# Only sync existing files
/sync-tech-docs --sync-only

# Generate only architecture documentation
/sync-tech-docs --section architecture

# Preview changes without writing
/sync-tech-docs --dry-run

# Verbose mode with full analysis
/sync-tech-docs --verbose
```

## Integration

This command can be:
- Integrated in CI to check documentation freshness
- Automatically executed after `/commit` on source files
- Combined with `/quality` to include documentation coverage

### Workflow Integration

| Event | Action |
|-------|--------|
| After `/speckit.implement` | Run `/sync-tech-docs` |
| Before release | Run `/sync-tech-docs --generate` |
| After API changes | Run `/sync-tech-docs --section api` |
| Developer onboarding | Run `/sync-tech-docs` to ensure up-to-date docs |

## When to Run

- **Initial generation**: On new project or after major refactoring
- **After feature additions**: New commands, checks, project types
- **After API modifications**: Signature changes, new modules
- **Before release**: Verify documentation is current
- **Onboarding**: Regenerate to ensure everything is documented
