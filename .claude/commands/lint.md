# Lint Project

Execute linting tools on the projinit codebase.

## Instructions

1. Run ruff linter on the source code:
   ```bash
   uvx ruff check src/
   ```

2. If there are errors, analyze them and propose fixes.

3. If the user wants to auto-fix (argument contains "fix"), run:
   ```bash
   uvx ruff check src/ --fix
   ```

4. If the user wants format check (argument contains "format"), run:
   ```bash
   uvx ruff format src/ --check
   ```

5. If the user wants to apply formatting (argument contains "format" and "fix"), run:
   ```bash
   uvx ruff format src/
   ```

6. Report a summary of:
   - Total errors found
   - Errors fixed (if fix was requested)
   - Remaining issues that need manual attention

## Arguments

Pass any of the following in $ARGUMENTS:
- `fix`: Auto-fix linting issues where possible
- `format`: Check code formatting
- `all`: Run both linting and formatting checks

$ARGUMENTS
