# MkDocs Knowledge Base Setup Guide

## Prerequisites
- Python 3.8+ installed
- Git installed and configured
- GitHub account
- Code editor (VS Code recommended)

## Step-by-Step Setup Process

### 1. Initial Repository Setup

```bash
# Create a new GitHub repository (via GitHub web interface)
# Repository name: knowledge-base (example)
# Make it public for free GitHub Pages hosting

# Clone the repository locally
git clone https://github.com/username/knowledge-base.git
cd knowledge-base

# Create initial project structure
mkdir docs
mkdir .github
mkdir .github/workflows
```

### 2. Install MkDocs and Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt with core dependencies
echo "mkdocs>=1.5.0
mkdocs-material>=9.4.0
mkdocs-git-revision-date-localized-plugin>=1.2.0" > requirements.txt

# Install dependencies
pip install -r requirements.txt

# Verify installation
mkdocs --version
```

### 3. Essential Commands Reference

#### Development Commands
```bash
# Start development server with live reload
mkdocs serve

# Start server on specific port
mkdocs serve -a 0.0.0.0:8080

# Enable dirty reload (faster for large sites)
mkdocs serve --dirtyreload

# Build static site locally
mkdocs build

# Build with verbose output
mkdocs build --verbose
```

#### Deployment Commands
```bash
# Manual deployment to GitHub Pages
mkdocs gh-deploy

# Force deployment (overwrites existing)
mkdocs gh-deploy --force

# Deploy with custom commit message
mkdocs gh-deploy -m "Updated documentation"
```

## Configuration Examples

### Basic mkdocs.yml
```yaml
site_name: Knowledge Base
site_url: https://username.github.io/knowledge-base/
theme:
  name: material
  features:
    - navigation.tabs
    - search.highlight
    - content.code.copy
plugins:
  - search
```

### GitHub Actions Workflow
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
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
```

## Troubleshooting Common Issues

### Site not updating after push
- Check GitHub Actions workflow status
- Verify GitHub Pages settings
- Ensure workflow has proper permissions

### Build fails with config errors
- Validate mkdocs.yml syntax
- Check all required dependencies installed
- Review error logs in Actions tab

### Theme not loading correctly
- Verify material theme installed
- Check theme configuration in mkdocs.yml
- Clear browser cache

## Security and Maintenance Best Practices

- Update dependencies monthly
- Use dependabot for automatic updates
- Monitor GitHub Actions for failures
- Regular content audits
- Performance monitoring
