---
name: shape-work
description: Turn a vague request, ticket, or idea into a scoped task with goal, in/out of scope, testable acceptance checks, risks, and a first slice. For large or ambiguous changes, run a decision pass (frontier questions with recommended answers) before writing the shape. Use when the user says shape this, scope this, stress-test the plan, or pastes a rough ask. Do not write product code.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Shape work

Turn the user's ask into a task another session can implement without guessing. Do not edit product code. Do not start implementing "just the first slice."

Read `AGENTS.md` if present. Skim only the files you need to name a real approach (entry points, an existing pattern). If you have not mapped the repo and the change is more than a few lines, run `explore-codebase` first — or say that you are shaping with incomplete repo knowledge.

## Decide the kind of work

| Signal | Kind | Next skill after this one |
| --- | --- | --- |
| Something failed, stack trace, "bug", "broken" | Defect | `debug` (shape the repro + expected; do not skip repro) |
| New or changed behavior | Change | `implement-change` |
| Production is down / data is wrong in prod | Incident | `incident-triage` (stabilize first; do not shape a feature) |
| Empty tree / no app yet | Greenfield | `start-project` |
| PRD / product spec / what should we build | Product | `write-prd` |
| System architecture / how the system is shaped | Architecture | `write-architecture` |
| Technical design / tech spec for an initiative | Design | `write-design` |
| Tickets / task breakdown / work plan | Tasks | `write-dev-tasks` |
| How does this code work | Question | `explain-code`; do not produce a fake task |
| README / API docs / runbook only | Docs | `write-docs` |
| Pure question, no change requested | Question | Answer; do not produce a fake task |

If kind is unclear, pick one and state the assumption.

If kind is **incident**, stop here and run `incident-triage`. Do not fill the shaped-work template below.

If kind is **greenfield**, stop here and run `start-project`. Do not shape an `implement-change` against an empty tree.

If the workspace has no product (only README / LICENSE / `.gitignore` / `AGENTS.md`), treat it as greenfield.

If the ask is only "how does this work", stop and run `explain-code`. If the ask is only documentation of existing code, stop and run `write-docs`.

If the ask is a PRD, architecture doc, technical design, or task breakdown, stop and run that skill. Do not flatten those into a shaped-work document.

If **kind is change**, the work has several slices or open product/system decisions, and the user asked to think it through (not "just scope the first slice"), prefer `write-prd` (why still open) or `write-design` (how still open) over a one-shot shape. Tiny one-file changes still skip that and stay here.

## Ask only when blocked

Ask the user at most a few **blocking** questions (missing product behavior, missing environment, contradicting requirements). Do not ask questions you can answer from the repo. Non-blocking questions go in the output and do not stop you from finishing the shape.

## Decision pass (large or ambiguous changes only)

Run this instead of a one-shot shape when **kind is change** and any of: several product decisions are open, the user said "think this through" / "stress-test the plan", or the first slice would commit a hard-to-reverse choice.

Map a **design tree**. Each round, ask the whole **frontier** (questions whose prerequisites are already settled). Number them. Give your recommended answer. Wait. Do not ask the user for facts you can look up.

```
**Q1 — <title>:** <body and options>

Recommended: <your answer>
```

A question that depends on an unanswered Q in this round belongs in a later round. Stop the pass when the frontier is empty, then write the shaped-work document from what you settled. Do not implement until the user confirms the shape.

Defects, incidents, and tiny one-file changes skip this pass.

## Write this document

Use this exact structure. Every acceptance check must be a yes/no a stranger can verify (command, UI observation, or API response). No vague checks like "works well" or "is clean."

```markdown
# Shaped work

## Goal
<one or two sentences>

## Kind
<defect | change | incident | question | greenfield | docs>

## Background
<what we know and which files/symbols we looked at>

## In scope
- ...

## Out of scope
- ...

## Acceptance checks
- [ ] <verifiable statement>
- [ ] ...

## Approach
- Need this at all?: <yes, because … | no — existing X / native Y covers it>
- Pattern to follow: <existing file or symbol, stdlib/native feature, or "none found">
- First slice: <the smallest change that proves the approach; prefer reuse over new code>
- Later slices: <optional>

## Likely files
- `<path>` — <why>

## Risks
- Blast radius:
- Data / compatibility:
- Security / privacy:
- Rollback:

## Open questions
- Blocking: <none | list>
- Non-blocking: <none | list>

## Next
<debug | implement-change | write-tests | start-project | write-prd | write-architecture | write-design | write-dev-tasks | write-docs | explain-code | incident-triage | stop — need user>
```

Save it only if the user asked for a file, or if that is this repo's habit (look for `docs/`, tickets, ADRs). Otherwise print it in the reply. Either way the document above is the deliverable.

## Quality bar for the shape

- Out of scope is non-empty unless the ask is already tiny.
- At least one acceptance check would fail on today's code (for a change or defect). If an existing or native capability already passes those checks, the first slice is "use that" and Next is stop or a one-line wire-up.
- First slice is smaller than the whole goal when the whole goal has more than one risk.
- Likely files are real paths, or you say you could not find them.
- If the ask is much larger than a reuse/stdlib/native option, put the smaller option in Approach and a blocking question: "Do you need full X, or does Y cover it?"

## Done

Show the shaped work. If there are blocking questions, stop and wait. Otherwise name the next skill and stop. Do not implement in the same turn unless the user explicitly said to shape **and** implement and the first slice is already fully specified.
