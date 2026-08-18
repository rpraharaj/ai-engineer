---
name: refactor-safely
description: Behavior-preserving cleanup — lock behavior with tests, refactor mechanically, re-run the same tests. Use when the user asks to refactor, clean up, simplify, or restructure without changing behavior.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Refactor safely

Change structure, not behavior. If the user also wants new behavior, stop and send that part to `shape-work` / `implement-change`. Do not mix the two in one diff.

Read `AGENTS.md` if present.

## Step 1 — Pin behavior

Name the unit (files, package, endpoint) and the behavior that must stay true. Prefer existing tests that already cover it.

If coverage is too thin to notice a break, add **characterization** tests first with `write-tests` (assert current behavior, including odd edges). Do not "improve" those assertions until after the refactor.

Run those tests once. That green run is the baseline. If they are red, this is `debug`, not a refactor.

## Step 2 — Plan the moves

List mechanical steps. Each step should be boring. Climb **Minimum path** in `engineering-bar`: delete dead flexibility, replace hand-rolls with stdlib/native, inline a one-implementation abstraction.

- Extract a helper that already exists inlined
- Move a type to the layer that owns it
- Collapse a duplicate
- Rename inside the unit (update all callers in the same change)

No new framework, no new caching, no "while we are here" feature flags. Never delete trust-boundary checks or data-loss handling to look smaller.

Load `engineering-bar` (paths in that skill). The bar's structure rules apply; its correctness rule here means **same results**, not new acceptance checks.

## Step 3 — Refactor

One cluster of moves, then re-run the same tests. Do not take the suite red across many unrelated files.

Stay inside the named unit plus its callers. Do not reformat files you did not otherwise touch.

## Step 4 — Prove sameness

1. Re-run the characterization / existing tests. They must pass.
2. Run **Test** (and **Lint** / **Typecheck** if known) from `AGENTS.md`.
3. Diff review: every change should be structural. If a conditional's meaning changed, revert that part or admit it is a behavior change and stop.

## Done

1. Behavior that was pinned
2. Moves made (files)
3. Tests run (baseline + after) and results
4. Any leftover cleanup you did **not** do

Do not commit unless asked. If the user wants this shipped: `ready-to-merge` then `commit`.
