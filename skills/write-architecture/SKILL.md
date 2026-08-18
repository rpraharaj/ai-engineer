---
name: write-architecture
description: Write a system architecture document — boundaries, data, control flow, and quality attributes. Use when the user asks for architecture, system design, or how the system is shaped. Do not write product code. Do not architecture a local rename.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Write architecture

Describe the **durable shape** of a system or area. This is not a PRD (`write-prd`), not a per-initiative design (`write-design`), and not a one-page ADR (`record-decision`).

Do not implement. Do not invent services, stores, or quality targets this product does not have.

## Is this the right skill?

| Signal | Do this instead |
| --- | --- |
| What / why for users | `write-prd` |
| How this feature will be built | `write-design` |
| One sticky choice (store, API family) | `record-decision` |
| One implementable slice | `shape-work` |
| Local rename, one-file change | stop — no architecture doc |

If the ask is a single feature inside a settled system, say so and offer `write-design`.

Read `AGENTS.md` if present. If you have not mapped the repo, run `explore-codebase` first or say the picture is incomplete.

## Find the home

Use the first that exists: `docs/architecture/`, `docs/arch/`, `architecture/`, a path `AGENTS.md` names.

If none: write in the reply, and offer to create `docs/architecture/` in this repo's markdown style.

Name the file like existing architecture docs. If there are none, `docs/architecture/<area>.md`.

## Write

Copy headings from `references/architecture-template.md` in this skill directory. Keep every heading; write `n/a` when a section does not apply. Do not invent extra sections. If that file is missing, use the same headings: Summary, Context, Scope of this doc, Goals and non-goals, Current state, Actors and systems, Proposed shape (Boundaries, Data, Control flow, Identity and tenancy, External), Deployment and environments, Quality attributes, Data classification, Migration and coexistence, Alternatives considered, Decisions, Risks and operability, Evolution, Open questions, Next.

Fill from evidence:

- **Current state** names real apps, packages, stores. Greenfield: say so.
- **Boundaries** are things that can fail or deploy apart — not every folder.
- **Quality attributes** use numbers this repo already has, or label them as targets the user set. Do not invent SLOs.
- **Alternatives considered** — at least two, including keep-current when a system exists.
- **Decisions** point at `record-decision` for anything expensive to reverse. Do not hide an ADR inside this doc.

## Quality

- A new engineer could name where a request enters and where data lives.
- Proposed shape is smaller than a platform rewrite unless the user asked for that.
- Unused sections are `n/a`, not deleted.
- No secrets, no invented vendors.

## Done

1. Path or the full text in the reply
2. The proposed shape in three to six sentences
3. Which ADRs should follow (or none)

Do not implement. Next is usually `record-decision` for sticky choices, then `write-design` for the first initiative.
