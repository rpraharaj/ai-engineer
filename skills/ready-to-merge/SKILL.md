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

Load `engineering-bar` and follow its **Shared procedures** for change scope and verification evidence. Include branch commits, staged and unstaged edits, and relevant untracked files. Pass the recorded scope to every dispatched check.

If the diff is empty, say so and stop.

## Always run

### 1. Mechanical checks

Discover commands from `AGENTS.md`, manifests, and CI. Apply the shared evidence procedure, including reuse of unchanged evidence; do not silently skip unknown or unexecuted checks:

1. **Format** check (avoid unrelated rewrites)
2. **Lint**
3. **Typecheck**
4. Focused tests for the changed area, then **Test**
5. **Build** when compilation, packaging, or generated artifacts can be affected

Record each command and exit status or the reason it could not run. Use the shared completion rule to decide whether equivalent evidence suffices or the result remains unverified. Fix failures only when authorized; otherwise report them.

### 2. Secret scan

Load `engineering-bar` (paths in that skill). Apply **Secret files**. Any match is **not ready**.

### 3. Engineering bar

Walk the rest of `engineering-bar` on the diff. Fails must be fixed or explicitly waived by the user.

### 4. Acceptance checks

Use the agreed task and carry forward its relevant upstream requirements. Do not let an older shape override a newer user instruction. Sources, from the most specific to broader context:

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

Mark irrelevant passes `not applicable` with a reason. Only user-approved gaps are waivers. Silent skips are **not ready**. Run `data-change` in assessment mode without creating or applying migrations.

## Verdict

**Ready** only if:

- Scope is complete and verification meets the shared completion rule
- All applicable configured checks passed or have an explicit user waiver
- Secret scan clean
- Engineering-bar has no unwaived fails
- Acceptance checks (if any) pass
- Every dispatched pass reported pass or an explicit waiver

Otherwise **not ready** (failed requirement) or **unverified** (insufficient evidence), with the blocking item first. Never convert missing evidence into a pass.

## Done

```markdown
## Ready to merge: yes | no | unverified

- Mechanical: <command + exit status, one per line>
- Secrets: pass | fail
- Engineering bar: pass | fails… | waivers…
- Acceptance: pass | fail | n/a
- Dispatched: <skill → pass/fail/waived/skipped and why>
```

Do not commit or open a PR unless the user asked. Next: `commit` then `open-pr`.
