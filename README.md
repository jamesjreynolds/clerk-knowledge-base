# Ward Clerk Knowledge Base

[![Deploy Status](https://github.com/jamesjreynolds/clerk-knowledge-base/actions/workflows/deploy.yml/badge.svg)](https://github.com/jamesjreynolds/clerk-knowledge-base/actions/workflows/deploy.yml)

A practical, community-maintained knowledge base for ward clerks, assistant clerks, and stake clerks in The Church of Jesus Christ of Latter-day Saints.

**Live Site:** [https://jamesjreynolds.github.io/clerk-knowledge-base/](https://jamesjreynolds.github.io/clerk-knowledge-base/)

## About This Project

This knowledge base provides step-by-step procedures, practical tips, and workarounds for common clerk responsibilities. The content goes beyond the official Church Handbook to share real-world experience from clerks serving in wards and stakes.

### What You'll Find Here

- **Membership Procedures** - Quarterly reports, record management, finding lost members
- **Financial Procedures** - Budgets, expenses, reimbursements, audits, signature cards
- **Reporting Guidance** - Various reports and their schedules
- **Annual History** - Documentation and preservation procedures
- **Agent Bishop Responsibilities** - Building management and coordination

### What This Is NOT

- ❌ A replacement for the [Church Handbook](https://www.churchofjesuschrist.org/study/manual/general-handbook) (official policies)
- ❌ A substitute for [Leader and Clerk Resources (LCR)](https://lcr.churchofjesuschrist.org/) training
- ❌ Official Church documentation

## Contributing

**We need your help!** If you're a current or former clerk with practical knowledge to share, please contribute.

### Quick Start for Contributors

1. Read the [Contributor Onboarding Guide](https://jamesjreynolds.github.io/clerk-knowledge-base/contributor-onboarding-guide/)
2. Fork this repository
3. Add or improve clerk procedures
4. Submit a pull request

**Don't know how to use Git or Markdown?** No problem! The contributor guide walks you through everything, or you can [open an issue](https://github.com/jamesjreynolds/clerk-knowledge-base/issues/new) with your procedure and we'll help format it.

### What Makes a Good Contribution?

- ✅ Step-by-step instructions for common tasks
- ✅ Screenshots showing where to click in LCR
- ✅ Troubleshooting tips for common problems
- ✅ Workarounds for LCR system quirks
- ✅ Real examples from your ward experience

- ❌ Ward-specific information (names, numbers, local policies)
- ❌ Confidential information
- ❌ Content copied directly from the Church Handbook

## Technology Stack

This site is built with:

- **[MkDocs](https://www.mkdocs.org/)** - Static site generator
- **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - Modern theme
- **[GitHub Pages](https://pages.github.com/)** - Free hosting
- **[GitHub Actions](https://github.com/features/actions)** - Automated deployment

## Local Development

Want to preview changes locally before submitting?

```bash
# Install dependencies (Python 3.8+ required)
pip install -r requirements.txt

# Start local development server
mkdocs serve

# Open http://localhost:8000 in your browser
```

The site will automatically reload as you edit Markdown files.

## Project Structure

```
docs/
├── index.md                  # Homepage
├── membership/               # Membership procedures
├── financial/                # Financial procedures
├── reports/                  # Reporting procedures
├── annual-history/           # Annual history procedures
├── agent-bishop/             # Building/facilities procedures
└── assets/
    ├── css/custom.css       # Custom styling
    └── images/              # Screenshots and images

mkdocs.yml                    # Site configuration
.github/workflows/deploy.yml  # Automated deployment
```

## Deployment

Deployment is fully automated:

1. Push changes to the `main` branch
2. GitHub Actions builds the site
3. Validates links and file sizes
4. Deploys to GitHub Pages automatically

No manual deployment needed! 🎉

## Support

- **Documentation Issues:** [Open an issue](https://github.com/jamesjreynolds/clerk-knowledge-base/issues/new)
- **Clerk Procedures Questions:** Ask your stake clerk or stake technology specialist
- **LCR Technical Support:** [Church Help Desk](https://www.churchofjesuschrist.org/help)

## License

Content is licensed under [Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to:
- **Share** - Copy and redistribute the material
- **Adapt** - Remix, transform, and build upon the material

Under these terms:
- **Attribution** - Give appropriate credit
- **ShareAlike** - Distribute contributions under the same license

## Acknowledgments

Thank you to all the ward clerks, assistant clerks, and stake clerks who have contributed their time and experience to help fellow clerks serve more effectively.

---

**Note:** This is an unofficial community resource. Always refer to the official Church Handbook and consult with your bishop or stake presidency for authoritative guidance.
