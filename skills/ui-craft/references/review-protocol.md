# REVIEW — UI Multi-Axis Audit (Deep Reference)

Deep reference for ui-craft `[6] REVIEW`. The main `SKILL.md` states the
goal, invokes `code-review-and-quality` for backend axes, and points here for
the UI-specific axes. Load this file only when executing the UI review pass so
the 8 axes don't sit in context during earlier phases.

---

**UI-Specific Review (in addition to code-review-and-quality):**

Review entire diff across UI-specific axes:

**Axis 1 — UX Best Practices:**
- Interaction patterns consistent?
- Error states handled (empty, loading, error)?
- Navigation intuitive?
- Forms usable (validation, errors, labels)?

**Axis 2 — Accessibility:**
- Color contrast ≥ 4.5:1 body, ≥ 3:1 large text
- Focus states visible on all interactive elements
- Touch targets ≥ 44x44px
- All interactive elements have aria labels
- Semantic HTML (button, nav, main, headings)
- `prefers-reduced-motion` respected

**Axis 2b — Screen Reader Testing:**
- Test with NVDA (Windows) or VoiceOver (macOS)
- All images have alt text
- All form inputs have labels
- All buttons have accessible names
- Page structure with headings (h1 → h2 → h3)
- Dynamic content with aria-live

**Axis 3 — Visual Consistency:**
- Colors match design system tokens
- Typography matches design system
- Spacing follows 4/8dp rhythm
- Shadows/border-radii consistent
- Icons from consistent set

**Axis 4 — Version Pattern Audit:**
- No deprecated APIs for detected version
- Code follows current-version docs
- Source citations for correct version
- Lint/format/tests pass
- **No cryptic identifiers / legacy idioms** — `any`→`unknown`, `var`→`const`, single-char vars banned. Enforced by ESLint `id-length` + `no-explicit-any`; config in dev-craft `references/lint-rules.md`.

**Axis 4b — Readability Gate (frontend):**
- Component/function/hook names are self-documenting (no `tmp`, `x`, `res`, `val`).
- Props and state have descriptive names; no cryptic destructuring aliases.
- Run the frontend lint gate from dev-craft `references/lint-rules.md` and read the output before claiming pass.

**Axis 5 — Visual Regression:**
- Run Playwright/Cypress screenshot comparison
- No unintended layout shifts
- No color/typography regressions
- Responsive at 375px, 768px, 1024px, 1440px

**Axis 6 — Testing:**
- Tests exist for new components
- Tests cover edge cases and error states
- Accessibility tests (jest-axe) pass
- Mocks at boundaries only

**Axis 7 — UI Lint:**
- No design system violations
- No unused CSS classes
- No missing responsive utilities
- Run automated UI lint tools
- **Run the frontend readability gate** (ESLint `id-length` + `no-explicit-any`) per dev-craft `references/lint-rules.md` and read output before claiming pass.

**Axis 8 — Security (UI-Specific):**

The agent reads the UI code and traces each concern:

```
XSS Prevention — agent reads every place user data reaches the DOM:
├── dangerouslySetInnerHTML / v-html present? → read context: is content
│   sanitized with DOMPurify before rendering?
├── href/src attrs from user data? → read: is protocol validated?
│   (javascript: URLs must be rejected, not just appended)
├── innerHTML/outerHTML/insertAdjacentHTML from user data? →
│   read: should use textContent or createTextNode instead
└── Template variables in JSX/Vue SFC? → React/Vue autoescape template
    expressions, but not attribute values like href/src

CSRF Protection — agent reads API client code:
├── State-changing requests include CSRF token or use SameSite cookies?
└── Cookie-based auth uses SameSite=Strict/Lax? (Lax for GET redirects)

Sensitive Data Exposure — agent reads bundle and storage code:
├── API responses cached with Cache-Control: no-store for sensitive data?
├── Auth tokens/Session IDs in URL query params? → must move to headers
├── Secrets or API keys in client bundle? (process.env.NEXT_PUBLIC_* or
    REACT_APP_* prefixed env vars are client-accessible)
└── Password fields use autocomplete="current-password"/"new-password"?

Client-Side Data — agent reads storage and logging code:
├── Auth/session data in localStorage/sessionStorage? → prefer
    httpOnly cookies (not accessible from JS, immune to XSS)
├── PII/user data in console.log, Sentry, or analytics? → strip
    sensitive fields before logging
└── File upload previews validate type client-side? (accept attr +
    early rejection of unexpected types)

Third-Party & Dependency Risk — agent reads package.json and templates:
├── Known-vulnerable UI libraries from agent knowledge?
    (old jQuery, Moment.js, deprecated packages)
├── Script tags with integrity hash (SRI) for external CDN resources?
└── Dev dependencies not bundled into production builds?

CSP Readiness — agent reads meta tags and server config:
├── CSP meta tag or header present? script-src policy allows inline
    scripts? (need nonce or hash for inline)
├── form-action restricts submission targets?
└── object-src 'none' and base-uri 'self' set?
```

**Categorize findings:**
| Label | Action |
|---|---|
| Critical | Must fix |
| Required | Must address |
| Nit | May ignore |
| Optional | Worth considering |

**Reality-Check Discipline (borrowed from evidence-based QA):** Approach review as a
skeptic, not an advocate.
- **Default stance is "needs work."** Do not declare a UI slice done on first pass;
  first implementations typically need 1–3 revision cycles.
- **Evidence, not assertion.** For every axis above, cite the actual file/line, the
  rendered output, or a captured screenshot at the required breakpoints (375/768/1024/1440).
  A claim like "looks consistent" without evidence is a RED FLAG.
- **Run real checks.** Execute the linter, type checker, build, and a11y test
  (`jest-axe`) and read the output. Do not infer pass/fail.
- **Spec reality-check:** for each P1/G1 row in `.ui-craft/requirements.md`, confirm the
  built UI actually satisfies it — quote the requirement, show the evidence.
- **Automatic-fail triggers:** claiming "zero issues", a perfect score without evidence,
  or "premium" for a basic implementation.
