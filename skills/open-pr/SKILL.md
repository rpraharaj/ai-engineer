---
name: open-pr
description: Open a pull request for the current branch with summary, risk, and test plan. Use when the user wants a PR, merge request, or to send work for review. Use the host CLI (gh, glab) if authenticated; otherwise print the body and push instructions.
license: MIT
compatibility: Requires git
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Open PR

Publish the current branch for review. Do not merge. Do not review the whole product — describe this change.

If `git` is missing, stop.

## Inspect

```sh
git rev-parse --abbrev-ref HEAD
git status --short
git remote -v
git log -1 --oneline
```

Resolve the selected remote and actual target using `engineering-bar` **Shared procedures** for base selection and change scope. Prefer the explicit or configured target and remote default over conventional branch names. Use the recorded merge-base and tip for the PR description.

```sh
git log --oneline <merge-base>..<tip>
git diff <merge-base> <tip> --
```

Stop if there are no commits on this branch vs the base. If the branch has uncommitted work the user likely wants in the PR, run `commit` first (or say it is uncommitted). If the user has not run `ready-to-merge` on this change, say so; do not block the PR unless they asked for a merge gate.

Do not open a PR from the selected default/base branch itself unless the user insisted.

## Body

Write a PR/MR body from the diff (not from memory):

```markdown
## Summary
<what changed and why, 2–6 sentences>

## Test plan
- [ ] <command you ran, or steps>
- [ ] ...

## Risk
<who/what this can break, data/compat, rollback>

## Notes
<docs or generated files updated, follow-ups, waivers>
```

If the repo has `.github/PULL_REQUEST_TEMPLATE.md` or a `merge_request_template`, fill that template instead and still include a test plan.

Title: match this repo's PR title style if you can see past PRs (`gh pr list` / `glab mr list` when those CLIs work). Otherwise match commit style.

## Publish

Detect the host from `git remote -v`.

**GitHub**, if `gh` works (`gh auth status` succeeds):

```sh
git push -u <remote> HEAD
gh pr create --title "..." --body "..." --base <base>
```

**GitLab**, if `glab` works:

```sh
git push -u <remote> HEAD
glab mr create --title "..." --description "..." --target-branch <base>
```

Otherwise:

1. `git push -u <remote> HEAD` if the user asked to publish and a remote exists
2. Print the title, body, base, and the compare URL if you can construct it from the remote
3. Say which CLI was missing

Do not `git push --force` to a shared branch. Do not add reviewers unless the user named them.

## Done

Report the PR/MR URL, or the printed body plus the push/compare instructions. List the test plan items and which of them you actually ran in this session.
