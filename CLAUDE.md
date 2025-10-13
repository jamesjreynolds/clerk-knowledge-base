# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Ward Clerk Knowledge Base** - A static documentation site for Ward Clerk procedures and guidance, built with MkDocs Material theme and deployed to GitHub Pages.

**Live Site**: https://jamesjreynolds.github.io/clerk-knowledge-base/

## Technology Stack

- **Static Site Generator**: MkDocs >=1.5.0 with Material theme >=9.4.0
- **Python**: 3.8+ (development), 3.11 (CI/CD)
- **Deployment**: GitHub Actions → GitHub Pages (gh-pages branch)
- **Branch Protection**: Enabled on `main` - requires "Build MkDocs site" check to pass

## Essential Commands

### Local Development
```bash
# Install dependencies (use virtual environment recommended)
pip install -r requirements.txt

# Serve locally with live reload (http://127.0.0.1:8000)
mkdocs serve

# Build site (outputs to site/ directory)
mkdocs build

# Build with strict mode (fails on warnings - same as CI)
mkdocs build --strict --verbose
```

### Deployment
Deployment is **fully automated** via GitHub Actions on push to `main`. Manual deployment is not needed.

## Architecture & Key Files

### Configuration
- **`mkdocs.yml`**: Main configuration
  - Site metadata and URLs
  - Material theme with custom color palette (`primary: custom` uses #027DA5)
  - Navigation structure defines site hierarchy
  - Markdown extensions (admonitions, code highlighting, tables, etc.)
  - Plugins: search, git-revision-date-localized, minify

- **`docs/assets/css/custom.css`**: Brand color customization
  - Primary color: #027DA5 (teal header/tabs/links)
  - Overrides Material theme defaults with `!important` flags
  - Separate definitions for light/dark modes

- **`requirements.txt`**: Python dependencies (MkDocs + plugins)

### Content Structure
```
docs/
├── index.md                      # Homepage
├── membership/                   # Membership procedures
│   ├── index.md
│   ├── quarterly-reports.md
│   └── lost-members.md
├── financial/                    # Financial procedures
│   ├── index.md
│   ├── expenses.md              # Comprehensive sample with tables/admonitions
│   ├── budgets.md
│   ├── audits.md
│   └── signature-cards.md
├── reports/index.md
├── annual-history/index.md
├── agent-bishop/index.md
└── assets/
    └── css/custom.css
```

**Content Guidelines**:
- All content is Markdown in `docs/`
- Navigation hierarchy defined in `mkdocs.yml` nav section
- Use Material theme admonitions: `!!! warning`, `!!! info`, `!!! danger`
- See `docs/financial/expenses.md` for formatting reference (tables, callouts, code blocks)

### CI/CD Pipeline
**`.github/workflows/deploy.yml`**: Three-job workflow

1. **Build Job** (runs on all pushes and PRs):
   - Validates MkDocs configuration
   - Builds site in strict mode (fails on broken links/warnings)
   - Checks file sizes (<5 MB limit)
   - Uploads artifacts for PR previews

2. **Deploy Job** (main branch only):
   - Builds and deploys to `gh-pages` branch using `mkdocs gh-deploy`
   - GitHub Pages serves from `gh-pages` branch automatically

3. **Notify-Failure Job** (on failure):
   - Logs failure details
   - Notes automatic rollback behavior

**Important**: Branch protection requires "Build MkDocs site" check to pass before merging PRs.

## Development Workflow

### Making Content Changes
1. Create a new branch from `main`
2. Edit Markdown files in `docs/`
3. Test locally with `mkdocs serve`
4. Commit and push branch
5. Create PR - CI will validate build
6. Merge to `main` - automatic deployment to live site

### Adding New Pages
1. Create Markdown file in appropriate `docs/` subdirectory
2. Add entry to `nav` section in `mkdocs.yml`
3. Test build with `mkdocs build --strict` to catch broken links

### Modifying Theme/Colors
- Edit `docs/assets/css/custom.css` for visual changes
- Primary brand color (#027DA5) is hardcoded in CSS with `!important`
- Changes require rebuild and redeploy (automatic on merge to main)

## Common Issues

### MkDocs Config YAML Validation
The `!!python/name:` tags in `mkdocs.yml` (for emoji extensions) are valid MkDocs syntax but fail generic YAML parsers. Don't try to validate with `yaml.safe_load()` - let MkDocs handle it.

### Broken Links in Strict Mode
CI fails on any broken internal links. When adding pages:
- Ensure all `nav` entries point to existing files
- Update relative links in content when files reference each other
- Run `mkdocs build --strict` locally before pushing

### File Size Limits
CI enforces 5 MB per-file limit. Optimize images before committing.

### Branch Protection
Direct pushes to `main` are blocked. All changes must go through PRs with passing CI checks.

## Repository Structure Notes

- **`specs/`**: Feature planning documents (not part of site build)
- **`site/`**: Generated output (gitignored, not committed)
- **`gh-pages` branch**: Auto-managed by GitHub Actions, contains deployed site
- **`main` branch**: Default branch, protected

## URLs and Links
- Repo: https://github.com/jamesjreynolds/clerk-knowledge-base
- Edit links point to `main` branch via `edit_uri: edit/main/docs/`
- All USERNAME placeholders have been replaced with `jamesjreynolds`
