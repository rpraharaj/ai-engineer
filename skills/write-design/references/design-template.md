# Design: <initiative>

Keep every heading. Write `n/a` when a section does not apply. Do not invent APIs, SLOs, or files.

- **Status:** draft | review | accepted
- **Date:** <YYYY-MM-DD>
- **Author:** <names or "this session">
- **Reviewers:** <names or none>
- **PRD:** <path or none>
- **Architecture:** <path or none>
- **ADRs:** <paths or none>

## Summary

<one paragraph: what we will build, the approach, the first slice>

## Problem

<one paragraph from the PRD or the user>

## Goals and non-goals

- Goals:
- Non-goals:

## Constraints

<this repo's patterns, compatibility, SLAs, time>

## Current vs proposed

- Today:
- After this initiative:

## Approach

<how we will build it, in this repo's terms — types, APIs, files, layers>

## Public surface

<HTTP/RPC/CLI/events/UI the outside world sees — shapes or examples, or n/a>

## Data and contracts

<schema / API / events. Expand then contract — name data-change if a stored shape moves>

## Sequence

<how a user action, request, or job moves through the system>

## UI

<screens, states, a11y — or n/a. Verification is verify-ui>

## Failure

<timeouts, retries, idempotency, what the user sees>

## Security

<authz, untrusted input, secrets, PII — or n/a and why>

## Performance

<bounds, pagination, hot-path cost — or n/a>

## Observability

<logs, metrics, traces this repo already uses — or n/a>

## Rollout and rollback

<flag, default, how to undo in production>

## Compatibility and migration

<old clients, backfill, dual-write — or n/a>

## Config

<env/flag *names* this change needs — never values or secrets>

## Testing

<seams and cases that would fail before this ships>

## Alternatives

### A. <chosen>

- Why:

### B. <not chosen>

- Why not:

## Key decisions

- <decision> — <why>. ADR: <path or none — not sticky>

## Risks

- Blast radius:
- Data / compatibility:
- Security / privacy:

## Assumptions

- ...

## Open questions

- Blocking: <none | list>
- Non-blocking: <none | list>

## Delivery

Ordered slices. Each must be independently reviewable. Detailed tickets live in `write-dev-tasks`.

1. <slice> — <why first>
2. ...

## Next

<write-dev-tasks | record-decision | shape-work | stop — need user>
