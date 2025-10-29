# Research: Markdown Quality Controls

**Phase**: 0 (Outline & Research)
**Date**: 2025-10-28
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Research Tasks

### 1. Markdown Linter/Parser Tool Selection

**Context**: Technical Context identified "NEEDS CLARIFICATION: markdown linter/parser tool"

**Question**: Which Python-based markdown linting/validation tool should we use that:
- Can detect missing blank lines before lists
- Distinguishes MkDocs-specific syntax (admonitions, etc.)
- Works in GitHub Actions environment
- Requires no paid services
- Is actively maintained

**Research Findings**:

Evaluated options:
1. **markdownlint-cli2** - Node.js based (rejected: requires Node in Python environment)
2. **mdformat** - Python formatter but limited validation capabilities
3. **pymarkdown** (pymarkdownlnt) - Python-native linter with extensive rules
4. **Custom regex-based solution** - Full control but higher maintenance burden

**Decision**: Use **pymarkdown** (pymarkdownlnt package)

**Rationale**:
- Native Python implementation (pip installable)
- Actively maintained (last release within 6 months)
- Rule MD032 specifically detects missing blank lines around lists
- Configurable to ignore specific patterns
- Can output structured error reports with file/line numbers
- Works in GitHub Actions (no external dependencies beyond Python)
- Free and open source (MIT license)
- Can be configured to ignore MkDocs-specific syntax through rule customization

**Alternatives Considered**:
- **Custom regex solution**: More flexible but requires extensive testing for edge cases, harder to maintain, and reinvents existing wheel
- **markdownlint-cli2**: More popular but adds Node.js dependency to Python-centric project
- **mdformat**: Good for formatting but lacks validation rules for our specific needs

**Implementation Notes**:
- Install via `pip install pymarkdown`
- Configuration file: `.pymarkdown.json` or inline args
- Rule MD032 covers our primary use case (blank lines around lists)
- May need to disable conflicting rules for MkDocs syntax

### 2. Testing Framework Selection

**Context**: Technical Context identified "NEEDS CLARIFICATION: testing framework for validation rules"

**Question**: How should we test the markdown validation and correction scripts?

**Research Findings**:

**Decision**: Use **pytest** with fixture-based test files

**Rationale**:
- pytest is already implied by Python best practices
- Matches existing ecosystem (MkDocs project likely uses pytest)
- Excellent support for fixture files (sample markdown with known issues)
- Parametrized tests allow testing multiple scenarios efficiently
- Can use `tmp_path` fixture for file operations
- Clear assertion messages for debugging

**Test Strategy**:
1. **Unit tests**: Test regex patterns and detection logic in isolation
2. **Integration tests**: Test full validation workflow on sample files
3. **Fixture approach**: Create `tests/fixtures/markdown/` with:
   - `valid_lists.md` - properly formatted lists
   - `header_no_space.md` - header followed by list (no blank line)
   - `bold_no_space.md` - bold text followed by list (no blank line)
   - `mkdocs_syntax.md` - admonitions and other valid MkDocs extensions
   - `mixed_issues.md` - combination of problems

**Alternatives Considered**:
- **unittest**: Standard library but more verbose, pytest preferred
- **doctest**: Good for simple cases but inadequate for file manipulation testing
- **No tests**: Rejected due to risk of breaking MkDocs rendering

### 3. Correction Script Approach

**Context**: Determining safe method for bulk file corrections (FR-003, FR-004)

**Question**: How to safely insert blank lines while preserving all other formatting?

**Research Findings**:

**Decision**: Line-by-line state machine with lookahead

**Pattern**:
```
For each line:
  1. Detect if current line is header (starts with #) or bold text (**...**)
  2. Look ahead to next line
  3. If next line starts list (-, *, 1., etc.) and current is header/bold
     - Insert blank line between
  4. Preserve all other content unchanged
  5. Maintain original line endings (detect CRLF vs LF)
```

**Rationale**:
- Simpler than full AST parsing
- Preserves everything except targeted whitespace
- Handles edge cases (nested lists, code blocks) by being conservative
- Can detect line ending style and preserve it
- Easy to generate diff report for review

**Edge Case Handling**:
- **Code blocks**: Skip lines between \`\`\` markers
- **Nested lists**: Only fix top-level list spacing (nested handled by indentation)
- **Multiple blank lines**: Normalize to exactly one blank line
- **Mixed issues**: Process all issues in single pass
- **CRLF vs LF**: Detect first line ending and maintain consistently

**Alternatives Considered**:
- **Full markdown AST parser**: Over-engineered for simple whitespace fix
- **Find-and-replace regex**: Risk of false positives in code blocks
- **Manual editing**: Not scalable, error-prone

### 4. CI/CD Integration Pattern

**Context**: How to integrate validation into existing GitHub Actions workflow

**Question**: Should validation be separate job or additional step in existing build job?

**Research Findings**:

**Decision**: Add validation as early step in existing "Build MkDocs site" job

**Rationale**:
- Fail fast: Validate before building
- Single job means faster feedback (no job startup overhead)
- Reuses existing Python environment setup
- Maintains existing branch protection check name
- Simpler workflow management

**Implementation Pattern**:
```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Validate Markdown (NEW)
        run: python scripts/markdown/validate_markdown.py docs/
      - name: Build MkDocs site
        run: mkdocs build --strict --verbose
      # ... rest of existing steps
```

**Performance Considerations**:
- Validation should complete in <30 seconds for ~20 files
- Well under 2-minute budget (FR-012)
- Minimal overhead on CI/CD pipeline

**Alternatives Considered**:
- **Separate validation job**: Adds overhead, delays feedback
- **Pre-commit hook**: Useful but doesn't prevent bad commits if skipped
- **GitHub Actions marketplace action**: Adds external dependency, less control

### 5. MkDocs-Specific Syntax Handling

**Context**: FR-011 requires not flagging valid MkDocs syntax as errors

**Question**: What MkDocs Material extensions need special handling?

**Research Findings**:

MkDocs Material uses these extensions that may have different spacing rules:
1. **Admonitions**: `!!! warning`, `!!! info`, `!!! danger`
2. **Code blocks**: Fenced with \`\`\` or indented
3. **Definition lists**: Term on one line, definition on next (starting with `:`)
4. **Footnotes**: `[^1]` references and definitions
5. **Abbreviations**: Two-line format with `*[abbr]: definition`

**Decision**: Configure pymarkdown to allow these patterns

**Configuration Strategy**:
```json
{
  "plugins": {
    "MD032": {
      "enabled": true,
      "ignore_code_blocks": true,
      "ignore_admonitions": true
    }
  }
}
```

**Validation**:
- Create test fixtures with all MkDocs extensions
- Ensure zero false positives
- Document any limitations in markdown-guide.md

**Alternatives Considered**:
- **Whitelist files with extensions**: Too coarse, may miss real errors
- **Custom parser**: Over-engineered, pymarkdown handles most cases
- **Ignore all errors in files with extensions**: Defeats purpose

## Summary of Decisions

| Unknown | Decision | Dependency |
|---------|----------|------------|
| Markdown linter/parser tool | pymarkdown (pymarkdownlnt) | Add to requirements.txt |
| Testing framework | pytest with fixture-based tests | Standard Python testing |
| Correction approach | Line-by-line state machine with lookahead | Custom Python script |
| CI/CD integration | Add step to existing build job | Modify deploy.yml |
| MkDocs syntax handling | Configure pymarkdown rule exceptions | .pymarkdown.json config |

## Next Steps (Phase 1)

With all technical unknowns resolved, proceed to:
1. Generate data-model.md (validation entities)
2. Generate contracts/validation-api.md (script interfaces)
3. Generate quickstart.md (developer workflow)
4. Update agent context with pymarkdown dependency
