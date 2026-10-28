---
name: write-dev-tasks
description: Break a PRD or technical design into ordered, implementable tasks with scope and yes/no acceptance. Use when the user asks for tickets, a task breakdown, detailed dev tasks, or a work plan. Do not write product code. Do not invent a backlog for a one-file change.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Write dev tasks

Turn an agreed **what/how** into an ordered list of slices another session can pick up. This is not a PRD, not a design, and not the implementable contract for a single slice (`shape-work`).

Do not implement. Do not open tracker issues unless the user asked and a tracker CLI this repo already uses works.

## Is this the right skill?

| Signal | Do this instead |
| --- | --- |
| Product why still open | `write-prd` |
| How we will build it still open | `write-design` |
| Exactly one small slice | `shape-work` |
| Start coding | `implement-change` |

If there is only one task and it is already small, stop and run `shape-work`. Do not produce a one-item backlog.

Read `AGENTS.md` if present. Read the PRD / design / architecture the user pointed at. If none exists and the work is large, say so and offer `write-prd` or `write-design` first.

## Find the home

Use the first that exists: `docs/tasks/`, `docs/dev/`, a path `AGENTS.md` names, or a sibling of the design/PRD.

If none: write in the reply, and offer to create `docs/tasks/` in this repo's markdown style.

Name the file like existing task lists. If there are none, `docs/tasks/<slug>.md`.

## Write

Copy headings from `references/dev-tasks-template.md` in this skill directory. Keep every heading; write `n/a` when a section does not apply. Do not invent extra sections. If that file is missing, use the same headings: Goal, Prerequisites, Order, Task N (Kind, Depends on, Traces to, In/out of scope, Acceptance, Likely files, Prove, Notes, Next skill), Out of this batch, Batch done, Risks, Next.

Reuse agreed upstream decisions and acceptance checks by reference; add only the detail needed for this slice. Do not repeat a design or re-open settled choices. Investigation tasks may accept a bounded evidence report rather than a behavior change.

Each task:

- One kind. One next skill.
- **Acceptance** is yes/no a stranger can verify. For a behavior change, at least one check would fail today. For an investigation, specify the question, time/effort bound, and evidence artifact instead.
- **Likely files** are real paths, or you say you could not find them.
- **Traces to** names the PRD requirement or design slice when those docs exist.
- Small enough that `shape-work` can tighten it or `implement-change` can take it if it is already clear.
- No "and also refactor the world" inside a feature task. That goes to Out of this batch or its own task.

Order is dependency-real (schema expand before readers, flag before default-on). Parallel only when there is no shared contract.

## Quality

- Task 1 is the smallest slice that proves the approach.
- Later tasks do not assume code Task 1 has not shipped.
- **Batch done** would fail today.
- Count is as small as the risks require. Do not split by file to look thorough.

## Done

1. Path or the full text in the reply
2. Task count and the first task title
3. Next skill for Task 1

Do not implement the list. Follow Task 1's recorded kind and next skill: `debug` for defects, `data-change` for migrations, `write-docs` for docs, or `verify-ui` for UI verification. For a change use `shape-work`, or `implement-change` when already clear. For a spike, run a bounded investigation and report evidence without implementing a speculative solution.
