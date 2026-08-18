---
name: review-change
description: Review a local or branch diff for bugs and engineering-bar failures. Use when the user wants a code review, review of uncommitted work, or a second look at a branch diff. Write structured findings. Do not edit product code. Do not post to a git host unless asked and a host CLI works.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Review change

Read-only review of a **diff**. Do not edit product source. Do not commit.

Named `review-change` so it does not replace a host's own review command.

## Target

Pick the first match:

1. User named a PR/MR number or URL → host CLI diff if `gh` or `glab` works; else ask for a branch
2. User named a branch → `git diff <merge-base>..<branch>` vs default base (`main` / `master` / `trunk` / remote `HEAD`)
3. Otherwise local: staged + unstaged + untracked (`git diff HEAD`, then untracked files)

If the diff is empty, say so and stop. If it is huge (multi-megabyte or hundreds of files), summarize by file and ask what to narrow; do not pretend you reviewed it all.

Read the changed files, not only the hunks, when a finding depends on callers or types.

## Load the bar

Load `engineering-bar` (paths in that skill). Use it for hygiene, structure, failure, data, security, performance guards, and operability.

Also look for:

- Incorrect behavior vs the stated intent
- Missing tests for new logic (point at `write-tests`; do not write them here)
- Authz / injection / secrets if the diff touches those (point at `security-pass` for a full pass)
- Over-engineering only (point at `lean-review`; do not turn this review into a delete-list)

## Spec axis

If a `shape-work` document, spec, or ticket the user pointed at exists, report it **separately** from Issues (do not fold it into bug/nit):

- Missing or partial vs the acceptance checks
- Behavior in the diff that was not asked for
- Checks that look implemented but look wrong

If there is no spec, write `Spec: n/a` and skip. Do not invent a spec.

Do not flood nits when there are bugs. Severity:

- **bug** — wrong, unsafe, or will fail in production
- **suggestion** — real improvement, not blocking unless the user asked for a hard bar
- **nit** — local style; skip if the repo's formatter would handle it

## Findings file

Write findings in the reply. Also write a file only if the user asked, or if this repo already stores reviews.

```markdown
## Summary
<2–4 sentences: what the change does, whether it looks correct, main risks>

## Issues

### Issue 1 — Severity: bug
- File: path/to/file.ext:LINE
- Description: <what is wrong>
- Suggestion: <how to fix>
- Status: open

## Bar
<engineering-bar fails and waivers only>

## Spec
<missing / extra / wrong, or n/a>
```

If there are no issues, keep Summary and an empty Issues section. Do not invent findings.

Line numbers refer to the new file. If you cannot pin a line, say so and put the finding in Summary.

## Optional publish

Only if the user asked to post the review **and** `gh` or `glab` is authenticated:

- Map each issue with a valid new-file line onto an inline comment
- Put the rest in the review body
- Do not submit/approve/request-changes unless the user named that action

If the CLI is missing, print the findings and stop.

## Done

Issue counts by severity, the summary, and the path of any file you wrote. Do not implement fixes unless the user asked — that is `implement-change` or `debug`.
