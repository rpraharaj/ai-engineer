---
name: engineering-bar
description: Shared engineering quality bar for any change — correctness, hygiene, structure, failure handling, data, security, performance guards, operability, and UI. Use when another skill says to apply the engineering bar, when asked if work meets engineering standards, or before calling a change done.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Engineering bar

Apply this to the **current diff**, not the whole product. Walk each section. Mark each item pass, fail, or n/a. Fix fails, or get an explicit user waiver. Do not invent extra standards this repo does not use.

If `AGENTS.md` exists, follow it. Repo-specific commands win when they conflict with examples here. You still must not commit secrets or claim unverified results.

## How to load

Other skills load this file, first readable:

1. `../engineering-bar/SKILL.md` (sibling of the calling skill)
2. `.agents/skills/engineering-bar/SKILL.md` from the workspace
3. `~/.agents/skills/engineering-bar/SKILL.md`

## Secret files

Fail commit and ready-to-merge (and any secret scan) if the change adds:

- `.env`, `.env.*` except a tracked `.env.example`
- private keys, `*.pem`, `*.p12`, `id_rsa`, `id_ed25519`
- credential files, keystores, dumped tokens
- secrets pasted into otherwise-normal files

## Defaults when AGENTS.md is missing

- Do not claim tests, types, lint, or builds passed unless this session ran the command and captured the output.
- Do not commit secrets, `.env` files, credentials, or private keys.
- Match this repository. Do not introduce a new stack, formatter, or test runner.
- Smallest change that satisfies the request. Prefer reuse, the standard library, and native platform features over new code or new dependencies. No drive-by refactors.
- Do not force-push shared branches. Do not amend other people's commits.
- Do not delete or skip a failing test to get a green run.

## Correctness

- Acceptance checks from `shape-work` (if any) are met, or the task is not done.
- Happy path, edge cases, and error paths that this change can hit are handled.
- No empty `catch` / swallowed rejection / ignored error return.

## Minimum path

Understand the problem first (read the code the change touches). Then stop at the first rung that holds:

1. **Need?** If the request is speculative, skip it and say so.
2. **Already here?** Reuse the helper, type, or pattern in this repo. Do not rewrite it.
3. **Stdlib?** Use the language or runtime library.
4. **Native platform?** Prefer a built-in (HTML control, CSS, DB constraint, OS API) over a new component or dependency.
5. **Already installed?** Use a dependency that is already in the lockfile. Do not add a new one for a few lines of code.
6. **One line?** Prefer it when it stays correct on edge cases.
7. **Only then** write the minimum that works.

Do not climb past a rung that already solves it. The smallest change in the **wrong** place is a second bug.

**Never cut** to win a smaller diff: validation at trust boundaries, error handling that prevents data loss, authorization, secret handling, or accessibility of new interactive UI. User-requested behavior stays.

If you accept a known ceiling (global lock, naive scan, in-memory only), say the ceiling and the trigger to revisit in the summary. Do not invent a comment brand.

## Change hygiene

- Diff is the smallest change that satisfies the request after the Minimum path.
- No unused code, no commented-out blocks, no unrelated cleanup.
- No interface/factory/config for a single implementation or a value that never changes.

## Structure

- Logic lives in the layer that already owns that concept.
- Do not grow a hard-to-scan file when a split is obvious.
- Do not add a flag or mode that turns one function into two programs.

## Failure

- I/O (network, disk, subprocess, queue) has a timeout or the repo's equivalent.
- Retries are bounded and safe to repeat, or there are no retries.
- Failures carry enough context to debug (what failed, which id) and never carry secrets.

## Data

- Input is validated where it enters the system (handler, edge, parser).
- Schema and public contract changes are expand, then deploy, then contract — not both in one step.
- Lists, pages, and jobs are bounded. Unbounded load is a fail.

## Security (this delta only)

- New reachable surface has authorization, not only authentication, if this repo uses auth.
- Untrusted input stays untrusted (query, path, HTML, command, header, file name).
- Secrets are not in source, logs, client bundles, or fixtures.

## Performance (guard, not heroics)

- No new query/RPC inside a loop (N+1).
- No unbounded work on a request or UI path.
- No accidental full-collection scan.
- No huge eager import on a hot route.

Do not "optimize" without a measurement unless the diff clearly adds one of the above. Guess-caching is a fail.

## UI

When the diff adds or changes interactive UI, routes, views, or layout:

- New controls have an accessible name, are reachable from the keyboard, and are not unreadable.
- No layout jump from images, embeds, or fonts with no reserved size.
- Empty, error, and loading states the change can hit are handled (or already were).

The walk-through is `verify-ui`. This section is the bar.

## Operability

- A new failure mode is visible with whatever this repo already uses (log, metric, trace, error report).
- Risky behavior has a rollback sentence you can say out loud (revert, flag, prior artifact).
- Docs, types, or generated clients that this change made wrong are updated in the same work.

## Output

When asked to apply this bar, report only fails and waivers, then the list of checks that ran. Silence on a section means pass or n/a — say which.
