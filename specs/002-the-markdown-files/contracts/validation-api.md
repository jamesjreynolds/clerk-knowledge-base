# Script Interface Contracts: Markdown Quality Controls

**Phase**: 1 (Design & Contracts)
**Date**: 2025-10-28
**Purpose**: Define command-line interfaces and Python module APIs for validation tooling

## Overview

This feature consists of two primary scripts and one supporting module. Since these are command-line tools (not REST APIs), the "contracts" define CLI interfaces, Python function signatures, and exit codes.

## CLI Script Contracts

### 1. validate_markdown.py

**Purpose**: Validate markdown files for syntax errors (used in CI/CD)

**Location**: `scripts/markdown/validate_markdown.py`

**CLI Interface**:
```bash
python scripts/markdown/validate_markdown.py [OPTIONS] <directory>

Arguments:
  directory              Path to directory containing markdown files (required)

Options:
  --config FILE          Path to .pymarkdown.json config file (default: .pymarkdown.json)
  --output FORMAT        Output format: text|json|github (default: text)
  --fail-on-warning      Fail with exit code 1 on warnings (default: errors only)
  --verbose, -v          Verbose output showing all files checked
  --quiet, -q            Suppress output except errors
  --help, -h             Show help message

Examples:
  python scripts/markdown/validate_markdown.py docs/
  python scripts/markdown/validate_markdown.py docs/ --output json
  python scripts/markdown/validate_markdown.py docs/ --output github --verbose
```

**Exit Codes**:
- `0`: Validation passed (no errors)
- `1`: Validation failed (errors found)
- `2`: Invalid arguments or configuration error
- `3`: File system error (permission denied, file not found)

**Output Formats**:

**Text Format** (default, for human consumption):
```
Validating markdown files in docs/...

✓ docs/index.md
✓ docs/membership/index.md
✗ docs/financial/expenses.md
  Line 42: Missing blank line before unordered list
  Line 87: Missing blank line before ordered list

Checked 15 files
Found 2 errors in 1 file

Validation FAILED
```

**JSON Format** (for machine parsing):
```json
{
  "timestamp": "2025-10-28T10:30:00Z",
  "files_checked": 15,
  "passed": false,
  "errors": [
    {
      "file_path": "docs/financial/expenses.md",
      "line_number": 42,
      "error_type": "missing_blank_before_unordered_list",
      "severity": "error",
      "message": "Missing blank line before unordered list",
      "suggestion": "Insert a blank line between '**Common expenses:**' and the list"
    }
  ],
  "duration_ms": 125.3
}
```

**GitHub Actions Format** (GitHub workflow annotations):
```
::error file=docs/financial/expenses.md,line=42::Missing blank line before unordered list
::error file=docs/financial/expenses.md,line=87::Missing blank line before ordered list

Checked 15 files, found 2 errors
```

**Python Function Signature**:
```python
def validate_directory(
    directory: Path,
    config: Optional[Path] = None,
    verbose: bool = False
) -> ValidationReport:
    """
    Validate all markdown files in directory.

    Args:
        directory: Path to directory to validate
        config: Optional path to .pymarkdown.json config
        verbose: Whether to output verbose messages

    Returns:
        ValidationReport with validation results

    Raises:
        FileNotFoundError: If directory doesn't exist
        PermissionError: If directory not readable
        ValueError: If config file is invalid
    """
```

---

### 2. fix_list_spacing.py

**Purpose**: Automatically correct markdown files with missing blank lines before lists

**Location**: `scripts/markdown/fix_list_spacing.py`

**CLI Interface**:
```bash
python scripts/markdown/fix_list_spacing.py [OPTIONS] <directory>

Arguments:
  directory              Path to directory containing markdown files (required)

Options:
  --dry-run              Show what would be changed without modifying files
  --backup               Create .bak backup files before modifying (default: true)
  --no-backup            Skip creating backup files
  --report FORMAT        Report format: text|json|markdown (default: text)
  --output FILE          Write report to file (default: stdout)
  --verbose, -v          Verbose output showing all operations
  --help, -h             Show help message

Examples:
  python scripts/markdown/fix_list_spacing.py docs/ --dry-run
  python scripts/markdown/fix_list_spacing.py docs/ --backup
  python scripts/markdown/fix_list_spacing.py docs/ --report markdown --output corrections.md
```

**Exit Codes**:
- `0`: Corrections applied successfully (or dry-run completed)
- `1`: Errors encountered during correction
- `2`: Invalid arguments
- `3`: File system error

**Output Formats**:

**Text Format** (default):
```
Scanning markdown files in docs/...

docs/financial/expenses.md
  Line 42: Inserted blank line before unordered list
  Line 87: Inserted blank line before ordered list

docs/membership/quarterly-reports.md
  Line 15: Inserted blank line before unordered list

Modified 2 files, applied 3 corrections
Backup files created with .bak extension
```

**JSON Format**:
```json
{
  "timestamp": "2025-10-28T10:31:00Z",
  "files_modified": [
    "docs/financial/expenses.md",
    "docs/membership/quarterly-reports.md"
  ],
  "corrections_applied": [
    {
      "file_path": "docs/financial/expenses.md",
      "line_number": 42,
      "operation_type": "insert_blank_line",
      "before_context": "**Common expenses:**",
      "after_context": "- Facilities maintenance"
    }
  ],
  "success": true,
  "backup_created": true
}
```

**Markdown Format** (for PR descriptions):
```markdown
# Markdown Correction Report

**Date**: 2025-10-28 10:31:00
**Files Modified**: 2

## Summary
- Total corrections: 3
- Files modified: 2
- Backup files: Created

## Modified Files

### docs/financial/expenses.md
- Line 42: Inserted blank line before unordered list
- Line 87: Inserted blank line before ordered list

### docs/membership/quarterly-reports.md
- Line 15: Inserted blank line before unordered list
```

**Python Function Signature**:
```python
def fix_directory(
    directory: Path,
    dry_run: bool = False,
    create_backup: bool = True,
    verbose: bool = False
) -> CorrectionReport:
    """
    Fix markdown files in directory by inserting blank lines before lists.

    Args:
        directory: Path to directory to process
        dry_run: If True, report changes without modifying files
        create_backup: If True, create .bak files before modifying
        verbose: Whether to output verbose messages

    Returns:
        CorrectionReport with correction details

    Raises:
        FileNotFoundError: If directory doesn't exist
        PermissionError: If files not writable
    """
```

---

## Python Module API

### markdown_validator Module

**Location**: `scripts/markdown/markdown_validator.py`

**Purpose**: Reusable validation logic used by both scripts

**Public Functions**:

```python
def load_markdown_file(path: Path) -> MarkdownFile:
    """
    Load markdown file from disk.

    Args:
        path: Path to markdown file

    Returns:
        MarkdownFile object with content and metadata

    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file isn't valid UTF-8
    """

def detect_list_spacing_issues(file: MarkdownFile) -> List[ValidationError]:
    """
    Detect missing blank lines before lists in markdown file.

    Args:
        file: MarkdownFile to validate

    Returns:
        List of ValidationError objects (empty if no issues)
    """

def fix_list_spacing(file: MarkdownFile) -> Tuple[MarkdownFile, List[CorrectionOperation]]:
    """
    Fix list spacing issues in markdown file.

    Args:
        file: MarkdownFile to correct

    Returns:
        Tuple of (corrected_file, list_of_corrections)
    """

def is_mkdocs_extension(line: str) -> bool:
    """
    Check if line is valid MkDocs-specific syntax.

    Args:
        line: Single line of markdown text

    Returns:
        True if line is MkDocs extension (admonition, etc.)
    """

def format_validation_report(
    report: ValidationReport,
    format: str = "text"
) -> str:
    """
    Format validation report for output.

    Args:
        report: ValidationReport to format
        format: Output format ("text", "json", "github")

    Returns:
        Formatted report string
    """

def format_correction_report(
    report: CorrectionReport,
    format: str = "text"
) -> str:
    """
    Format correction report for output.

    Args:
        report: CorrectionReport to format
        format: Output format ("text", "json", "markdown")

    Returns:
        Formatted report string
    """
```

**Data Classes** (see data-model.md for details):
- `MarkdownFile`
- `ValidationError`
- `ValidationRule`
- `ValidationReport`
- `CorrectionOperation`
- `CorrectionReport`

---

## GitHub Actions Integration

**Workflow Step Contract**:

```yaml
- name: Validate Markdown Syntax
  run: |
    python scripts/markdown/validate_markdown.py docs/ \
      --output github \
      --verbose
  continue-on-error: false
```

**Expected Behavior**:
- Step fails (workflow fails) if validation errors found
- Errors annotated on PR with file/line references
- Success message logged if no errors
- Completes in < 30 seconds for typical project

---

## Configuration File Contract

**File**: `.pymarkdown.json`

**Schema**:
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

**Fields**:
- `plugins.MD032.enabled` (bool): Enable blank line rule
- `ignore_paths` (array): Directory patterns to skip

---

## Testing Contracts

**Test File**: `scripts/tests/test_markdown_validation.py`

**Required Test Functions**:

```python
def test_detect_missing_blank_before_ordered_list():
    """Verify detection of missing blank line before ordered list"""

def test_detect_missing_blank_before_unordered_list():
    """Verify detection of missing blank line before unordered list"""

def test_ignore_code_blocks():
    """Verify code blocks are not flagged as errors"""

def test_ignore_mkdocs_admonitions():
    """Verify MkDocs admonitions are not flagged"""

def test_fix_preserves_content():
    """Verify corrections preserve all content except whitespace"""

def test_fix_preserves_line_endings():
    """Verify line ending style (CRLF/LF) is preserved"""

def test_fix_idempotent():
    """Verify running fix twice produces same result"""

def test_validation_report_json_format():
    """Verify JSON output matches schema"""

def test_cli_exit_codes():
    """Verify correct exit codes for success/failure/error"""
```

**Test Fixtures Required**:
- `fixtures/markdown/valid_lists.md`
- `fixtures/markdown/header_no_space.md`
- `fixtures/markdown/bold_no_space.md`
- `fixtures/markdown/mkdocs_syntax.md`
- `fixtures/markdown/mixed_issues.md`

---

## Performance Requirements

**Validation Script**:
- Single file (1 KB): < 10ms
- Single file (100 KB): < 100ms
- Full directory (20 files, 500 KB total): < 2 seconds
- Must meet FR-012: Complete within 2 minutes for entire documentation set

**Correction Script**:
- Single file: < 50ms
- Full directory (20 files): < 5 seconds

**Memory Usage**:
- Peak memory: < 100 MB
- No memory leaks across multiple files

---

## Error Handling Contracts

**All Scripts Must**:
1. Validate inputs before processing
2. Provide clear error messages with context
3. Use appropriate exit codes
4. Clean up resources (close files) on error
5. Not leave files in inconsistent state (backup on failure)

**Error Message Format**:
```
ERROR: {error_type}
  File: {file_path}
  Line: {line_number}
  Details: {detailed_message}
  Suggestion: {how_to_fix}
```

---

## Backward Compatibility

**Version 1.0**:
- Initial implementation
- No backward compatibility concerns

**Future Considerations**:
- Config file format is extensible (add new rules)
- JSON output schema versioned if structure changes
- CLI arguments follow semver (breaking changes require major version bump)
