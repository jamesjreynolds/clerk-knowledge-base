# Data Model: Markdown Quality Controls

**Phase**: 1 (Design & Contracts)
**Date**: 2025-10-28
**Purpose**: Define entities and data structures for validation system

## Overview

This feature operates on markdown files and validation results. Since it's a tooling feature rather than an application with persistent storage, the "data model" consists of runtime data structures and file-based entities.

## Core Entities

### 1. MarkdownFile

**Description**: Represents a markdown documentation file to be validated or corrected

**Attributes**:
- `path` (str): Absolute or relative path to the markdown file
- `content` (str): Full text content of the file
- `lines` (List[str]): Content split into individual lines
- `line_ending` (str): Detected line ending style ("\\n" or "\\r\\n")
- `encoding` (str): File encoding (default: "utf-8")

**Validation Rules**:
- Path must end with `.md` extension
- Path must exist in filesystem
- File must be readable with UTF-8 encoding
- Content must not be empty

**State Transitions**: N/A (immutable after loading)

**Relationships**:
- Contains zero or more `ValidationError` instances
- May be processed by `CorrectionOperation`

### 2. ValidationError

**Description**: Represents a specific markdown syntax error detected in a file

**Attributes**:
- `file_path` (str): Path to file containing the error
- `line_number` (int): Line number where error occurs (1-indexed)
- `error_type` (str): Type of error (e.g., "missing_blank_before_list")
- `severity` (str): Error severity level ("error" or "warning")
- `message` (str): Human-readable description of the problem
- `suggestion` (str): Recommended fix for the error
- `context_before` (Optional[str]): Line before the error (for context)
- `context_line` (str): The actual line with the error

**Validation Rules**:
- `line_number` must be positive integer
- `error_type` must be from predefined set:
  - `missing_blank_before_ordered_list`
  - `missing_blank_before_unordered_list`
  - `missing_blank_after_header_before_list`
  - `missing_blank_after_bold_before_list`
- `severity` must be "error" or "warning"
- `file_path` must reference valid MarkdownFile

**State Transitions**: N/A (immutable once created)

**Relationships**:
- Belongs to one `MarkdownFile`
- Included in `ValidationReport`

### 3. ValidationRule

**Description**: Defines a specific markdown syntax requirement to be enforced

**Attributes**:
- `rule_id` (str): Unique identifier (e.g., "MD032", "BLANK_BEFORE_LIST")
- `name` (str): Short descriptive name
- `description` (str): Full description of what the rule checks
- `severity` (str): Default severity level ("error" or "warning")
- `enabled` (bool): Whether rule is active
- `pattern` (Optional[str]): Regex pattern for detection (if applicable)
- `exclude_patterns` (List[str]): Patterns to exclude from checking (e.g., code blocks)

**Validation Rules**:
- `rule_id` must be unique across all rules
- `severity` must be "error" or "warning"
- `pattern` must be valid regex if provided

**Predefined Rules**:
```python
RULES = [
    ValidationRule(
        rule_id="BLANK_BEFORE_ORDERED_LIST",
        name="Blank line before ordered list",
        description="Ordered lists must be preceded by a blank line",
        severity="error",
        pattern=r"^\d+\.\s",
        exclude_patterns=["```", "!!!"]
    ),
    ValidationRule(
        rule_id="BLANK_BEFORE_UNORDERED_LIST",
        name="Blank line before unordered list",
        description="Unordered lists must be preceded by a blank line",
        severity="error",
        pattern=r"^[-*+]\s",
        exclude_patterns=["```", "!!!"]
    )
]
```

**State Transitions**: N/A (configuration is static)

**Relationships**:
- Produces `ValidationError` instances when violations detected

### 4. ValidationReport

**Description**: Aggregates all validation results for a validation run

**Attributes**:
- `timestamp` (datetime): When validation was executed
- `files_checked` (int): Total number of files validated
- `errors` (List[ValidationError]): All errors found
- `warnings` (List[ValidationError]): All warnings found (if applicable)
- `passed` (bool): Whether validation passed (no errors)
- `duration_ms` (float): Time taken to complete validation

**Computed Properties**:
- `error_count`: len(errors)
- `warning_count`: len(warnings)
- `files_with_errors`: Set of unique file paths with errors

**Validation Rules**:
- `files_checked` must be non-negative
- `passed` is True only if `error_count == 0`
- `duration_ms` must be positive

**Output Formats**:
- JSON: For machine parsing
- Text: For console output with color coding
- GitHub Actions: Formatted as GitHub workflow annotations

**Relationships**:
- Contains multiple `ValidationError` instances
- Aggregates results from multiple `MarkdownFile` validations

### 5. CorrectionOperation

**Description**: Represents a single correction to be applied to a markdown file

**Attributes**:
- `file_path` (str): Path to file to be corrected
- `line_number` (int): Line number where correction occurs (1-indexed)
- `operation_type` (str): Type of correction ("insert_blank_line")
- `before_context` (str): Line content before the insertion point
- `after_context` (str): Line content after the insertion point
- `applied` (bool): Whether correction has been applied

**Validation Rules**:
- `line_number` must be positive integer within file bounds
- `operation_type` must be from predefined set: `insert_blank_line`, `remove_blank_line`, `normalize_spacing`
- `applied` starts as False, set to True after successful application

**State Transitions**:
```
Created (applied=False) → Applied (applied=True) → [terminal state]
```

**Relationships**:
- Targets one `MarkdownFile`
- Generated based on `ValidationError` instances

### 6. CorrectionReport

**Description**: Summary of all corrections applied during a fix operation

**Attributes**:
- `timestamp` (datetime): When corrections were applied
- `files_modified` (List[str]): Paths of files that were changed
- `corrections_applied` (List[CorrectionOperation]): All corrections made
- `files_unchanged` (List[str]): Files that had no issues
- `success` (bool): Whether all corrections applied successfully
- `backup_created` (bool): Whether backup was created before modifications

**Computed Properties**:
- `total_corrections`: len(corrections_applied)
- `total_files_modified`: len(files_modified)

**Output Formats**:
- JSON: For programmatic consumption
- Markdown: For PR descriptions or commit messages
- Text: For console output

**Relationships**:
- Contains multiple `CorrectionOperation` instances
- References multiple `MarkdownFile` instances

## Data Flow

```
1. Discovery Phase:
   Directory → [MarkdownFile, MarkdownFile, ...]

2. Validation Phase:
   MarkdownFile → ValidationRule.check() → [ValidationError, ...]
   [ValidationError, ...] → ValidationReport

3. Correction Phase (if errors found):
   ValidationError → CorrectionOperation
   CorrectionOperation → Modified MarkdownFile
   [CorrectionOperation, ...] → CorrectionReport

4. Reporting Phase:
   ValidationReport → Console/JSON/GitHub Actions output
   CorrectionReport → Console/Markdown output
```

## File Formats

### Configuration: .pymarkdown.json

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
    "site/"
  ]
}
```

### Validation Output: validation-report.json

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
      "suggestion": "Insert a blank line before the list",
      "context_before": "**Common expenses:**",
      "context_line": "- Facilities maintenance"
    }
  ],
  "duration_ms": 125.3
}
```

### Correction Output: correction-report.md

```markdown
# Markdown Correction Report

**Date**: 2025-10-28 10:31:00
**Files Modified**: 3

## Summary

- Total corrections: 7
- Files modified: 3
- Files unchanged: 12

## Details

### docs/financial/expenses.md
- Line 42: Inserted blank line before unordered list
- Line 87: Inserted blank line before ordered list

### docs/membership/quarterly-reports.md
- Line 15: Inserted blank line before unordered list
- Line 56: Inserted blank line before unordered list
- Line 123: Inserted blank line before ordered list

### docs/annual-history/index.md
- Line 8: Inserted blank line before unordered list
- Line 34: Inserted blank line before unordered list
```

## Validation Constraints

### Cross-Entity Rules

1. **Correction-Validation Consistency**: Every `CorrectionOperation` should fix exactly one `ValidationError`
2. **File State Consistency**: A `MarkdownFile` cannot be both in `files_modified` and `files_unchanged`
3. **Error Uniqueness**: No duplicate `ValidationError` entries for same file/line combination
4. **Path Consistency**: All file paths should be relative to project root or absolute

### Performance Constraints

- `ValidationReport.duration_ms` must be < 120000 (2 minutes per FR-012)
- Individual file validation should complete in < 100ms for typical file size
- Memory usage should remain < 100MB even with 50+ files

## Testing Considerations

### Test Data Requirements

Need fixture files for each scenario:
- `valid_lists.md`: No errors (baseline)
- `header_no_space.md`: Header directly followed by list
- `bold_no_space.md`: Bold text directly followed by list
- `mixed_issues.md`: Multiple error types
- `mkdocs_extensions.md`: Valid MkDocs syntax that should NOT error

### State Verification

For each test:
1. Load MarkdownFile from fixture
2. Run validation to produce ValidationReport
3. Assert expected error_count and error_types
4. Apply corrections to produce CorrectionReport
5. Re-validate to confirm error_count == 0
6. Verify file content matches expected corrected state
