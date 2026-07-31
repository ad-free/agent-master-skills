---
name: refactor-and-cleanup
description: |
  Systematic code refactoring and cleanup — dead code removal, duplication
  elimination, naming improvements, complexity reduction, and dependency
  cleanup. Use when the codebase has accumulated technical debt, after a
  feature is merged, or as part of a structured cleanup sprint. Do NOT use
  for adding new features (see dev-craft) or for security fixes (see
  bug-hunting).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "refactor code"
  - "clean up code"
  - "remove dead code"
  - "eliminate duplication"
  - "code cleanup"
  - "technical debt"
  - "rename for clarity"
  - "reduce complexity"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, testing-strategies]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# refactor-and-cleanup

## Relationship to existing skills

- dev-craft: Provides the overall engineering pipeline; refactor-and-cleanup is invoked during the REFACTOR phase or as a standalone cleanup task.
- code-review-and-quality: Validates refactoring quality; refactor-and-cleanup produces the changes that code-review-and-quality then reviews.
- bug-hunting: Identifies code smells and anti-patterns that should be cleaned up; refactor-and-cleanup executes the fixes.
- dev-craft/plugins/performance-profiling: Performance-related refactoring (e.g., N+1 query elimination) falls under this skill.

## When to Use

- Removing dead code, unused imports, unused variables, and unreachable branches
- Eliminating duplicated code through extraction of shared functions or utilities
- Improving naming clarity (rename vague identifiers to descriptive ones)
- Reducing cyclomatic complexity in functions that exceed a threshold
- Cleaning up dependency imports (remove unused, resolve circular imports)
- Standardizing code style and patterns across a module
- Preparing code for a feature addition by reducing coupling

## When NOT to Use

- Adding new features or functionality — see dev-craft
- Fixing security vulnerabilities — see bug-hunting
- Optimizing performance-critical paths — see dev-craft/plugins/performance-profiling
- Restructuring module boundaries — see backend-patterns
- Fixing bugs in existing behavior — see debugging-and-error-recovery

## Workflow

### Phase 1: Analysis

1. **Identify the scope**: which files, modules, or directories are targeted
2. **Run static analysis**: use linter and typechecker output to find issues
3. **Detect dead code**: find unused functions, classes, variables, imports, and branches
4. **Detect duplication**: find copy-pasted blocks or near-duplicated logic
5. **Measure complexity**: identify functions with high cyclomatic complexity (>10) or cognitive complexity
6. **Prioritize findings**:
   - `P0`: dead code that could cause confusion or import cycles
   - `P1`: duplicated code in hot paths or core logic
   - `P2`: naming that obscures intent
   - `P3`: cosmetic cleanup (import ordering, whitespace)

### Phase 2: Planning

1. **Create a refactoring plan**: list each change with its priority, location, and expected impact
2. **Group related changes**: batch changes in the same file or module together
3. **Define safety boundaries**: identify tests that cover the areas being changed
4. **Get user confirmation** on the plan before executing

### Phase 3: Execution

Execute changes in priority order, one group at a time:

1. **Dead code removal**: delete unused functions, imports, variables, and branches
2. **Duplication elimination**: extract shared logic into reusable functions or utilities
3. **Rename for clarity**: rename identifiers to be self-documenting
4. **Complexity reduction**: extract helper functions, simplify conditionals, remove nesting
5. **Import cleanup**: remove unused imports, resolve circular imports, sort imports
6. **After each group**: run the relevant tests to verify no behavior changed

### Phase 4: Verification

1. **Run full test suite**: all tests must pass
2. **Run linter and typechecker**: no new warnings or errors introduced
3. **Diff review**: review the complete diff to ensure only intended changes were made
4. **Check for regressions**: specifically test the areas around changed code
5. **Update documentation**: if function signatures or public APIs changed, update docs

## Context Management

- Track refactoring state in `.dev-craft/refactor/<project>/state.json` with fields: `session_id`, `changes_made`, `tests_passed`, `pending_groups`
- On session resume, check state.json for any in-progress refactoring and continue from the last completed group

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read source files before editing | Only read files in the target scope |
| Write | Create new utility or shared modules | Follow existing module conventions |
| Edit | Make targeted refactoring changes | One change at a time; verify tests after each edit |
| Bash | Run tests, linter, typechecker | Must run tests after each group of changes |
| Grep | Find duplicated code patterns, unused references | Search within the target scope |
| Glob | Find files in the target scope | Pattern: `<module>/**/*.py` (or relevant extension) |
| Task | Spawn subagent for large-scale dead code detection | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. A diff of all changes made, grouped by priority
2. Test results confirming no regressions
3. A summary of what was removed, extracted, renamed, and simplified
4. Updated state.json with the refactoring session results
5. Any new utility or shared modules created

## Quality Gates

- [ ] All tests pass after refactoring
- [ ] Linter and typechecker pass with no new warnings
- [ ] No behavior changes — only structural improvements
- [ ] Dead code removal does not remove code that is used dynamically (e.g., via reflection or string references)
- [ ] Duplication extraction preserves existing behavior
- [ ] Rename does not break any external API or public interface
- [ ] Diff contains only intended changes

## Error Handling

- **Test failure after a change**: revert that specific change, investigate, and fix before proceeding
- **Linter/typechecker error introduced**: revert the offending change, fix the issue, and re-run
- **Dead code is actually used dynamically**: do not remove it; flag it for manual review
- **Duplication extraction introduces a bug**: revert the extraction, re-examine the original code, and try a different extraction approach
- **User interrupts mid-refactoring**: save state to state.json, report what was completed and what remains