# Ward Clerk Contributor Onboarding Guide

Welcome! This guide will help you contribute your ward clerk knowledge and experience to help other clerks in the Church.

## Who Should Contribute?

- Current or former ward clerks
- Assistant clerks (financial or membership)
- Stake clerks
- Anyone with practical clerk experience to share

You don't need to be a technical expert - if you can write an email, you can contribute!

## New Contributor Onboarding Checklist

### Prerequisites (5 minutes)
- [ ] GitHub account created (free at github.com)
- [ ] Git installed locally (or use GitHub Desktop - simpler option)
- [ ] Text editor installed (VS Code recommended, but Notepad works too)
- [ ] Basic familiarity with Markdown (we'll teach you!)

### Initial Setup (10 minutes)

**Option A: Using GitHub Desktop (Recommended for non-technical users)**

- [ ] Install GitHub Desktop from desktop.github.com
- [ ] Fork the repository by clicking "Fork" at github.com/jamesjreynolds/clerk-knowledge-base
- [ ] Clone your fork using GitHub Desktop
- [ ] Open the folder in your text editor

**Option B: Using Command Line (For technical users)**

- [ ] Fork the repository on GitHub
- [ ] Clone your fork locally: `git clone https://github.com/YOUR-USERNAME/clerk-knowledge-base.git`
- [ ] Set up upstream remote: `git remote add upstream https://github.com/jamesjreynolds/clerk-knowledge-base.git`

### First Test (5 minutes)

**Testing Locally (Optional but Recommended)**

If you want to preview your changes before submitting:

- [ ] Install Python 3.8+ from python.org
- [ ] Open terminal/command prompt in the project folder
- [ ] Run: `pip install -r requirements.txt`
- [ ] Run: `mkdocs serve`
- [ ] Open http://localhost:8000 in browser

**Simple Editing (No local testing)**

- [ ] Edit files directly on GitHub.com in your browser
- [ ] Preview changes using GitHub's preview button

### Make Your First Contribution (15 minutes)
- [ ] Create a new branch (GitHub Desktop: Branch → New Branch, or click "Edit" on GitHub.com)
- [ ] Make a small edit (fix a typo, add a tip you've learned)
- [ ] Save and commit your changes
- [ ] Push to your fork (GitHub Desktop does this automatically)
- [ ] Create a Pull Request on github.com
- [ ] Wait for review and merge

## Content Creation Guidelines

### What Makes Good Clerk Documentation?

**Focus on practical "how-to" procedures:**
- ✅ Step-by-step instructions for common tasks
- ✅ Screenshots showing where to click in LCR
- ✅ Troubleshooting tips for common problems
- ✅ Workarounds for LCR system quirks
- ✅ Real examples from your ward experience

**Avoid these:**
- ❌ Copying directly from the Church Handbook (link to it instead)
- ❌ Ward-specific information (names, numbers, local policies)
- ❌ Confidential information
- ❌ Opinions about Church policies (stick to procedures)

### File Naming for Clerk Procedures

Use descriptive, lowercase filenames with hyphens:
- ✅ `quarterly-report-submission.md`
- ✅ `reimbursement-procedures.md`
- ✅ `lost-member-search.md`
- ❌ `Report.md` (too vague, capitalized)
- ❌ `my notes.md` (has spaces)

Store files in the appropriate section folder:
- `docs/membership/` - Membership record procedures
- `docs/financial/` - Financial procedures
- `docs/reports/` - Reporting procedures
- `docs/annual-history/` - Annual history procedures
- `docs/agent-bishop/` - Building/facilities procedures

### Markdown Basics for Clerks

Markdown is just text with simple formatting marks. Here's everything you need:

#### Basic Text Formatting
```markdown
# Page Title (use once at top)

## Main Section Heading

### Subsection Heading

Regular paragraph text goes here.

**Bold text** for important terms or UI elements
*Italic text* for emphasis

- Bullet point item
- Another bullet point

1. Numbered step one
2. Numbered step two
3. Numbered step three
```

#### Links and References
```markdown
# Link to another page in this site
See also [Quarterly Reports](quarterly-reports.md)

# Link to external resource
[Church Handbook Chapter 33](https://www.churchofjesuschrist.org/study/manual/general-handbook/33)

# Link to LCR
[Leader and Clerk Resources](https://lcr.churchofjesuschrist.org/)
```

#### Adding Screenshots and Images
```markdown
![Screenshot description](../assets/images/lcr-screenshot.png)
```

**Image Guidelines:**
- Save screenshots to `docs/assets/images/`
- Use descriptive filenames: `lcr-quarterly-report-button.png`
- Keep images under 5 MB (compress if needed at tinypng.com)
- Black out any sensitive information before uploading

#### Callout Boxes for Important Information

```markdown
!!! warning "Important"
    Always verify the member's identity before making record changes.

!!! danger "Critical: System Limitation"
    🚨 LCR does not save drafts automatically. Complete your entry in one session or you'll lose your work.

!!! info "Pro Tip"
    Save time by opening multiple browser tabs for different LCR tasks.

!!! note "Helpful Resources"
    Contact your stake clerk if you have questions about this procedure.
```

#### Tables for Organizing Information

```markdown
| Task | When | Who |
|------|------|-----|
| Quarterly Report | Last Sunday of quarter | Ward Clerk |
| Annual History | January 31 | Assistant Clerk |
| Budget Review | October | Financial Clerk |
```

### Content Structure Example

Here's a template for a typical clerk procedure page:

```markdown
# Submitting Quarterly Reports

Brief introduction explaining what quarterly reports are and why they matter.

## When to Submit

- Quarterly reports are due the last Sunday of March, June, September, and December
- Submit even if there are no changes to report
- Late submissions may delay stake reporting

## Step-by-Step Instructions

### 1. Access the Report in LCR

1. Log in to [LCR](https://lcr.churchofjesuschrist.org/)
2. Click **Reports** in the top navigation
3. Select **Quarterly Report** from the dropdown menu
4. Choose the correct quarter from the calendar

### 2. Review Required Sections

Go through each section and verify the information is current:

- **Membership Statistics**: Auto-populated from your records
- **Attendance Averages**: Enter average sacrament meeting attendance
- **Missionary Progress**: Report convert baptisms and referrals
- **Leadership Changes**: Note any changes in callings

!!! warning "Common Mistake"
    Don't forget to click **Save** after each section before moving to the next one!

### 3. Submit the Report

1. Review the summary page for accuracy
2. Click **Submit Report** (not just Save)
3. Print or save the confirmation page for your records

## Troubleshooting

**Problem:** "Submit" button is grayed out
- **Solution:** Check that all required fields are filled in. Look for red asterisks (*) marking required fields.

**Problem:** Report doesn't show recent baptisms
- **Solution:** Ensure the baptism date was recorded in the membership record before running the report.

## Related Procedures

- [How to Update Membership Records](membership-record-updates.md)
- [Common LCR Reporting Issues](lcr-troubleshooting.md)

## Church Resources

- [Church Handbook - Chapter 33: Records and Reports](https://www.churchofjesuschrist.org/study/manual/general-handbook/33-records-and-reports)
```

### Writing Style for Clerks

**Use clear, step-by-step language:**
- ✅ "Click the blue Submit button in the upper right corner"
- ❌ "Navigate to the submission interface and execute the report"

**Write for busy clerks who need quick answers:**
- Start with the most common scenario
- Put troubleshooting tips in callout boxes
- Include time estimates ("This takes about 5 minutes")

**Include helpful context:**
- Explain WHY something matters, not just HOW
- Mention common mistakes to avoid
- Share tips that save time

## Git Workflow for Clerks

### Branch Naming for Clerk Content

Use clear names that describe what you're adding:
- `add-quarterly-report-guide` - New procedure page
- `fix-reimbursement-link` - Fixing broken links
- `update-lost-member-search` - Updating existing content
- `add-lcr-screenshot` - Adding helpful screenshots

### Commit Messages

Keep it simple and descriptive:

**Good examples:**
- `Add procedure for submitting quarterly reports`
- `Fix broken link to Church Handbook`
- `Update screenshot for new LCR interface`
- `Add troubleshooting section for reimbursements`

**What to avoid:**
- `Update` (too vague)
- `Fixed stuff` (not descriptive)
- `WIP` (don't commit incomplete work)

### Pull Request Checklist

Before creating your pull request:

- [ ] Read through your changes one more time
- [ ] Check that all links work
- [ ] Verify images display correctly
- [ ] Make sure you didn't include any ward-specific information
- [ ] Ensure you followed the style guide
- [ ] Write a clear PR description explaining what you added or changed

**Pull Request Description Template:**
```markdown
## What I Added

Brief description of the procedure or information you're contributing.

## Why This Is Helpful

Explain the problem this solves or the common question it answers.

## My Experience

Mention how long you've been a clerk or where you learned this procedure.
(e.g., "I'm a financial clerk and discovered this workaround after 2 years")

## Screenshots

If applicable, include before/after screenshots showing the change.
```

## Common Tasks for Clerk Contributors

### Adding a New Procedure Page

1. Decide which section folder it belongs in (membership, financial, reports, etc.)
2. Create a new `.md` file with a descriptive name
3. Use the content structure template above
4. Add the page to the navigation in `mkdocs.yml` (ask for help if needed)
5. Test locally or submit for review

### Updating an Existing Page

1. Find the file in the `docs/` folder
2. Make your changes using Markdown formatting
3. Keep the same structure and style as the existing content
4. Add a note about what changed in your commit message

### Adding Screenshots from LCR

1. Take the screenshot (use your operating system's screenshot tool)
2. **Important:** Black out any member names, dates of birth, or other sensitive information
3. Save to `docs/assets/images/` with a descriptive name
4. Reference in your Markdown: `![Description](../assets/images/filename.png)`
5. Keep file size under 5 MB (use tinypng.com to compress if needed)

### Fixing Broken Links

If you find a broken link:
1. Note which page has the broken link
2. Find the correct link (test it in your browser)
3. Update the Markdown file with the correct link
4. Test that it works
5. Submit a quick pull request

## Tools and Resources

### For Non-Technical Clerks

- **GitHub Desktop** - Easy way to manage git without the command line
- **VS Code** - Free code editor that shows Markdown preview
- **Markdown Tutorial** - markdowntutorial.com (10 minute interactive tutorial)
- **Snipping Tool** (Windows) or Command+Shift+4 (Mac) - For screenshots

### Helpful Online Tools

- [Markdown Table Generator](https://www.tablesgenerator.com/markdown_tables) - Create tables visually
- [TinyPNG](https://tinypng.com/) - Compress large screenshots
- [Markdown Guide](https://www.markdownguide.org/basic-syntax/) - Quick reference

### Church Resources

- [Church Handbook](https://www.churchofjesuschrist.org/study/manual/general-handbook) - Official policies
- [LCR Help Center](https://lcr.churchofjesuschrist.org/) - LCR documentation
- [Help Desk](https://www.churchofjesuschrist.org/help) - Technical support

## Getting Help

### Where to Ask Questions

1. **GitHub Issues** - Report problems or suggest new procedure pages
2. **Pull Request Comments** - Ask questions about your specific contribution
3. **Your Stake Clerk** - For questions about clerk procedures
4. **Ward/Stake Technologist** - For technical help with git/markdown

### What to Do If You're Stuck

**Scenario 1: "I don't know Markdown"**
- Start with the 10-minute tutorial at markdowntutorial.com
- Look at existing pages and copy their formatting
- Use GitHub's online editor which has a preview button
- Ask for help in your pull request - we're happy to guide you!

**Scenario 2: "I have a procedure to share but don't know where it should go"**
- Create the page anyway and ask in your pull request
- We'll help you find the right place and update navigation

**Scenario 3: "Git is confusing me"**
- Use GitHub Desktop instead of command line
- Or edit files directly on GitHub.com in your browser
- Watch a 5-minute YouTube tutorial on "GitHub Desktop basics"

**Scenario 4: "I want to contribute but don't have time to learn all this"**
- Write up your procedure in an email or Word doc
- Open a GitHub Issue and paste it there
- Someone else can help format it into Markdown

## Recognition

Every contribution helps fellow clerks serve more effectively. Thank you for sharing your experience!

- Contributors are recognized in the repository
- You'll be helping clerks you've never met
- Your practical tips will save hours of frustration for others

## Remember

**The most valuable contributions are:**
- Real procedures you've actually used in your calling
- Workarounds for common LCR frustrations
- Tips that save time or prevent mistakes
- Clear explanations for confusing parts of clerk work

**You don't need to be perfect:**
- Other contributors will help improve your writing
- It's okay to start with a rough draft
- We'd rather have your knowledge than have it stay in your head!

Thank you for contributing to help fellow clerks serve better!
