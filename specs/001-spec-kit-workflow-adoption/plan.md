# Implementation Plan: Spec Kit Workflow Adoption

**Branch**: `chore/adopt-spec-kit` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-spec-kit-workflow-adoption/spec.md`

## Summary

Install the Specify CLI for the user, enable Spec Kit's core SDD commands in this
repository for OpenCode, Oh My Pi, and Claude Code, and make the OpenCode global
`AGENTS.md` the shared cross-agent policy source. Route substantial feature work
through reviewed Spec Kit artifacts before implementation; retain lightweight
debugging and verification paths for small fixes.

## Technical Context

<!--
  Configuration-only workflow change: there is no application source stack.
  Details below describe the installed CLI, integration targets, and verification.
-->

**Language/Version**: Markdown and Bash; Python 3.13.15; Specify CLI 1.0.12

**Primary Dependencies**: `specify-cli`, installed with the existing `uv` tool

**Storage**: Versioned Markdown/JSON in this repository; user-level agent policy in
the home configuration directories

**Testing**: `specify version`, `specify integration status --json`, integration
manifest checks, and static checks of global instruction imports

**Target Platform**: Linux; OpenCode, Oh My Pi, and Claude Code

**Project Type**: Agent workflow and configuration repository

**Performance Goals**: No runtime performance change; keep global instructions concise

**Constraints**: Preserve existing project/user files, use one canonical global policy,
use one feature artifact set, and check other repositories before initializing them

**Scale/Scope**: Three integrations in this repository and one shared global policy

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- User intent and current truth: PASS — all three integrations and global policy are
  explicit user requirements; installation and runtime paths were inspected.
- Specify before substantial implementation: PASS — this work has a reviewed
  specification before global policy edits.
- Reuse and minimize: PASS — use the existing cross-agent policy and Spec Kit's
  generated integration files; avoid copying workflow instructions three times.
- Safety and existing contracts: PASS — the worktree is clean on a feature branch;
  preserve global and project files.
- Evidence before completion: PASS — use the CLI's JSON integration status plus
  path/content checks and review the final diff.

## Project Structure

### Documentation (this feature)

```text
specs/001-spec-kit-workflow-adoption/
├── spec.md
├── plan.md
├── research.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)
<!--
  Configuration-only work: concrete repository and user-level paths are listed below.
-->

```text
.specify/
├── memory/constitution.md
├── integrations/{opencode,claude,omp}.manifest.json
└── scripts/bash/ and templates/
.opencode/commands/speckit.*.md
.omp/commands/speckit.*.md
.claude/skills/speckit-*/SKILL.md

User-level configuration (outside this repository):
~/.config/opencode/AGENTS.md       # canonical shared policy
~/.claude/AGENTS.md                # imports canonical shared policy
~/.claude/CLAUDE.md                # existing wrapper imports ~/.claude/AGENTS.md
~/.omp/agent/AGENTS.md             # OMP-only pointer; no duplicate policy
```

**Structure Decision**: Use Spec Kit's project-managed `.specify` infrastructure
and agent-specific generated integrations. Keep shared global guidance in the
existing OpenCode global policy; Claude imports it, and OMP's OpenCode compatibility
provider already loads it. Keep OMP-specific instructions limited to a pointer.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations.
