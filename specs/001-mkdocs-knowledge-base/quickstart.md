# Quickstart: MkDocs Knowledge Base Platform

**Target Time**: 35 minutes (SC-001 requirement)
**Difficulty**: Beginner-friendly
**Prerequisites**: Basic command-line familiarity

---

## What You'll Build

By the end of this guide, you'll have:
- ✅ A working knowledge base running locally
- ✅ Automated deployment to GitHub Pages
- ✅ Your first documentation page published
- ✅ Understanding of the contribution workflow

---

## Prerequisites (5 minutes)

Verify you have these installed before starting:

### 1. Git

```bash
git --version
# Should show: git version 2.x.x or higher
```

**Don't have Git?** [Download here](https://git-scm.com/downloads)

### 2. Python 3.8+

```bash
python --version
# Should show: Python 3.8.x or higher
# On some systems, try: python3 --version
```

**Don't have Python?** [Download here](https://www.python.org/downloads/)

### 3. Code Editor

Recommended: [Visual Studio Code](https://code.visualstudio.com/)

### 4. GitHub Account

Create one at [github.com](https://github.com/) if you don't have one.

---

## Part 1: Repository Setup (5 minutes)

### Step 1.1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `clerk-knowledge-base` (or your choice)
3. **Visibility**: ✅ Public (required for free GitHub Pages)
4. **Initialize**: ✅ Add a README file
5. Click **Create repository**

### Step 1.2: Clone Repository Locally

```bash
# Clone your repository (replace USERNAME)
git clone https://github.com/USERNAME/clerk-knowledge-base.git

# Navigate into directory
cd clerk-knowledge-base
```

---

## Part 2: Project Initialization (10 minutes)

### Step 2.1: Create Project Structure

```bash
# Create documentation directory
mkdir docs

# Create .github/workflows directory for automation
mkdir -p .github/workflows

# Create homepage
echo "# Welcome to Clerk Knowledge Base" > docs/index.md
echo "" >> docs/index.md
echo "This is the homepage of clerk knowledge base." >> docs/index.md
```

### Step 2.2: Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
mkdocs>=1.5.0
mkdocs-material>=9.4.0
mkdocs-git-revision-date-localized-plugin>=1.2.0
EOF
```

### Step 2.3: Create mkdocs.yml Configuration

Replace `USERNAME` and `clerk-knowledge-base` with your values:

```bash
cat > mkdocs.yml << 'EOF'
site_name: Clerk Knowledge Base
site_url: https://USERNAME.github.io/clerk-knowledge-base/

repo_name: USERNAME/clerk-knowledge-base
repo_url: https://github.com/USERNAME/clerk-knowledge-base
edit_uri: edit/main/docs/

theme:
  name: material
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - content.code.copy

plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - tables
  - attr_list
EOF
```

### Step 2.4: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install MkDocs and dependencies
pip install -r requirements.txt

# Verify installation
mkdocs --version
```

✅ **Checkpoint**: You should see `mkdocs, version 1.5.x` or higher

---

## Part 3: Local Development (5 minutes)

### Step 3.1: Start Development Server

```bash
mkdocs serve
```

You should see:
```
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.52 seconds
INFO    -  [12:34:56] Serving on http://127.0.0.1:8000/
```

### Step 3.2: View Your Site

1. Open browser to [http://localhost:8000](http://localhost:8000)
2. You should see your homepage: "Welcome to Clerk Knowledge Base"

### Step 3.3: Test Live Reload

1. Keep the server running
2. Open `docs/index.md` in your editor
3. Add a new line: `## Getting Started`
4. Save the file
5. Browser should auto-refresh showing your changes

✅ **Checkpoint**: Changes appear in browser without manual refresh

---

## Part 4: Create Your First Content (3 minutes)

### Step 4.1: Create a New Page

```bash
# Create a new directory and page
mkdir docs/guides
echo "# Installation Guide" > docs/guides/installation.md
echo "" >> docs/guides/installation.md
echo "Follow these steps to install the software:" >> docs/guides/installation.md
echo "" >> docs/guides/installation.md
echo "1. Download the installer" >> docs/guides/installation.md
echo "2. Run the installation wizard" >> docs/guides/installation.md
echo "3. Verify the installation" >> docs/guides/installation.md
```

### Step 4.2: Add Navigation

Update `mkdocs.yml` to add manual navigation (optional):

```yaml
# Add this section after markdown_extensions:
nav:
  - Home: index.md
  - Guides:
    - Installation: guides/installation.md
```

### Step 4.3: View New Page

With `mkdocs serve` still running, navigate to [http://localhost:8000/guides/installation/](http://localhost:8000/guides/installation/)

✅ **Checkpoint**: New installation guide page is visible and navigable

---

## Part 5: Automated Deployment (5 minutes)

### Step 5.1: Create GitHub Actions Workflow

```bash
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy Documentation

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configure Git
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com

      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          key: mkdocs-${{ github.sha }}
          path: ~/.cache
          restore-keys: mkdocs-

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Deploy to GitHub Pages
        run: mkdocs gh-deploy --force
EOF
```

### Step 5.2: Create .gitignore

```bash
cat > .gitignore << 'EOF'
# MkDocs
site/

# Python
__pycache__/
*.py[cod]
venv/
.venv/

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
EOF
```

### Step 5.3: Commit and Push

```bash
# Stage all files
git add .

# Commit
git commit -m "feat: initialize knowledge base with MkDocs and automation"

# Push to GitHub
git push origin main
```

### Step 5.4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
5. Click **Save**

### Step 5.5: Wait for Deployment

1. Go to **Actions** tab in your repository
2. You should see "Deploy Documentation" workflow running
3. Wait 3-5 minutes for it to complete (green checkmark)
4. Go to **Settings > Pages** to see your site URL

✅ **Checkpoint**: Your knowledge base is live at `https://USERNAME.github.io/clerk-knowledge-base/`

---

## Part 6: Make Your First Contribution (2 minutes)

### Step 6.1: Create a Feature Branch

```bash
git checkout -b feature/add-troubleshooting-guide
```

### Step 6.2: Create New Content

```bash
mkdir -p docs/guides
cat > docs/guides/troubleshooting.md << 'EOF'
# Troubleshooting Guide

## Common Issues

### Issue: Site not loading

**Symptom**: Error 404 when accessing GitHub Pages URL

**Solution**:
1. Check GitHub Pages settings
2. Verify `gh-pages` branch exists
3. Wait 5 minutes after first deployment

### Issue: Build failing

**Symptom**: GitHub Actions shows red X

**Solution**:
1. Check Actions log for specific error
2. Run `mkdocs build --strict` locally
3. Fix any broken links or syntax errors
EOF
```

### Step 6.3: Test Locally

```bash
mkdocs serve
# Visit http://localhost:8000/guides/troubleshooting/
```

### Step 6.4: Commit and Push

```bash
git add docs/guides/troubleshooting.md
git commit -m "feat: add troubleshooting guide"
git push origin feature/add-troubleshooting-guide
```

### Step 6.5: Create Pull Request

1. Go to your repository on GitHub
2. Click **Compare & pull request** banner
3. Fill in:
   - **Title**: "Add troubleshooting guide"
   - **Description**: "Adds common troubleshooting scenarios"
4. Click **Create pull request**
5. Wait for build check to pass (green checkmark)
6. Click **Merge pull request**
7. Click **Confirm merge**

✅ **Checkpoint**: Changes deployed automatically to live site in <5 minutes

---

## Success Criteria Verification

You've successfully completed the quickstart if:

- [x] ✅ **SC-001**: Completed setup in under 35 minutes
- [x] ✅ **SC-002**: Site loads in under 2 seconds
- [x] ✅ **SC-003**: Deployment completed in under 5 minutes
- [x] ✅ **SC-008**: Local preview started in under 10 seconds
- [x] ✅ **FR-002**: Local development server with live reload works
- [x] ✅ **FR-003**: Automated deployment on main branch push works
- [x] ✅ **FR-006**: Search functionality works (try it on your live site)
- [x] ✅ **FR-011**: Can preview documentation locally before submitting

---

## Next Steps

### Learn More

- 📚 Read [MkDocs Documentation](https://www.mkdocs.org/)
- 🎨 Explore [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- 📖 Review [Markdown Guide](https://www.markdownguide.org/)

### Customize Your Site

- Change theme colors in `mkdocs.yml` (palette section)
- Add more sections to `docs/` directory
- Customize navigation structure
- Add custom CSS in `docs/stylesheets/extra.css`

### Contribute

- Follow Git workflow in `contracts/git-workflow.md`
- Use conventional commit format
- Create pull requests for all changes
- Request reviews before merging

### Monitor Performance

- Check GitHub Actions for build status
- Use [PageSpeed Insights](https://pagespeed.web.dev/) to test load times
- Monitor search performance with browser dev tools

---

## Troubleshooting

### "mkdocs: command not found"

**Solution**: Activate virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### "Permission denied to gh-pages"

**Solution**: Verify GitHub Actions has `permissions: contents: write` in `.github/workflows/deploy.yml`

### "Site not updating after merge"

**Solution**:
1. Check Actions tab for workflow status
2. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
3. Wait 5 minutes for CDN cache to clear

### "Build failed with broken link"

**Solution**: Run `mkdocs build --strict` locally to see specific error:
```bash
mkdocs build --strict
```
Fix the broken link path and try again.

---

## Time Breakdown

| Phase | Target Time | What You Did |
|-------|------------|--------------|
| Prerequisites | 5 min | Verified Git, Python, editor |
| Repository Setup | 5 min | Created and cloned GitHub repo |
| Project Init | 10 min | Installed MkDocs, created config |
| Local Development | 5 min | Ran local server, tested live reload |
| First Content | 3 min | Created installation guide page |
| Automated Deployment | 5 min | Set up GitHub Actions, enabled Pages |
| First Contribution | 2 min | Feature branch, PR workflow |
| **Total** | **35 min** | ✅ Meets SC-001 target |

---

## Congratulations!

You now have a fully functional knowledge base with:
- ✅ Local development environment
- ✅ Automated CI/CD deployment
- ✅ Live website on GitHub Pages
- ✅ Pull request workflow
- ✅ Search functionality
- ✅ Responsive design

**Ready to build something amazing!** 🚀
