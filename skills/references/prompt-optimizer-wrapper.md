# Prompt Optimizer Wrapper Utility

Shared utility for invoking `prompt-optimizer` skill across all agents. Provides consistent optimization profiles, token tracking, and cost reporting.

## Usage

```bash
# From any agent or skill
source skills/references/prompt-optimizer-wrapper.sh

# Pre-routing optimization (triage level) - uses pipeline mode by default
optimize_pre_routing "user request here"

# Per-agent optimization - uses pipeline mode by default
optimize_for_agent "debugger" "Fix the flaky login test in auth module"
optimize_for_agent "code-reviewer" "Review PR #247 - auth refactor"

# Chat mode (human-facing prompts) - explicit opt-in
optimize_for_agent "planner" "Build a payment integration" "chat"
```

## Agent Optimization Profiles

Each agent declares its optimization needs via frontmatter metadata:

```yaml
metadata:
  prompt-optimizer-profile:
    role: "senior product strategist"
    structure: "xml-sections"
    examples: true
    grounding: "quotes-for-long-inputs"
    self-check: true
```

### Profile Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `role` | string | Persona for the LLM | none |
| `structure` | enum | `none`, `xml-sections`, `markdown-sections` | `xml-sections` for complex, `none` for simple |
| `examples` | boolean | Include examples in prompt | `false` |
| `grounding` | enum | `none`, `quotes-for-long-inputs`, `citations` | `none` |
| `self-check` | boolean | Add verification instruction | `true` for code/review tasks |
| `output-format` | string | Expected output format hint | none |

### Agent Profiles (Pipeline Mode)

| Agent | Role | Structure | Examples | Grounding | Self-Check |
|-------|------|-----------|----------|-----------|------------|
| `debugger` | senior debugger | xml-sections | false | citations | true |
| `code-reviewer` | senior code reviewer | xml-sections | true | citations | true |
| `verifier` | verification engineer | xml-sections | false | quotes-for-long-inputs | true |
| `api-designer` | API architect | xml-sections | true | quotes-for-long-inputs | true |
| `frontend-engineer` | senior frontend engineer | xml-sections | true | none | true |
| `database-engineer` | database architect | xml-sections | false | citations | true |
| `devops-engineer` | DevOps engineer | xml-sections | false | none | true |
| `security-auditor` | security auditor | xml-sections | true | citations | true |
| `test-engineer` | test engineer | xml-sections | true | none | true |
| `docs-engineer` | technical writer | markdown-sections | true | none | false |
| `retro-analyst` | engineering analyst | markdown-sections | false | none | false |

**Note:** `planner` and `implementer` do NOT use prompt-optimizer — their skills (`product-thinking`, `planning-and-task-breakdown`, `dev-craft`) handle requirement gathering directly.

## Wrapper Functions

### `optimize_pre_routing(request, mode="pipeline")`

Runs prompt-optimizer at triage level — before any classification.

**Input:** Raw user request string, optional mode ("pipeline" | "chat")
**Output:** Optimized request + token savings metrics

```bash
optimize_pre_routing() {
    local request="$1"
    local mode="${2:-pipeline}"
    local optimized=$(skill "prompt-optimizer" <<EOF
$request

MODE: $mode
EOF
)
    
    # Extract metrics (prompt-optimizer returns JSON block with metrics)
    local original_tokens=$(echo "$optimized" | grep -o '"original_tokens":[0-9]*' | cut -d: -f2)
    local optimized_tokens=$(echo "$optimized" | grep -o '"optimized_tokens":[0-9]*' | cut -d: -f2)
    
    # Report to cost-optimizer
    report_savings "triage" "pre-routing" "$original_tokens" "$optimized_tokens"
    
    echo "$optimized"
}
```

### `optimize_for_agent(agent_name, task_context, mode="pipeline")`

Runs prompt-optimizer with agent-specific profile.

**Input:** Agent name + task context + optional mode ("pipeline" | "chat")
**Output:** Optimized prompt for that agent + token savings metrics

```bash
optimize_for_agent() {
    local agent="$1"
    local context="$2"
    local mode="${3:-pipeline}"
    
    # Load agent profile
    local profile=$(get_agent_profile "$agent")
    
    # Build optimization prompt with profile
    local optimization_prompt=$(cat <<EOF
Optimize this task for $agent agent.

Agent Profile:
- Role: $(echo "$profile" | jq -r '.role // "none"')
- Structure: $(echo "$profile" | jq -r '.structure // "xml-sections"')
- Examples: $(echo "$profile" | jq -r '.examples // false')
- Grounding: $(echo "$profile" | jq -r '.grounding // "none"')
- Self-check: $(echo "$profile" | jq -r '.self-check // true')
- Mode: $mode

Task Context:
$context
EOF
)
    
    local optimized=$(skill "prompt-optimizer" <<EOF
$optimization_prompt
EOF
)
    
    # Extract and report metrics
    local original_tokens=$(echo "$optimized" | grep -o '"original_tokens":[0-9]*' | cut -d: -f2)
    local optimized_tokens=$(echo "$optimized" | grep -o '"optimized_tokens":[0-9]*' | cut -d: -f2)
    
    report_savings "$agent" "per-agent" "$original_tokens" "$optimized_tokens"
    
    echo "$optimized"
}
```

### `get_agent_profile(agent_name)`

Loads agent's prompt-optimizer profile from agent file frontmatter.

```bash
get_agent_profile() {
    local agent="$1"
    local agent_file="agents/${agent}.md"
    
    if [[ ! -f "$agent_file" ]]; then
        echo '{}'
        return
    fi
    
    # Extract frontmatter metadata.prompt-optimizer-profile
    yq eval '.metadata["prompt-optimizer-profile"] // {}' "$agent_file" -o json
}
```

### `report_savings(agent, stage, original, optimized)`

Reports token savings to cost-optimizer for budget tracking.

```bash
report_savings() {
    local agent="$1"
    local stage="$2"
    local original="$3"
    local optimized="$4"
    
    local savings_pct=0
    if [[ "$original" -gt 0 ]]; then
        savings_pct=$(( (original - optimized) * 100 / original ))
    fi
    
    # Append to cost-optimizer tracking
    local metrics_file=".dev-craft/prompt-optimizer-metrics.jsonl"
    mkdir -p "$(dirname "$metrics_file")"
    
    cat >> "$metrics_file" <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "agent": "$agent",
  "stage": "$stage",
  "original_tokens": $original,
  "optimized_tokens": $optimized,
  "savings_percent": $savings_pct
}
EOF
}
```

## Integration Points

### In Triage Agent
```bash
# First thing triage does - pipeline mode for structured classification
optimized_request=$(optimize_pre_routing "$USER_REQUEST")
# Then classify the optimized request
```

### In Agent Router
```bash
# Router runs prompt-optimizer before routing - pipeline mode
optimized_request=$(optimize_pre_routing "$USER_REQUEST")
# Then route based on optimized request
```

### In Each Agent (via skill chain)
```bash
# Agent's first step after receiving task - pipeline mode
# Only for agents that use prompt-optimizer (not planner/implementer)
optimized_task=$(optimize_for_agent "$AGENT_NAME" "$TASK_CONTEXT")
# Then proceed with optimized task
```

## Token Savings Tracking

All savings are logged to `.dev-craft/prompt-optimizer-metrics.jsonl` for analysis:

```jsonl
{"timestamp":"2026-08-04T10:30:00Z","agent":"triage","stage":"pre-routing","original_tokens":1200,"optimized_tokens":850,"savings_percent":29}
{"timestamp":"2026-08-04T10:30:05Z","agent":"debugger","stage":"per-agent","original_tokens":2400,"optimized_tokens":1800,"savings_percent":25}
{"timestamp":"2026-08-04T10:30:10Z","agent":"code-reviewer","stage":"per-agent","original_tokens":3100,"optimized_tokens":2200,"savings_percent":29}
```

### Cost-Optimizer Integration

The `cost-optimizer` skill reads this file to:
- Report total token savings per session
- Adjust model routing based on optimized prompt complexity
- Calculate ROI of prompt-optimizer integration

## Configuration

Agent profiles can be overridden via `.dev-craft/prompt-optimizer-config.json`:

```json
{
  "global": {
    "enabled": true,
    "default_structure": "xml-sections",
    "default_self_check": true,
    "default_mode": "pipeline"
  },
  "agents": {
    "debugger": {
      "grounding": "citations"
    },
    "code-reviewer": {
      "examples": true
    }
  }
}
```

## Testing

```bash
# Test pre-routing optimization (pipeline mode - default)
optimize_pre_routing "I want to build a dashboard"

# Test pre-routing optimization (chat mode - explicit)
optimize_pre_routing "I want to build a dashboard" "chat"

# Test per-agent optimization (pipeline mode - default)
optimize_for_agent "debugger" "Fix the flaky login test"
optimize_for_agent "code-reviewer" "Review PR #247"

# Test per-agent optimization (chat mode - explicit)
optimize_for_agent "planner" "Build a payment integration" "chat"

# View metrics
cat .dev-craft/prompt-optimizer-metrics.jsonl
```

## Ponytail Notes

- Wrapper is ~100 lines — minimal, reusable, no framework
- Uses existing `skill()` invocation — no new infrastructure
- Profiles declared in agent frontmatter — single source of truth
- Metrics appended to JSONL — streaming, no locking issues
- Cost-optimizer already exists — just feeds it data