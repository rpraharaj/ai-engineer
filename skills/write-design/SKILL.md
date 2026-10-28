---
name: write-design
description: Write a technical design for one initiative — approach, contracts, failure, security, and delivery slices. Use when the user asks for a technical design, tech spec, or how we will build this. Do not write product code. Do not design a one-line bug.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Write design

Describe **how this initiative** will be built in **this** repository. This is not a PRD (`write-prd`), not durable system shape (`write-architecture`), and not a ticket list (`write-dev-tasks`).

Do not implement. Do not start coding "just the first slice."

## Is this the right skill?

| Signal | Do this instead |
| --- | --- |
| Users / success / non-goals still open | `write-prd` first |
| New system boundaries or greenfield shape | `write-architecture` first |
| One sticky library/store choice only | `record-decision` |
| One small, already-clear change | `shape-work` |
| Break an existing design into tickets | `write-dev-tasks` |

If product "why" is still unknown, stop and run `write-prd`. If the first slice **is** the whole goal, say so and offer `shape-work` instead of a design doc.

Read `AGENTS.md` if present. Skim entry points and an existing pattern. If you have not mapped the repo and the change is more than a few files, run `explore-codebase` or say the design is incomplete.

Carry forward agreed upstream decisions and acceptance checks by reference. Add only missing detail for this deliverable; do not regenerate or seek approval again for settled decisions. Existing authorization to implement continues to apply once blocking decisions are resolved.

## Ask only when blocked

Ask at most a few **blocking** questions (product fork, compatibility, environment). Prefer a recommended answer. Non-blocking questions go in the doc.

## Find the home

Use the first that exists: `docs/design/`, `docs/designs/`, `docs/specs/`, a path `AGENTS.md` names.

If none: write in the reply, and offer to create `docs/design/` in this repo's markdown style.

Name the file like existing designs. If there are none, `docs/design/YYYY-MM-DD-<slug>.md`.

## Write

Copy headings from `references/design-template.md` in this skill directory. Keep every heading; write `n/a` when a section does not apply. Do not invent extra sections. If that file is missing, use the same headings: Summary, Problem, Goals and non-goals, Constraints, Current vs proposed, Approach, Public surface, Data and contracts, Sequence, UI, Failure, Security, Performance, Observability, Rollout and rollback, Compatibility and migration, Config, Testing, Alternatives, Key decisions, Risks, Assumptions, Open questions, Delivery, Next.

Fill from the repo and any PRD/architecture the user pointed at:

- **Approach** names real files, types, or layers — or says none exist (greenfield).
- **Data and contracts** stay expand-then-contract. Destructive shape change is a later `data-change`, not this doc's "also drop the column."
- **Config** is names only — never secret values.
- **Delivery** is ordered slices, each independently reviewable. Do not write full tickets here (`write-dev-tasks` does that).
- **Key decisions** that are expensive to reverse get `record-decision`, not a buried paragraph.
- Load `engineering-bar` (paths in that skill) and check the design against Minimum path, Failure, Data, Security, UI. Do not paste the bar.

## Quality

- An engineer could start slice 1 without guessing the approach.
- Alternatives include a smaller option (reuse / stdlib / native).
- At least one Delivery slice is smaller than the whole initiative.
- Unused sections are `n/a`, not deleted.
- No secrets.

## Done

1. Path or the full text in the reply
2. Chosen approach in a few sentences
3. Slice 1, and the next skill

Continue into implementation only when the user has authorized it, blocking decisions are resolved, and slice 1 is fully specified — then `shape-work` or `implement-change` on that slice only.
