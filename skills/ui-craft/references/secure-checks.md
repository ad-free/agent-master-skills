# UI SECURE Checks

The SECURE check runs per-slice during BUILD. The agent determines what the UI slice touches, then runs matching checks.

## Check Tree

```
Read the slice's files to determine what it does:
│
├── Renders user data (displays user content, messages, profiles)?
│   Read templates → verify:
│   ├── dangerouslySetInnerHTML / v-html used? → must use DOMPurify
│   ├── User content in href/src attrs? → validate protocol (no javascript:)
│   ├── innerHTML/outerHTML/insertAdjacentHTML from user data? → use textContent
│   └── Template variables: React/Vue autoescape in templates, but not in attrs
│
├── Handles forms/input (login, signup, search, upload)?
│   Read form handlers → verify:
│   ├── Sensitive data in URL params? (?token=..., ?password=...)
│   ├── File upload preview: type validated before render? (accept attr)
│   └── Form state in URL hash? (leaks via Referer header)
│
├── Stores data client-side (localStorage, cookies, IndexedDB)?
│   Read storage code → verify:
│   ├── Auth tokens in localStorage/sessionStorage? → prefer httpOnly cookies
│   ├── PII in console.log or error tracking? → strip before logging
│   └── Sensitive API responses cached? → Cache-Control: no-store
│
├── Makes API calls (fetch, axios, Apollo, tRPC)?
│   Read API client → verify:
│   ├── API keys in client bundle? → move to server proxy
│   ├── Sensitive data in URL query strings? → use body/headers
│   ├── CSRF token on state-changing requests?
│   └── Error responses shown to user? (no stack traces)
│
└── Uses REGEX (validation, formatting, routing)?
    Read each regex → verify:
    ├── ReDoS: (a+)+b, (a|aa)+b, (.*a)* patterns?
    ├── Injection: new RegExp(userValue) without escape?
    ├── Anchors: /[a-z]+/ matches partial → use /^[a-z]+$/
    └── Unicode: JS without u flag? → \w doesn't match Unicode
```

## Output Format

```
SECURE CHECK: [component name]
- User Data: [PASS / FLAG]
- Forms: [PASS / FLAG]
- Storage: [PASS / FLAG]
- API Calls: [PASS / FLAG]
- Regex: [PASS / FLAG]
```
