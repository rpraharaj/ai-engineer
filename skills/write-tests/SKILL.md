---
name: write-tests
description: Add tests for a change using this repository's runner and style, at public seams, with independent expected values. Use when the user asks for tests or coverage, after an implementation, for a regression check, or for a red-green loop.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Write tests

Add tests that match **this** repository. Do not introduce a new test framework, assertion library, or folder layout.

When the user asks for test-first / red-green: one failing test at a confirmed seam, then only enough code to pass, then the next slice. Do not write a bulk suite and then implement. Refactor is `refactor-safely` or `lean-review`, not this loop.

## Detect the runner

1. Read `AGENTS.md` **Test** command if present.
2. Else take the test command from the manifest or CI (same rules as `explore-codebase`).
3. Open 2–3 existing tests nearest the change. Copy file name pattern, location, fixtures, case names, and how they assert errors.

If you cannot find a runner or any existing test, say so. Ask before generating a new harness.

## Seams

A **seam** is the public boundary you observe: the interface a caller already uses. Tests live at seams, not against private methods or internal collaborators.

Before the first new test, name the seam(s) in one line. Prefer an existing seam over a new one. If the module's interface itself is unclear, say so and test the highest existing boundary you can.

## What to cover

Smallest set that would have failed before the change, **one behavior per cycle**:

- One happy path
- Edge / boundary this code can hit
- Error or missing-input path if the change handles failure

Do not add:

- Tests that only assert "does not throw"
- Tests locked to incidental internals if neighboring tests assert behavior
- Mocks of private collaborators, private-method tests, or DB peeks that bypass the public interface
- **Tautologies** — the expected value must not be recomputed the same way the code computes it (`expect(add(a,b)).toBe(a+b)`). Use an independent literal or a worked example from the spec
- Tests for code you did not change, unless a characterization harness for `refactor-safely`

If this is a regression for `debug`, start with a test that reproduces the bug. Confirm it fails on the previous revision when you can (`git stash` or the parent commit), then leave it passing with the fix. Do not comment out product code to simulate the old behavior.

## Write and run

- Put new tests next to existing ones of the same kind.
- Run the focused file or filter, then the repo **Test** command if it is known and reasonable.
- Keep the command output. If it fails, fix the test or the code; do not skip the case.

Load `engineering-bar` (paths in that skill) when the tests required production-code changes. Keep those changes as small as the tests demand.

## Done

1. Seam(s) tested
2. Runner and command
3. Files added or edited
4. Behaviors covered
5. Command output (pass/fail). If unverified, say unverified.

Do not commit unless asked.
