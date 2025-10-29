# Implementation Plan: Markdown Quality Controls

**Branch**: `002-the-markdown-files` | **Date**: 2025-10-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-the-markdown-files/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement markdown quality controls to fix existing formatting issues where lists render as run-on sentences due to missing blank lines after headers/bold text, and establish automated validation in CI/CD pipeline to prevent future formatting errors. The solution will use Python-based tooling compatible with existing MkDocs infrastructure and GitHub Actions environment.

## Technical Context

**Language/Version**: Python 3.11 (matches CI/CD environment per CLAUDE.md)
**Primary Dependencies**: MkDocs >=1.5.0, Material theme >=9.4.0 (existing); pymarkdownlnt >=0.9.0 (resolved in research.md)
**Storage**: N/A (operates on markdown files in `docs/` directory)
**Testing**: pytest with fixture-based tests (resolved in research.md)
**Target Platform**: GitHub Actions (Ubuntu runner), local development environments
**Project Type**: Documentation tooling (scripts + CI/CD integration)
**Performance Goals**: Complete validation of entire documentation set in <2 minutes (per FR-012)
**Constraints**:
- Must not require additional paid services or tools (per spec)
- Must preserve MkDocs-specific syntax (admonitions, footnotes, etc.) per FR-011
- Must work within existing GitHub Actions runner environment
- Must complete validation within CI/CD time budget (<2 min)
**Scale/Scope**:
- ~10-20 markdown files in `docs/` directory (based on typical MkDocs project)
- 2-3 specific validation rules (missing blank lines before ordered/unordered lists)
- Single GitHub Actions workflow modification

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Documentation-First Architecture ✓ COMPLIANT

- All content remains in Markdown format under version control
- No changes to Markdown storage structure
- Git history preserved during bulk corrections (per constraint)
- Continues to render through MkDocs

**Status**: PASS - Feature enhances documentation quality without changing architecture

### Principle II: Contributor Accessibility ✓ COMPLIANT

- Validation provides clear error messages with file/line numbers (FR-010, FR-013)
- Contributors can understand and fix errors within 5 minutes (SC-005)
- Guidance documentation will be provided (P3 user story)
- Local testing capability with `mkdocs serve` maintained
- Setup time unaffected (no new local dependencies required beyond existing Python environment)

**Status**: PASS - Feature improves contributor experience through clear feedback

### Principle III: Automation-Driven Deployment (NON-NEGOTIABLE) ✓ COMPLIANT

- Validation integrated into existing GitHub Actions workflow (FR-007)
- No manual deployment steps introduced
- Automated checks run on every PR
- Build feedback maintained through CI/CD pipeline
- Must complete within reasonable time (<2 min per FR-012, well under 5 min target)

**Status**: PASS - Feature strengthens automation by adding quality gates

### Principle IV: Quality Assurance & Review ✓ COMPLIANT

- Adds automated quality gate for markdown syntax (FR-007)
- Link validation complemented by syntax validation
- Maintains PR review requirement
- Enhances formatting consistency (core goal of feature)
- Branch protection integration (merge blocked on validation errors per acceptance scenario)

**Status**: PASS - Feature directly implements quality assurance improvements

### Principle V: Static-First & Performance ✓ COMPLIANT

- No backend dependencies introduced
- Operates on static markdown files
- Validation runs at build time (not runtime)
- No impact on page load times or mobile responsiveness
- GitHub Pages hosting unchanged

**Status**: PASS - Feature maintains static-first architecture

### Overall Gate Status: ✓ ALL GATES PASSED

No constitution violations identified. Feature aligns with all core principles and enhances quality assurance capabilities.

## Project Structure

### Documentation (this feature)

```
specs/002-the-markdown-files/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── validation-api.md
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
# Tooling scripts (new for this feature)
scripts/
├── markdown/
│   ├── fix_list_spacing.py      # Script to fix existing markdown files
│   └── validate_markdown.py     # Validation script for CI/CD
└── tests/
    └── test_markdown_validation.py

# CI/CD integration (modified)
.github/
└── workflows/
    └── deploy.yml               # Modified to add validation step

# Documentation (modified + new)
docs/
├── [existing markdown files]    # Will be corrected by fix script
└── contributing/
    └── markdown-guide.md        # New P3 guidance documentation

# Project configuration (modified)
requirements.txt                 # Updated with validation dependencies
```

**Structure Decision**: This is a tooling feature that adds scripts to support the existing documentation project. We use the "single project" pattern extended with a `scripts/` directory for tooling code. The feature modifies existing infrastructure (CI/CD workflow) and documentation files rather than creating a standalone application. No complex source hierarchy needed since this is utility scripting, not a multi-tier application.

## Complexity Tracking

*No constitution violations to justify - all gates passed.*

---

## Phase 1 Complete: Constitution Re-Evaluation

**Date**: 2025-10-28
**Status**: ✓ ALL GATES STILL PASSED

### Re-Evaluation Summary

After completing Phase 0 (Research) and Phase 1 (Design & Contracts), all technical unknowns have been resolved and the design artifacts have been generated. Re-evaluating constitution compliance with full implementation details:

### Principle I: Documentation-First Architecture ✓ CONFIRMED COMPLIANT

**Design Validation**:
- Scripts operate on markdown files in place (no format changes)
- Version control preserved (git history maintained)
- Backup strategy implemented (.bak files before modifications)
- MkDocs rendering unaffected (only whitespace changes)

**Status**: ✓ PASS - Design maintains documentation-first principles

### Principle II: Contributor Accessibility ✓ CONFIRMED COMPLIANT

**Design Validation**:
- CLI scripts have clear `--help` documentation
- Error messages include file/line/suggestion (per contracts/validation-api.md)
- Quickstart.md provides step-by-step developer guide
- New dependency (pymarkdownlnt) is pip-installable, no complex setup
- Local testing workflow: `python scripts/markdown/validate_markdown.py docs/`
- Estimated setup time impact: +2 minutes (well within 35-minute budget)

**Status**: ✓ PASS - Design improves accessibility with clear tooling

### Principle III: Automation-Driven Deployment (NON-NEGOTIABLE) ✓ CONFIRMED COMPLIANT

**Design Validation**:
- Validation integrated as CI/CD step (see quickstart.md Step 11)
- No manual steps required (automated validation on every PR)
- GitHub Actions format output for workflow annotations
- Performance target: <30 seconds validation overhead (well within 5-minute budget)
- Fail-fast approach (validate before build)

**Status**: ✓ PASS - Design strengthens automation with quality gates

### Principle IV: Quality Assurance & Review ✓ CONFIRMED COMPLIANT

**Design Validation**:
- Automated validation catches errors before merge (FR-007)
- Test suite with fixtures ensures validation accuracy (data-model.md)
- PR review still required (validation complements, doesn't replace)
- Clear reporting in multiple formats (text/json/github/markdown)
- Branch protection integration via exit codes

**Status**: ✓ PASS - Design implements robust quality assurance

### Principle V: Static-First & Performance ✓ CONFIRMED COMPLIANT

**Design Validation**:
- No runtime dependencies (validation at build time only)
- No backend services introduced
- Performance benchmarks documented (quickstart.md)
- Zero impact on GitHub Pages hosting
- Static site generation unchanged

**Status**: ✓ PASS - Design maintains static-first architecture

### New Dependencies Assessment

**pymarkdownlnt** (Python package, free/open-source):
- Purpose: Markdown linting with rule MD032 (blank lines around lists)
- License: MIT (no legal/cost concerns)
- Maintenance: Active (last release within 6 months per research.md)
- Installation: `pip install pymarkdownlnt` (standard Python workflow)
- CI/CD Impact: Added to requirements.txt, installed in existing Python step
- **Constitution Impact**: ✓ No violations - aligns with Python-based tooling approach

### Overall Phase 1 Status: ✓ READY FOR IMPLEMENTATION

All constitution checks passed. No violations or concerns identified. Design artifacts complete:
- ✓ research.md - All technical unknowns resolved
- ✓ data-model.md - Entities and data structures defined
- ✓ contracts/validation-api.md - CLI and module interfaces specified
- ✓ quickstart.md - Developer workflow documented

**Next Phase**: Run `/speckit.tasks` to generate dependency-ordered implementation tasks
