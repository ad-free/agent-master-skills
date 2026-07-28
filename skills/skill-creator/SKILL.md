---
name: skill-creator
description: Create new skills, modify and improve existing skills for the agent-master-skills library. Use when the user wants to create a skill from scratch, edit or optimize an existing skill, or add a plugin. Follows the skill-composer integration pattern for dependency-aware loading.
model: deepseek-v4-flash-free
version: 1.0.0
preamble-tier: 2
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "create skill"
  - "modify skill"
  - "new skill"
  - "edit skill"
  - "skill template"
disable-model-invocation: true
preferred-model: deepseek-v4-flash-free
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Skill Creator

A skill for creating agent-master-skills and keeping them healthy. Each skill lives in `skills/<name>/` with a `SKILL.md` as the core instruction file.

## Structure

Every skill follows this structure:

```
skills/<name>/
  SKILL.md              — Core instructions (YAML front-matter + markdown body)
  references/           — Reference docs loaded into context as needed
  scripts/              — Executable scripts (called, not read into context)
  assets/               — Files used in output (templates, icons, fonts)
  plugins/              — Optional sub-skills loaded on demand
```

## Creating a Skill

### 1. Understand Intent

Determine from the user's request:
- What should the skill enable the agent to do?
- When should it trigger?
- What skills does it complement or depend on?
- Should it be a standalone skill or a plugin under an existing skill?

Check `skills/SHARED.md` for the skill router table — every new skill needs a row there.

### 2. Create the Directory

```
skills/<skill-name>/
  references/           — Optional
  scripts/              — Optional
  assets/               — Optional
  plugins/              — Optional
```

### 3. Write SKILL.md

Every SKILL.md starts with YAML front-matter:

```yaml
---
name: skill-name
description: Use when [specific task context]. [What it does and when to trigger].
metadata:
  origin: agent-master-skills
---
```

The description is the primary trigger mechanism — include both what the skill does AND when to use it. If it's a plugin, add `plugin-for: <parent-skill>` and `phase: <phase-name>`.

### 4. Body Guidelines

- **Under 500 lines** — if approaching this limit, extract content into `references/` files with clear pointers about when to read them
- **Progressive disclosure** — reference files are loaded on demand; keep the main body focused on the workflow
- **Imperative tone** — say what to do, not what to think about
- **Explain why** — explain reasoning behind instructions so the agent can generalize beyond rote rules
- **Avoid heavy-handed MUSTs** — prefer explaining consequences over ALL CAPS rules
- **Prefer extracting** — inline templates → `references/`, inline scripts → `scripts/`

### 5. Register in Router

Update `skills/SHARED.md` to add the new skill to the router table. Also update `README.md` if the skill is publicly notable.

### 6. Test

Create 2-3 realistic test prompts and run the skill against them. Check:
- Does it trigger correctly?
- Do the instructions produce correct output?
- Are there gaps or contradictions?

## Modifying a Skill

1. Read the current SKILL.md and understand its structure
2. Read `skills/SHARED.md` for the router context
3. Apply changes — prefer minimal edits over rewrites
4. Update README.md and SHARED.md if the skill's name, description, or router entry changes
5. Run the eval harness if available: `uv run python skills/eval-harness/scripts/run.py`

## Optimizing Skills for Token Efficiency

When asked to reduce token cost:

1. **Extract inline content** — move templates to `references/`, scripts to `scripts/`
2. **Remove duplication** — checklists that mirror exit criteria, repeated integration flows
3. **Shorten descriptions** — cut fluff, keep only actionable instructions
4. **Merge overlapping sections** — consolidation over fragmentation
5. **Trim examples** — one example beats three
6. **Use progressive disclosure** — reference files only when needed

## Plugins

For optional capabilities that extend a skill:

```
skills/<parent>/plugins/<plugin-name>/
  SKILL.md
```

Add `plugin-for` and `phase` to the plugin's front-matter. Register in the parent skill's text with a pointer.

## Reference

- `skills/SHARED.md` — Skill router, shared terminology, handoff schema
- `skills/PLUGIN-SYSTEM.md` — Plugin architecture and conventions
- `README.md` — Repo-level documentation

## Verification

Before finishing:
- [ ] SKILL.md has valid front-matter
- [ ] Directory structure matches conventions
- [ ] Router updated in SHARED.md
- [ ] README.md updated if needed
- [ ] No broken symlinks in `~/.config/opencode/skills/`
