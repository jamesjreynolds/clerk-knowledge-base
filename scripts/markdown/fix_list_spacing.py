#!/usr/bin/env python3
"""
Fix markdown files by inserting blank lines before lists.

This script scans markdown files and automatically inserts blank lines
before ordered and unordered lists where they are missing, which fixes
rendering issues in MkDocs and other markdown renderers.

Usage:
    python fix_list_spacing.py docs/
    python fix_list_spacing.py docs/ --dry-run
    python fix_list_spacing.py docs/ --backup --report markdown
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from markdown_validator import fix_directory, format_correction_report


def main():
    """Main entry point for fix_list_spacing script."""
    parser = argparse.ArgumentParser(
        description="Fix markdown files by inserting blank lines before lists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/                                  # Fix all files with backup
  %(prog)s docs/ --dry-run                        # Preview changes without modifying
  %(prog)s docs/ --no-backup                      # Fix without creating backups
  %(prog)s docs/ --report markdown --output fix.md  # Generate markdown report
        """
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Path to directory containing markdown files"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files"
    )

    parser.add_argument(
        "--backup",
        dest="backup",
        action="store_true",
        default=True,
        help="Create .bak backup files before modifying (default: true)"
    )

    parser.add_argument(
        "--no-backup",
        dest="backup",
        action="store_false",
        help="Skip creating backup files"
    )

    parser.add_argument(
        "--report",
        choices=["text", "json", "markdown"],
        default="text",
        help="Report format (default: text)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Write report to file (default: stdout)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output showing all operations"
    )

    args = parser.parse_args()

    # Validate directory exists
    if not args.directory.exists():
        print(f"ERROR: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(3)

    if not args.directory.is_dir():
        print(f"ERROR: Not a directory: {args.directory}", file=sys.stderr)
        sys.exit(3)

    try:
        # Run corrections
        report = fix_directory(
            args.directory,
            dry_run=args.dry_run,
            create_backup=args.backup and not args.dry_run,
            verbose=args.verbose
        )

        # Format report
        output = format_correction_report(report, args.report)

        # Output report
        if args.output:
            args.output.write_text(output, encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(output)

        # Exit with success
        sys.exit(0 if report.success else 1)

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    except PermissionError as e:
        print(f"ERROR: Permission denied: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
