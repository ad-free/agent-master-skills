# Tasks: Spec Kit Workflow Adoption

**Input**: Design documents from `specs/001-spec-kit-workflow-adoption/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`

## Phase 1: Setup

**Purpose**: Install the CLI and prepare this repository's project-scoped integrations.

- [x] T001 Install `specify-cli` with `uv tool install specify-cli`; verify with `specify version`.
- [x] T002 Initialize the OpenCode, Claude Code, and Oh My Pi integrations; verify manifests under `.specify/integrations/`.
- [x] T003 Establish project principles in `.specify/memory/constitution.md` and create the feature artifacts under `specs/001-spec-kit-workflow-adoption/`.

---

## Phase 2: Foundational

**Purpose**: Lock down the shared policy and platform-specific loading path before relying on the workflow.

- [x] T004 Add the complete Spec Kit routing policy, project-initialization gate, and lightweight-task exceptions to `/home/adfree/.config/opencode/AGENTS.md`.
- [x] T005 Replace the duplicated policy in `/home/adfree/.claude/AGENTS.md` with an import of the canonical global policy.
- [x] T006 Add an Oh My Pi global pointer in `/home/adfree/.omp/agent/AGENTS.md` without copying the shared policy.

---

## Phase 3: User Story 1 - Follow a reviewed feature workflow (Priority: P1)

**Goal**: Require Spec Kit's full, reviewed feature lifecycle when a project is configured for substantial feature work.

**Independent Test**: The global policy states the command stages, artifact review, no implementation before tasks and analysis, and repeated convergence.

- [x] T007 [US1] Verify the policy in `/home/adfree/.config/opencode/AGENTS.md` requires the reviewed Spec Kit lifecycle before feature implementation.

---

## Phase 4: User Story 2 - Keep routine fixes lightweight (Priority: P2)

**Goal**: Preserve the existing root-cause bug workflow and avoid unnecessary feature specs for routine work.

**Independent Test**: The global policy distinguishes substantial features from small fixes and routes bugs to the existing debugging workflow.

- [x] T008 [US2] Verify the policy in `/home/adfree/.config/opencode/AGENTS.md` requires setup approval for uninitialized projects and keeps routine fixes lightweight.

---

## Phase 5: User Story 3 - Use one workflow across supported agents (Priority: P1)

**Goal**: Ensure OpenCode, Oh My Pi, and Claude Code can access the same project artifacts and aligned global instructions.

**Independent Test**: Each project integration is healthy, and each agent's global policy path reaches the same canonical Spec Kit guidance.

- [x] T009 [P] [US3] Verify generated OpenCode commands in `.opencode/commands/` and confirm OpenCode is the default integration in `.specify/integration.json`.
- [x] T010 [P] [US3] Verify generated Oh My Pi commands in `.omp/commands/` and confirm its manifest in `.specify/integrations/omp.manifest.json`.
- [x] T011 [P] [US3] Verify generated Claude Code skills in `.claude/skills/` and confirm its manifest in `.specify/integrations/claude.manifest.json`.
- [x] T012 [US3] Run `specify integration status --json` and verify all three integrations have no missing, modified, or invalid managed files.
- [x] T013 [US3] Check global policy import paths and review `specs/001-spec-kit-workflow-adoption/quickstart.md` against actual agent command syntax.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate artifact coverage and inspect the final changes.

- [x] T014 Review requirement coverage and task dependencies across `specs/001-spec-kit-workflow-adoption/spec.md`, `plan.md`, and `tasks.md`.
- [x] T015 Review the complete working-tree diff for unintended files or overwrites.

---

## Dependencies & Execution Order

- Setup (T001-T003) is complete.
- Foundational global policy tasks (T004-T006) precede cross-agent routing verification.
- T007 and T008 depend on T004 because they refine the same canonical policy file.
- T009-T011 are independent integration checks; T012-T013 follow the policy and integration setup.
- T014-T015 are final review gates.

## Parallel Opportunities

- T009, T010, and T011 inspect distinct integration paths and can be verified independently.
- Global policy edits remain sequential because they update the same canonical file.
