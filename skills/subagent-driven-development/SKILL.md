---
name: subagent-driven-development
description: |
  Coordinate multiple sub-agents working in parallel on different parts of a
  feature, each operating in an isolated worktree with a shared contract.
  Use for large features that can be decomposed into independent work streams.
  Do NOT use for single-agent work (see dev-craft) or for simple parallel
  task execution without worktree isolation (see dispatching-parallel-agents).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Agent
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "subagent driven development"
  - "parallel feature work"
  - "multi-agent feature"
  - "worktree feature development"
  - "coordinate subagents"
  - "parallel implementation"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: planning-execution
  integrates-with: [agent-orchestration, dev-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# subagent-driven-development

## Relationship to existing skills

- agent-orchestration: Provides the git worktree and API contract framework; subagent-driven-development applies it specifically for feature development with sub-agents.
- dispatching-parallel-agents: Handles simple parallel task dispatch; subagent-driven-development adds worktree isolation, shared contracts, and merge coordination.
- dev-craft: Provides the engineering pipeline; subagent-driven-development is invoked when a feature requires parallel sub-agent execution within dev-craft.
- verification-before-completion: Validates each sub-agent's work before merge; this skill delegates verification to the sub-agents and the orchestrator.

## When to Use

- A feature can be decomposed into 2+ independent work streams (e.g., backend + frontend, API + worker, multiple independent modules)
- Each work stream can be implemented in isolation without blocking the others
- A shared contract (API interface, data schema, or event contract) defines how the work streams interact
- Worktree isolation is needed to avoid conflicts between parallel implementations
- The feature is large enough that parallel execution saves meaningful time

## When NOT to Use

- A single, linear feature that one agent can complete — see dev-craft
- Simple parallel execution without worktree isolation — see dispatching-parallel-agents
- Work streams that are tightly coupled and must be developed together — see agent-orchestration for coordinated parallel work
- Tasks that do not benefit from parallelism (e.g., quick fixes, documentation)

## Workflow

### Phase 1: Feature Decomposition

1. **Define the feature scope**: what is the end goal, and what are the acceptance criteria?
2. **Identify independent work streams**: break the feature into 2+ parts that can be developed in parallel
3. **Define the shared contract**: what interfaces, data schemas, or events will the work streams exchange?
4. **Assign ownership**: which sub-agent handles which work stream?
5. **Define dependencies**: which work streams depend on others, and in what order must they be integrated?
6. **Create a plan document**: write the decomposition to `.dev-craft/runs/<slug>/plan.md`

### Phase 2: Worktree Creation

1. **Create a base branch** from the current main/develop branch
2. **Create worktrees** for each sub-agent:
   - `git worktree add ../worktrees/<agent-name> <branch-name>`
   - Each worktree gets its own branch: `feature/<slug>/<agent-name>`
3. **Share the contract**: copy the shared contract file to each worktree
4. **Assign sub-agents**: launch each sub-agent into its worktree with the contract and acceptance criteria

### Phase 3: Parallel Execution

1. **Launch sub-agents in parallel**: each sub-agent works in its own worktree
2. **Sub-agent responsibilities**:
   - Implement the assigned work stream
   - Follow the shared contract exactly
   - Run tests within the worktree
   - Report completion status and any contract violations
3. **Orchestrator monitors**: check worktree status periodically, resolve conflicts if branches diverge too far
4. **Contract enforcement**: if a sub-agent's implementation violates the shared contract, halt that agent and negotiate a contract update

### Phase 4: Integration

1. **Merge worktrees**: merge each sub-agent branch into the base feature branch in order of dependency
2. **Resolve conflicts**: if merge conflicts arise, resolve them against the shared contract
3. **Run integration tests**: verify that all work streams work together
4. **Run full test suite**: all tests must pass across the integrated codebase
5. **Verify contract compliance**: ensure all sub-agent implementations adhere to the shared contract

### Phase 5: Verification

1. **Run verification-before-completion** on the integrated feature
2. **Run quality gates**: lint, typecheck, test, security scan
3. **Review the complete diff**: ensure all work streams are correctly integrated
4. **Clean up worktrees**: remove worktree directories after successful merge
5. **Update state**: mark the run as complete in `.dev-craft/runs/<slug>/state.json`

## Context Management

- Feature plan persisted in `.dev-craft/runs/<slug>/plan.md`
- Shared contract persisted in `.dev-craft/runs/<slug>/contract.md`
- Sub-agent results persisted in `.dev-craft/runs/<slug>/results/<agent-name>.json`
- Worktree branches tracked in `.dev-craft/runs/<slug>/worktrees.json`
- On session resume, check for existing run state and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Agent | Launch sub-agents into worktrees | Each sub-agent gets a scoped prompt with the contract and acceptance criteria |
| Bash | Create worktrees, merge branches, run tests | Must use `--dry-run` for merges first; never force-push to shared branches |
| Read | Read contract, plan, and sub-agent results | Only read from `.dev-craft/runs/<slug>/` and worktree directories |
| Write | Create plan, contract, and result files | Follow the naming conventions above |
| Edit | Update plan or contract during execution | Only edit before Phase 3; changes during execution require user confirmation |
| Grep | Search for contract violations in sub-agent output | Search within worktree directories |
| Glob | Find worktree branches and files | Pattern: `.dev-craft/runs/<slug>/**/*` |

## Output Contract

On completion, the skill must produce:

1. A merged feature branch with all sub-agent work integrated
2. A run summary in `.dev-craft/runs/<slug>/summary.md` including: work streams completed, conflicts resolved, test results, contract compliance status
3. Cleaned-up worktrees (removed after successful merge)
4. Updated run state.json with completion status and all sub-agent results
5. A verification report from verification-before-completion

## Quality Gates

- [ ] Shared contract is defined and agreed upon before any sub-agent starts
- [ ] Each sub-agent's work passes its own tests within the worktree
- [ ] All work streams integrate without contract violations
- [ ] Full test suite passes after integration
- [ ] Lint and typecheck pass after integration
- [ ] No worktrees left orphaned after completion
- [ ] Run summary documents all decisions, conflicts, and resolutions

## Error Handling

- **Sub-agent fails or times out**: halt that work stream, assess impact on dependent streams, and decide whether to retry or reassign
- **Contract violation detected**: halt the violating sub-agent, negotiate a contract update with the user, and restart that stream
- **Merge conflict that cannot be resolved automatically**: pause integration, present the conflict to the user with context, and resolve together
- **Worktree branch diverges significantly from contract**: rebase the branch onto the latest contract, re-run tests, and verify compliance
- **Integration test failure**: identify which work stream caused the failure, revert that merge, fix the issue, and retry