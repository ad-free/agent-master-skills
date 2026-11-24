# i18next / react-i18next

Load when a change adds or changes user-visible text in an app that uses i18next.

- **No hard-coded UI text.** Every new string gets a key in every locale file the app ships (`en.json`, `vi.json`,
  ...), in the same commit. Match the repo's key naming and namespaces; read two neighbouring keys first.
- **Key parity is a test.** If the repo has one (a test comparing locale key sets), run it; if not, add one: every
  locale has the same keys and no value is empty. Missing keys fall back silently, so only a test catches them.
- **Plurals:** JSON v4 suffixes `key_one` / `key_other` (plus the forms a language needs, e.g. `_few`, `_many`),
  called with `t('key', { count })`. Never build plurals with `count === 1 ? ... : ...`. Languages without plural
  forms (Vietnamese) still need `_other`.
- **Interpolation, not concatenation:** `t('greeting', { name })` with `"Hello {{name}}"`; word order differs
  between languages. Rich text: the `Trans` component, not split strings.
- **Formatting:** numbers, money and dates through `Intl` (or the repo's helper) with the active language, never
  string templates.
- **Runtime check in dev and tests:** `saveMissing: true` with a `missingKeyHandler` that logs or fails the test
  surfaces keys the code asks for but the files lack.
- **Layout:** check the longest locale (often German or Vietnamese) at 390 px for overflow and truncation.
- **Done:** parity test passes, UI checked in every locale the change touches (screenshots per locale).
