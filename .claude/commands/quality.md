# Quality Check

Run all quality checks defined in the constitution.

## Instructions

Execute the following checks in order:

### 1. Linting (ruff check)
```bash
uvx ruff check src/
```

### 2. Formatting (ruff format)
```bash
uvx ruff format src/ --check
```

### 3. Tests (pytest)
```bash
if [ -d "tests" ] && [ "$(find tests -name '*.py' -type f 2>/dev/null | head -1)" ]; then
  uv run pytest tests/ -v
else
  echo "No tests found, skipping pytest"
fi
```

## Report Summary

After running all checks, provide a summary table:

| Check | Status | Details |
|-------|--------|---------|
| Lint | PASS/FAIL | Number of errors |
| Format | PASS/FAIL | Files to reformat |
| Tests | PASS/FAIL/SKIP | Tests passed/failed |

## Arguments

Pass any of the following in $ARGUMENTS:
- `fix`: Auto-fix linting and formatting issues
- `lint`: Run only linting check
- `format`: Run only format check
- `test`: Run only tests

If no argument provided, run all checks in read-only mode.

$ARGUMENTS
