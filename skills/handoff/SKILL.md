---
name: handoff
description: Write a continuation brief so another person or session can pick up the work — what changed, what is left, how to verify, landmines. Use when stopping mid-task, switching agents, ending a session, or the user says handoff, wrap up, or continue later.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Handoff

Leave a brief another session can trust. Do not implement more product code. Do not "just finish" a half-done feature unless the user asked to finish, not to hand off.

Read `AGENTS.md` if present.

## Gather from this session (do not invent)

- Goal and acceptance checks (`shape-work` if it exists)
- Files you actually changed (`git status`, `git diff --stat`)
- Commands you ran and their last result
- Open fails from `ready-to-merge`, `review-change`, or a pass
- Decisions and leftover questions
- Existing artifacts to point at (spec, ADR, PR) — do not restate them

If you did not run a command, write **unverified**, not "probably passes."

## Write this document

Reply with the brief. Write a file only if the user asked, or if this repo already keeps handoff notes.

```markdown
# Handoff

## Goal
<one or two sentences>

## State
in progress | blocked | ready for review | done pending merge

## Done
- <behavior or file that is actually finished>

## Not done
- <remaining work, ordered>

## Verify
- Commands: `<exact>` — last result: pass | fail | not run
- Manual: <steps or none>

## Tree
- Branch:
- Uncommitted: yes | no
- Files: <paths>

## Landmines
- Do not touch: <generated paths, fragile areas>
- Secrets / env needed:
- Failed approaches (do not retry blindly):

## Artifacts
- <path or URL> — <what it already holds>

## Next skills
- `<skill-name>` — <why>
```

## Quality

- **Not done** is honest. A half-written function is not done.
- **Verify** lists the real **Test** / **Lint** commands from `AGENTS.md` when known.
- **Landmines** includes anything that wasted time this session.
- No secrets in the brief (tokens, `.env` values). Point at the variable name instead. Use `<REDACTED>` if a value leaked into notes.
- **Next skills** are real skill names from this pack (`debug`, `implement-change`, `ready-to-merge`, …), not a host command.

## Done

Show the brief. If the user wanted a file, give its path. Stop.
