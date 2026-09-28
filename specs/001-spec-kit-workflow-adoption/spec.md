# Feature Specification: Spec Kit Workflow Adoption

**Feature Branch**: `chore/adopt-spec-kit`

**Created**: 2026-09-28

**Status**: Complete

**Input**: User description: "Please install spec kit and update AGENTS.md global for both opencode/omp/claude. Make sure you're using correctly and strong of spec kit instead of implementing everything."

## User Scenarios & Testing

### User Story 1 - Follow a reviewed feature workflow (Priority: P1)

When a maintainer requests a substantial feature in a project configured for Spec Kit, the coding agent guides the work from user requirements through an implementation plan and ordered tasks before changing product code, then checks the result against the requirements.

**Why this priority**: The user's primary goal is to prevent the agent from jumping directly from a feature prompt into implementation and to retain a durable record of intent.

**Independent Test**: In a Spec Kit-enabled project, present a multi-step feature request and verify that specification, planning, task generation, and consistency analysis precede implementation, followed by convergence.

**Acceptance Scenarios**:

1. **Given** a substantial feature request in an initialized project, **When** an agent begins work, **Then** it creates or updates the feature artifacts and analyzes them before implementation.
2. **Given** implementation tasks exist, **When** the agent works on the feature, **Then** it implements against those tasks and repeats convergence until the specification is satisfied.

### User Story 2 - Keep routine fixes lightweight (Priority: P2)

A maintainer asks for a small, well-understood fix or routine maintenance change and the agent uses the established targeted workflow without creating an unnecessary feature specification.

**Why this priority**: Spec Kit should prevent premature implementation on substantial work without turning every maintenance action into ceremony.

**Independent Test**: Give an agent a narrowly scoped bug report and verify that it reproduces or establishes the failure, fixes the root cause, and runs relevant verification without generating SDD artifacts.

**Acceptance Scenarios**:

1. **Given** a small bug or maintenance request, **When** an agent begins work, **Then** it follows the repository's debugging and verification rules without starting the full SDD workflow.

### User Story 3 - Use the same project workflow across supported agents (Priority: P1)

A maintainer switches among OpenCode, Oh My Pi, and Claude Code in the configured project and can invoke the same Spec Kit process with each agent's native command syntax.

**Why this priority**: The requested setup spans three coding agents and should not require three divergent sets of process instructions.

**Independent Test**: Check each integration's managed status and confirm each target has the installed Spec Kit commands while sharing one project-level set of feature artifacts.

**Acceptance Scenarios**:

1. **Given** the repository is opened with any of the three supported agents, **When** the maintainer requests a substantial feature, **Then** the agent can discover the Spec Kit workflow and the same active feature artifacts.
2. **Given** a future project does not have Spec Kit initialized, **When** a substantial feature is requested, **Then** the agent explains that setup is needed and asks before adding project files; it does not start implementation unless the user approves setup or explicitly waives Spec Kit.

### Edge Cases

- A project is not initialized for Spec Kit or lacks the relevant agent integration.
- An existing repository has local or uncommitted files at paths Spec Kit manages.
- A request is small or is a bug fix rather than a new feature.
- More than one agent integration is installed; all must resolve to the same project feature state.
- The current feature artifacts conflict with project policy or existing behavior; resolve the conflict in the artifacts before implementation.

## Requirements

### Functional Requirements

- **FR-001**: The user's environment MUST provide the `specify` CLI for initializing and managing Spec Kit projects.
- **FR-002**: This repository MUST expose Spec Kit's core SDD commands to OpenCode, Oh My Pi, and Claude Code without maintaining separate copies of feature artifacts.
- **FR-003**: The shared global agent policy MUST make Spec Kit the default workflow for substantial feature work when the project is initialized.
- **FR-004**: Before implementing a substantial feature, agents MUST review the specification, resolve consequential ambiguity, create a plan and ordered tasks, and analyze the artifacts for consistency.
- **FR-005**: During feature implementation, agents MUST follow the approved tasks, preserve existing project architecture and conventions, and converge against the specification before claiming completion.
- **FR-006**: Agents MUST NOT force the full SDD workflow on small maintenance changes or targeted bug fixes; they MUST use the repository's established debugging, verification, and safety policies for those tasks.
- **FR-007**: When a substantial feature is requested in a project without Spec Kit, agents MUST explain that project setup is needed and ask before adding files; they MUST NOT start implementation unless the user approves setup or explicitly waives Spec Kit.
- **FR-008**: Project initialization and integration changes MUST preserve existing user work, and generated managed-file changes MUST be reviewable.
- **FR-009**: Spec Kit MUST complement, not replace, fresh tests, security checks, code review, and other applicable repository gates.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `specify version` completes successfully and reports the installed CLI version.
- **SC-002**: `specify integration status --json` reports `status: ok` with OpenCode, Oh My Pi, and Claude Code installed, no missing or modified managed files, and no invalid manifest paths.
- **SC-003**: Each target integration exposes the same core Spec Kit SDD commands for this repository.
- **SC-004**: A substantial feature workflow requires reviewed spec, plan, tasks, and analysis artifacts before implementation, then convergence and normal repository verification.
- **SC-005**: A small fix can use the existing lightweight workflow without producing Spec Kit feature artifacts.
- **SC-006**: Global policy is available to OpenCode, OMP, and Claude Code through a single shared policy source, without three divergent copies.

## Assumptions

- This repository is the first configured project and will serve as the integration pilot.
- The OpenCode global `AGENTS.md` is the canonical cross-agent policy. OMP also loads it through its OpenCode compatibility instructions provider, and Claude Code's global instruction wrapper imports its own `AGENTS.md`.
- Spec Kit CLI installation is user-level; agent commands and project artifacts are initialized per repository.
- Future project setup must respect existing files and user work; no automatic force-overwrite is allowed.
- Spec Kit's optional bug-fixing and idea-assessment extensions are not required for this installation because existing debugging and product-discovery workflows already cover those needs.

## Out of Scope

- Replacing existing engineering, debugging, testing, security, or release skills.
- Installing optional Spec Kit extensions or presets.
- Automatically initializing every future repository without checking its state and managed paths.
- Committing, pushing, or opening a pull request.
