# Red flags

If you catch yourself thinking the left column, do the right column. Each is a mistake made before.

## Frame / Challenge
| Thought | Why it is wrong | Do instead |
|---|---|---|
| "The task is clear enough, start coding" | Gaps become bugs | Run the Challenge pass |
| "The user said it, so it must be right" | Requests can contradict the code | Check against the repo, report conflicts |
| "I'll pick a reasonable default" | A silent choice may be wrong | State as assumption or ask |
| "I'll ask lots of questions to be safe" | Wastes the user's time | Max 3, each with a default |
| "It's FE only, so the API isn't my concern" | The UI must match the real API | Read the backend; report gaps |
| "I'll keep the schema as given" | Bad schemas are costly later | Run the schema review, offer options |
| "I'll just tweak the backend a little" | Out-of-scope change | Ask first; escalate to full-stack |

## Plan / Implement
| Thought | Why it is wrong | Do instead |
|---|---|---|
| "I'll match the backend shape from memory" | Fields get invented | Read the real contract or response |
| "The change is tiny, no test needed" | Tiny changes cause outages | Run the relevant test |
| "I'll use default styling" | Produces a plain UI | Write `design.md`; design system, icons, charts |
| "An index can be added later" | Late changes hit production data | Check queries with EXPLAIN now |
| "The UI validates it, so the server need not" | Clients can be bypassed | Validate on the backend too |

## Review / Verify
| Thought | Why it is wrong | Do instead |
|---|---|---|
| "My new test passes, so it works" | A test that never failed proves nothing | Show it fails without the fix |
| "I'll adjust the failing test's expectation" | Hides a real bug | Investigate the cause |
| "It looks right to me" | Reading is not running | Run it, paste output |
| "I can't run it here" | Usually something can be run | Try; else list under Not verified |
| "Frontend works with my mock, so it's done" | The mock may differ | Run against the real backend |
| "Backend tests pass, so the feature works" | The UI may not consume it correctly | Run the end-to-end flow |
| "The page renders, so the UI is done" | Functional is not good | Checklist + screenshot review |
| "My test passes, so my reading of the requirement is right" | A misreading is identical in code and test | Check the `Source:` tag; confirm `Assumption` examples |
| "I copied the expected value from the current output" | The test then proves nothing | Use a source-tagged value (user, doc, repo, hand calc) |
| "I'll call this a bug; I think it is wrong" | No reproduction means a possible false positive | Repro it, or report as Cited/Suspected |
| "The requirement is probably wrong" | An unsourced doubt is a guess | Cite the contradicting source or ask |
| "I'll decide this policy myself" | Business rules are the user's call | Label `Business rule`; list under Needs your confirmation |
| "I wrote the code, so I know the tests are right" | Author and tests share one misreading | Use a Test Designer (`test-agent.md`) or state independence not achieved |
| "The subagent said it passes" | A claim without output is Weak | Demand the command output; re-run the key command |
| "I'll edit the Test Designer's test so it fits my code" | Hides the disagreement | Fix the code, or go back to the brief |
| "Everything is covered" | No matrix, no proof | Fill the requirement matrix; show `none` rows |
