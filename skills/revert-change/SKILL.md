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

For a live incident, use the action and evidence already recorded by `incident-triage`; do not restart triage when it has already selected rollback. If no action is selected, run triage first. Operational rollback may proceed without git; source-history changes require git.

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
| Shared branch, already pushed, or a merge | Create a new `git revert` commit. For a merge, inspect its parents and choose the mainline that preserves the intended branch history; never assume parent 1. |
| Unpushed local commits, your branch only, user said undo | `git reset --soft` to keep files, or `git reset --hard` **only** if they asked to discard |
| Deploy / release already out | Run the documented operational rollback first when safe (prior artifact or flag), checking data compatibility. Source-history repair is a separate follow-up if needed and authorized; restoring service does not require a git revert. If no rollback exists, report the missing operation rather than inventing an inverse command. |
| Default branch (`main` / `master` / `trunk`) | Revert only. Never reset it. |

Preserve unrelated dirty files and staging. Inspect the target diff and merge parents before undoing source changes; do not use reset or stash to clear unrelated work. Do not rewrite other people's commits. Do not `--force` to `main` / `master` / `trunk`.

Load `engineering-bar` (paths in that skill) **Secret files**. Stop a source revert that would restore secrets; explain the blocked content and construct a safe targeted undo instead. Disclosure alone does not permit committing secrets.

## Prove

After operational rollback, check the original symptom and the affected service's health using the recorded incident window; report recovered, still degraded, or unverified. Record the running artifact/flag and any incompatible data remaining. For source changes, run `AGENTS.md` **Test** (and **Lint** / **Typecheck** if cheap). If the revert was to stop a fire, a focused test or health check is enough; say what you did not run.

## Done

1. Target (SHA / PR / release)
2. Method (`revert` / `reset` / deploy rollback)
3. New commit hash, or that history was reset
4. Commands and results
5. What is still live in production (if you could not roll that back)

Do not push unless asked. If they want it on the remote, push the revert commit (no force) or say the reset is local only.
