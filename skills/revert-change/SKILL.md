---
name: revert-change
description: Safely undo a commit, merge, PR, or deploy without rewriting shared history. Use when the user asks to revert, roll back, undo a merge, or back out a change. Do not reset shared branches. Do not invent a third behavior.
license: MIT
compatibility: Requires git
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Revert change

Undo a **known** change. Prefer a new revert commit. Do not `reset --hard` or force-push a branch other people use.

If `git` is missing, stop. If this is a live incident, run `incident-triage` first and come back only if the chosen action is rollback.

Read `AGENTS.md` if present.

## Target

Identify exactly what to undo: commit SHA, merge commit, PR/MR, tag, or release. If the user said "the last change" and HEAD is yours and not on a shared default branch, that is enough.

```sh
git log -8 --oneline
git status --short
git rev-parse --abbrev-ref HEAD
```

Stop if you cannot name the target.

## How to undo

| Situation | Do |
| --- | --- |
| Shared branch, already pushed, or a merge | `git revert` (use `-m 1` on a merge). New commit. |
| Unpushed local commits, your branch only, user said undo | `git reset --soft` to keep files, or `git reset --hard` **only** if they asked to discard |
| Deploy / release already out | Revert the git change, then run this repo's existing rollback (prior artifact, flag, inverse of `cut-release`). If none exists, say what a human must roll back |
| Default branch (`main` / `master` / `trunk`) | Revert only. Never reset it. |

Do not rewrite other people's commits. Do not `--force` to `main` / `master` / `trunk`.

Load `engineering-bar` (paths in that skill) **Secret files** — a revert must not restore committed secrets into a new commit without telling the user.

## Prove

Run `AGENTS.md` **Test** (and **Lint** / **Typecheck** if cheap). If the revert was to stop a fire, a focused test or health check is enough; say what you did not run.

## Done

1. Target (SHA / PR / release)
2. Method (`revert` / `reset` / deploy rollback)
3. New commit hash, or that history was reset
4. Commands and results
5. What is still live in production (if you could not roll that back)

Do not push unless asked. If they want it on the remote, push the revert commit (no force) or say the reset is local only.
