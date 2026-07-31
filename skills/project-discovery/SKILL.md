---
name: project-discovery
description: |
  Parse existing spec files (Excel, CSV, MD, PDF, text) into structured DOMAIN.md.
  Use when user provides requirement documents — before planning or dev-craft.
  Invoked by: triage, planner.
  
model: nemotron-3-ultra-free
version: 2.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "parse this spec file"
  - "extract domain from requirements"
  - "convert Excel to domain model"
  - "ingest requirement documents"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: product-discovery
  integrates-with: [product-thinking, planning-and-task-breakdown]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~10K tokens. If skill exceeds, extract sections to references/.

# Project Discovery — Domain Model Extraction

## Overview

Parse existing requirement documents (Excel, CSV, plain text, Markdown, PDF) and extract a structured domain model: entities, features, priorities, dependencies, and effort estimates. The output `DOMAIN.md` feeds directly into the `dev-craft` REQUIRE phase, enabling structured planning from raw specifications.

> **Goal:** Turn messy specs into a machine-readable domain model without loss of information.

## When to Activate

Activate this skill when **any** of these conditions are true:

| Condition | Example |
|-----------|---------|
| User has existing spec files | PRD, functional spec, requirements doc |
| User has spreadsheets with requirements | Excel sheets listing features, modules, entities |
| User has estimates or cost sheets | Cost/effort tables mapped to features |
| User is migrating from another system | Legacy docs, exported data, old requirement artifacts |
| User pastes raw requirements in chat | Bullet lists, numbered items, free-form text |
| User says "I have all the requirements in this file" | Any file attachment with domain info |
| User needs to bridge from documents to `dev-craft` | Raw requirements → structured plan pipeline |

**When NOT to use:** User has no existing documentation, requirements are being gathered fresh from scratch (use `planning-and-task-breakdown` instead), or the domain is already modeled in a structured format like a proper ERD or UML.

## Invocation Protocol

**Load when:** User provides files or pasted text containing requirements
**Invoke via:** `skill(name="project-discovery")`
**Resume to:** Feed `DOMAIN.md` into `dev-craft` REQUIRE phase or `planning-and-task-breakdown`

```
┌─────────────┐     ┌──────────────────┐     ┌────────────┐     ┌─────────────────────┐
│ Raw files/  │────▶│ project-discovery │────▶│ DOMAIN.md  │────▶│ dev-craft (REQUIRE) │
│ paste/text  │     │ (this skill)      │     │            │     │ planning-and-task   │
└─────────────┘     └──────────────────┘     └────────────┘     └─────────────────────┘
```

## Ingestion Pipeline

### Step 1: Detect File Type

Identify the format of each input file:

| Extension | Type | Parser Strategy |
|-----------|------|-----------------|
| `.xlsx` / `.xls` | Excel | Read sheets, extract named ranges, scan rows/columns for entity headers |
| `.csv` | Comma-separated | Parse headers and rows, detect named entities in first column |
| `.md` | Markdown | Parse headings, bullet lists, tables, code blocks, bold/italic patterns |
| `.txt` | Plain text | Line-by-line scan, detect sections via blank lines, detect lists via indentation/bullets |
| `.pdf` | PDF | Extract text via `pdftotext` or `python -m pdfminer`, then treat as `.txt` |

```
# Manual parsing (no scripts required)
# Agent: read the file, analyze its structure, extract entities and features directly
```

If format is ambiguous, attempt all parsers and use the one with highest confidence.

### Step 2: Scan for Entity Names

Entities are the core nouns of the domain (tables, classes, domain objects). Scan for:

- **Headings** — Markdown `##`, Excel bold rows, CSV column groups
- **Repeated capitalization** — PascalCase, SCREAMING_SNAKE_CASE patterns (e.g., `PayrollRecord`, `EMPLOYEE_MASTER`)
- **Table headers** — First row of tables ("Name", "Employee", "Attendance")
- **Glossary patterns** — Bold terms, definitions, "entity" or "table" keywords
- **Common domain suffixes**: `-ment`, `-ion`, `-ance`, `-ory`, `-er`, `-or`

**Heuristics:**
- Nouns used **3+ times** across the document → probable entity
- Appears in **feature descriptions** as subject → probable entity
- Has **attributes or fields listed** under it → confirmed entity

### Step 3: Scan for Feature Lists

Features are capabilities or functions the system must provide. Look for:

- **Bullet points** (`-`, `*`, `+`)
- **Numbered items** (`1.`, `2.`, `(a)`, `(b)`)
- **Task/checklist items** (`- [ ]`, `- [x]`)
- **Table rows** with feature descriptions
- **"Must", "Should", "Shall"** statements
- **User story patterns** (`As a...`, `I want to...`, `So that...`)
- **Use case labels** (`UC-01`, `US-001`, `FR-01`)

**Boundary heuristic:** A feature is a single capability. If a bullet contains "and" or "or", it may be two features merged — flag for user review.

### Step 4: Scan for Priority Indicators

Priorities tell us what to build first. Look for:

| Pattern | Normalized Priority |
|---------|-------------------|
| `G1`, `G1/G3` | Group 1 (Critical), Group 2 (Important), Group 3 (Nice-to-have) |
| `P0`, `P1`, `P2`, `P3` | P0=Blocker, P1=Critical, P2=Important, P3=Nice-to-have |
| `Must-have`, `Should-have`, `Could-have`, `Won't-have` | MoSCoW mapping → M=G1, S=G2, C=G3 |
| `High`, `Medium`, `Low` | High=G1, Medium=G2, Low=G3 |
| `Critical`, `Major`, `Minor`, `Trivial` | Critical=G1, Major=G2, Minor=G3, Trivial=G3 |
| `Phase 1`, `Phase 2`, `Phase 3` | Phase 1=G1, Phase 2=G2, Phase 3=G3 |
| `Core`, `Standard`, `Advanced` | Core=G1, Standard=G2, Advanced=G3 |

If a feature has **no** priority indicator, assign `UNKNOWN` and flag for user.

### Step 5: Scan for Cost / Effort Estimates

Look for numerical estimates associated with features:

- **Hours** — `40h`, `120 hours`, `~2 weeks`
- **Story points** — `3 SP`, `8 story points`, `SP: 13`
- **Cost** — `$500`, `$2,500 USD`, `Budget: 10k`
- **T-shirt sizes** — `XS`, `S`, `M`, `L`, `XL`
- **Date ranges** — `Jan 15 - Feb 1`, `Q3 2026`
- **Complexity ratings** — `Low`, `Medium`, `High`, `Complex`

Extract as raw values — do not normalize (users understand their own units).

### Step 6: Identify Dependency Relationships

Dependencies connect entities and features. Look for:

- **Explicit dependency mentions:** "depends on", "requires", "needs", "prerequisite"
- **Entity references across modules** — if `Payroll` mentions `Employee`, there's a dependency
- **Implied ordering:** "First we need X before Y" or sequential numbering
- **Data flow:** "X feeds into Y" or "X generates Y"
- **Cross-reference patterns:** `(see Employee)`, `cf. Attendance`, `-> Payroll`
- **Module groupings:** Features grouped under a heading may share dependencies

**Low confidence detection:** Use **textual proximity** — if two entity names appear within 3 sentences of each other repeatedly, flag as a possible implicit dependency.

## Domain Model Extraction

See the template structure in the [Output File](#output-file-domainmd) section below.

### Confidence Scoring

Each extraction dimension gets a confidence score:

| Dimension | High Confidence (90%+) | Medium Confidence (70-89%) | Low Confidence (<70%) |
|-----------|----------------------|---------------------------|-----------------------|
| Entities | Explicit heading, 3+ references | Named once, no clear definition | Inferred from context, not directly named |
| Features | Bullet/numbered list with verb | Sentence with "shall/must" | Implied capability, passive mention |
| Priorities | Explicit label (G1, P1, MoSCoW) | Phase/grouping membership | Inferred from ordering/emphasis |
| Dependencies | "depends on", explicit cross-ref | Shared entity between features | Proximity-based inference |
| Estimates | Numeric with unit | T-shirt size or complexity label | Vague time reference |

**Overall confidence** = weighted average of all dimensions (entities 30%, features 30%, priorities 20%, dependencies 20%).

## Output File: DOMAIN.md

Save the complete extracted model to `DOMAIN.md` at the project root (or a user-specified path):

```
/DOMAIN.md
```

**File structure:**
1. **Header** — source files, extraction date, overall confidence
2. **Modules** — each module with priority, features, dependencies, entities, estimate
3. **Entity Relationship Summary** — basic ER notation of connections found
4. **Priority Distribution** — summary table
5. **Extraction Notes** — all flags, low-confidence items, ambiguities
6. **Raw Data Appendix** — original text snippets mapped to extracted items (for traceability)



## Validation

Before finalizing the output, run validation checks:

### Confidence Check
- [ ] Overall confidence ≥ 70%? → Proceed
- [ ] Overall confidence 50-69%? → Flag uncertain items for user, ask for confirmation
- [ ] Overall confidence < 50%? → Report back to user: "Could not reliably extract domain model. Please structure requirements and try again."

### Consistency Check
- [ ] All features assigned to a module
- [ ] All features have a priority (or UNKNOWN)
- [ ] All module dependencies reference existing modules
- [ ] No circular dependencies without explicit user confirmation
- [ ] Entity names are consistent across modules (no aliases)

### Completeness Check
- [ ] No orphan features (features not in any module)
- [ ] No phantom dependencies (dependencies on non-existent modules)
- [ ] All referenced entities appear in at least one module

### User Presentation

Present findings to user in this compact format:

```
Extraction Results — Source: (3) files | Confidence: 82%
Modules: Employee Mgmt(G1), Attendance(G1), Payroll(G1)
Entities: 9 · Dependencies: 2
⚠ Ambiguous: Employee Reports, Manage users, Dashboard priority
```

## Handoff: DOMAIN.md → dev-craft

Once the user confirms the domain model, the pipeline continues:

```
DOMAIN.md
    │
    ▼
dev-craft — REQUIRE phase
    │ Read DOMAIN.md
    │ Extract requirements from each module/feature
    │ Prioritize based on G1/G3
    │ Build dependency order
    │
    ▼
planning-and-task-breakdown — PLAN phase
    │ Break features into implementable tasks
    │ Size them
    │ Order for vertical slicing
    │
    ▼
[Implementation begins]
```

### Integration Points

| Downstream Skill | What It Receives | How to Invoke |
|------------------|-----------------|---------------|
| `dev-craft` | Extracted modules, features, priorities, entities | Feed DOMAIN.md path to dev-craft REQUIRE phase |
| `planning-and-task-breakdown` | Feature list with dependencies | Pass module feature list for task breakdown |
| `verification-before-completion` | Feature acceptance conditions | Reference features in verification checklist |

## Outputs / Handoffs

On completion, invokes: `skill("planning-and-task-breakdown")` with context:
  - `domainPath`: "DOMAIN.md"
  - `specFiles`: [...] (original input files)

## Guidelines

### Do's
- **Preserve original data** — always include raw text appendix for traceability
- **Mark low-confidence extractions** with `[LOW CONFIDENCE]` or `[INFERRED]` tags
- **Ask for confirmation** before writing the final DOMAIN.md — present and let user adjust
- **Over-extract rather than under-extract** — easier to remove noise than recover missed items
- **Use original terminology** — don't rename entities to match a convention; the user's vocabulary matters
- **Flag duplicates** — if the same feature or entity appears in multiple places, list both occurrences

### Don'ts
- **Don't invent features** — if it's not in the source, don't add it
- **Don't guess priority** — leave as UNKNOWN rather than assuming
- **Don't discard ambiguity** — surface it to the user, don't hide it
- **Don't merge modules without evidence** — keep them separate if unclear
- **Don't overwrite original files** — DOMAIN.md is a derived artifact, source files remain untouched

## Gotchas

### Encoding Issues
- **Excel (.xlsx):** ZIP-based format, use `openpyxl` (handles modern Excel). Older `.xls` files may need `xlrd` or LibreOffice conversion.
- **CSV:** Watch for BOM, delimiter variations (comma vs semicolon), and quoted fields with embedded commas. BOM = `\xef\xbb\xbf` prefix.
- **PDF:** Text extraction quality varies wildly. Tables often come out as garbled text. Prefer source files over PDF when possible.
- **Encoding detection:** Use `chardet` or `cchardet` for non-UTF-8 files. Common traps: ISO-8859-1 (Latin-1), Windows-1252, Shift-JIS.

### Ambiguous Feature Boundaries
- A bullet that says "Employee onboarding with document upload and manager approval" = 1 feature or 3? Conservative approach: treat as 1, flag for user.
- "CRUD operations" in requirements often means 4 features (Create, Read, Update, Delete). Only split if the source differentiates them.

### Hidden Dependencies
- **Implicit data flows:** Not written down, but deducible. Example: "Generate pay slip" depends on "Calculate salary" which depends on "Mark attendance."
- **External dependencies:** System may depend on third-party services (SMS, email, payment gateways) that aren't listed as modules.
- **Political dependencies:** "Module X must launch first" may be a business dependency not in the technical spec.

### Priority Inconsistency
- Same priority label may mean different things across documents. A "High" from one stakeholder might be a "Medium" for another. Note the source for each priority.
- Some features will have no explicit priority but are described enthusiastically (lots of detail, positive language) — this often indicates high priority.

### Document Staleness
- Check dates on source files. Requirements from 6+ months ago may be outdated. Flag if source age exceeds 3 months.
- Mismatched version numbers across documents (e.g., "spec-v2" contradicts "spec-v3") — flag for user to reconcile.

### Parsing Edge Cases
- **Tables in markdown:** Multi-line cell content can break naive parsers. Use a proper MD parser (e.g., `python-markdown` with table extension).
- **Excel merged cells:** Can cause empty rows/columns in parsed output. Detect and skip.
- **Track changes / comments in documents:** Can insert spurious text. Flag if detected.
- **Image-based PDFs:** Cannot extract text. Inform user: "PDF appears to contain scanned images — no text could be extracted. Please provide text-based source."


## Appendix B: JSON Model Schema

See `references/domain-model-schema.json`
