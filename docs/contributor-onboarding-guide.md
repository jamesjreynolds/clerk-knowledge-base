# MkDocs Knowledge Base Contributor Onboarding Guide

## New Contributor Onboarding Checklist

### Prerequisites (5 minutes)
- [ ] GitHub account created and configured
- [ ] Git installed locally
- [ ] Code editor installed (VS Code recommended)
- [ ] Python 3.8+ installed
- [ ] Basic Markdown knowledge

### Initial Setup (10 minutes)
- [ ] Fork the repository on GitHub
- [ ] Clone your fork locally: `git clone https://github.com/YOUR-USERNAME/clerk-knowledge-base.git`
- [ ] Set up upstream remote: `git remote add upstream https://github.com/jamesjreynolds/clerk-knowledge-base.git`
- [ ] Create Python virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

### First Test (5 minutes)
- [ ] Start local development server: `mkdocs serve`
- [ ] Open http://localhost:8000 in browser
- [ ] Verify site loads correctly
- [ ] Test live reload by editing docs/index.md
- [ ] Confirm changes appear automatically

### Make Your First Contribution (15 minutes)
- [ ] Create a feature branch: `git checkout -b fix-typo-homepage`
- [ ] Make a small edit (fix typo, improve wording)
- [ ] Test changes locally with `mkdocs serve`
- [ ] Commit changes: `git commit -m "Fix typo on homepage"`
- [ ] Push branch: `git push origin fix-typo-homepage`
- [ ] Create Pull Request via GitHub web interface
- [ ] Wait for review and merge

## Content Creation Guidelines

### Markdown Best Practices

#### File Naming
- Use lowercase filenames
- Separate words with hyphens: `user-guide.md`
- Use descriptive names: `api-authentication.md`
- Include section in path: `getting-started/installation.md`

#### Content Structure
```markdown
# Page Title (H1 - only one per page)

Brief introduction paragraph explaining the page purpose.

## Main Section (H2)

Content organized in logical sections.

### Subsection (H3)

More specific content.

#### Details (H4 - use sparingly)

Fine-grained details when needed.
```

#### Code Blocks
```markdown
Use triple backticks with language specification:

​```python
def example_function():
    return "Hello, World!"
​```

​```bash
# Commands should include comments
mkdocs serve --help
​```
```

#### Links and References
```markdown
# Internal links (relative paths)
[User Guide](../user-guide/basic-usage.md)

# External links
[MkDocs Documentation](https://www.mkdocs.org/)

# Images
![Alt text](../assets/images/screenshot.png)
```

### Navigation Organization

#### Automatic Navigation
- MkDocs auto-generates navigation from file structure
- Files sorted alphabetically within directories
- Use descriptive directory and file names

#### Manual Navigation (mkdocs.yml)
```yaml
nav:
  - Home: index.md
  - Getting Started:
    - getting-started/index.md
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
  - User Guide:
    - user-guide/index.md
    - Basic Usage: user-guide/basic-usage.md
```

### Content Style Guide

#### Writing Style
- Use clear, concise language
- Write in second person ("you can...")
- Use active voice
- Break up long paragraphs
- Include examples and code samples

#### Formatting Standards
- Use **bold** for UI elements and important terms
- Use `code formatting` for commands, filenames, and variables
- Use > blockquotes for important notes
- Use numbered lists for sequential steps
- Use bullet points for non-sequential items

## Git Workflow Best Practices

### Branch Naming Conventions
- `feature/add-api-docs` - New features or content
- `fix/broken-link-homepage` - Bug fixes
- `docs/update-contributing-guide` - Documentation updates
- `style/improve-navigation` - Design/style improvements

### Commit Message Format
```
type: brief description (50 chars max)

Optional longer explanation of what changed and why.
Include issue references if applicable.

Closes #123
```

**Types:**
- `feat:` New features or content
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Formatting changes
- `refactor:` Code/content reorganization

### Pull Request Process

#### Before Creating PR
- [ ] Sync with upstream: `git fetch upstream && git merge upstream/main`
- [ ] Test locally: `mkdocs serve`
- [ ] Build successfully: `mkdocs build`
- [ ] Review changes: `git diff`
- [ ] Commit with clear messages

#### PR Description Template
```markdown
## Summary
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Documentation update
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)

## Testing
- [ ] Changes tested locally
- [ ] All links work correctly
- [ ] Navigation functions properly
- [ ] Content renders correctly

## Screenshots (if applicable)
Include before/after screenshots for visual changes.

## Checklist
- [ ] Self-review completed
- [ ] Comments added for complex sections
- [ ] Documentation updated (if needed)
- [ ] Follows project style guide
```

## Review Process

### For Reviewers
- Check content accuracy and clarity
- Verify all links work
- Test navigation changes
- Ensure consistent formatting
- Provide constructive feedback

### For Contributors
- Address all reviewer feedback
- Make requested changes promptly
- Ask questions if feedback unclear
- Test changes after modifications
- Thank reviewers for their time

## Common Tasks and Solutions

### Adding New Pages
1. Create markdown file in appropriate directory
2. Add to navigation in mkdocs.yml (if using manual nav)
3. Link from other relevant pages
4. Test locally and create PR

### Fixing Broken Links
1. Find broken link in content
2. Update with correct path or URL
3. Test all links on page
4. Consider adding link checking to workflow

### Updating Navigation
1. Modify nav section in mkdocs.yml
2. Test navigation structure locally
3. Ensure all pages are accessible
4. Consider user experience flow

### Adding Images
1. Save images to docs/assets/images/
2. Use descriptive filenames
3. Optimize image size for web
4. Include alt text for accessibility
5. Reference with relative paths

## Tools and Resources

### Recommended VS Code Extensions
- **YAML** - YAML language support
- **Markdown All in One** - Enhanced Markdown editing
- **markdownlint** - Markdown linting
- **Python** - Python language support

### Useful Online Tools
- [Markdown Table Generator](https://www.tablesgenerator.com/markdown_tables)
- [YAML Validator](http://www.yamllint.com/)
- [Image Compression](https://tinypng.com/)
- [Emoji Shortcodes](https://gist.github.com/rxaviers/7360908)

### Documentation References
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Docs](https://docs.github.com/)

## Getting Help

### Where to Ask Questions
1. **GitHub Issues** - Bug reports and feature requests
2. **GitHub Discussions** - General questions and ideas
3. **Pull Request Comments** - Specific review questions
4. **Stake Clerk/Stake Technologist** - Quick questions (if available)

### Escalation Path
1. Check existing documentation first
2. Search closed issues and discussions
3. Ask in appropriate channel
4. Tag maintainers if urgent (sparingly)

## Recognition and Growth

### Contributing Recognition
- Contributors listed in README
- Regular contributor highlights
- GitHub contribution graph
- Learning opportunities through reviews

### Advanced Contributions
- Help review other PRs
- Propose new features or improvements
- Assist with onboarding new contributors
- Contribute to project maintenance

This guide should help new contributors get up to speed quickly while maintaining high quality standards for the knowledge base.
