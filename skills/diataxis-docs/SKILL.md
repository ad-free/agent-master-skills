---
name: diataxis-docs
description: "Use when you need Diataxis documentation framework integration. Syncs documentation on ship using the four Diataxis quadrants: tutorials, how-to guides, explanation, and reference. Ensures documentation stays in sync with code changes."
model: big-pickle
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
triggers:
  - "docs sync"
  - "diataxis"
  - "documentation"
  - "update docs"
  - "doc sync"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
---

# Diataxis Documentation Sync

Syncs documentation on ship using the Diataxis framework.

---

## 1. THE FOUR QUADRANTS

### Tutorials (Learning-oriented)
- **Purpose:** Help users learn by doing
- **Style:** Lesson-style, incremental
- **Example:** "Getting Started with X"
- **When to update:** New features, major changes

### How-To Guides (Task-oriented)
- **Purpose:** Help users accomplish specific tasks
- **Style:** Recipe-style, goal-focused
- **Example:** "How to Deploy to Production"
- **When to update:** New workflows, changed procedures

### Explanation (Understanding-oriented)
- **Purpose:** Help users understand context
- **Style:** Discussion-style, conceptual
- **Example:** "Architecture Overview"
- **When to update:** New concepts, changed architecture

### Reference (Information-oriented)
- **Purpose:** Provide accurate technical information
- **Style:** Description-style, factual
- **Example:** "API Reference"
- **When to update:** New APIs, changed parameters

---

## 2. SYNC ON SHIP

### Pre-ship Documentation Check
```bash
# Check if documentation exists
ls -la docs/

# Check if documentation is up to date
git diff --name-only HEAD~1 | grep -E "\.(md|mdx)$"

# Check if new features have docs
git log --oneline HEAD~10..HEAD | grep -i "feat:" | while read line; do
  echo "Feature: $line"
  # Check if feature has documentation
done
```

### Post-ship Documentation Update
```bash
# Update API reference
npm run docs:api

# Update changelog
npm run docs:changelog

# Update tutorials
npm run docs:tutorials

# Deploy documentation
npm run docs:deploy
```

---

## 3. DOCUMENTATION STRUCTURE

### docs/
```
docs/
├── tutorials/          # Learning-oriented
│   ├── getting-started.md
│   ├── first-feature.md
│   └── advanced-usage.md
├── how-to/            # Task-oriented
│   ├── deploy.md
│   ├── configure.md
│   └── troubleshoot.md
├── explanation/       # Understanding-oriented
│   ├── architecture.md
│   ├── concepts.md
│   └── design-decisions.md
├── reference/         # Information-oriented
│   ├── api.md
│   ├── cli.md
│   └── config.md
└── CHANGELOG.md
```

---

## 4. AUTO-GENERATION

### API Reference
```bash
# Generate API docs from code
npx typedoc --out docs/reference/api src/

# Or for JavaScript
npx jsdoc --out docs/reference/api src/

# Or for Go
godoc -http=:6060
```

### CLI Reference
```bash
# Generate CLI docs
npm run build && ./bin/cli --help > docs/reference/cli.md
```

### Changelog
```bash
# Generate changelog from commits
git log --oneline --no-merges HEAD~10..HEAD > docs/CHANGELOG.md

# Or use conventional-changelog
npx conventional-changelog -p angular -i docs/CHANGELOG.md -s
```

---

## 5. DOCUMENTATION QUALITY CHECKS

### Link Checker
```bash
# Check for broken links
npx markdown-link-check docs/**/*.md

# Or use specific tool
npx broken-link-checker http://localhost:3000
```

### Spelling Checker
```bash
# Check spelling
npx cspell "docs/**/*.md"

# Or use specific dictionary
npx cspell --config cspell.json "docs/**/*.md"
```

### Format Checker
```bash
# Check markdown format
npx prettier --check "docs/**/*.md"

# Fix formatting
npx prettier --write "docs/**/*.md"
```

---

## 6. SYNC TRIGGERS

### On Merge to Main
```yaml
# .github/workflows/docs-sync.yml
name: Docs Sync
on:
  push:
    branches: [main]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run docs:generate
      - run: npm run docs:check
      - run: npm run docs:deploy
```

### On Tag
```yaml
name: Release Docs
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - run: npm run docs:changelog
      - run: npm run docs:tutorials
      - run: npm run docs:deploy
```

---

## 7. DOCUMENTATION TEMPLATES

### Tutorial Template
```markdown
# Tutorial: [Title]

## What you'll learn
- [Learning objective 1]
- [Learning objective 2]

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]

## Step 1: [Step Title]
[Instructions]

## Step 2: [Step Title]
[Instructions]

## Next steps
- [Link to related tutorial]
- [Link to how-to guide]
```

### How-To Template
```markdown
# How to [Task]

## Prerequisites
- [Prerequisite 1]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Troubleshooting
- [Common issue 1]
- [Common issue 2]

## Related
- [Link to explanation]
- [Link to reference]
```

### Explanation Template
```markdown
# [Concept]

## Overview
[High-level overview]

## How it works
[Detailed explanation]

## Why it matters
[Context and rationale]

## Related concepts
- [Related concept 1]
- [Related concept 2]
```

### Reference Template
```markdown
# [API/CLI/Config] Reference

## [Endpoint/Command/Option]
- **Description:** [What it does]
- **Parameters:** [List of parameters]
- **Returns:** [What it returns]
- **Examples:** [Usage examples]

## [Next endpoint/command/option]
...
```

---

## 8. DOCUMENTATION DEPLOYMENT

### Static Site
```bash
# Build documentation site
npm run docs:build

# Deploy to GitHub Pages
gh-pages -d docs/dist

# Or deploy to Netlify
netlify deploy --dir=docs/dist
```

### API Documentation
```bash
# Deploy API docs
npm run docs:api:deploy

# Or use Swagger UI
npx swagger-ui-dist
```

---

## 9. BEST PRACTICES

### Do
- Update docs on every release
- Use the four Diataxis quadrants
- Auto-generate when possible
- Check links and spelling
- Deploy documentation automatically

### Don't
- Forget to update docs
- Mix tutorial and reference styles
- Leave broken links
- Skip documentation quality checks
- Deploy without testing

---

## 10. QUICK DOC SYNC

For a fast documentation sync:
```bash
# Generate docs
npm run docs:generate

# Check quality
npm run docs:check

# Deploy
npm run docs:deploy
```
