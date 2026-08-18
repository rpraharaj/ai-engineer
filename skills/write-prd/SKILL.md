---
name: write-prd
description: Write a product requirements document — problem, audience, goals, non-goals, and testable success. Use when the user asks for a PRD, product spec, requirements, or "what should we build." Do not write product code. Do not PRD a one-line bug.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Write PRD

Capture **what** to build and **why**. This is not a technical design (`write-design`), not system shape (`write-architecture`), and not an implementable slice (`shape-work`).

Do not implement. Do not invent users, metrics, or legal constraints.

## Is this the right skill?

| Signal | Do this instead |
| --- | --- |
| One-line bug, typo, or clear small change | `shape-work` or `implement-change` |
| How we will build an already-agreed product | `write-design` |
| System boundaries / durable shape | `write-architecture` |
| Tickets from an existing PRD | `write-dev-tasks` |
| Why we picked library X | `record-decision` |

If the product ask is already tiny (one behavior, success is obvious), say so and offer `shape-work`. Do not pad a PRD.

Read `AGENTS.md` if present. Skim only enough of the product to avoid inventing a second app.

## Ask only when blocked

Ask at most a few **blocking** questions (who it is for, what success looks like, contradicting goals). Do not ask what you can see in the repo or an existing PRD.

## Find the home

Use the first that exists: `docs/prd/`, `docs/product/`, `docs/requirements/`, a path `AGENTS.md` names.

If none: write in the reply, and offer to create `docs/prd/` in this repo's markdown style.

Name the file like existing PRDs. If there are none, `docs/prd/YYYY-MM-DD-<slug>.md`.

## Write

Copy headings from `references/prd-template.md` in this skill directory. Keep every heading; write `n/a` when a section does not apply. Do not invent extra sections. If that file is missing, use the same headings: Summary, Problem, Current behavior, Audience, Goals, Non-goals, Scope, Success, User stories, Journeys, Requirements, UX notes, Analytics, Privacy and data, Constraints, Dependencies, Rollout, Risks, Assumptions, Open questions, Next.

Fill from the user and the repo:

- **Problem** is a real hurt, not a solution in disguise.
- **Non-goals** is non-empty.
- **Success** checks are yes/no (command, UI observation, metric this product already has). At least one would fail today. Do not invent a baseline.
- **Must / Should / Later** — do not dump a wishlist into Must.
- **Journeys** cover happy, empty, and error when the change is user-facing.
- No secrets. Mark unknowns as unknowns.

## Quality

- A stranger could tell shipped vs not from Success.
- Requirements do not specify tables, frameworks, or folder layout (that is `write-design`).
- Unused sections are `n/a`, not deleted.
- Next names a real skill.

## Done

1. Path or the full text in the reply
2. The problem in one sentence
3. Blocking questions, or none

Do not implement. Next is usually `write-design` (how), `write-architecture` (new boundaries), or `write-dev-tasks` if they only want a breakdown. Tiny first slice: `shape-work`.
