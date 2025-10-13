# Data Model: MkDocs Knowledge Base Platform

**Phase**: 1 (Design & Contracts)
**Date**: 2025-10-09
**Source**: Entities extracted from spec.md

## Overview

This knowledge base platform is primarily a **content management system** using the filesystem and Git as the source of truth. There is no application database - all data is stored as:
- Markdown files (content)
- YAML configuration (site settings)
- Git metadata (history, authorship)
- Generated HTML/CSS/JS (build artifacts)

The entities below represent logical concepts rather than database tables.

---

## Core Entities

### Documentation Page

**Represents**: A single article or guide in the knowledge base

**Storage**: Markdown file in `/docs` directory

**Attributes**:
- `file_path` (string): Relative path from `/docs`, e.g., `getting-started/installation.md`
- `title` (string): Page title, extracted from H1 heading or filename
- `content` (markdown): Full Markdown content including headings, paragraphs, code blocks, images
- `last_modified` (datetime): Extracted from Git history via git-revision-date-localized plugin
- `creation_date` (datetime): First commit timestamp for the file from Git history
- `author` (string): Git committer name/email from commit history
- `url_slug` (string): Generated URL segment, e.g., `/getting-started/installation/`

**Validation Rules**:
- Must have exactly one H1 heading (best practice, not enforced)
- Filename must use lowercase with hyphens (`user-guide.md` not `User Guide.md`)
- Must be valid Markdown per CommonMark specification
- Internal links must reference valid page paths (validated by `mkdocs build --strict`)
- Images must reference files in `/docs/assets/images/` or valid URLs

**State Transitions**:
```
[Draft] ---> [In Review (PR)] ---> [Published (merged to main)]
                   |
                   v
              [Needs Changes]
```

**Relationships**:
- Belongs to exactly one Documentation Section (directory)
- Can link to many other Documentation Pages (via Markdown links)
- Modified by many Contributors (via Git commits)
- Can be part of many Change Requests (via PRs)

---

### Documentation Section

**Represents**: A logical grouping of related pages (e.g., "Getting Started", "User Guide")

**Storage**: Directory in `/docs`

**Attributes**:
- `directory_path` (string): Relative path from `/docs`, e.g., `getting-started/`
- `section_name` (string): Human-readable name, extracted from directory name or nav config
- `index_page` (Documentation Page): Optional `index.md` serving as section landing page
- `navigation_order` (integer): Position in site navigation (automatic from filesystem or manual from `mkdocs.yml`)
- `page_count` (integer): Number of Markdown files in directory

**Validation Rules**:
- Directory name must use lowercase with hyphens
- Should contain at least one Markdown file
- If manual navigation used, must be declared in `mkdocs.yml` nav section

**Relationships**:
- Contains many Documentation Pages
- Can contain child Documentation Sections (subdirectories)
- Part of overall Site Navigation structure

---

### Contributor

**Represents**: A person who creates or modifies documentation content

**Storage**: Git commit metadata

**Attributes**:
- `name` (string): Git user.name from commit
- `email` (string): Git user.email from commit
- `github_username` (string): GitHub account username (for PR workflow)
- `role` (enum): `author` (write access) | `reviewer` (can approve PRs) | `admin` (can manage settings)
- `first_contribution_date` (datetime): Timestamp of first merged commit
- `contribution_count` (integer): Number of merged commits

**Access Permissions**:
- **Read**: Anyone (public GitHub repository)
- **Write**: Collaborators with push access to feature branches
- **Approve**: Designated reviewers with branch protection rules
- **Admin**: Repository administrators (settings, branch protection, collaborators)

**Onboarding Flow**:
```
[Discover Project] -> [Fork Repository] -> [Setup Local Environment]
    -> [Make Test Edit] -> [Create First PR] -> [Become Contributor]
```

**Validation Rules**:
- Must have valid Git identity configured (`git config user.name/email`)
- Must have GitHub account for PR workflow
- Must complete onboarding steps within 35 minutes (SC-001 target)

**Relationships**:
- Creates many Documentation Pages (via commits)
- Creates many Change Requests (via PRs)
- Reviews many Change Requests (if reviewer role)

---

### Change Request

**Represents**: A proposed set of documentation changes submitted for review (Git Pull Request)

**Storage**: GitHub Pull Request metadata

**Attributes**:
- `pr_number` (integer): GitHub PR number
- `title` (string): PR title describing changes
- `description` (markdown): Detailed explanation of changes, motivation, testing performed
- `branch_name` (string): Source branch name (e.g., `feature/add-api-authentication-guide`)
- `author` (Contributor): Person who created the PR
- `reviewers` (list[Contributor]): Assigned reviewers
- `status` (enum): `open` | `changes_requested` | `approved` | `merged` | `closed`
- `created_at` (datetime): PR creation timestamp
- `merged_at` (datetime): When PR was merged to main (null if not merged)
- `build_status` (enum): `pending` | `success` | `failure` (from GitHub Actions)
- `files_changed` (list[string]): Paths of modified/added/deleted files
- `commit_count` (integer): Number of commits in the PR

**Workflow States**:
```
[Open] -> [Build Running] -> [Build Pass/Fail]
   |
   v
[Review Requested] -> [Changes Requested] -> [Updated]
   |
   v
[Approved] -> [Merged] -> [Deployed]
```

**Validation Rules**:
- Must pass `mkdocs build --strict` before merge
- Must have at least one approval from designated reviewer
- Must have descriptive title and description
- Should link to related issues if applicable (best practice)

**Relationships**:
- Created by one Contributor (author)
- Reviewed by many Contributors (reviewers)
- Modifies many Documentation Pages
- Triggers one Static Site Build when merged

---

### Static Site Build

**Represents**: The generated output from Markdown source files, ready for web hosting

**Storage**: `site/` directory (local) or `gh-pages` branch (deployed)

**Attributes**:
- `build_id` (string): GitHub Actions workflow run ID
- `commit_sha` (string): Git commit SHA that triggered the build
- `build_timestamp` (datetime): When build started
- `build_duration` (seconds): Time to complete build (target: <300 seconds per SC-003)
- `build_status` (enum): `queued` | `in_progress` | `success` | `failure`
- `artifact_count` (integer): Number of generated HTML files
- `total_size_mb` (float): Size of generated site/ directory
- `error_log` (string): Build error messages if failed

**Build Process**:
```
[Trigger: Push to main]
    -> [Checkout code]
    -> [Install dependencies]
    -> [Run mkdocs build]
    -> [Deploy to gh-pages]
    -> [GitHub Pages publishes]
```

**Performance Targets**:
- Build completion: <5 minutes (SC-003)
- Success rate: >95% (SC-005)
- Generated page load time: <2 seconds (SC-002)

**Validation Rules**:
- Must complete without errors to deploy
- Must generate valid HTML/CSS/JS
- All internal links must resolve
- Search index must be generated

**Relationships**:
- Triggered by one Change Request (merge event)
- Generates many Documentation Pages (as HTML)
- Creates one Deployment (to GitHub Pages)

---

### Theme Configuration

**Represents**: Settings controlling visual appearance and navigation behavior

**Storage**: `mkdocs.yml` file

**Attributes**:
- `site_name` (string): Knowledge base title
- `site_url` (string): Production URL (e.g., `https://username.github.io/repo-name/`)
- `theme_name` (string): "material" (Material for MkDocs)
- `color_scheme` (object): Primary/accent colors, light/dark mode settings
- `navigation_mode` (enum): `automatic` (from filesystem) | `manual` (defined in nav section)
- `nav_structure` (yaml): Manual navigation hierarchy if mode is manual
- `features_enabled` (list[string]): Material theme features (e.g., `navigation.tabs`, `search.highlight`)
- `plugins` (list[object]): Enabled MkDocs plugins with configuration
- `markdown_extensions` (list[string]): Enabled Markdown extensions (e.g., `pymdownx.highlight`)

**Required Configuration**:
```yaml
site_name: Knowledge Base Name
site_url: https://username.github.io/repo-name/
theme:
  name: material
  features:
    - navigation.tabs
    - search.highlight
    - content.code.copy
plugins:
  - search
  - git-revision-date-localized
```

**Validation Rules**:
- `site_url` must match GitHub Pages URL for correct asset paths
- `theme.name` must be "material"
- Must include `search` plugin (FR-006 requirement)
- Must include `git-revision-date-localized` plugin (FR-017 requirement)
- YAML must be valid per mkdocs.yml schema

**Relationships**:
- Applies to all Documentation Pages
- Controls all Static Site Builds
- Modified by Contributors (via PR workflow)

---

## Filesystem Structure

The data model maps to this filesystem structure:

```
/docs/                          # Documentation Section (root)
├── index.md                    # Documentation Page (homepage)
├── getting-started/            # Documentation Section
│   ├── index.md                # Documentation Page
│   ├── installation.md         # Documentation Page
│   └── quick-start.md          # Documentation Page
├── user-guide/                 # Documentation Section
│   ├── index.md                # Documentation Page
│   └── basic-usage.md          # Documentation Page
└── assets/                     # Asset storage
    ├── images/                 # Image files referenced by pages
    └── css/                    # Custom CSS if needed

/mkdocs.yml                     # Theme Configuration
/.github/workflows/ci.yml       # Build/deployment automation
/requirements.txt               # Python dependency specifications
/site/                          # Static Site Build (generated, git-ignored)
```

---

## Git Integration

### Git as Data Store

Git provides these data model capabilities:
- **Version history**: Every change to every page tracked
- **Authorship**: Who made what changes when
- **Branching**: Parallel development of multiple features
- **Merging**: Integration of approved changes
- **Rollback**: Revert to any previous state

### Metadata Extraction

MkDocs plugins extract data from Git:
- `git log` → `last_modified` dates for Documentation Pages
- `git log --follow` → `creation_date` for new pages
- `git blame` → line-by-line authorship (viewable in GitHub)
- `git diff` → change sets for Change Requests

---

## Relationships Diagram

```
Contributor
    |-- creates --> Documentation Page
    |-- creates --> Change Request
    |-- reviews --> Change Request

Documentation Section
    |-- contains --> Documentation Page (many)
    |-- contains --> Documentation Section (children, optional)

Documentation Page
    |-- belongs to --> Documentation Section
    |-- links to --> Documentation Page (many)
    |-- modified by --> Contributor (many, via commits)

Change Request
    |-- created by --> Contributor
    |-- reviewed by --> Contributor (many)
    |-- modifies --> Documentation Page (many)
    |-- triggers --> Static Site Build

Static Site Build
    |-- generated from --> Documentation Page (many)
    |-- controlled by --> Theme Configuration
    |-- deployed to --> GitHub Pages

Theme Configuration
    |-- applies to --> Static Site Build
    |-- defines --> Documentation Section hierarchy (if manual nav)
```

---

## Validation Summary

| Entity | Validation Method | Timing |
|--------|------------------|--------|
| Documentation Page | `mkdocs build --strict` | PR build check |
| Documentation Section | mkdocs.yml validation | PR build check |
| Contributor | Git config validation | Local setup |
| Change Request | GitHub Actions workflow | On PR creation/update |
| Static Site Build | Build success/failure | Post-merge deployment |
| Theme Configuration | YAML schema validation | PR build check |

---

## Query Patterns

Since there's no database, "queries" are filesystem/Git operations:

- **List all pages**: `find docs -name '*.md'`
- **Find pages modified in last week**: `git log --since='1 week ago' --name-only --pretty=format: docs/ | sort -u`
- **Get page history**: `git log --follow docs/path/to/page.md`
- **Find contributor stats**: `git shortlog -sn --all docs/`
- **Search content**: MkDocs search index (client-side JSON)
- **List open PRs**: GitHub API `/repos/:owner/:repo/pulls?state=open`

---

## Scalability Considerations

- **100-500 pages**: Material theme search handles well (SC-006)
- **Multiple contributors**: Git branching supports parallel work
- **Large files**: Git LFS available if needed (images, PDFs)
- **Build time**: Grows linearly with page count, caching helps
- **Search index**: Grows with content, may need optimization at 500+ pages

Per research.md, these limits are acceptable for target scope. Future optimization strategies documented if needed.
