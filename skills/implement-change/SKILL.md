---
name: implement-change
description: Implement a scoped software change in the current repository using existing patterns. Use when the user wants a feature, bug fix, or code change applied (implement, build, add, make the change) and the ask is already shaped or is a clear small change. Detect and run this repo's checks. Do not claim done without command output.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Implement change

Apply the smallest change that satisfies the request (a shaped task, or a clear small change). You are one agent with a filesystem and a shell. Do not orchestrate other agents unless the user asked.

## Before you edit

1. Read `AGENTS.md` if present. Use its commands.
2. If the workspace has no product yet (empty, or only bootstrap files such as `README`, `LICENSE`, `.gitignore`, `AGENTS.md`), stop and run `start-project`.
3. If the request is vague (no acceptance checks, no in/out of scope, and more than one product decision is open), run `shape-work` first and stop after shaping unless the user already told you to implement the result. If they pointed at a `write-dev-tasks` list, take Task 1 (or the task they named) — `shape-work` it if it is still loose. A clear small change (one behavior, likely files are obvious, no open product fork) does not need a shape document — implement it.
4. Load `engineering-bar` (paths in that skill). If it is missing, follow repository instructions and disclose the incomplete shared-bar assessment rather than claiming it passed.
5. Climb **Minimum path** in that bar. Search this repo for an existing helper before writing a new one.
6. If this is a bug fix, find every caller of the function you will change and fix the shared cause once. Do not patch only the ticket's path.

## Make the change

- Touch only files needed for the request and for tests that belong to it.
- No drive-by refactors, no formatting-only edits outside the files you already must change.
- Do not add a dependency unless a lower rung cannot do the job. If you add one, say why.
- Do not edit generated or vendored paths listed in `AGENTS.md`.
- If a smaller equivalent approach covers the ask, ship that and name what you skipped (add when …). Do not stall asking permission for that smaller solution.

## Prove it

Run, in order, whatever `AGENTS.md` (or `explore-codebase`) recorded:

1. The focused test for this change, if you know how to target it
2. **Test**
3. **Lint** / **Typecheck** if those commands are known and cheap enough to run on the change

If a command is `(unknown)`, say so and run the closest command you already observed in CI or a manifest. If you still cannot run anything, say that the change is **unverified**.

Never claim pass without this session's command output.

If tests are missing for new behavior, add them using the `write-tests` procedure (same runner and style as existing tests) before claiming done.

If the change touches UI (components, routes, CSS, views, client state), follow `verify-ui` before claiming done.

## Apply the bar

Walk the diff against `engineering-bar`. Fix fails. Only the user may waive an item; report their explicit waiver and its risk. Load the bar's shared evidence procedure and reuse current results rather than repeating unchanged checks.

## Done

Report:

1. What changed (files + behavior)
2. Rung used (need / reuse / stdlib / native / installed dep / one line / minimum) and what you skipped
3. Acceptance checks: each pass/fail
4. Commands run and their exit status
5. Verify UI: pass | fail | unverified | n/a
6. Engineering-bar fails or waivers
7. Known ceiling + revisit trigger, or none

Do not commit unless the user asked. Next: `write-tests` if coverage is still thin, `verify-ui` if UI is still unverified, `ready-to-merge` before calling it shippable, then `commit`.
