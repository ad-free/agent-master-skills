<!--
Sync Impact Report
- Version change: unratified scaffold → 1.0.0 (initial ratification)
- Added principles: user/repository truth, specification-first feature work, minimal design, safety, evidence
- Added sections: Scope and Constraints; Development Workflow and Quality Gates
- Removed sections: none
- Follow-up TODOs: none
-->

# Agent Master Skills Constitution

## Core Principles

### I. User Intent and Current Truth
The user's current request defines the goal. Verify behavior against current source,
tests, configuration, and project documentation; historical context never overrides
current evidence.

### II. Specify Before Substantial Feature Implementation
For substantial or ambiguous feature work, use the project's Spec Kit workflow:
specify requirements, resolve consequential ambiguity, plan, create tasks, analyze
artifact consistency, implement against approved tasks, and converge against the spec.
Do not impose this ceremony on routine maintenance or small, well-scoped fixes.

### III. Reuse and Minimize
Inspect existing patterns and reuse suitable helpers, types, and workflows before
adding new ones. Make the smallest correct change; avoid speculative abstractions,
duplicate sources of truth, and unnecessary dependencies.

### IV. Preserve Safety and Existing Contracts
Preserve established public interfaces and repository policies unless the user
explicitly requests a change. Validate inputs at trust boundaries, protect user work,
and do not perform commits, pushes, deployments, or destructive actions without
explicit authorization.

### V. Evidence Before Completion
Verify the changed behavior with the smallest relevant fresh checks, review the final
diff, and report only checks actually performed. Spec Kit convergence complements but
does not replace tests, security review, or repository quality gates.

## Scope and Constraints

Spec Kit artifacts define feature intent and implementation plans; they do not replace
the repository's `AGENTS.md`, system instructions, or the user's authority over scope.
Use one authoritative plan/task source per feature. Existing-project behavior is
preserved unless the spec explicitly changes it. A missing Spec Kit installation is
not permission to silently skip planning for substantial work.

## Development Workflow and Quality Gates

For substantial feature work, follow the Spec Kit stages one at a time and review each
artifact before proceeding. Run clarification when needed, requirements checklists
when useful, and consistency analysis before implementation. Implement in reviewable
slices; repeat implementation and convergence until the feature is complete. For bugs,
follow the repository's root-cause and regression-verification workflow rather than
forcing a feature-spec workflow. Routine edits use task-scoped checks.

## Governance

System and platform instructions and the user's current request take precedence over
this constitution; repository `AGENTS.md` governs operating and safety rules. Amend
this constitution only with an explicit rationale and review of affected artifacts.
Use semantic versioning: patch for clarifications, minor for added principles or
material guidance, major for removals or incompatible changes. Recheck alignment
during Spec Kit analysis and code review.

**Version**: 1.0.0 | **Ratified**: 2026-09-28 | **Last Amended**: 2026-09-28
