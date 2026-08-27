---
name: two-axis-review
description: Two-axis code review: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel and reports them side by side. Ported from mattpocock/engineering/code-review.
version: 1.0.0
triggers:
  - "code review"
  - "review code"
  - "review branch"
  - "review diff"
  - "review pr"
  - "two axis"
  - "standards review"
  - "spec review"
metadata:
  origin: agent-master-skills
  ports: mattpocock/engineering/code-review
---

# Two-Axis Code Review

Review the diff between HEAD and a fixed point along two axes:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as parallel reviews so they don't pollute each other's context.

---

## 1. PIN THE FIXED POINT

Whatever the user said is the fixed point (a commit SHA, branch name, tag, main, HEAD~5, etc.). If they didn't specify one, ask for it.

Capture the diff command once:
```bash
git diff <fixed-point>...HEAD
```

Also note the list of commits:
```bash
git log <fixed-point>..HEAD --oneline
```

Before going further, confirm the fixed point resolves and the diff is non-empty.

---

## 2. IDENTIFY THE SPEC SOURCE

Look for the originating spec, in this order:

1. Issue references in the commit messages (#123, Closes #45, etc.)
2. A path the user passed as an argument
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name
4. If nothing is found, ask the user where the spec is

If there is no spec, the Spec axis will skip and report "no spec available."

---

## 3. IDENTIFY THE STANDARDS SOURCES

Anything in the repo that documents how code should be written:
- `CODING_STANDARDS.md`
- `CONTRIBUTING.md`
- `CLAUDE.md`
- `.cursorrules`

### Smell Baseline (Fowler Code Smells)

Always carry this baseline, even when a repo documents nothing. Two rules:
- **The repo overrides.** A documented repo standard always wins.
- **Always a judgement call.** Each smell is a labelled heuristic, never a hard violation.

**Smells:**
- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file. → extract the shared shape.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data.
- **Data Clumps**: the same few fields or params keep travelling together. → bundle them into one type.
- **Primitive Obsession**: a primitive or string standing in for a domain concept. → give the concept its own type.
- **Repeated Switches**: the same switch/if-cascade on the same type recurs across the change. → replace with polymorphism.
- **Shotgun Surgery**: one logical change forces scattered edits across many files. → gather what changes together.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it.
- **Message Chains**: long `a.b().c().d()` navigation. → hide the walk behind one method.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores most of what it inherits. → drop the inheritance.

---

## 4. RUN BOTH REVIEWS

### Standards Review

For each file/hunk in the diff:
1. Check against documented standards (cite the file + rule)
2. Check against smell baseline (name the smell + quote the hunk)
3. Distinguish hard violations from judgement calls
4. Skip anything tooling already enforces

Output format:
```markdown
### Standards Findings

#### [filename.ts]

**Line 42-58: Duplicated Code**
The same validation logic appears in both `validateInput()` and `validateForm()`.
Extract to shared `validate()` helper.

**Line 12: Violation of CODING_STANDARDS.md §3.2**
"Use descriptive variable names" — variable `d` is unclear.
Rename to `distance` or `duration`.
```

### Spec Review

For each requirement in the spec:
1. Check if it's implemented
2. Check if the implementation matches the spec
3. Check for scope creep (behaviour not asked for)
4. Quote the spec line for each finding

Output format:
```markdown
### Spec Findings

**Missing: User can export to CSV (spec §2.3)**
The diff implements JSON export but not CSV.

**Scope Creep: Added rate limiting (not in spec)**
Rate limiting logic was added but not requested.

**Wrong Implementation: Login uses basic auth (spec §1.1 says OAuth)**
Spec requires OAuth2, implementation uses basic auth.
```

---

## 5. AGGREGATE

Present the two reports under `## Standards` and `## Spec` headings. Do **not** merge or rerank findings.

End with a one-line summary per axis:
```
Standards: 3 findings (worst: Shotgun Surgery in auth.ts)
Spec: 2 findings (worst: Missing requirement §2.3)
```

---

## 6. WHY TWO AXES

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

---

## 7. QUICK REVIEW

For a fast review, run only the Standards axis:
```bash
git diff <fixed-point>...HEAD | head -200
```

Check for:
- Obvious code smells
- Naming issues
- Missing error handling
- Hardcoded values
- Missing tests
