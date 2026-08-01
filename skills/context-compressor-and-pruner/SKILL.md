---
name: context-compressor-and-pruner
description: |
  Manage long-horizon agent state, summarize context windows,
  and prune stale context without losing operational memory.
  Use when agent context is approaching token limits, when resuming
  long-running sessions, or when managing multi-session context.
  Do NOT use for general context setup (see context-engineering)
  or for agent routing (see agent-router).
  
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
  - "compress context"
  - "prune context"
  - "context window full"
  - "summarize conversation"
  - "context management"
  - "long-running session"
  - "context rotation"
  - "state pruning"
  - "token budget"
  - "context overflow"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: context-memory
  integrates-with: [context-engineering, agent-orchestration]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# context-compressor-and-pruner

## Relationship to existing skills

- context-engineering: Provides the context management framework (setup, memory hierarchy, session continuity); context-compressor-and-pruner handles the compression and pruning operations within that framework.
- agent-orchestration: Manages multi-agent context; context-compressor-and-pruner ensures each agent's context stays within token limits.
- dev-craft: Provides the engineering pipeline; context-compressor-and-pruner is invoked when context grows too large during a dev-craft session.
- dispatching-parallel-agents: Dispatches parallel tasks; context-compressor-and-pruner ensures each dispatched agent has a clean, compressed context.

## When to Use

- Agent context is approaching token limits
- Resuming a long-running session with accumulated context
- Managing context across multiple sessions or agents
- Pruning stale or irrelevant context from a conversation
- Summarizing a large conversation for handoff
- Rotating context to maintain operational memory
- Preparing context for a new agent or sub-agent

## When NOT to Use

- Setting up initial context for a new session — see context-engineering
- Routing requests to the right agent — see agent-router
- General conversation management — see context-engineering
- Adding new context or memories — see context-engineering

## Workflow

### Phase 1: Context Assessment

1. **Measure the current context size**: estimate the token count of the current conversation and state
2. **Identify the token budget**: what is the maximum allowed context size?
3. **Determine the overflow severity**: approaching limit, at limit, or over limit
4. **Identify the context sources**: what contributes to the context size? (conversation history, state files, reference documents, tool outputs)
5. **Classify context items by importance**:
   - `critical`: current task, active state, recent decisions
   - `important`: relevant history, key findings, important context
   - `moderate`: older context that may be relevant
   - `stale`: outdated context that can be pruned
   - `irrelevant`: context that is no longer relevant

### Phase 2: Compression

1. **Summarize conversation history**: compress older messages into concise summaries that preserve key facts and decisions
2. **Compress tool outputs**: replace large tool outputs with summaries that capture the essential information
3. **Compress reference documents**: extract key points from large reference files and replace the full content with summaries
4. **Use structured summaries**: follow a consistent format for summaries (key facts, decisions, open questions, next steps)
5. **Preserve operational memory**: ensure that critical state, active decisions, and ongoing tasks are not lost during compression
6. **Apply token budget allocation**: reserve a portion of the token budget for the current task and use the rest for compressed context

### Phase 3: Pruning

1. **Remove stale context**: delete context items that are no longer relevant to the current task
2. **Remove duplicate context**: consolidate redundant information
3. **Remove low-importance context**: remove context items classified as `moderate` or `stale` that are not needed for the current task
4. **Archive pruned context**: save pruned context to a state file for potential future reference
5. **Verify no critical information was lost**: check that all critical and important context is preserved

### Phase 4: State Rotation

1. **Rotate active state**: move the current task state to a completed state and start a new active state
2. **Update the state file**: persist the compressed and pruned state to the state file
3. **Prepare context for the next agent or session**: ensure the context is clean and focused for the next operation
4. **Document the rotation**: record what was compressed, pruned, and rotated

### Phase 5: Validation

1. **Measure the new context size**: verify it is within the token budget
2. **Verify operational memory is preserved**: check that critical state and active decisions are intact
3. **Verify no critical information was lost**: compare the compressed context against the original to ensure nothing critical was dropped
4. **Test the next operation**: ensure the compressed context supports the next task or agent handoff

## Context Management

- Track compression state in `.dev-craft/context/<project>/state.json` with fields: `session_id`, `original_token_count`, `compressed_token_count`, `pruned_items`, `preserved_items`, `rotation_count`, `status`
- On session resume, check state.json for any in-progress compression and continue from the last completed phase
- Persist pruned context in `.dev-craft/context/<project>/archive/` for potential future reference

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read current context, state files, and reference documents | Only read project source and state files |
| Write | Create compressed summaries and archive files | Follow the compression and archive formats |
| Edit | Update state files with compression results | Preserve critical state; never delete critical information |
| Bash | Run token counting tools, state validation | Use established tools for token estimation |
| Grep | Find context items by importance or relevance | Search within the context scope |
| Glob | Find state files and archive files | Pattern: `.dev-craft/context/**/*` |
| Task | Spawn subagent for deep context analysis or compression | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. A compressed context with summaries replacing verbose content
2. A pruned context with stale and irrelevant items removed
3. An archive of pruned context for potential future reference
4. A compression report showing before/after token counts and what was preserved/pruned
5. Updated state.json with the compression session results
6. Validation that the compressed context supports the next operation

## Quality Gates

- [ ] Compressed context is within the token budget
- [ ] All critical and important context is preserved
- [ ] No critical information was lost during compression
- [ ] Stale and irrelevant context is pruned
- [ ] Operational memory is maintained across rotations
- [ ] Compressed context supports the next task or agent handoff
- [ ] Pruned context is archived for potential future reference
- [ ] Compression report documents what was changed and why

## Error Handling

- **Compression tool fails**: retry once; if it fails again, use manual compression with a simplified summary format
- **Critical information lost during compression**: restore from the archive, re-compress with higher preservation settings, and verify
- **Token budget still exceeded after compression**: escalate to the user, suggest splitting the task into smaller sub-tasks, or reducing the scope
- **Archive write fails**: log the error, continue with the compression, and retry the archive write
- **Context rotation causes state inconsistency**: restore from the state file, re-apply the rotation, and verify