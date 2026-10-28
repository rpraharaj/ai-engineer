---
name: verify-ui
description: Exercise a UI change the way a user would — the changed flow, shared routes that read the same state, empty/error/loading states, and desktop plus narrow viewports. Use when the change touches UI, layout, CSS, routes, views, or client state, when ready-to-merge dispatches it, or the user asks to verify the UI. Do not stop at a single screenshot.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Verify UI

Prove the **changed UI** still works for a person. A render or screenshot of the happy path is not enough. Do not add features.

Read `AGENTS.md` if present. Load `engineering-bar` (paths in that skill) and apply the **UI** section.

## Collect

Follow `engineering-bar` **Shared procedures** for scope and evidence, reusing the caller's recorded scope when provided. Inventory routes, screens, components, CSS, and client state this change touches.

If there is no UI in the diff, report **n/a** and stop.

## How to drive it

Use the first that exists in this session:

1. A browser or device preview tool
2. This repo's existing UI/e2e runner from `AGENTS.md` / CI
3. The running app (`Run` in `AGENTS.md`) plus curl/script against the pages
4. A render or component test this repo already has

Use `engineering-bar` shared evidence rules for what each method can prove. Record a result per applicable flow, state, viewport, and accessibility requirement. HTTP or render checks may supply partial evidence; they cannot substitute for unexercised browser interaction or layout. If an applicable requirement cannot be exercised, overall status is **unverified** unless another check has failed. List the exact remaining steps; do not invent a browser harness.

## Exercise

Walk as a user, not as the author. Cover every item that applies:

1. **Changed flow** — click, type, submit, navigate the feature end to end
2. **Shared surfaces** — every route or screen that reads the same state, data, or component
3. **Edge states** — empty, error, loading, permission-denied, and flag/route variants this change can hit
4. **Viewports** — a desktop width and a narrow (~375px) width when layout or CSS changed
5. **Bar UI** — new controls have a name, are keyboard-reachable, and are not unreadable; no layout jump from missing sizes

Hunt regressions. A change that works on one screen and breaks another is a fail.

Mobile/native: use this repo's simulator, preview, or device script if one exists; otherwise **unverified** for device chrome.

## Output

```markdown
## Verify UI: pass | fail | unverified | n/a

- Surfaces:
- How driven:
- Exercised:
- Viewports:
- Bar UI:
- Fails:
- Not verified:
```

If the user asked to fix fails, use `implement-change` and re-run this skill.

## Done

The output above. Do not claim the UI works if you only looked at code or one screenshot.
