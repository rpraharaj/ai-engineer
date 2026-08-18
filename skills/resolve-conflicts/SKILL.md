---
name: resolve-conflicts
description: Resolve an in-progress git merge or rebase conflict hunk by hunk from each side's intent, then run this repo's checks and finish the operation. Use when git is mid-merge or mid-rebase, or the user asks to resolve conflicts. Do not invent behavior. Do not abort unless the user asks.
license: MIT
compatibility: Requires git
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Resolve conflicts

Finish a merge or rebase that is already in progress. Do not start a new feature. Do not `--abort` unless the user explicitly asked to abandon the operation.

If `git` is missing, stop.

## Step 1 — See the state

```sh
git status
git diff --name-only --diff-filter=U
```

Detect merge vs rebase (`MERGE_HEAD` vs `REBASE_HEAD` / `.git/rebase-merge`). If there are no unmerged paths, say so and stop (or continue an already-clean rebase if that is what `status` asks).

Read the conflicting files and the surrounding history:

```sh
git log --oneline --merge
git log -1 --format='%s%n%n%b' MERGE_HEAD 2>/dev/null || true
git log -1 --format='%s%n%n%b' REBASE_HEAD 2>/dev/null || true
```

## Step 2 — Intent per hunk

For each conflict, find why each side changed (commit message, nearby PR/issue if a host CLI works, the code around the markers). Preserve **both** intents when they do not contradict.

Where they contradict, pick the side that matches the operation's goal (the branch being merged in, or the commit being replayed) and write the trade-off in the final report. Do **not** invent a third behavior that neither side had.

## Step 3 — Resolve

Edit until conflict markers are gone. `git add` each resolved path. Do not `git add .` if unrelated dirty files exist.

## Step 4 — Prove

Run `AGENTS.md` **Typecheck**, **Test**, then **Lint** if known. Fix breakages the merge introduced. Load `engineering-bar` (paths in that skill) on those fixes.

## Step 5 — Finish

- Merge: `git commit` only to complete the merge (use the default merge message unless this repo's log shows a different habit). Do not add extra files.
- Rebase: `git rebase --continue` until the rebase completes or the next conflict. Repeat from Step 1 for the next commit.

Do not force-push unless the user asked and the branch is not a shared default branch.

## Done

1. Merge or rebase, and whether it completed
2. Files resolved
3. Any intent trade-off
4. Commands run and results
