---
name: record-decision
description: Capture a sticky technical decision as a one-page ADR — context, options, choice, consequences. Use when the user asks to record a decision, write an ADR, or lock a choice of library, shape, or approach. Do not start a full design document.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Record decision

Write a **short** architecture decision record. This is not a design doc (no delivery plan, no multi-page spec). If the user wants README, API reference, or a runbook, that is `write-docs`. If they want a PRD, that is `write-prd`. If they want system shape, that is `write-architecture`. If they want how this initiative will be built, that is `write-design`. This skill locks **one** expensive choice those docs can point at.

Read `AGENTS.md` if present.

## When to write one

Write when the choice will be expensive to reverse: store shape, public API, a new dependency family, a cross-cutting pattern. Do not ADR a local rename or a one-line bug fix.

If the decision is not yet made, list options and **ask** the blocking question. Do not pick for the user when the options trade product risk.

## Find the home

Use the first that exists:

1. `docs/adr/`, `doc/adr/`, `adr/`, `docs/decisions/`
2. A path `AGENTS.md` names
3. If none: write in the reply, and offer to create `docs/adr/` using this repo's markdown style

Number the file like existing ADRs (`0007-title.md`). If there are none, start at `0001`.

Copy sections from `assets/adr-template.md` in this skill directory. Keep every heading; write `n/a` when a section does not apply. Do not invent extra headings. If that file is missing, use the same headings: Context, Drivers, Options, Decision, Consequences.

## Fill from evidence

- **Context** is facts: current constraint, failing approach, requirement. Link files/symbols you read.
- **Drivers** are the two or three forces that pick among the options (or `n/a` if Context is enough).
- **Options** are real alternatives (including "do nothing"). At least two.
- **Decision** is one option. If the user already chose, quote them; do not relitigate.
- **Consequences** include what you are giving up and when to revisit.
- **Related** points at the PRD, architecture, or design that this choice serves.

No secrets. No host or vendor lock-in language unless that *is* the decision.

## Done

1. Path of the ADR or the full text in the reply
2. The decision in one sentence
3. Whether a later `data-change` / `implement-change` / `write-docs` / `write-design` should follow

Do not implement the decision unless the user asked. Do not commit unless asked.
