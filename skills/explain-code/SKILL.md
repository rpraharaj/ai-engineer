---
name: explain-code
description: Teach a feature, path, or subsystem from the code that exists — entry points, data flow, and what to change. Use when the user asks how X works, explain this, walk me through, or is onboarding onto a feature. Do not implement. Do not invent architecture the tree does not have.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Explain code

Teach **one** feature or path so the next edit is aimed. Do not implement. Do not map the whole repository (`explore-codebase` does that). Do not invent types, services, or diagrams the code does not support.

Read `AGENTS.md` if present (glossary first).

## Target

Use the symbol, file, route, or feature the user named. If they did not name one, pick the hottest match from their question and say so. If you still cannot tell, ask one blocking question and stop.

## Read

Skim only what the path needs:

1. The entry (route, CLI command, job, screen, exported function)
2. The next 1–2 layers it calls
3. The data it reads or writes (types, tables, events)
4. Tests nearest the path

Stop when you can say where it starts, what it does, and where an edit would go. Do not dump the tree.

## Write this tour

```markdown
# How <target> works

## Starts at
<path or symbol> — <one line>

## What it does
<three to eight sentences, in this repo's terms>

## Data
- In:
- Out:
- Stored / sent:

## Call chain
1. `symbol` (`path`) — …
2. …

## Tests
<files that pin this path, or none found>

## If you change it
- Touch:
- Do not touch:
- Nearby trap:
```

Use names from this repo. If a term is in the `AGENTS.md` glossary, use that meaning. Do not add glossary entries here.

## Done

The tour. Next is usually `shape-work` or `implement-change` if they want a change, not a refactor you were not asked for.
