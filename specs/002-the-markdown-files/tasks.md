# Tasks: Markdown Quality Controls

**Input**: Design documents from `/specs/002-the-markdown-files/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/validation-api.md

**Tests**: This feature does NOT include test tasks - tests are not explicitly requested in the specification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- Repository root for project structure
- `scripts/markdown/` for tooling scripts
- `scripts/tests/` for test files
- `.github/workflows/` for CI/CD integration
- `docs/contributing/` for documentation

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure needed by all user stories

- [X] T001 Create `scripts/markdown/` directory for validation and correction scripts
- [X] T002 Create `scripts/tests/` directory for test files
- [X] T003 Create `scripts/tests/fixtures/markdown/` directory for test fixture files
- [X] T004 [P] Add `pymarkdownlnt>=0.9.0` to `requirements.txt`
- [X] T005 [P] Create `.pymarkdown.json` configuration file in repository root
- [X] T006 [P] Create `scripts/markdown/__init__.py` (empty file for Python module)

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core validation module that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Implement `MarkdownFile` dataclass in `scripts/markdown/markdown_validator.py`
- [X] T008 [P] Implement `ValidationError` dataclass in `scripts/markdown/markdown_validator.py`
- [X] T009 [P] Implement `ValidationRule` dataclass in `scripts/markdown/markdown_validator.py`
- [X] T010 [P] Implement `ValidationReport` dataclass in `scripts/markdown/markdown_validator.py`
- [X] T011 [P] Implement `CorrectionOperation` dataclass in `scripts/markdown/markdown_validator.py`
- [X] T012 [P] Implement `CorrectionReport` dataclass in `scripts/markdown/markdown_validator.py`
- [X] T013 Implement `load_markdown_file()` function in `scripts/markdown/markdown_validator.py`
- [X] T014 Implement `is_mkdocs_extension()` function in `scripts/markdown/markdown_validator.py` (detect admonitions, code blocks)
- [X] T015 Implement `detect_list_spacing_issues()` function in `scripts/markdown/markdown_validator.py` (core validation logic)
- [X] T016 Implement `format_validation_report()` function in `scripts/markdown/markdown_validator.py` (text/json/github formats)
- [X] T017 Implement `format_correction_report()` function in `scripts/markdown/markdown_validator.py` (text/json/markdown formats)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Fix Existing Markdown Formatting Issues (Priority: P1) 🎯 MVP

**Goal**: Correct all existing markdown files so lists render properly on the live site

**Independent Test**: Review all documentation pages on the live site and verify that all ordered and unordered lists display as separate lines (not run-on sentences). Success means zero improperly rendered lists across all pages.

**Acceptance Criteria**:
- Given a markdown file with a header immediately followed by a list (no blank line), When the correction is applied, Then a blank line is inserted between the header and list
- Given a markdown file with bold text immediately followed by a list (no blank line), When the correction is applied, Then a blank line is inserted between the bold text and list
- Given all corrected files are deployed to the live site, When any page is viewed, Then all lists render as distinct line items (not run-on sentences)
- Given the corrected files, When validated with standard markdown parsers, Then no list formatting errors are reported

### Implementation for User Story 1

- [X] T018 [US1] Implement `fix_list_spacing()` function in `scripts/markdown/markdown_validator.py` (line-by-line state machine with lookahead)
- [X] T019 [US1] Implement `fix_directory()` function in `scripts/markdown/markdown_validator.py` (process all markdown files in directory)
- [X] T020 [US1] Create `scripts/markdown/fix_list_spacing.py` CLI script with argument parsing (directory, --dry-run, --backup, --no-backup, --report, --output, --verbose, --help)
- [X] T021 [US1] Implement main() function in `scripts/markdown/fix_list_spacing.py` (calls fix_directory, formats report, handles exit codes)
- [X] T022 [US1] Make `scripts/markdown/fix_list_spacing.py` executable (chmod +x)
- [X] T023 [US1] Test `fix_list_spacing.py` locally with --dry-run on docs/ directory
- [X] T024 [US1] Run `fix_list_spacing.py` with --backup to correct existing markdown files in docs/
- [X] T025 [US1] Verify corrections by running `mkdocs serve` and checking list rendering on http://127.0.0.1:8000
- [X] T026 [US1] Commit corrected markdown files with descriptive message including correction report

**Checkpoint**: At this point, User Story 1 should be fully functional - all existing markdown files are corrected and lists render properly

---

## Phase 4: User Story 2 - Automated Quality Checks for Future Changes (Priority: P2)

**Goal**: Prevent markdown syntax errors from being committed through automated validation in CI/CD pipeline

**Independent Test**: Create a markdown file with common syntax errors (missing blank lines before lists, etc.) and verify that the automated process detects and reports these errors before they reach the live site

**Acceptance Criteria**:
- Given a new markdown file is created with a list immediately after a header (no blank line), When the validation process runs, Then an error is reported identifying the specific file and line number
- Given validation errors exist, When attempting to merge changes, Then the merge is blocked until errors are corrected
- Given all markdown follows correct syntax, When validation runs, Then the process completes successfully with no errors
- Given MkDocs-specific markdown extensions are used, When validation runs, Then these valid extensions are not flagged as errors

### Implementation for User Story 2

- [ ] T027 [US2] Implement `validate_directory()` function in `scripts/markdown/markdown_validator.py` (scan directory, run validation, generate report)
- [ ] T028 [US2] Create `scripts/markdown/validate_markdown.py` CLI script with argument parsing (directory, --config, --output, --fail-on-warning, --verbose, --quiet, --help)
- [ ] T029 [US2] Implement main() function in `scripts/markdown/validate_markdown.py` (calls validate_directory, formats report, handles exit codes)
- [ ] T030 [US2] Make `scripts/markdown/validate_markdown.py` executable (chmod +x)
- [ ] T031 [US2] Test `validate_markdown.py` locally on docs/ directory with --verbose flag
- [ ] T032 [US2] Test `validate_markdown.py` with all output formats (text, json, github)
- [ ] T033 [US2] Create test fixture `scripts/tests/fixtures/markdown/valid_lists.md` (properly formatted lists)
- [ ] T034 [P] [US2] Create test fixture `scripts/tests/fixtures/markdown/header_no_space.md` (header followed by list, no blank line)
- [ ] T035 [P] [US2] Create test fixture `scripts/tests/fixtures/markdown/bold_no_space.md` (bold text followed by list, no blank line)
- [ ] T036 [P] [US2] Create test fixture `scripts/tests/fixtures/markdown/mkdocs_syntax.md` (admonitions, code blocks - should NOT error)
- [ ] T037 [P] [US2] Create test fixture `scripts/tests/fixtures/markdown/mixed_issues.md` (multiple error types)
- [ ] T038 [US2] Modify `.github/workflows/deploy.yml` to add validation step after dependencies install, before MkDocs build
- [ ] T039 [US2] Test CI/CD integration by pushing feature branch and observing validation in GitHub Actions
- [ ] T040 [US2] Verify that validation errors block merge in PR (create test PR with intentional error)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - existing files are corrected AND automated validation prevents future errors

---

## Phase 5: User Story 3 - Developer Guidance on Markdown Standards (Priority: P3)

**Goal**: Provide clear guidance on proper markdown syntax and MkDocs-specific conventions so contributors can write correctly-formatted content from the start

**Independent Test**: Provide the documentation to a new contributor and observe whether they successfully create properly-formatted markdown files without prior MkDocs experience

**Acceptance Criteria**:
- Given a new contributor accesses the project, When they review the markdown standards documentation, Then they understand the blank line requirement for lists and other common syntax rules
- Given the markdown standards document, When a contributor encounters MkDocs-specific syntax (admonitions, etc.), Then they find clear examples showing proper formatting
- Given a validation error message, When a contributor reads it, Then they understand what the error is and how to fix it

### Implementation for User Story 3

- [ ] T041 [US3] Create `docs/contributing/` directory if it doesn't exist
- [ ] T042 [US3] Create `docs/contributing/markdown-guide.md` with introduction explaining purpose
- [ ] T043 [US3] Add "Lists" section to `markdown-guide.md` with correct/incorrect examples showing blank line requirement
- [ ] T044 [US3] Add "Headers and Lists" section with examples of proper spacing
- [ ] T045 [US3] Add "Bold Text and Lists" section with examples of proper spacing
- [ ] T046 [US3] Add "MkDocs Extensions" section documenting admonitions, code blocks, footnotes, definition lists
- [ ] T047 [US3] Add "Validation" section explaining how to run validation locally and fix issues
- [ ] T048 [US3] Add "Common Errors" section with examples of validation errors and how to fix them
- [ ] T049 [US3] Add `contributing/markdown-guide.md` to `mkdocs.yml` navigation under "Contributing" section
- [ ] T050 [US3] Test documentation by reviewing rendered page at http://127.0.0.1:8000/contributing/markdown-guide/
- [ ] T051 [US3] Verify all examples render correctly and are easy to understand

**Checkpoint**: All user stories should now be independently functional - files corrected, automation in place, and contributor guidance available

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories or provide additional validation

- [ ] T052 [P] Add helpful comments to `scripts/markdown/markdown_validator.py` explaining complex logic
- [ ] T053 [P] Add docstrings to all functions in `scripts/markdown/markdown_validator.py`
- [ ] T054 [P] Add helpful comments to `scripts/markdown/validate_markdown.py` explaining CLI interface
- [ ] T055 [P] Add helpful comments to `scripts/markdown/fix_list_spacing.py` explaining CLI interface
- [ ] T056 Test validation performance on docs/ directory (should complete in <30 seconds per requirements)
- [ ] T057 Run `mkdocs build --strict --verbose` to verify no warnings or errors
- [ ] T058 Test edge cases: files with CRLF line endings, nested lists, lists in blockquotes
- [ ] T059 Verify .bak backup files are created when running fix script with --backup
- [ ] T060 Clean up any .bak files from testing (git status should show clean working directory except intended changes)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - User Story 1 (P1) can start after Foundational
  - User Story 2 (P2) can start after Foundational (though logically should test US1 corrections first)
  - User Story 3 (P3) can start after Foundational (independent documentation task)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Logically should validate US1 corrections but technically independent
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Completely independent documentation task

### Within Each User Story

- User Story 1: fix_list_spacing() → fix_directory() → CLI script → test locally → run corrections → verify → commit
- User Story 2: validate_directory() → CLI script → test locally → test output formats → create fixtures → CI/CD integration → test automation
- User Story 3: create directory → create markdown-guide.md → add sections → add to navigation → test rendering

### Parallel Opportunities

- **Phase 1 (Setup)**: Tasks T004, T005, T006 marked [P] can run in parallel
- **Phase 2 (Foundational)**: Tasks T008-T012 (dataclasses) marked [P] can run in parallel, T016-T017 (format functions) marked [P] can run in parallel
- **Phase 4 (US2)**: Tasks T034-T037 (test fixtures) marked [P] can run in parallel
- **Phase 6 (Polish)**: Tasks T052-T055 (documentation) marked [P] can run in parallel
- **Cross-Phase**: Once Foundational phase completes, User Stories 1, 2, and 3 can be worked on in parallel by different team members

---

## Parallel Example: Foundational Phase

```bash
# Launch all dataclasses together after T007 (MarkdownFile) is complete:
Task: "Implement ValidationError dataclass in scripts/markdown/markdown_validator.py"
Task: "Implement ValidationRule dataclass in scripts/markdown/markdown_validator.py"
Task: "Implement ValidationReport dataclass in scripts/markdown/markdown_validator.py"
Task: "Implement CorrectionOperation dataclass in scripts/markdown/markdown_validator.py"
Task: "Implement CorrectionReport dataclass in scripts/markdown/markdown_validator.py"
```

---

## Parallel Example: User Story 2 Test Fixtures

```bash
# Launch all test fixture creation together:
Task: "Create test fixture scripts/tests/fixtures/markdown/header_no_space.md"
Task: "Create test fixture scripts/tests/fixtures/markdown/bold_no_space.md"
Task: "Create test fixture scripts/tests/fixtures/markdown/mkdocs_syntax.md"
Task: "Create test fixture scripts/tests/fixtures/markdown/mixed_issues.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T017) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T018-T026)
4. **STOP and VALIDATE**:
   - Run mkdocs serve and verify all lists render correctly
   - Check that docs/ files have proper blank lines before lists
   - Ensure no run-on list sentences anywhere
5. Commit and potentially deploy if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **MVP COMPLETE** (fixes existing issues)
3. Add User Story 2 → Test independently → **Automation added** (prevents future issues)
4. Add User Story 3 → Test independently → **Documentation complete** (educates contributors)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T017)
2. Once Foundational is done:
   - Developer A: User Story 1 (T018-T026) - Fix existing files
   - Developer B: User Story 2 (T027-T040) - Add validation automation
   - Developer C: User Story 3 (T041-T051) - Write documentation
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 60
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 11 tasks (CRITICAL - blocks all user stories)
- Phase 3 (User Story 1): 9 tasks (P1 - MVP)
- Phase 4 (User Story 2): 14 tasks (P2)
- Phase 5 (User Story 3): 11 tasks (P3)
- Phase 6 (Polish): 9 tasks

**Parallel Opportunities**: 18 tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1, 2, and 3 only (26 tasks) delivers minimum viable product - existing files corrected, lists render properly

**Full Feature**: All 60 tasks delivers complete solution - corrections + automation + documentation

---

## Notes

- [P] tasks = different files, no dependencies - safe to execute in parallel
- [Story] label (US1, US2, US3) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No test tasks included - testing is through manual verification as described in acceptance criteria
- Commit after completing each user story phase for clean git history
- Stop at any checkpoint to validate story independently before proceeding
- Foundational phase (Phase 2) is CRITICAL - no user story work can begin until it's complete
- User Story 1 (P1) is the MVP - delivers immediate value by fixing current broken documentation
