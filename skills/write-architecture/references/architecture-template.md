# Architecture: <system or area>

Keep every heading. Write `n/a` when a section does not apply. Do not invent services, SLOs, or vendors.

- **Status:** draft | accepted | superseded
- **Date:** <YYYY-MM-DD>
- **Author:** <names or "this session">
- **Reviewers:** <names or none>
- **Related:** <PRD / design / ADR paths, or none>

## Summary

<three to six sentences: what the system is, the proposed shape, the main trade-off>

## Context

<what system, who uses it, why the shape is in question>

## Scope of this doc

- In (areas, services):
- Out:

## Goals and non-goals

- Goals:
- Non-goals:

## Current state

<what exists today, with real paths/services — or greenfield>

## Actors and systems

<people, apps, and external systems that talk to this area — or n/a>

## Proposed shape

### Boundaries

<apps, packages, services, trust boundaries — things that can fail or deploy apart>

### Data

<stores, who owns them, how data moves>

### Control flow

<request path, jobs, events, sync vs async>

### Identity and tenancy

<authn/authz, tenant isolation — or n/a>

### External

<third parties, auth, payments — or none>

## Deployment and environments

<how it runs: regions, envs, runtime — from this repo, or n/a>

## Quality attributes

Use numbers this repo already has, or targets the user set. Otherwise `n/a` — do not invent SLOs.

- Availability:
- Consistency:
- Latency:
- Throughput:
- Durability:
- Security / tenancy:
- Cost:

## Data classification

<PII / secrets / residency / retention — or n/a>

## Migration and coexistence

<how current and proposed live together, expand-then-contract — or n/a / greenfield>

## Alternatives considered

### A. <name>

- Pros:
- Cons:

### B. <name>

- Pros:
- Cons:

## Decisions

- <one-liner + pointer to an ADR, or "none yet — run record-decision">

## Risks and operability

- Failure modes:
- Observability:
- Rollback:
- Disaster recovery (RPO/RTO if this repo has them):

## Evolution

<what we will not solve yet, and the trigger to revisit>

## Open questions

- Blocking: <none | list>
- Non-blocking: <none | list>

## Next

<write-design | record-decision | write-dev-tasks | stop — need user>
