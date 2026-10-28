---
name: incident-triage
description: First response for a production or customer-facing incident — blast radius, stabilize vs fix, evidence to gather. Use when production is down, data is wrong in prod, users are impacted, or the user says incident, outage, sev, or page.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Incident triage

Stabilize first. Do not start a feature. Do not "improve" unrelated code while prod is hurting.

Read `AGENTS.md` if present.

## Step 1 — Snapshot (do not wait for perfect data)

Write this immediately from what you have. Unknown is allowed; label it.

```markdown
## Incident

- Started (known or approx):
- Symptom (what users or systems see):
- Expected:
- Scope (who/what): unknown | <service, region, tenant, % >
- Severity (your call): user-blocking | degraded | latent
- What we know:
- What we do not know:
```

If this is a local test failure or a ticket with no live impact, this is `debug` or `shape-work`, not an incident. Say so and stop.

## Step 2 — Blast radius

From logs, metrics, feature flags, recent deploys, and the failing path in code (read, do not rewrite yet):

- What still works
- What is broken
- Whether it is getting worse
- The last change that could explain it (`git log` on the path, release notes, flag flips) — guess only if labeled

Do not page more systems than the evidence supports.

## Step 3 — Stabilize vs fix

Pick **one** primary action and say why:

| Action | When |
| --- | --- |
| **Rollback / flag off** | A recent change or flag lines up with the start time and revert is safe |
| **Mitigate** | Limit traffic, disable a path, fail closed, serve stale — without a full fix |
| **Fix forward** | Cause is known, fix is smaller than rollback, or rollback is impossible |
| **Observe** | Impact is gone and you are confirming; do not declare closed yet |

Rollback and mitigate come **before** a clever fix. If you choose **Rollback / flag off**, the mechanical undo is `revert-change` (and this repo's flag/console if that is the rollback). Pass the snapshot, selected action, evidence window, and recovery check to the next skill; nested skills must reuse that context rather than restarting triage. If you choose fix forward, hand the actual diagnosis to `debug` (repro if you can get one without making things worse; otherwise use prod evidence as the baseline).

Do not run destructive data repairs (drop, unscoped delete, unbatched rewrite) unless the user explicitly asked and you wrote the blast radius.

## Step 4 — Evidence

Gather only what changes the next action. Typical sources this repo already has: logs, traces, error reporter, deploy history, feature-flag console, the failing query. Record:

- Queries or dashboard links you used (no secrets)
- Time range
- One representative error (redact tokens)

If you cannot access prod, list the exact checks a human should run.

## Step 5 — Comms and next

Keep a running log in the reply (and a file only if the user asked or this repo stores incident notes):

```markdown
## Actions
- <time> <what> <result>

## Current status
mitigating | monitoring | fix-forward | needs-user

## Next
<debug | revert-change | data-change | stop — need user> — <one sentence>
```

When the fire is contained, `debug` + `write-tests` for the root cause, then `record-decision` if the response taught a lasting rule. `handoff` if another person or session will take over.

## Done

The snapshot, blast radius, chosen action, evidence, and next skill. Do not commit a speculative fix unless the user chose fix-forward and `debug` produced a real cause.
