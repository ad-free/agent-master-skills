# Quickstart: Verify Spec Kit Adoption

## Prerequisites

- Run commands from the repository root.
- `specify`, OpenCode, Oh My Pi, and Claude Code are available.
- A substantial feature is active in `specs/` and recorded by
  `.specify/feature.json`.

## Verify the installation

```sh
specify version
specify integration status --json
```

Expected: CLI version is reported; status is `ok`; installed integrations include
`opencode`, `claude`, and `omp`; each manifest has no missing, modified, or invalid
managed files.

## Exercise the feature workflow

Follow these steps one at a time, reviewing each artifact before continuing:

1. Run the constitution command once, deriving principles from existing repository
   rules rather than inventing standards.
2. Start one bounded feature with the specify command.
3. Clarify consequential ambiguity when needed.
4. Create the plan, validate requirements with the checklist, generate tasks, then
   analyze cross-artifact consistency.
5. Resolve critical artifact conflicts before implementation.
6. Implement from the task list and converge; repeat until convergence reports
   `Converged`.
7. Run the repository's directly relevant tests and review/security gates.

For routine maintenance or a narrow bug fix, use the normal project workflow and
do not create a Spec Kit feature merely to satisfy process.

## Integration invocation

- **OpenCode**: `/speckit.constitution`, `/speckit.specify`, `/speckit.clarify`,
  `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, `/speckit.implement`,
  `/speckit.converge` from `.opencode/commands/`.
- **Oh My Pi**: the same dotted command form from `.omp/commands/`.
- **Claude Code**: hyphenated skills such as `/speckit-constitution` and
  `/speckit-specify` from `.claude/skills/`.

Use the invocation form exposed by the active agent. Project feature state is stored
in `.specify/feature.json`, not inferred from the checked-out Git branch.
