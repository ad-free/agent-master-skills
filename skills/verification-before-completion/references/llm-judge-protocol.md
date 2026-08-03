# LLM-Judge Protocol — Gate 5

**Goal:** Apply LLM judgment to code quality aspects that cannot be deterministically verified. Runs only after Gates 1-4 pass.

## Core Rules

1. **Evidence-first:** Require specific line numbers and code citations before any score
2. **No "vibe" scoring:** Every score must be justified with concrete observations
3. **Bias mitigation:** Use position swaps for pairwise reviews; length normalization for long files
4. **Confidence calibration:** Judge reports confidence level for each score (high/medium/low)

## Direct Scoring (Objective Criteria)

Use when there is a clear factual basis. Each criterion is scored independently.

**When to use:**
- Does the code compile? (post-build verification)
- Is test coverage above threshold? (quantitative)
- Does the code match the schema? (compliance)
- Does the code follow a specific algorithm correctly? (correctness)
- Is there documentation for every public API? (completeness)

**Format:**
```
┌─────────────────────────────────────────────────────┐
│  DIRECT SCORE: [CRITERION NAME]                      │
├─────────────────────────────────────────────────────┤
│  Evidence:                                           │
│  ├── src/auth/login.ts:45-52 — JWT token expires     │
│  │   in 15 min as required by spec §3.2              │
│  └── src/auth/login.ts:88 — Refresh token rotation   │
│      implemented per security policy                 │
│                                                      │
│  Score: 9/10                                         │
│  Confidence: High                                    │
│                                                      │
│  Note: Token blacklist on logout not implemented     │
│  but not in scope for this change. Flag for follow-up│
└─────────────────────────────────────────────────────┘
```

**Scoring scale:**
| Score | Meaning |
|-------|---------|
| 10/10 | Perfect — no improvements possible |
| 8-9/10 | Excellent — minor nits only |
| 6-7/10 | Good — has some issues but acceptable |
| 4-5/10 | Marginal — significant issues |
| 1-3/10 | Poor — fundamental problems |
| 0/10 | Fails basic requirements |

## Pairwise Scoring (Subjective Criteria)

Use when evaluation requires comparison or taste.

**When to use:** Code style, architecture decisions, API design, component composition, naming.

**Format:**
```
┌─────────────────────────────────────────────────────┐
│  PAIRWISE: Code Readability                          │
├─────────────────────────────────────────────────────┤
│  Variant A: src/feature/v1/service.ts               │
│  Variant B: src/feature/v2/service.ts               │
│                                                      │
│  Evidence A: [specific line references]               │
│  Evidence B: [specific line references]               │
│                                                      │
│  Winner: Variant A                                   │
│  Confidence: High                                    │
│  Reasoning: A has clearer separation of concerns     │
└─────────────────────────────────────────────────────┘
```

## Bias Mitigation

| Bias | Mitigation |
|------|-----------|
| Position bias | Swap order for pairwise reviews; run A→B and B→A |
| Length bias | Require evidence-per-line-count ratio |
| Verbosity bias | Add "succinctness" as criterion |
| First-impression bias | Judge reads entire file before scoring |
| Anchor bias | Score each criterion independently |
| Self-consistency bias | 3-shot sampling for critical evaluations |
| Recency bias | Randomize file order |

**Position swap protocol:**
1. Present A first, B second → score
2. Present B first, A second → score
3. Same winner? → Accept with higher confidence
   Different winner? → Flag for human review
   Score diff > 2? → Flag — bias detected

## Evidence-First Protocol

**Rules:**
1. Cite first, score second
2. Line numbers are mandatory
3. Code snippets required for correctness/convention claims
4. No "it feels like" — every claim references observable code
5. Missing evidence = invalid score (N/A)

**Invalid:** "Score 7/10. The code is fairly well-structured but could be cleaner."
→ REJECTED. No evidence, no line numbers, no specific claims.

**Valid:**
```
Evidence:
- src/orders.ts:22-30 — `calculateTotal()` uses single reduce(). Clear, tested.
- src/orders.ts:55-60 — `applyDiscount()` mutates original array, caused bug #142.

Score: 6/10
Confidence: Medium
```
→ ACCEPTED. Specific, observable, actionable.
