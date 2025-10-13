# Research: MkDocs Knowledge Base Platform

**Phase**: 0 (Outline & Research)
**Date**: 2025-10-09
**Status**: Complete

## Technology Stack Decisions

### Static Site Generator: MkDocs

**Decision**: Use MkDocs as the core static site generator

**Rationale**:
- Python-based, aligning with target contributor skillsets
- Extensive ecosystem with 100+ plugins
- Built-in development server with live reload
- Simple configuration via YAML
- Active community and well-maintained
- Excellent Markdown support (CommonMark + extensions)

**Alternatives Considered**:
- **Jekyll**: Ruby-based, GitHub's default, but requires Ruby ecosystem knowledge
- **Hugo**: Extremely fast, but Go templates have steeper learning curve
- **Docusaurus**: React-based, feature-rich, but requires Node.js/React knowledge
- **Sphinx**: Python documentation standard, but more complex for non-code docs

**Why MkDocs Won**: Best balance of simplicity (Markdown-focused), contributor accessibility (Python is specified), and feature completeness (search, themes, plugins).

### Theme: Material for MkDocs

**Decision**: Use Material for MkDocs theme as primary UI framework

**Rationale**:
- Most popular MkDocs theme (10k+ GitHub stars)
- Mobile-responsive out of the box
- Built-in dark/light mode toggle (FR-013 requirement)
- Client-side search with highlighting (FR-006)
- Comprehensive navigation features (tabs, sections, TOC)
- Extensive customization without breaking core functionality (FR-018)
- Active development and documentation
- Performance-optimized (meets SC-002: <2 sec loads)

**Alternatives Considered**:
- **ReadTheDocs theme**: Default, but lacks modern features
- **mkdocs-bootstrap**: Responsive, but less feature-rich
- **Custom theme**: Maximum control, but violates contributor accessibility principle

**Why Material Won**: Only theme that satisfies all requirements (responsive, dark mode, client search, customizable) while maintaining contributor simplicity.

### Hosting: GitHub Pages

**Decision**: Deploy to GitHub Pages for static site hosting

**Rationale**:
- Free for public repositories
- Zero backend costs (SC-011)
- Automatic HTTPS/SSL
- Global CDN distribution
- Native integration with GitHub Actions
- Custom domain support
- No server maintenance required

**Alternatives Considered**:
- **Netlify**: More features (build previews, forms), but adds external dependency
- **Vercel**: Fast, but optimized for Next.js/React
- **AWS S3 + CloudFront**: Scalable, but requires AWS account and more complexity
- **GitLab Pages**: Similar to GitHub Pages, but requires GitLab migration

**Why GitHub Pages Won**: Specification assumes GitHub repository, zero-cost requirement (SC-011), and eliminates external dependencies for simpler contributor model.

### CI/CD: GitHub Actions

**Decision**: Use GitHub Actions for automated deployment workflow

**Rationale**:
- Included with every GitHub repository (no setup)
- `contents: write` permission sufficient for deployment
- Caching support for faster builds
- Workflow marketplace for reusable actions
- Directly integrates with GitHub Pages
- Meets 5-minute deployment target (FR-005, SC-003)

**Alternatives Considered**:
- **Travis CI**: External service, requires account
- **CircleCI**: More features, but external dependency
- **Jenkins**: Self-hosted, violates static-first principle
- **Manual deployment**: Violates NON-NEGOTIABLE automation principle

**Why GitHub Actions Won**: Only option that meets automation principle without external dependencies. Native GitHub integration ensures simplest contributor workflow.

### Version Control Plugin: git-revision-date-localized

**Decision**: Use mkdocs-git-revision-date-localized-plugin for page metadata

**Rationale**:
- Automatically extracts last modified dates from Git history (FR-017)
- Localization support for international contributors
- Shows creation date when needed
- Zero contributor burden (automatic)
- Reinforces version control as source of truth

**Alternatives Considered**:
- **Manual metadata**: Error-prone, contributors forget
- **Build timestamps**: Loses historical accuracy
- **git-revision-date plugin**: Less flexible, no localization

**Why git-revision-date-localized Won**: Only automated solution that meets FR-017 without contributor overhead.

## Architecture Patterns

### Documentation-as-Code

**Pattern**: Treat documentation like source code with version control, branching, reviews, and CI/CD

**Rationale**:
- Aligns with Constitution Principle I (Documentation-First Architecture)
- Enables collaborative editing through Git workflow
- Full audit trail for all changes (FR-010)
- Rollback capability for errors
- Branch-based development for large changes

**Implementation**:
- All content in `/docs` directory
- Conventional commit messages for changes
- Pull request workflow for all merges
- Automated build checks before merge (FR-012)

### Static-First Architecture

**Pattern**: Generate complete static HTML/CSS/JS with no runtime server dependencies

**Rationale**:
- Aligns with Constitution Principle V (Static-First & Performance)
- Zero backend = zero backend vulnerabilities
- Scales infinitely with CDN (no server capacity planning)
- Fastest possible page loads (SC-002: <2 seconds)
- Lowest possible hosting costs (SC-011: zero)

**Implementation**:
- MkDocs generates static files in `site/` directory
- Client-side search (no search server needed)
- All navigation pre-rendered
- Assets served directly from CDN

### Progressive Enhancement

**Pattern**: Core content accessible without JavaScript, enhanced features with JS

**Rationale**:
- Maximum accessibility (screen readers, text browsers)
- Works even if JS fails or is disabled
- Better SEO (search engines see content)
- Faster initial page render

**Implementation**:
- Markdown content renders as HTML
- Navigation works without JS
- Search requires JS (acceptable tradeoff for static architecture)
- Theme switcher requires JS (acceptable enhancement)

## Development Workflow

### Local Development

**Decision**: Use `mkdocs serve` for local preview with live reload

**Rationale**:
- Meets FR-011 (local preview requirement)
- Live reload enables rapid iteration
- Same rendering as production (WYSIWYG)
- No separate build step needed for development
- Meets SC-008 (<10 second startup)

**Implementation**:
```bash
# Standard workflow
mkdocs serve              # Default port 8000
mkdocs serve -a 0.0.0.0:8080  # Custom port
mkdocs serve --dirtyreload    # Faster for large sites
```

### Build Validation

**Decision**: Use `mkdocs build --strict` for PR validation

**Rationale**:
- Catches broken links before deployment
- Validates navigation structure
- Ensures all pages render
- Fails loudly on errors (better than silent failures)
- Meets FR-012 (PR validation requirement)

**Implementation**:
- GitHub Actions runs `mkdocs build --strict` on all PRs
- Build failure blocks merge
- Clear error messages guide fixes (FR-020)

### Deployment

**Decision**: Use `mkdocs gh-deploy --force` for automated deployment

**Rationale**:
- Single command deployment
- Automatically updates `gh-pages` branch
- Force flag prevents merge conflicts
- Built-in Git commit with timestamp
- Meets FR-003/FR-004 (automated deployment)

**Implementation**:
- Triggered automatically on main branch push
- GitHub Actions handles authentication via workflow token
- Completes in <5 minutes (SC-003)
- Clear success/failure feedback in Actions UI

## Performance Optimization

### Build Performance

**Decision**: Use GitHub Actions caching for Python dependencies

**Rationale**:
- Faster builds = faster feedback for contributors
- Reduces GitHub Actions minutes usage
- Improves probability of meeting 5-minute target (SC-003)

**Implementation**:
```yaml
- uses: actions/cache@v4
  with:
    key: mkdocs-material-${{ github.sha }}
    path: ~/.cache
    restore-keys: mkdocs-material-
```

### Page Load Performance

**Decision**: Rely on Material theme's built-in optimizations

**Rationale**:
- Theme already optimized for <2 second loads (SC-002)
- Minified CSS/JS included
- Lazy loading for images
- Efficient client-side search index
- No additional optimization needed initially

**Future Optimizations** (if needed):
- Image compression pipeline
- Custom CSS minification
- Search index optimization for 500+ pages
- Service worker for offline support

## Security Considerations

### GitHub Actions Permissions

**Decision**: Use minimal `contents: write` permission for deployment workflow

**Rationale**:
- Sufficient for pushing to `gh-pages` branch
- Meets Constitution Security Requirements
- Follows principle of least privilege
- Reduces blast radius if workflow compromised

**Implementation**:
```yaml
permissions:
  contents: write
```

### Dependency Management

**Decision**: Pin minimum versions in requirements.txt, enable Dependabot

**Rationale**:
- Minimum versions allow security patches
- Dependabot automates security updates
- Meets Constitution maintenance requirements (monthly updates)
- Reduces vulnerability window

**Implementation**:
```
mkdocs>=1.5.0
mkdocs-material>=9.4.0
mkdocs-git-revision-date-localized-plugin>=1.2.0
```

### Content Security

**Decision**: No authentication/authorization for public knowledge base

**Rationale**:
- Specification assumes public content
- Static site cannot implement authentication
- Private repositories require GitHub authentication naturally
- Reduces complexity (aligns with simplicity principle)

**Alternative** (if private content needed):
- GitHub Pages with private repo (requires GitHub Pro/Team)
- Netlify with password protection
- VPN + internal hosting

## Open Questions Resolved

### Q1: How to handle navigation structure?

**Decision**: Support both automatic and manual navigation

**Rationale**:
- Automatic navigation (from directory structure) easiest for contributors
- Manual navigation (in mkdocs.yml) gives control for complex sites
- Material theme supports both modes
- Let each project choose based on complexity

**Implementation**: Document both approaches in quickstart.md

### Q2: How to handle search for large sites (500+ pages)?

**Decision**: Use Material theme's client-side search with monitoring

**Rationale**:
- Built-in search meets SC-006 (<1 second) for up to 500 pages
- No server-side infrastructure needed
- Degrades gracefully if too large (can optimize later)
- Most documentation sites are under 500 pages

**Contingency**: If search becomes slow, investigate mkdocs-material Insiders features or custom search index optimization.

### Q3: How to handle broken link detection?

**Decision**: Use `mkdocs build --strict` for internal links, recommend periodic link checking tool

**Rationale**:
- `--strict` mode catches broken internal links at build time
- External link checking requires additional tool (htmltest, linkchecker)
- Constitution requires "periodic" link checks (not necessarily automated)
- Manual quarterly checks acceptable initially

**Future Enhancement**: Add automated external link checking to GitHub Actions workflow.

### Q4: How to handle image optimization?

**Decision**: Document best practices, don't enforce automatically initially

**Rationale**:
- Automatic optimization adds build complexity
- Most contributors can use online tools (TinyPNG, etc.)
- Constitution requires "optimized assets" but doesn't mandate automation
- Can add later if becomes bottleneck

**Implementation**: Include image optimization guidance in contributor-onboarding-guide.md

## Next Steps

This research phase resolves all technical unknowns. Proceed to Phase 1 (Design & Contracts) to generate:

1. **data-model.md**: Document entities (Documentation Page, Section, Contributor, etc.)
2. **contracts/**: Define any integration points (Git workflows, GitHub API usage if needed)
3. **quickstart.md**: Step-by-step guide for setting up the knowledge base
4. **Agent context update**: Update claude.md with MkDocs, Material, GitHub Pages context
