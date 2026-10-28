---
name: production-pass
description: Check whether this change is safe to run in production — timeouts, retries and idempotency, visibility, rollback, and compatibility. Use when the change adds I/O, jobs, queues, webhooks, flags, or public contracts, when ready-to-merge dispatches it, or when the user asks if a change is production-safe.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Production pass

Operability of **this delta**. Do not redesign the platform. Do not edit product code unless the user asked you to fix fails.

Read `AGENTS.md` if present. Load `engineering-bar` (paths in that skill) for Failure + Operability + Data; this skill is how to walk those on a shipping change.

## Collect

Follow `engineering-bar` **Shared procedures** for scope and evidence, reusing the caller's recorded scope when provided. Note new or changed:

- Outbound I/O (HTTP, DB, disk, subprocess)
- Inbound async (queue consumer, cron, webhook)
- Public contracts (API, events, flags)
- State that can be half-applied

## Checks

Use the shared evidence statuses for each requirement; missing evidence is unverified, and irrelevant checks are not applicable. Fails need `file:line`.

### Timeouts

Every new outbound I/O uses a timeout or this repo's standard client (which already has one). Infinite waits are a fail.

### Retries and idempotency

If the change retries:

- Bound + jitter, or the repo's retry helper
- Safe to repeat (idempotency key, upsert, or the handler is naturally idempotent)

If a webhook/job can be delivered twice, handling it twice must not corrupt state.

### Backpressure and bounds

New lists, batches, and jobs have a limit. Unbounded `while`/`fan-out` on request or consume paths is a fail.

### Visibility

A new failure mode is visible with whatever this repo already uses (structured log, metric, trace, error reporter). The record includes enough to debug (operation, id) and no secrets.

### Rollback

Write one sentence: how to undo this in production (`revert-change`, flip a flag already in the diff, restore the prior artifact). If you cannot, **fail** unless the change is trivially reversible by revert alone.

### Compatibility

Public request/response, event, or flag changes are backward compatible for current callers, or the user accepted a break.

- Additive fields require producer/consumer evidence: a new required request field, strict decoder, enum value, or changed default can still break callers. Check old callers against new producers and new callers against old producers during rollout.
- Rename/remove/change meaning: fail while any supported reader or writer relies on the old shape. A separate contract phase may pass with the deployment, backfill, consumer migration, and rollback evidence required by `data-change`; do not reject it solely because it removes a field.
- Flag default that instantly forces a new path with no undo: fail unless rollback is documented

Do not invent a migration here. Do not call `data-change` from this skill — report the compat fail and stop.

## Output

```markdown
## Production pass: pass | fail | unverified

- Timeouts:
- Retries / idempotency:
- Bounds:
- Visibility:
- Rollback: <one sentence>
- Compatibility:
- Fails: …
```

If the user asked to fix fails, use `implement-change` and keep the diff small.
