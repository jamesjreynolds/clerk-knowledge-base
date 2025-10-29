# Markdown Style Guide

This guide explains the markdown syntax rules for this documentation site and how to avoid common formatting errors.

## Why This Matters

Proper markdown syntax ensures that content renders correctly on the live site. The most common issue is **missing blank lines before lists**, which causes list items to display as run-on sentences instead of separate lines.

This project includes automated validation to catch these errors before they reach the live site.

## Lists

Lists (ordered and unordered) must be preceded by a blank line when they follow other content.

### Correct: Blank Line Before Lists

```markdown
Here is some introductory text.

- First list item
- Second list item
- Third list item
```

**Result:** List items render as separate, properly formatted lines.

### Incorrect: No Blank Line

```markdown
Here is some introductory text.
- First list item
- Second list item
- Third list item
```

**Result:** The list runs together with the previous paragraph as a single line.

## Headers and Lists

Always include a blank line between a header and a list.

### Correct Example

```markdown
## Section Title

- First item
- Second item
```

### Incorrect Example

```markdown
## Section Title
- First item
- Second item
```

**Error:** `Missing blank line before unordered list`

## Bold Text and Lists

Include a blank line between bold text and lists.

### Correct Example

```markdown
**Important points:**

1. First point
2. Second point
```

### Incorrect Example

```markdown
**Important points:**
1. First point
2. Second point
```

**Error:** `Missing blank line before ordered list`

## MkDocs Extensions

This site uses MkDocs Material theme with several extensions. These are valid syntax and will not trigger validation errors.

### Admonitions

Admonitions create colored callout boxes:

```markdown
!!! warning
    This is a warning message.
    - List items inside admonitions are fine
    - No blank line needed here

!!! info "Custom Title"
    This is an info box with a custom title.
```

**Types:** `note`, `info`, `tip`, `warning`, `danger`, `success`

### Code Blocks

Code blocks are created with triple backticks:

````markdown
```python
def example():
    # This is code
    return True
```
````

### Definition Lists

Definition lists use colons:

```markdown
Term 1
:   Definition for term 1

Term 2
:   Definition for term 2
```

### Footnotes

```markdown
This is a sentence with a footnote[^1].

[^1]: This is the footnote content.
```

## Validation

### Running Validation Locally

Before committing changes, run validation to catch errors:

```bash
# Validate all markdown files in docs/ directory
python scripts/markdown/validate_markdown.py docs/ --verbose

# See detailed output
python scripts/markdown/validate_markdown.py docs/ --output text --verbose
```

### Exit Codes

- `0` - Validation passed (no errors)
- `1` - Validation failed (errors found)

### Output Formats

```bash
# Human-readable text (default)
python scripts/markdown/validate_markdown.py docs/ --output text

# JSON format (for tooling)
python scripts/markdown/validate_markdown.py docs/ --output json

# GitHub Actions format (used in CI)
python scripts/markdown/validate_markdown.py docs/ --output github
```

## Fixing Errors

### Automated Correction

The project includes a tool to automatically fix list spacing errors:

```bash
# Preview changes without modifying files
python scripts/markdown/fix_list_spacing.py docs/ --dry-run

# Apply fixes with backup files created
python scripts/markdown/fix_list_spacing.py docs/ --backup

# Apply fixes without backup
python scripts/markdown/fix_list_spacing.py docs/ --no-backup
```

### Manual Correction

When you see a validation error:

**Error message:**
```
✗ docs/example.md
  Line 15: Missing blank line before unordered list
```

**Fix:** Open the file and add a blank line before the list at line 15.

## Common Errors

### Error 1: Missing Blank Before Ordered List

**Error:**
```
Line 25: Missing blank line before ordered list
```

**Cause:**
```markdown
Follow these steps:
1. First step
2. Second step
```

**Fix:**
```markdown
Follow these steps:

1. First step
2. Second step
```

### Error 2: Missing Blank Before Unordered List

**Error:**
```
Line 10: Missing blank line before unordered list
```

**Cause:**
```markdown
## Features
- Feature one
- Feature two
```

**Fix:**
```markdown
## Features

- Feature one
- Feature two
```

### Error 3: Paragraph to List Transition

**Cause:**
```markdown
The benefits include:
- Better performance
- Easier maintenance
```

**Fix:**
```markdown
The benefits include:

- Better performance
- Easier maintenance
```

## CI/CD Integration

All pull requests automatically run validation checks. If validation fails:

1. The build will fail and show error details
2. GitHub will show annotations on the specific lines with errors
3. The PR cannot be merged until errors are fixed

**Example annotation:**
```
docs/example.md:25 - Missing blank line before ordered list
```

## Tips for Success

1. **Preview locally:** Run `mkdocs serve` to preview your changes before committing
2. **Validate before commit:** Run the validation script to catch errors early
3. **Check the live site:** After deployment, verify that lists render correctly
4. **Use the fix tool:** For bulk changes, the automated fix tool saves time

## Getting Help

If you encounter validation errors you don't understand:

1. Check this guide for common error patterns
2. Look at existing documentation files for examples
3. Run the fix tool to see what changes are suggested
4. Ask for help in the repository issues or discussions

## Quick Reference

| Situation | Need Blank Line? |
|-----------|------------------|
| Header → List | ✅ Yes |
| Paragraph → List | ✅ Yes |
| Bold text → List | ✅ Yes |
| List item → List item | ❌ No (continuation) |
| Code block → List | ✅ Yes |
| Inside admonition | ❌ No (special context) |

---

Remember: **When in doubt, add a blank line before lists!**
