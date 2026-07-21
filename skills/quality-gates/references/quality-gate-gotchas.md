# Common Gotchas

## 1. Judge Sensitivity to Prompt Wording

**Problem:** LLM judges are highly sensitive to how scoring criteria are phrased. Changing "rate code quality" to "rate code maintainability" can change scores by 2+ points.

**Solution:**
- Use fixed, versioned prompt templates stored in `.quality-gates/prompts/`
- Never ad-lib the judge prompt
- Prompt changes require team review + version bump

## 2. Rubric Drift

**Problem:** Over time, the judge's scoring standards drift.

**Solution:**
- Calibrate weekly against a held-out set of 10 reference code samples
- Track score distribution over time
- Re-run rubric calibration against human-annotated gold standard monthly
- Store calibration results in `.quality-gates/calibration.json`

## 3. Confidence Calibration

**Problem:** Judges may be overconfident or underconfident.

**Solution:**
- Track judge accuracy per confidence level
- If "High" confidence accuracy falls below 90%, flag for investigation
- If "Low" confidence > 30% of scores, retune the judge

## 4. False Positives / False Negatives

**Solution:**
- Track FP/FN rate per gate
- If FP > 20%, relax criteria; if FN > 10%, tighten
- NEVER auto-block on judge findings — require human verification for rejections

## 5. Position Bias in Practice

**Solution:**
- Add `lengthRatio` to pairwise output
- If both position-swap runs agree, confidence increases
- If they disagree, hard-block for human review

## 6. Context Window Limits

**Solution:**
- Break large diffs into chunks of ≤ 500 lines each
- Evaluate each chunk independently; aggregate scores (min or mean)
- Flag: "File was evaluated in N chunks"

## 7. Latency Impact

**Solution:**
- Run Gates 1-4 in CI (fast path); Gate 5 on-demand or async
- Cache identical evaluations (same code, same prompt)
- Use cheaper models for low-confidence evaluations
