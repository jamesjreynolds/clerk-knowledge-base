
# Recommended MkDocs Knowledge Base Project Structure

## Repository Root Structure
```
knowledge-base/                    # Repository root
├── .github/                       # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml                 # Automated deployment workflow
├── .gitignore                     # Git ignore file (includes site/ directory)
├── README.md                      # Repository documentation
├── requirements.txt               # Python dependencies
├── mkdocs.yml                     # MkDocs configuration file
├── docs/                          # Documentation source files
│   ├── index.md                   # Homepage (required)
│   ├── getting-started/           # Getting started section
│   │   ├── index.md               # Section landing page
│   │   ├── installation.md
│   │   └── quick-start.md
│   ├── user-guide/               # User guide section
│   │   ├── index.md
│   │   ├── basic-usage.md
│   │   ├── advanced-features.md
│   │   └── troubleshooting.md
│   ├── api-reference/            # API documentation
│   │   ├── index.md
│   │   ├── authentication.md
│   │   └── endpoints.md
│   ├── tutorials/                # Step-by-step tutorials
│   │   ├── index.md
│   │   ├── tutorial-1.md
│   │   └── tutorial-2.md
│   ├── contributing/             # Contributor information
│   │   ├── index.md
│   │   ├── code-of-conduct.md
│   │   └── development-guide.md
│   ├── assets/                   # Static assets
│   │   ├── images/
│   │   │   ├── screenshots/
│   │   │   └── diagrams/
│   │   ├── css/
│   │   │   └── extra.css         # Custom styling
│   │   └── js/
│   │       └── extra.js          # Custom JavaScript
│   └── stylesheets/              # Additional CSS (Material theme)
│       └── extra.css
└── site/                         # Generated static site (git ignored)
    └── (auto-generated files)
```

## Key Configuration Files

### mkdocs.yml Example
```yaml
site_name: Knowledge Base
site_url: https://username.github.io/knowledge-base/
site_author: Your Organization
site_description: Comprehensive knowledge base documentation

# Repository
repo_name: username/knowledge-base
repo_url: https://github.com/username/knowledge-base
edit_uri: edit/main/docs/

# Theme
theme:
  name: material
  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
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
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy

# Plugins
plugins:
  - search
  - git-revision-date-localized:
      enable_creation_date: true

# Extensions
markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - attr_list
  - def_list
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

# Navigation
nav:
  - Home: index.md
  - Getting Started:
    - getting-started/index.md
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
  - User Guide:
    - user-guide/index.md
    - Basic Usage: user-guide/basic-usage.md
    - Advanced Features: user-guide/advanced-features.md
    - Troubleshooting: user-guide/troubleshooting.md
  - Tutorials:
    - tutorials/index.md
    - Tutorial 1: tutorials/tutorial-1.md
    - Tutorial 2: tutorials/tutorial-2.md
  - API Reference:
    - api-reference/index.md
    - Authentication: api-reference/authentication.md
    - Endpoints: api-reference/endpoints.md
  - Contributing:
    - contributing/index.md
    - Code of Conduct: contributing/code-of-conduct.md
    - Development Guide: contributing/development-guide.md

# Extra CSS and JS
extra_css:
  - stylesheets/extra.css

extra_javascript:
  - assets/js/extra.js
```

### requirements.txt
```
mkdocs>=1.5.0
mkdocs-material>=9.4.0
mkdocs-git-revision-date-localized-plugin>=1.2.0
```

### .gitignore
```
# MkDocs
site/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### GitHub Actions Workflow (.github/workflows/ci.yml)
```yaml
name: Deploy MkDocs

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Configure Git Credentials
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ github.sha }}
          path: ~/.cache
          restore-keys: |
            mkdocs-material-

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Deploy to GitHub Pages
        run: |
          mkdocs gh-deploy --force

  build-pr:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Build site
        run: |
          mkdocs build --strict
```
