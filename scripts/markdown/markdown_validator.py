"""
Markdown validation and correction tools.

This module provides functionality to detect and fix markdown syntax issues,
specifically focusing on missing blank lines before lists.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
import re
import json


# ============================================================================
# Data Classes (T007-T012)
# ============================================================================

@dataclass
class MarkdownFile:
    """Represents a markdown documentation file to be validated or corrected."""
    path: Path
    content: str
    lines: List[str]
    line_ending: str = "\n"
    encoding: str = "utf-8"


@dataclass
class ValidationError:
    """Represents a specific markdown syntax error detected in a file."""
    file_path: str
    line_number: int
    error_type: str
    severity: str
    message: str
    suggestion: str
    context_before: Optional[str] = None
    context_line: str = ""


@dataclass
class ValidationRule:
    """Defines a specific markdown syntax requirement to be enforced."""
    rule_id: str
    name: str
    description: str
    severity: str
    enabled: bool = True
    pattern: Optional[str] = None
    exclude_patterns: List[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Aggregates all validation results for a validation run."""
    timestamp: datetime
    files_checked: int
    errors: List[ValidationError]
    warnings: List[ValidationError] = field(default_factory=list)
    passed: bool = True
    duration_ms: float = 0.0

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def files_with_errors(self) -> set:
        return {err.file_path for err in self.errors}


@dataclass
class CorrectionOperation:
    """Represents a single correction to be applied to a markdown file."""
    file_path: str
    line_number: int
    operation_type: str
    before_context: str
    after_context: str
    applied: bool = False


@dataclass
class CorrectionReport:
    """Summary of all corrections applied during a fix operation."""
    timestamp: datetime
    files_modified: List[str]
    corrections_applied: List[CorrectionOperation]
    files_unchanged: List[str]
    success: bool
    backup_created: bool = False

    @property
    def total_corrections(self) -> int:
        return len(self.corrections_applied)

    @property
    def total_files_modified(self) -> int:
        return len(self.files_modified)


# Predefined validation rules
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


# ============================================================================
# Core Functions (T013-T017)
# ============================================================================

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
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    content = path.read_text(encoding="utf-8")

    # Detect line ending style
    if "\r\n" in content:
        line_ending = "\r\n"
        lines = content.split("\r\n")
    else:
        line_ending = "\n"
        lines = content.split("\n")

    return MarkdownFile(
        path=path,
        content=content,
        lines=lines,
        line_ending=line_ending,
        encoding="utf-8"
    )


def is_mkdocs_extension(line: str) -> bool:
    """
    Check if line is valid MkDocs-specific syntax.

    Args:
        line: Single line of markdown text

    Returns:
        True if line is MkDocs extension (admonition, etc.)
    """
    # Admonitions (!!!)
    if line.strip().startswith("!!!"):
        return True

    # Code block markers
    if line.strip().startswith("```"):
        return True

    # Definition lists (starts with colon and space)
    if re.match(r"^\s*:\s+", line):
        return True

    return False


def detect_list_spacing_issues(file: MarkdownFile) -> List[ValidationError]:
    """
    Detect missing blank lines before lists in markdown file.

    Args:
        file: MarkdownFile to validate

    Returns:
        List of ValidationError objects (empty if no issues)
    """
    errors = []
    in_code_block = False

    for i, line in enumerate(file.lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip if in code block or is MkDocs extension
        if in_code_block or is_mkdocs_extension(line):
            continue

        # Check if current line is a list item
        is_ordered_list = bool(re.match(r"^\d+\.\s", line))
        is_unordered_list = bool(re.match(r"^[-*+]\s", line))

        if is_ordered_list or is_unordered_list:
            # Check if previous line exists and is not blank
            if i > 0:
                prev_line = file.lines[i - 1]
                prev_is_list = bool(re.match(r"^\d+\.\s", prev_line)) or bool(re.match(r"^[-*+]\s", prev_line))

                # Only flag error if previous line is not blank AND not a list item
                # (i.e., this is the START of a new list, not a continuation)
                if prev_line.strip() != "" and not prev_is_list:
                    error_type = "missing_blank_before_ordered_list" if is_ordered_list else "missing_blank_before_unordered_list"
                    list_type = "ordered" if is_ordered_list else "unordered"

                    errors.append(ValidationError(
                        file_path=str(file.path),
                        line_number=i + 1,  # 1-indexed for user display
                        error_type=error_type,
                        severity="error",
                        message=f"Missing blank line before {list_type} list",
                        suggestion=f"Insert a blank line between '{prev_line.strip()}' and the list",
                        context_before=prev_line.strip(),
                        context_line=line.strip()
                    ))

    return errors


def format_validation_report(report: ValidationReport, format: str = "text") -> str:
    """
    Format validation report for output.

    Args:
        report: ValidationReport to format
        format: Output format ("text", "json", "github")

    Returns:
        Formatted report string
    """
    if format == "json":
        return json.dumps({
            "timestamp": report.timestamp.isoformat(),
            "files_checked": report.files_checked,
            "passed": report.passed,
            "errors": [
                {
                    "file_path": err.file_path,
                    "line_number": err.line_number,
                    "error_type": err.error_type,
                    "severity": err.severity,
                    "message": err.message,
                    "suggestion": err.suggestion
                }
                for err in report.errors
            ],
            "duration_ms": report.duration_ms
        }, indent=2)

    elif format == "github":
        # GitHub Actions annotation format
        lines = []
        for err in report.errors:
            lines.append(f"::error file={err.file_path},line={err.line_number}::{err.message}")
        lines.append(f"\nChecked {report.files_checked} files, found {report.error_count} errors")
        return "\n".join(lines)

    else:  # text format
        lines = []
        lines.append(f"Validating markdown files...\n")

        # Group errors by file
        errors_by_file = {}
        for err in report.errors:
            if err.file_path not in errors_by_file:
                errors_by_file[err.file_path] = []
            errors_by_file[err.file_path].append(err)

        # Show files with errors
        for file_path, file_errors in errors_by_file.items():
            lines.append(f"✗ {file_path}")
            for err in file_errors:
                lines.append(f"  Line {err.line_number}: {err.message}")

        lines.append(f"\nChecked {report.files_checked} files")
        lines.append(f"Found {report.error_count} errors in {len(errors_by_file)} file(s)")
        lines.append(f"\nValidation {'PASSED' if report.passed else 'FAILED'}")

        return "\n".join(lines)


def fix_list_spacing(file: MarkdownFile) -> Tuple[MarkdownFile, List[CorrectionOperation]]:
    """
    Fix list spacing issues in markdown file.

    Args:
        file: MarkdownFile to correct

    Returns:
        Tuple of (corrected_file, list_of_corrections)
    """
    corrections = []
    new_lines = []
    in_code_block = False
    i = 0

    while i < len(file.lines):
        line = file.lines[i]

        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            i += 1
            continue

        # Skip if in code block or is MkDocs extension
        if in_code_block or is_mkdocs_extension(line):
            new_lines.append(line)
            i += 1
            continue

        # Check if current line is a list item
        is_list = bool(re.match(r"^\d+\.\s", line)) or bool(re.match(r"^[-*+]\s", line))

        if is_list and len(new_lines) > 0:
            prev_line = new_lines[-1]
            prev_is_list = bool(re.match(r"^\d+\.\s", prev_line)) or bool(re.match(r"^[-*+]\s", prev_line))

            # Only insert blank line if previous line is not blank AND not a list item
            # (i.e., this is the START of a new list, not a continuation)
            if prev_line.strip() != "" and not prev_is_list:
                # Insert blank line
                corrections.append(CorrectionOperation(
                    file_path=str(file.path),
                    line_number=i + 1,
                    operation_type="insert_blank_line",
                    before_context=prev_line.strip(),
                    after_context=line.strip(),
                    applied=True
                ))
                new_lines.append("")  # Add blank line

        new_lines.append(line)
        i += 1

    # Create corrected file
    corrected_content = file.line_ending.join(new_lines)
    corrected_file = MarkdownFile(
        path=file.path,
        content=corrected_content,
        lines=new_lines,
        line_ending=file.line_ending,
        encoding=file.encoding
    )

    return corrected_file, corrections


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
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    start_time = datetime.now()
    all_corrections = []
    files_modified = []
    files_unchanged = []

    # Find all markdown files
    md_files = list(directory.rglob("*.md"))

    if verbose:
        print(f"Found {len(md_files)} markdown files in {directory}")

    for md_file in md_files:
        if verbose:
            print(f"Processing {md_file}...")

        # Load file
        file = load_markdown_file(md_file)

        # Fix list spacing
        corrected_file, corrections = fix_list_spacing(file)

        if corrections:
            files_modified.append(str(md_file))
            all_corrections.extend(corrections)

            if not dry_run:
                # Create backup if requested
                if create_backup:
                    backup_path = md_file.with_suffix(md_file.suffix + ".bak")
                    backup_path.write_text(file.content, encoding=file.encoding)

                # Write corrected file
                md_file.write_text(corrected_file.content, encoding=file.encoding)

                if verbose:
                    print(f"  Applied {len(corrections)} corrections")
        else:
            files_unchanged.append(str(md_file))
            if verbose:
                print(f"  No changes needed")

    return CorrectionReport(
        timestamp=datetime.now(),
        files_modified=files_modified,
        corrections_applied=all_corrections,
        files_unchanged=files_unchanged,
        success=True,
        backup_created=create_backup and not dry_run
    )


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
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    start_time = datetime.now()
    all_errors = []

    # Find all markdown files
    md_files = list(directory.rglob("*.md"))

    if verbose:
        print(f"Found {len(md_files)} markdown files in {directory}")

    for md_file in md_files:
        if verbose:
            print(f"Validating {md_file}...")

        # Load file
        file = load_markdown_file(md_file)

        # Detect list spacing issues
        errors = detect_list_spacing_issues(file)

        if errors:
            all_errors.extend(errors)
            if verbose:
                print(f"  Found {len(errors)} error(s)")
        else:
            if verbose:
                print(f"  ✓ No errors")

    # Calculate duration
    duration = (datetime.now() - start_time).total_seconds() * 1000

    return ValidationReport(
        timestamp=datetime.now(),
        files_checked=len(md_files),
        errors=all_errors,
        warnings=[],
        passed=len(all_errors) == 0,
        duration_ms=duration
    )


def format_correction_report(report: CorrectionReport, format: str = "text") -> str:
    """
    Format correction report for output.

    Args:
        report: CorrectionReport to format
        format: Output format ("text", "json", "markdown")

    Returns:
        Formatted report string
    """
    if format == "json":
        return json.dumps({
            "timestamp": report.timestamp.isoformat(),
            "files_modified": report.files_modified,
            "corrections_applied": [
                {
                    "file_path": op.file_path,
                    "line_number": op.line_number,
                    "operation_type": op.operation_type,
                    "before_context": op.before_context,
                    "after_context": op.after_context
                }
                for op in report.corrections_applied
            ],
            "success": report.success,
            "backup_created": report.backup_created
        }, indent=2)

    elif format == "markdown":
        lines = []
        lines.append("# Markdown Correction Report")
        lines.append(f"\n**Date**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Files Modified**: {report.total_files_modified}\n")
        lines.append("## Summary")
        lines.append(f"- Total corrections: {report.total_corrections}")
        lines.append(f"- Files modified: {report.total_files_modified}")
        lines.append(f"- Backup files: {'Created' if report.backup_created else 'Not created'}\n")

        # Group corrections by file
        corrections_by_file = {}
        for op in report.corrections_applied:
            if op.file_path not in corrections_by_file:
                corrections_by_file[op.file_path] = []
            corrections_by_file[op.file_path].append(op)

        lines.append("## Modified Files\n")
        for file_path, ops in corrections_by_file.items():
            lines.append(f"### {file_path}")
            for op in ops:
                lines.append(f"- Line {op.line_number}: Inserted blank line before list")
            lines.append("")

        return "\n".join(lines)

    else:  # text format
        lines = []
        lines.append(f"Scanning markdown files...\n")

        # Group corrections by file
        corrections_by_file = {}
        for op in report.corrections_applied:
            if op.file_path not in corrections_by_file:
                corrections_by_file[op.file_path] = []
            corrections_by_file[op.file_path].append(op)

        for file_path, ops in corrections_by_file.items():
            lines.append(f"{file_path}")
            for op in ops:
                lines.append(f"  Line {op.line_number}: Inserted blank line before list")
            lines.append("")

        lines.append(f"Modified {report.total_files_modified} files, applied {report.total_corrections} corrections")
        if report.backup_created:
            lines.append("Backup files created with .bak extension")

        return "\n".join(lines)
