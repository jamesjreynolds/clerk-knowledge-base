#!/usr/bin/env python3
"""
Validate markdown files for syntax errors.

This script scans markdown files and reports any syntax errors such as
missing blank lines before lists, which cause rendering issues in MkDocs
and other markdown renderers.

Usage:
    python validate_markdown.py docs/
    python validate_markdown.py docs/ --output json
    python validate_markdown.py docs/ --output github --verbose
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from markdown_validator import validate_directory, format_validation_report


def main():
    """Main entry point for validate_markdown script."""
    parser = argparse.ArgumentParser(
        description="Validate markdown files for syntax errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/                           # Validate all files (text output)
  %(prog)s docs/ --output json             # JSON output for machine parsing
  %(prog)s docs/ --output github --verbose # GitHub Actions format with details
        """
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Path to directory containing markdown files"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to .pymarkdown.json config file (default: .pymarkdown.json)"
    )

    parser.add_argument(
        "--output",
        choices=["text", "json", "github"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Fail with exit code 1 on warnings (default: errors only)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output showing all files checked"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output except errors"
    )

    args = parser.parse_args()

    # Validate directory exists
    if not args.directory.exists():
        if not args.quiet:
            print(f"ERROR: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(3)

    if not args.directory.is_dir():
        if not args.quiet:
            print(f"ERROR: Not a directory: {args.directory}", file=sys.stderr)
        sys.exit(3)

    try:
        # Run validation
        report = validate_directory(
            args.directory,
            config=args.config,
            verbose=args.verbose and not args.quiet
        )

        # Format and output report (unless quiet)
        if not args.quiet:
            output = format_validation_report(report, args.output)
            print(output)

        # Determine exit code
        if report.passed:
            sys.exit(0)
        else:
            sys.exit(1)

    except FileNotFoundError as e:
        if not args.quiet:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    except PermissionError as e:
        if not args.quiet:
            print(f"ERROR: Permission denied: {e}", file=sys.stderr)
        sys.exit(3)
    except ValueError as e:
        if not args.quiet:
            print(f"ERROR: Invalid configuration: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        if not args.quiet:
            print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
