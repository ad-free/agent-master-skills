# Challenge pass

The request may be wrong or incomplete, and the user may not be able to tell. Treat it as a hypothesis, test it
against the repo and against itself, and report concerns with their basis. Guessing here turns into rework later.

Standard: a few lines inside the Task Brief, assumptions stated, no interrogation. Large: the full format below.

## Basis tags

| Basis | Meaning | Example |
|---|---|---|
| Code | found in the repo (`file:line`) | `refund()` exists in `billing.py:88` and conflicts with step 3 |
| Docs | found in docs, tickets, schema, tests | schema says `status` is nullable; your flow assumes it is set |
| Run | observed by running something | endpoint returns 409 on duplicates, not 400 |
| Logic | reasoned from the text alone | step 2 forbids edits, step 5 edits |
| Unknown | cannot be determined | can guests check out? |

**Claims about systems you cannot inspect** (a provider's delivery guarantee, another team's SLA, "the client
already handles it") are Unknown even when the user states them confidently. Build on them only behind a cheap
guard (for example an idempotency check) or ask; never remove the guard because of the claim.

Code, Docs and Run may be stated as fact. **Logic is labeled as reasoning for the user to confirm. Unknown
becomes a question. Never present Logic or Unknown as fact.** Anything checkable in the repo is looked up, not asked.

## Lenses (use the ones that apply)

Contradictions; gaps (inputs, outputs, error cases, empty states, permissions, limits, concurrency, data
migration); ambiguity ("user", "delete", "recent", "real-time"); conflicts with the codebase (existing feature,
convention, test the request would break); hidden impact (other callers, consumers, jobs, reports); missing
goal (if only "how" is given, ask for the outcome); simpler alternative (only if you can cite the existing
function); data model (schemas touched, `data-modeling.md`); experience (UI touched, `frontend-design.md`).
If the request asks for something the repo already has, stop and point to it.

## Output

```markdown
## Findings
1. [Contradiction | Logic] Step 2 forbids edits, step 5 edits an order. -> Which wins? (default: step 2)
2. [Gap | Code] No behavior for stock 0 (inventory.py:41 returns None). -> Reject, backorder, or hide? (default: reject)
## Assumptions I will make unless you object
- A1 [Docs] Prices are stored in cents (schema.sql).
## Not checkable
- Whether guests can check out.
## Proposals (max 3, not built without approval)
- P1 [Code] Leave-balance chart on the dashboard; data exists in `leave_balances`. Cost: ~1h.
```

## Questions, proposals, spikes

- **A question blocks only when the default is unsafe or hard to undo** (destructive, data loss, security, a
  contract with consumers outside the repo). An explicit instruction plus consumers you can all see in the repo
  is not blocking: state the assumption, update every consumer, prove it, and note the outside-repo risk under
  "Not verified". Stopping to ask about what the user already said wastes their time.
- Ask only what would change the design if answered differently; max 3 per round, most important first, each
  with a recommended default so the answer can be one word.
- Proposals are improvements the task did not ask for: max 3, each with a basis tag, one-line benefit and cost.
  Never build one without approval. Existing production data is a hard constraint: schema changes always
  include a migration and rollback.
- If a requirement depends on something unknown (external API behavior, library feature, performance), run a
  small experiment and report the result instead of assuming. Reproduce current behavior before changing it.

## Make logic concrete

Restate the task as acceptance criteria with examples (input -> expected output) and edge cases with proposed
behavior. Wrong logic shows up fast in examples. The confirmed brief is the goal for everything after.
Every example names where its expected value comes from, because a misreading looks identical in the code and
in your own tests; only a source you do not control can expose it.

```markdown
REQ-2: A manager approves a leave request.
 Given a pending request of 3 days and a balance of 5, when approved, then status=approved and balance=2.
 Source: Hand calc (5 - 3). Edge: balance 2 -> 409 "insufficient balance". Source: Repo leave.py:61.
Invariants: leave balance = accruals - usages (check query in tests/test_ledger.py)
```

- **Sources:** `User`, `Document <path>`, `Repo <file:line>`, `Run <command>`, `Hand calc <steps>`, `Assumption`.
- **Precedence when sources disagree:** User > Document > Repo behavior > Run observation > Hand calc >
  Assumption. A test that disagrees with a higher source changes; the source does not. Equal sources that
  disagree: ask.
- **User vs Document/legal/policy conflict:** do not let "User outranks Document" pick silently. The user may
  not know the rule exists. Label it `Business rule`, show both readings with their effect, and ask. Headless:
  take the reading that breaks neither the user's evident intent nor the document (reversible, compliant), and
  list the other under "Needs your confirmation".
- **Confirmation scope:** ask the user to confirm only every `Assumption` example and the 2-3 examples you judge
  riskiest (money, state changes, permissions), saying why. Show the rest; do not ask.
- **Invariants:** rules that hold for all inputs (debits equal credits; on-hand equals the sum of movements; a
  posted document is never edited). Each maps to a test, a DB constraint, or a check query and gets a row in the
  requirement matrix (`verify.md`).
- **Business rule:** a question only the user can answer (policy, thresholds, approval chains) is labeled
  `Business rule`. Never decide one silently; it goes under "Needs your confirmation" in the final report.
- **Changing existing logic:** capture current outputs on representative inputs first (characterization tests
  or saved outputs); after the change show before/after and mark each difference intentional or not.

## Task template (offer when the description is thin)

Goal (why) / Actors / Inputs / Outputs / Rules / Error cases / Out of scope / Done when. Blanks become your
questions. After finishing, add a short "What was missing from the task" note for future inputs.

## Decisions

Anything assumed or chosen goes into the decision/assumption lists (`phases-large.md` State; Standard: the report) and the final report.
