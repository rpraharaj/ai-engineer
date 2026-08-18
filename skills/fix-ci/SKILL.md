---
name: fix-ci
description: Make a failing pipeline check green by reproducing it locally and fixing the cause. Use when CI failed, a required check is red, or the user pastes a failing job log. Do not skip, delete, or weaken the failing test to get green.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Fix CI

Green the **same check** that failed. This is `debug` aimed at a pipeline job, not a new feature.

Read `AGENTS.md` if present.

## Step 1 — Identify the check

From the user, the PR/MR status, or a job log, record:

- Check / job name
- Command the job ran (from the workflow file or the log)
- Error text and first failing file

If `gh` or `glab` works and the user pointed at a PR/MR or run, fetch that log. If not, use the pasted log or open the workflow file under `.github/workflows`, `.gitlab-ci.yml`, or whatever this repo uses.

If you cannot name the command, stop and say what you need.

## Step 2 — Reproduce locally

Run the **same** command, or the closest `AGENTS.md` **Test** / **Lint** / **Typecheck** / **Build** that implements that check.

- Same failure → you have a baseline. Continue.
- Cannot run (missing service, runner OS) → say what is missing; do not guess a fix.
- Passes locally but failed in CI → compare versions, env vars, secrets, and file set. Do not "fix" passing local tests.

## Step 3 — Fix the cause

Follow `debug`: one hypothesis at a time, then the smallest cause-level change.

Forbidden:

- Deleting or skipping the failing test
- Weakening an assertion to hide the bug
- Disabling the workflow job or `continue-on-error`
- `--no-verify` as the solution
- Pinning a broken dependency with no explanation

Allowed: fix product code, fix the test if the test is wrong, update a fixture, match a version the repo already intended.

Load `engineering-bar` (paths in that skill). If the failure is a flake (order, time, network), make the test deterministic — do not retry-loop the job.

## Step 4 — Prove

1. Re-run the **same** local command. It must pass.
2. Run neighboring checks you might have broken (**Test** / **Lint** if cheap).
3. If the user wants it on the PR, commit only if they asked, then push only if they asked. Otherwise report that CI still has to run remotely.

## Done

1. Check name + command
2. Root cause
3. Fix (files)
4. Local re-run output
5. What you did not change (jobs left enabled, assertions still strict)

If the suite is red for a different reason than this check, list it; do not silently expand scope.
