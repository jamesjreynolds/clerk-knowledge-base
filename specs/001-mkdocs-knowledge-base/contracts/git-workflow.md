# Git Workflow Contract

**Type**: Process Integration Contract
**System**: Git version control workflow for documentation changes
**Updated**: 2025-10-09

## Overview

This contract defines how contributors interact with the Git repository to create, review, and deploy documentation changes. It ensures consistency with Constitution principles (Documentation-First, Automation-Driven Deployment, Quality Assurance).

---

## Branch Strategy

### Main Branch: `main`

**Purpose**: Production-ready documentation

**Protection Rules**:
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass (GitHub Actions build)
- ✅ Require branches to be up to date before merging
- ❌ Do not allow force pushes
- ❌ Do not allow deletions

**Deployment**:
- Every push to `main` triggers automatic deployment via GitHub Actions
- Deployment builds site and pushes to `gh-pages` branch
- GitHub Pages serves content from `gh-pages` branch

### Feature Branches

**Naming Convention**:
```
feature/<descriptive-name>    # New content or features
fix/<descriptive-name>         # Bug fixes or corrections
docs/<descriptive-name>        # Documentation improvements
style/<descriptive-name>       # Formatting or style changes
```

**Examples**:
- `feature/add-api-authentication-guide`
- `fix/broken-link-homepage`
- `docs/update-contributing-guide`
- `style/improve-code-block-formatting`

**Lifecycle**:
1. Created from `main`
2. Commits pushed to feature branch
3. Pull request opened when ready for review
4. Approved and merged to `main`
5. Branch deleted after merge

---

## Commit Message Format

**Convention**: Conventional Commits

**Structure**:
```
<type>: <subject>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature or content
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `style`: Formatting, whitespace, style changes
- `refactor`: Restructuring without changing meaning
- `chore`: Maintenance tasks (dependencies, config)

**Subject Guidelines**:
- Use imperative mood ("add", not "added" or "adds")
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

**Examples**:
```
feat: add authentication guide for API users

Add comprehensive guide covering OAuth2, API keys, and session
management with code examples in multiple languages.

Closes #42
```

```
fix: correct broken link in installation page

Link to Python downloads was outdated. Updated to point to
python.org/downloads.

Closes #38
```

```
docs: improve contributor onboarding instructions

Add missing step for virtual environment activation on Windows.
Clarify prerequisites section.
```

---

## Pull Request Workflow

### Creating a Pull Request

**Prerequisites**:
- Feature branch has at least one commit
- Changes tested locally with `mkdocs serve`
- Build passes locally with `mkdocs build --strict`

**PR Template**:
```markdown
## Summary
Brief description of changes made (1-2 sentences).

## Type of Change
- [ ] New feature/content
- [ ] Bug fix/correction
- [ ] Documentation improvement
- [ ] Style/formatting change

## Testing
- [ ] Tested locally with `mkdocs serve`
- [ ] Build passes with `mkdocs build --strict`
- [ ] All links verified to work
- [ ] Content renders correctly
- [ ] Navigation functions properly

## Screenshots (if applicable)
Include before/after screenshots for visual changes.

## Checklist
- [ ] Self-review completed
- [ ] Follows style guide
- [ ] Commit messages follow convention
```

### Review Process

**Reviewer Responsibilities**:
1. Verify content accuracy and clarity
2. Check all links work (internal and external)
3. Ensure consistent formatting per style guide
4. Test navigation changes if structural
5. Provide constructive, specific feedback

**Review Timeline**:
- Reviewers should review within 3 business days (per Constitution)
- Contributors should address feedback within 5 business days

**Approval Requirements**:
- At least 1 approval from designated reviewer
- All GitHub Actions checks must pass
- No unresolved conversations

**Review Comments**:
```
✅ Approve: "LGTM! Clear explanation with good examples."

🔄 Request Changes: "The authentication section needs more detail
   about token expiration. See inline comments."

💬 Comment: "Consider adding a diagram here to visualize the flow."
```

### Merge Process

**Method**: Squash and Merge (recommended)
- Combines all commits into single commit on `main`
- Keeps main branch history clean
- Preserves full history in feature branch

**Alternative**: Merge Commit
- Preserves all individual commits
- Use for complex features with meaningful commit history

**After Merge**:
1. GitHub Actions automatically triggers deployment
2. Build completes in <5 minutes (SC-003)
3. Changes appear on live site
4. Feature branch can be deleted

---

## Local Development Workflow

### Initial Setup

```bash
# Clone repository
git clone https://github.com/username/knowledge-base.git
cd knowledge-base

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
mkdocs --version
```

### Creating New Content

```bash
# Ensure on main branch and up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/add-deployment-guide

# Create new Markdown file
touch docs/guides/deployment.md

# Start development server
mkdocs serve

# Edit content in browser at http://localhost:8000
# Server auto-reloads on file changes
```

### Testing Changes

```bash
# Validate build
mkdocs build --strict

# Check for errors in output
# If successful, ready to commit
```

### Committing Changes

```bash
# Stage changes
git add docs/guides/deployment.md

# Commit with conventional format
git commit -m "feat: add deployment guide for production"

# Push to remote
git push origin feature/add-deployment-guide
```

### Creating Pull Request

```bash
# Via GitHub CLI (optional)
gh pr create --title "Add deployment guide" --body "Comprehensive guide for production deployment"

# Or via GitHub web interface
# Go to repository, click "Compare & pull request"
```

---

## GitHub Actions Integration

### Build Workflow

**Trigger**: Push to any branch, pull request to main

**Steps**:
1. Checkout repository
2. Setup Python 3.x
3. Install dependencies from requirements.txt
4. Run `mkdocs build --strict`
5. Report success/failure

**Configuration**:
```yaml
name: Build Documentation
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict
```

### Deploy Workflow

**Trigger**: Push to main branch only

**Steps**:
1. Checkout repository with full history
2. Configure Git credentials for deployment
3. Setup Python 3.x
4. Install dependencies (with caching)
5. Run `mkdocs gh-deploy --force`
6. GitHub Pages serves updated content

**Permissions**:
```yaml
permissions:
  contents: write  # Required for gh-pages push
```

**Configuration**:
```yaml
name: Deploy Documentation
on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git-revision-date
      - name: Configure Git
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - uses: actions/cache@v4
        with:
          key: mkdocs-${{ github.sha }}
          path: ~/.cache
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
```

---

## Error Handling

### Build Failures

**Common Errors**:

1. **Broken internal link**:
   ```
   ERROR - Doc file 'guides/api.md' contains a link to 'authentication.md',
   but the target file does not exist.
   ```
   **Fix**: Update link to correct path or create missing file

2. **Invalid YAML**:
   ```
   ERROR - Config file 'mkdocs.yml' contains invalid YAML.
   ```
   **Fix**: Validate YAML syntax, check indentation

3. **Missing dependency**:
   ```
   ERROR - Could not import module 'material'
   ```
   **Fix**: Run `pip install -r requirements.txt`

### Merge Conflicts

**Scenario**: Multiple contributors edit same file

**Resolution**:
```bash
# Update feature branch with main
git checkout feature/my-changes
git fetch origin
git merge origin/main

# Resolve conflicts in editor
# Look for <<<<<<<, =======, >>>>>>> markers

# Stage resolved files
git add docs/conflicted-file.md

# Complete merge
git commit

# Push updated branch
git push origin feature/my-changes
```

### Deployment Failures

**Monitoring**: Check GitHub Actions tab for workflow status

**Common Issues**:
- Insufficient permissions: Verify `contents: write` in workflow
- gh-pages branch conflicts: Use `--force` flag in `mkdocs gh-deploy`
- Large site size: GitHub Pages has 1GB limit

**Rollback**:
```bash
# Revert bad commit
git revert <commit-sha>
git push origin main

# Or reset to previous state (use with caution)
git reset --hard <good-commit-sha>
git push origin main --force
```

---

## Performance SLAs

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Pull request build | <3 minutes | GitHub Actions duration |
| Deployment build | <5 minutes | GitHub Actions duration (SC-003) |
| Merge to live | <5 minutes | Time from merge to site update |
| Build success rate | >95% | Successful builds / total builds (SC-005) |

---

## Security Considerations

### Branch Protection

**Required**:
- Pull request reviews enforced
- Status checks must pass
- Force push disabled on main

**Recommended**:
- Require specific reviewers (CODEOWNERS)
- Dismiss stale reviews on new commits
- Require signed commits

### Secrets Management

**Never Commit**:
- API keys
- Passwords
- Private keys
- Environment-specific config

**Use GitHub Secrets** for sensitive data:
```yaml
- name: Deploy with secret
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
```

### Dependency Security

**Dependabot Configuration**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "monthly"
```

---

## Compliance Checklist

Before merging any pull request, verify:

- [ ] Branch follows naming convention
- [ ] Commits follow conventional format
- [ ] PR description is clear and complete
- [ ] All tests/checks pass (GitHub Actions)
- [ ] At least one approval from reviewer
- [ ] No unresolved review comments
- [ ] Changes tested locally
- [ ] Links validated
- [ ] Style guide followed
- [ ] No sensitive data committed

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [MkDocs Deployment](https://www.mkdocs.org/user-guide/deploying-your-docs/)
- Constitution principles: Documentation-First, Automation-Driven, Quality Assurance
