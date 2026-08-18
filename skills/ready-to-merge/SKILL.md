---
name: ready-to-merge
description: Decide if the current change is ready to merge. Run this repo's format, lint, typecheck, and tests; secret-scan the diff; apply engineering-bar; dispatch security-pass, performance guard, production-pass, data-change, or verify-ui when the diff matches. Use when the user says ready to merge, are we done, definition of done, or ship check.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Ready to merge

Gate the **current change**. Do not add features. Do not declare ready without this session's command output.

Read `AGENTS.md` if present.

## Collect the diff

Prefer git (working tree vs `HEAD`, including staged). If the user named a branch, diff that branch against its merge-base with the default base (`main` / `master` / `trunk` / remote `HEAD`). If there is no git, the files edited in this session are the diff.

If the diff is empty, say so and stop.

## Always run

### 1. Mechanical checks

Run whatever `AGENTS.md` recorded, in this order, skipping `(unknown)`:

1. Format (if the repo has a check/fix command)
2. **Lint**
3. **Typecheck**
4. Focused tests for the changed area, then **Test**

Record each command and exit status. A failure means **not ready** unless you fix it in this run and re-run the same command.

### 2. Secret scan

Load `engineering-bar` (paths in that skill). Apply **Secret files**. Any match is **not ready**.

### 3. Engineering bar

Walk the rest of `engineering-bar` on the diff. Fails must be fixed or explicitly waived by the user.

### 4. Acceptance checks

Use the first spec that exists in this conversation or a file the user pointed at:

1. `shape-work` acceptance checks
2. The named `write-dev-tasks` task (Acceptance + Batch done if this change claims the whole batch)
3. `write-prd` Success checks (only those this change was meant to satisfy)

Mark each check pass/fail. Any fail is **not ready**. If none of those specs exist, write `n/a`.

## Dispatch (only when the diff matches)

Load each sibling from `../NAME/SKILL.md`, else `.agents/skills/NAME/SKILL.md`, else `~/.agents/skills/NAME/SKILL.md`. Follow that skill on **this** diff. If the skill is missing, run the one-line fallback and say it was a fallback.

| Diff signal | Run | Fallback if skill missing |
| --- | --- | --- |
| Auth, user input, uploads, HTML, URLs, secrets, PII | `security-pass` | New reachable surface must be authorized; treat input as untrusted; no secrets in the diff |
| Query or RPC in a loop, pagination, hot path, large bundle/import, "slow" | `performance` in **guard** mode | No new N+1, no unbounded list/job, no huge eager import on a hot route |
| Network, queue, job, webhook, retry, timeout, feature flag | `production-pass` | Timeouts on I/O; retries bounded and idempotent; one rollback sentence |
| Schema, migration, protobuf, OpenAPI, event shape, column drop/rename | `data-change` (check the plan; do not start a new migration unless the user asked) | Expand and contract are not in the same change |
| UI components, routes, CSS, views, client state | `verify-ui` | New controls have a name, are keyboard-reachable, and are not unreadable; exercise the changed flow, not only a screenshot |

Waivers are explicit: `performance guard skipped: comment-only change`. Silent skips are **not ready**.

## Verdict

**Ready** only if:

- Every mechanical command that ran exited 0
- Secret scan clean
- Engineering-bar has no unwaived fails
- Acceptance checks (if any) pass
- Every dispatched pass reported pass or an explicit waiver

Otherwise **not ready**, with the failing item first.

## Done

```markdown
## Ready to merge: yes | no

- Mechanical: <command + exit status, one per line>
- Secrets: pass | fail
- Engineering bar: pass | fails… | waivers…
- Acceptance: pass | fail | n/a
- Dispatched: <skill → pass/fail/waived/skipped and why>
```

Do not commit or open a PR unless the user asked. Next: `commit` then `open-pr`.
