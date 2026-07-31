---
name: agent-evaluator-and-benchmark
description: |
  Run self-correcting evaluation loops, benchmark agent output
  quality against specifications, and diagnose failures. Use when
  evaluating agent performance, benchmarking output quality, or
  running evaluation loops. Do NOT use for general testing
  (see qa-and-edge-case-tester) or for code review (see
  code-review-and-quality).
  
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
  - "evaluate agent output"
  - "benchmark agent"
  - "evaluation loop"
  - "agent quality assessment"
  - "self-correcting evaluation"
  - "failure diagnosis"
  - "benchmark against spec"
  - "agent performance"
  - "output quality check"
  - "evaluation metrics"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: planning-execution
  integrates-with: [quality-gates, code-review-and-quality]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# agent-evaluator-and-benchmark

## Relationship to existing skills

- quality-gates: Provides the layered quality validation pipeline; agent-evaluator-and-benchmark provides the agent-specific evaluation framework.
- verification-before-completion: Validates task completion with evidence; agent-evaluator-and-benchmark validates agent output quality against specifications.
- code-review-and-quality: Reviews code quality after the fact; agent-evaluator-and-benchmark evaluates agent output in real-time during execution.
- dev-craft: Provides the engineering pipeline; agent-evaluator-and-benchmark is invoked during the REVIEW and TEST phases for agent output validation.

## When to Use

- Evaluating agent output quality against a specification
- Benchmarking agent performance across multiple runs
- Running self-correcting evaluation loops to improve agent output
- Diagnosing why an agent's output fails to meet quality standards
- Comparing agent output across different models or configurations
- Validating that agent output meets acceptance criteria
- Measuring agent consistency and reliability

## When NOT to Use

- General test generation or edge-case analysis — see qa-and-edge-case-tester
- Code quality review — see code-review-and-quality
- Task completion verification — see verification-before-completion
- Security auditing — see secops-and-vulnerability-scanner
- Performance profiling — see performance-profiler-and-tuner

## Workflow

### Phase 1: Evaluation Specification

1. **Define the evaluation criteria**: what dimensions of quality are being measured? (accuracy, completeness, relevance, format, style, safety)
2. **Define the acceptance threshold**: what score or rating is considered acceptable?
3. **Define the benchmark dataset**: what inputs and expected outputs are used for benchmarking?
4. **Define the evaluation method**: human review, automated scoring, LLM-as-judge, or a combination
5. **Define the iteration limit**: how many self-correction iterations are allowed?
6. **Get user confirmation** on the evaluation specification before proceeding

### Phase 2: Baseline Benchmarking

1. **Run the agent on the benchmark dataset**: execute the agent against each test case
2. **Collect outputs**: record the agent's output for each test case
3. **Score each output**: apply the evaluation criteria to each output
4. **Compute baseline metrics**: accuracy rate, completeness score, relevance score, format compliance, average score
5. **Identify failure modes**: categorize failures by type (missing information, incorrect information, formatting issues, safety violations)
6. **Document the baseline**: record all metrics and failure modes

### Phase 3: Self-Correcting Evaluation Loop

1. **Analyze failures**: for each failed test case, identify the root cause of the failure
2. **Generate corrections**: for each failure, propose a correction or improvement
3. **Apply corrections**: update the agent's instructions, prompts, or configuration based on the corrections
4. **Re-run the benchmark**: execute the agent again on the benchmark dataset
5. **Compare results**: measure improvement against the baseline
6. **Repeat if needed**: if the score has not improved, iterate the correction process (up to the iteration limit)
7. **Stop when**: the score meets the acceptance threshold or the iteration limit is reached

### Phase 4: Failure Diagnosis

1. **Categorize each failure**:
   - `accuracy`: the output contains incorrect information
   - `completeness`: the output is missing required information
   - `relevance`: the output addresses the wrong topic or is off-topic
   - `format`: the output does not follow the required format
   - `style`: the output does not match the required style or tone
   - `safety`: the output contains unsafe or inappropriate content
2. **Identify patterns**: are failures clustered around specific test cases, input types, or criteria?
3. **Trace the root cause**: for each failure pattern, trace back to the agent's instructions, prompt, or configuration
4. **Propose targeted fixes**: for each root cause, propose a specific fix to the agent's instructions or configuration
5. **Validate the fix**: re-run the affected test cases to confirm the fix works

### Phase 5: Benchmark Reporting

1. **Compile the benchmark report**: baseline metrics, iteration results, final metrics
2. **Document failure modes**: all failure categories and their frequencies
3. **Document improvement trajectory**: how did the score change across iterations?
4. **Document root causes**: what were the root causes of the most common failures?
5. **Document fixes applied**: what corrections were made and what was their impact?
6. **Generate recommendations**: what further improvements are needed?

### Phase 6: Continuous Monitoring

1. **Set up automated evaluation**: schedule regular benchmark runs
2. **Track metrics over time**: monitor accuracy, completeness, and other scores across runs
3. **Detect regressions**: alert when metrics drop below a threshold
4. **Update the benchmark dataset**: add new test cases as the agent's scope evolves
5. **Archive evaluation results**: store results for historical comparison

## Context Management

- Track evaluation state in `.dev-craft/eval/<project>/state.json` with fields: `eval_id`, `criteria`, `baseline_metrics`, `iterations`, `final_metrics`, `failure_modes`, `status`
- On session resume, check state.json for any in-progress evaluation and continue from the last completed phase
- Persist benchmark results in `.dev-craft/eval/<project>/results/`

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read agent output, evaluation criteria, and benchmark data | Only read project source and evaluation data |
| Write | Create evaluation reports and benchmark results | Follow the evaluation report format |
| Edit | Update evaluation criteria or benchmark data | Preserve the original benchmark dataset |
| Bash | Run evaluation scripts, scoring tools, and benchmark suites | Use established tools for evaluation |
| Grep | Find failure patterns or evaluation criteria in output | Search within the evaluation scope |
| Glob | Find evaluation data and result files | Pattern: `.dev-craft/eval/**/*` |
| Task | Spawn subagent for deep failure analysis or benchmark execution | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. A benchmark report with baseline and final metrics
2. A failure mode analysis document with root causes and frequencies
3. An improvement trajectory showing score changes across iterations
4. A corrections log documenting fixes applied and their impact
5. Updated state.json with the evaluation session results
6. Recommendations for further improvements

## Quality Gates

- [ ] Evaluation criteria are clearly defined and measurable
- [ ] Baseline metrics are established before any corrections
- [ ] Self-correction loop runs for at least one iteration
- [ ] Failure modes are categorized and root causes are identified
- [ ] Each root cause has a proposed fix that is validated
- [ ] Final metrics are documented and compared against the baseline
- [ ] Improvement trajectory is documented
- [ ] Benchmark report is complete and actionable
- [ ] No test cases are removed to make the score look better
- [ ] Evaluation results are archived for historical comparison

## Error Handling

- **Evaluation tool fails**: retry once; if it fails again, use manual evaluation for that dimension
- **Self-correction loop does not improve the score**: escalate to the user, suggest changing the evaluation criteria or the agent's instructions, and document the plateau
- **Failure mode cannot be categorized**: document the failure as `unknown`, investigate manually, and add a new category if needed
- **Benchmark dataset is insufficient**: expand the dataset with additional test cases that cover the missing scenarios
- **Evaluation results are inconsistent**: run additional iterations to verify the results, check for non-determinism in the agent's output