---
name: write-docs
description: Write or update documentation that matches this repository — README, API docs, or runbooks — from the code that exists. Use when the user asks for docs, README, API reference, or a runbook. Do not start a multi-page design document. Do not invent features the code does not have.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Write docs

Document **what the code does**. Do not invent APIs, flags, or metrics. This is not an ADR (`record-decision`) and not a changelog (`ship-notes`).

Read `AGENTS.md` if present. Read the code and existing docs you will touch.

## Kind

| Ask | Kind | Home |
| --- | --- | --- |
| README, getting started, how to run | Product readme | Root `README.md` or the one this repo already uses |
| Endpoint/type/flag reference | API docs | Existing `docs/`, OpenAPI comments, or doc site this repo has |
| Operate / recover / deploy steps | Runbook | Existing `docs/runbooks/` or ops folder; else reply only unless they asked for a file |
| Why we chose X | Decision | Stop — `record-decision` |
| What shipped | Notes | Stop — `ship-notes` |
| PRD / what we should build | Product | Stop — `write-prd` |
| System architecture | Architecture | Stop — `write-architecture` |
| Technical design / tech spec | Design | Stop — `write-design` |
| Tickets / task breakdown | Tasks | Stop — `write-dev-tasks` |

If kind is Decision, Notes, Product, Architecture, Design, or Tasks, stop after naming the other skill.

## Match this repo

- Follow heading level, tone, and link style of the nearest existing doc.
- Do not switch the repo to a new doc system.
- If no doc exists, write the smallest file that answers the ask in this repo's markdown style.

## Write from evidence

- Commands come from `AGENTS.md` or a file you opened. Never invent `npm test`.
- Public behavior comes from handlers, types, and tests — not from memory.
- Mark unknowns as unknowns. Do not fill them with typical advice.
- No secrets, tokens, or real `.env` values. Point at variable names.

Load `engineering-bar` (paths in that skill) if you must edit code comments or generated doc stubs that this change made wrong. Prefer editing docs only.

## Done

1. Kind and path (or the text in the reply)
2. What you documented
3. What you left out (and which skill owns it)

Do not commit unless asked.
