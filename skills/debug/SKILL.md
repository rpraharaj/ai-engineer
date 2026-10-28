---
name: debug
description: Diagnose a failure with a tight red loop first, then minimise, hypothesise, fix the shared cause, and prove it. Use when something is broken, a test fails, a bug is reported, or the user asks to debug, diagnose, or find the root cause.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Debug

Find the cause of a known failure. Do not shotgun-edit. Do not start a feature while debugging. Ground hypotheses in a reproduction or captured incident evidence for **this** bug.

Read `AGENTS.md` if present. Redact secrets in anything you show (`<REDACTED>`). Prefer env vars over pasting credentials.

## Step 1 — Pin the failure

Write down:

- **Expected:** what should happen
- **Actual:** what happens instead (error text, exit code, wrong value)
- **Repro:** the exact command or the shortest UI/API steps

If this is a live incident and you cannot get a local repro, treat captured production evidence from `incident-triage` as the baseline. If you have neither a repro nor that evidence, **stop**.

## Step 2 — Build a tight red loop

This is the job. A tight pass/fail signal for *this* symptom is the skill. Hypotheses come after.

Try, in order, until you have **one command you have already run**:

1. Failing test at a public seam (`write-tests`)
2. HTTP/script against a local server
3. CLI + fixture, diff stdout to a known-good
4. Browser script if the bug is UI-only and a browser tool exists
5. Replay a captured payload through the path in isolation
6. Throwaway harness that calls the failing path once
7. Property/fuzz loop if it is "sometimes wrong"
8. `git bisect` / automated "boot at state X, check" if it appeared between two known states
9. Differential: same input on old vs new

Then tighten: faster, asserts the user's exact symptom (not "didn't crash"), deterministic (pin time/RNG/network). Flakes: raise reproduction rate until it is debuggable.

**Done with this step when** you have a fast, red-capable command with captured output and controlled inputs. For intermittent failures, record reproduction frequency and remaining nondeterminism. For a live incident where safe replay is unavailable, captured production evidence remains an accepted baseline: proceed with bounded probes, label causal uncertainty, and verify the original production symptom after mitigation. Without either a loop or incident evidence, list what you tried and stop.

Read the entry point, nearby tests, and necessary callers to construct the loop. Keep inspection focused; do not change code based on an unsupported theory.

## Step 3 — Reproduce and minimise

Run the loop when available; otherwise use the captured incident symptom. Confirm it is the **user's** failure, not a nearby one. Capture the symptom.

For a replayable loop, cut inputs, callers, config, and steps one at a time. Do not minimize a live production system by disrupting traffic. Re-run after each cut. Stop when every leftover piece is load-bearing (remove any one and the loop goes green).

## Step 4 — Hypothesise, then probe

Write the smallest useful ranked set of falsifiable hypotheses: one for a direct, evidenced cause; several when the cause is uncertain:

`If <X> is the cause, then <changing Y> will make it disappear / <changing Z> will make it worse.`

Show the ranked list. Then test **one** at a time. Change one variable. Prefer a debugger or a few targeted logs over "log everything."

Tag temporary logs with a unique prefix (e.g. `[DBG-a4f2]`). For slowness, measure first (`performance`) — do not guess-cache.

Cap: if five hypotheses fail, stop and report the map.

## Step 5 — Fix the cause

- Find every caller of the function you will change. One guard in the shared function beats a patch on only the ticket's path.
- Do not delete or skip the failing test, catch-and-ignore, or disable lint to hide it.
- Load `engineering-bar` (paths in that skill). Climb **Minimum path**.

If a correct public seam exists, turn the minimised repro into a failing test (`write-tests`) **before** the fix, then make it pass. If no correct seam exists, say so — that is an architecture finding.

## Step 6 — Prove and clean

1. Re-run the original (un-minimised) loop, or verify the captured incident symptom against fresh production evidence. Report any verification gap; a mitigation alone is not proof of root cause.
2. Regression test passes, or missing seam is written down.
3. Grep out every tagged debug log. Delete throwaway harnesses.
4. Run focused tests and, if cheap, repo **Test**.

## Done

1. The red-loop command and its last output, or incident evidence and its verification limits
2. Root cause (file/symbol)
3. Hypotheses discarded
4. The fix
5. Cleanup done (tagged logs gone)
