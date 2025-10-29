# Quickstart: Markdown Quality Controls

**Phase**: 1 (Design & Contracts)
**Date**: 2025-10-28
**Purpose**: Developer guide for implementing and using the markdown validation tooling

## Overview

This quickstart walks through the implementation workflow for the Markdown Quality Controls feature, from initial setup through testing and deployment.

## Prerequisites

- Python 3.11+ installed
- Git repository cloned locally
- Virtual environment activated (recommended)
- Basic familiarity with pytest and Python scripting

## Development Workflow

### Step 1: Install Dependencies

```bash
# Add to requirements.txt
echo "pymarkdownlnt>=0.9.0" >> requirements.txt

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Project Structure

```bash
# Create directories
mkdir -p scripts/markdown
mkdir -p scripts/tests/fixtures/markdown

# Create placeholder files
touch scripts/markdown/__init__.py
touch scripts/markdown/markdown_validator.py
touch scripts/markdown/validate_markdown.py
touch scripts/markdown/fix_list_spacing.py
touch scripts/tests/test_markdown_validation.py
```

### Step 3: Implement Core Validation Logic

**File**: `scripts/markdown/markdown_validator.py`

Start with the data classes and basic file loading:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime

@dataclass
class MarkdownFile:
    path: Path
    content: str
    lines: List[str]
    line_ending: str = "\n"
    encoding: str = "utf-8"

@dataclass
class ValidationError:
    file_path: str
    line_number: int
    error_type: str
    severity: str
    message: str
    suggestion: str
    context_before: Optional[str] = None
    context_line: str = ""

# Implement load_markdown_file() function
# Implement detect_list_spacing_issues() function
# See contracts/validation-api.md for full signatures
```

**Testing Strategy**: Write tests first for each function before implementation (TDD).

### Step 4: Create Test Fixtures

**File**: `scripts/tests/fixtures/markdown/header_no_space.md`

```markdown
# Test Header
- List item without blank line
- Should trigger error
```

**File**: `scripts/tests/fixtures/markdown/valid_lists.md`

```markdown
# Valid Header

- List item with blank line
- Should pass validation
```

Create fixtures for all scenarios listed in data-model.md.

### Step 5: Implement Tests

**File**: `scripts/tests/test_markdown_validation.py`

```python
import pytest
from pathlib import Path
from scripts.markdown.markdown_validator import (
    load_markdown_file,
    detect_list_spacing_issues
)

@pytest.fixture
def fixture_dir():
    return Path(__file__).parent / "fixtures" / "markdown"

def test_detect_missing_blank_before_unordered_list(fixture_dir):
    file = load_markdown_file(fixture_dir / "header_no_space.md")
    errors = detect_list_spacing_issues(file)

    assert len(errors) == 1
    assert errors[0].error_type == "missing_blank_before_unordered_list"
    assert errors[0].line_number == 2

def test_valid_lists_pass(fixture_dir):
    file = load_markdown_file(fixture_dir / "valid_lists.md")
    errors = detect_list_spacing_issues(file)

    assert len(errors) == 0
```

Run tests:
```bash
cd /path/to/project
pytest scripts/tests/test_markdown_validation.py -v
```

### Step 6: Implement CLI Scripts

**File**: `scripts/markdown/validate_markdown.py`

```python
#!/usr/bin/env python3
"""
Validate markdown files for syntax errors.
See contracts/validation-api.md for full interface specification.
"""

import sys
import argparse
from pathlib import Path
from markdown_validator import validate_directory, format_validation_report

def main():
    parser = argparse.ArgumentParser(
        description="Validate markdown files for syntax errors"
    )
    parser.add_argument("directory", type=Path, help="Directory to validate")
    parser.add_argument("--output", choices=["text", "json", "github"],
                       default="text", help="Output format")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    try:
        report = validate_directory(args.directory, verbose=args.verbose)
        print(format_validation_report(report, args.output))
        sys.exit(0 if report.passed else 1)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x scripts/markdown/validate_markdown.py
```

### Step 7: Test Locally

```bash
# Test validation on actual docs
python scripts/markdown/validate_markdown.py docs/ --verbose

# Test with different output formats
python scripts/markdown/validate_markdown.py docs/ --output json
python scripts/markdown/validate_markdown.py docs/ --output github
```

### Step 8: Implement Fix Script

**File**: `scripts/markdown/fix_list_spacing.py`

```python
#!/usr/bin/env python3
"""
Fix markdown files by inserting blank lines before lists.
See contracts/validation-api.md for full interface specification.
"""

import sys
import argparse
from pathlib import Path
from markdown_validator import fix_directory, format_correction_report

def main():
    parser = argparse.ArgumentParser(
        description="Fix markdown list spacing issues"
    )
    parser.add_argument("directory", type=Path, help="Directory to process")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show changes without modifying files")
    parser.add_argument("--no-backup", dest="backup", action="store_false",
                       help="Skip creating backup files")
    parser.add_argument("--report", choices=["text", "json", "markdown"],
                       default="text", help="Report format")

    args = parser.parse_args()

    try:
        report = fix_directory(
            args.directory,
            dry_run=args.dry_run,
            create_backup=args.backup
        )
        print(format_correction_report(report, args.report))
        sys.exit(0 if report.success else 1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Step 9: Run Corrections (Dry Run First)

```bash
# Preview changes
python scripts/markdown/fix_list_spacing.py docs/ --dry-run

# Apply corrections with backup
python scripts/markdown/fix_list_spacing.py docs/ --backup

# Verify corrections
python scripts/markdown/validate_markdown.py docs/
```

### Step 10: Configure pymarkdown

**File**: `.pymarkdown.json` (create in project root)

```json
{
  "plugins": {
    "MD032": {
      "enabled": true
    }
  },
  "ignore_paths": [
    "node_modules/",
    ".venv/",
    "site/",
    "specs/"
  ]
}
```

### Step 11: Integrate with CI/CD

**File**: `.github/workflows/deploy.yml`

Add validation step to existing build job (after checkout, before build):

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      # NEW STEP - Add here
      - name: Validate Markdown Syntax
        run: |
          python scripts/markdown/validate_markdown.py docs/ \
            --output github \
            --verbose

      - name: Build MkDocs site
        run: mkdocs build --strict --verbose

      # ... rest of workflow
```

### Step 12: Test CI/CD Integration

```bash
# Commit changes to feature branch
git add scripts/ requirements.txt .pymarkdown.json .github/workflows/deploy.yml
git commit -m "feat: add markdown quality controls

- Add validation and fix scripts
- Integrate validation into CI/CD pipeline
- Configure pymarkdown linter

Implements specs/002-the-markdown-files/spec.md"

# Push and observe CI/CD
git push origin 002-the-markdown-files
```

Create PR and verify:
- CI/CD runs validation step
- Validation errors appear as annotations
- Build fails if errors present

### Step 13: Create Documentation (P3 User Story)

**File**: `docs/contributing/markdown-guide.md`

```markdown
# Markdown Formatting Guide

## Lists

Lists must be preceded by a blank line:

✅ **Correct**:
\`\`\`markdown
## Section Header

- First item
- Second item
\`\`\`

❌ **Incorrect**:
\`\`\`markdown
## Section Header
- First item
- Second item
\`\`\`

## Validation

Run validation locally:
\`\`\`bash
python scripts/markdown/validate_markdown.py docs/
\`\`\`

Fix issues automatically:
\`\`\`bash
python scripts/markdown/fix_list_spacing.py docs/
\`\`\`
```

Add to `mkdocs.yml` navigation:
```yaml
nav:
  # ... existing sections
  - Contributing:
    - contributing/markdown-guide.md
```

## Common Tasks

### Running Validation Locally

```bash
# Validate all docs
python scripts/markdown/validate_markdown.py docs/

# Verbose output
python scripts/markdown/validate_markdown.py docs/ -v

# JSON output for scripting
python scripts/markdown/validate_markdown.py docs/ --output json
```

### Fixing Existing Files

```bash
# Preview changes
python scripts/markdown/fix_list_spacing.py docs/ --dry-run

# Apply with backup
python scripts/markdown/fix_list_spacing.py docs/ --backup

# Generate markdown report
python scripts/markdown/fix_list_spacing.py docs/ --report markdown --output report.md
```

### Adding New Validation Rules

1. Add rule to `ValidationRule` definitions in `markdown_validator.py`
2. Implement detection logic in `detect_list_spacing_issues()`
3. Add test fixtures for new rule
4. Update tests to cover new rule
5. Document rule in `docs/contributing/markdown-guide.md`

### Debugging Validation Issues

```bash
# Check specific file
python -c "
from pathlib import Path
from scripts.markdown.markdown_validator import load_markdown_file, detect_list_spacing_issues

file = load_markdown_file(Path('docs/financial/expenses.md'))
errors = detect_list_spacing_issues(file)
for error in errors:
    print(f'Line {error.line_number}: {error.message}')
"
```

## Troubleshooting

### Issue: False Positives on MkDocs Syntax

**Solution**: Update `.pymarkdown.json` to exclude specific patterns:
```json
{
  "plugins": {
    "MD032": {
      "enabled": true,
      "ignore_patterns": ["!!!"]
    }
  }
}
```

### Issue: CI/CD Timeout

**Solution**: Validation should complete in <30 seconds. If timing out:
1. Check for infinite loops in detection logic
2. Verify files aren't being read multiple times
3. Add performance logging with `--verbose`

### Issue: Line Endings Changed After Fix

**Solution**: Fix script should preserve line endings. Verify:
```python
# In fix_list_spacing():
original_ending = file.line_ending  # Detected during load
# ... apply fixes ...
corrected_content = "\n".join(lines).replace("\n", original_ending)
```

## Performance Benchmarks

Expected performance on typical project:
- Validation: 15-20 files in <2 seconds
- Correction: 15-20 files in <5 seconds
- CI/CD overhead: <30 seconds total

If performance degrades:
1. Profile with `python -m cProfile`
2. Check for unnecessary file I/O
3. Verify rules aren't overlapping

## Next Steps

After implementing Phase 1:
1. Run `/speckit.tasks` to generate actionable task breakdown
2. Follow tasks.md for step-by-step implementation
3. Create PR with all changes once validated
4. Monitor CI/CD for 1-2 weeks to catch edge cases

## Resources

- **Spec**: `specs/002-the-markdown-files/spec.md`
- **Data Model**: `specs/002-the-markdown-files/data-model.md`
- **Contracts**: `specs/002-the-markdown-files/contracts/validation-api.md`
- **pymarkdown Docs**: https://github.com/jackdewinter/pymarkdown
- **MkDocs Material**: https://squidfunk.github.io/mkdocs-material/
