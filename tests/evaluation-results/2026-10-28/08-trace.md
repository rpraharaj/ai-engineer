# UI verification trace

1. Command (cwd /tmp/ai-engineer-agent-eval-20261028/08): `pwd && cat AGENTS.md && git status --short && rg --files .agents/skills | head -60`
   Result: cwd resolved to /private/tmp/ai-engineer-agent-eval-20261028/08. AGENTS.md requires matching local skills, evidence for test claims, and ready-to-merge before calling a change done. Working tree: ` M style.css`. Local verify-ui, engineering-bar, and ready-to-merge skills exist.

2. Command: `cat .agents/skills/verify-ui/SKILL.md .agents/skills/engineering-bar/SKILL.md .agents/skills/ready-to-merge/SKILL.md; rg --files -g '!.agents/**'; git diff -- style.css`
---
name: verify-ui
description: Exercise a UI change the way a user would — the changed flow, shared routes that read the same state, empty/error/loading states, and desktop plus narrow viewports. Use when the change touches UI, layout, CSS, routes, views, or client state, when ready-to-merge dispatches it, or the user asks to verify the UI. Do not stop at a single screenshot.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Verify UI

Prove the **changed UI** still works for a person. A render or screenshot of the happy path is not enough. Do not add features.

Read `AGENTS.md` if present. Load `engineering-bar` (paths in that skill) and apply the **UI** section.

## Collect

Follow `engineering-bar` **Shared procedures** for scope and evidence, reusing the caller's recorded scope when provided. Inventory routes, screens, components, CSS, and client state this change touches.

If there is no UI in the diff, report **n/a** and stop.

## How to drive it

Use the first that exists in this session:

1. A browser or device preview tool
2. This repo's existing UI/e2e runner from `AGENTS.md` / CI
3. The running app (`Run` in `AGENTS.md`) plus curl/script against the pages
4. A render or component test this repo already has

Use `engineering-bar` shared evidence rules for what each method can prove. Record a result per applicable flow, state, viewport, and accessibility requirement. HTTP or render checks may supply partial evidence; they cannot substitute for unexercised browser interaction or layout. If an applicable requirement cannot be exercised, overall status is **unverified** unless another check has failed. List the exact remaining steps; do not invent a browser harness.

## Exercise

Walk as a user, not as the author. Cover every item that applies:

1. **Changed flow** — click, type, submit, navigate the feature end to end
2. **Shared surfaces** — every route or screen that reads the same state, data, or component
3. **Edge states** — empty, error, loading, permission-denied, and flag/route variants this change can hit
4. **Viewports** — a desktop width and a narrow (~375px) width when layout or CSS changed
5. **Bar UI** — new controls have a name, are keyboard-reachable, and are not unreadable; no layout jump from missing sizes

Hunt regressions. A change that works on one screen and breaks another is a fail.

Mobile/native: use this repo's simulator, preview, or device script if one exists; otherwise **unverified** for device chrome.

## Output

```markdown
## Verify UI: pass | fail | unverified | n/a

- Surfaces:
- How driven:
- Exercised:
- Viewports:
- Bar UI:
- Fails:
- Not verified:
```

If the user asked to fix fails, use `implement-change` and re-run this skill.

## Done

The output above. Do not claim the UI works if you only looked at code or one screenshot.
---
name: engineering-bar
description: Shared engineering quality bar for any change — correctness, hygiene, structure, failure handling, data, security, performance guards, operability, and UI. Use when another skill says to apply the engineering bar, when asked if work meets engineering standards, or before calling a change done.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Engineering bar

Apply this to the **current diff**, not the whole product. Walk each section and assess each applicable item using the shared evidence statuses. The invoking skill controls whether edits are authorized: reviews report failures; implementation fixes failures within scope. Only the user may waive a failure or verification gap. Do not invent extra standards this repo does not use.

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

## Shared procedures

Load `references/change-scope.md` and `references/evidence.md` relative to this skill directory for change collection, base selection, result statuses, and evidence reuse. These are the shared procedures for all checks. If a required procedure is unavailable, report the assessment as incomplete rather than inventing a pass.

## Repository defaults

Always-on defaults belong to the repository's `AGENTS.md`. If missing, use `../explore-codebase/references/agents-template.md` when available; do not maintain a second defaults list here. Apply this bar even when no template is available.

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

Report failures, unverified requirements, and user waivers, then the checks and evidence used. Explicitly identify remaining assessed sections as pass or not applicable; silence is not evidence of a pass.
---
name: ready-to-merge
description: Decide if the current change is ready to merge. Run this repo's format, lint, typecheck, and tests; secret-scan the diff; apply engineering-bar; dispatch security-pass, performance guard, production-pass, data-change, or verify-ui when the diff matches. Use when the user says ready to merge, are we done, definition of done, or ship check.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Ready to merge

Gate the **current change**. Do not add features. Do not declare ready without this session's command output.

Read `AGENTS.md` if present.

## Collect the diff

Load `engineering-bar` and follow its **Shared procedures** for change scope and verification evidence. Include branch commits, staged and unstaged edits, and relevant untracked files. Pass the recorded scope to every dispatched check.

If the diff is empty, say so and stop.

## Always run

### 1. Mechanical checks

Discover commands from `AGENTS.md`, manifests, and CI. Apply the shared evidence procedure, including reuse of unchanged evidence; do not silently skip unknown or unexecuted checks:

1. **Format** check (avoid unrelated rewrites)
2. **Lint**
3. **Typecheck**
4. Focused tests for the changed area, then **Test**
5. **Build** when compilation, packaging, or generated artifacts can be affected

Record each command and exit status or the reason it could not run. Use the shared completion rule to decide whether equivalent evidence suffices or the result remains unverified. Fix failures only when authorized; otherwise report them.

### 2. Secret scan

Load `engineering-bar` (paths in that skill). Apply **Secret files**. Any match is **not ready**.

### 3. Engineering bar

Walk the rest of `engineering-bar` on the diff. Fails must be fixed or explicitly waived by the user.

### 4. Acceptance checks

Use the agreed task and carry forward its relevant upstream requirements. Do not let an older shape override a newer user instruction. Sources, from the most specific to broader context:

1. `shape-work` acceptance checks
2. The named `write-dev-tasks` task (Acceptance + Batch done if this change claims the whole batch)
3. `write-prd` Success checks (only those this change was meant to satisfy)

Mark each check pass/fail. Any fail is **not ready**. If none of those specs exist, write `n/a`.

## Dispatch (only when the diff matches)

Load each sibling from `../NAME/SKILL.md`, else `.agents/skills/NAME/SKILL.md`, else `~/.agents/skills/NAME/SKILL.md`. Follow that skill on **this** diff. If the skill is missing, run the one-line fallback and say it was a fallback.

| Diff signal | Run | Fallback if skill missing |
| --- | --- | --- |
| Auth, user input, uploads, HTML, URLs, secrets, PII | `security-pass` | New reachable surface must be authorized; treat input as untrusted; no secrets in the diff |
| Query or RPC in a loop, pagination, hot path, large bundle/import, "slow" | `performance` in **guard** mode | No new N+1, no unbounded list/job, no huge eager import on a hot route |
| Network, queue, job, webhook, retry, timeout, feature flag | `production-pass` | Timeouts on I/O; retries bounded and idempotent; one rollback sentence |
| Schema, migration, protobuf, OpenAPI, event shape, column drop/rename | `data-change` (check the plan; do not start a new migration unless the user asked) | Expand and contract are not in the same change |
| UI components, routes, CSS, views, client state | `verify-ui` | New controls have a name, are keyboard-reachable, and are not unreadable; exercise the changed flow, not only a screenshot |

Mark irrelevant passes `not applicable` with a reason. Only user-approved gaps are waivers. Silent skips are **not ready**. Run `data-change` in assessment mode without creating or applying migrations.

## Verdict

**Ready** only if:

- Scope is complete and verification meets the shared completion rule
- All applicable configured checks passed or have an explicit user waiver
- Secret scan clean
- Engineering-bar has no unwaived fails
- Acceptance checks (if any) pass
- Every dispatched pass reported pass or an explicit waiver

Otherwise **not ready** (failed requirement) or **unverified** (insufficient evidence), with the blocking item first. Never convert missing evidence into a pass.

## Done

```markdown
## Ready to merge: yes | no | unverified

- Mechanical: <command + exit status, one per line>
- Secrets: pass | fail
- Engineering bar: pass | fails… | waivers…
- Acceptance: pass | fail | n/a
- Dispatched: <skill → pass/fail/waived/skipped and why>
```

Do not commit or open a PR unless the user asked. Next: `commit` then `open-pr`.
AGENTS.md
style.css
README.md
tests/test_render.py
index.html
diff --git a/style.css b/style.css
index d9bdcc5..c9dfe21 100644
--- a/style.css
+++ b/style.css
@@ -1 +1 @@
-form { width: 800px; }
+form { width: 90%; max-width: 800px; }

3. Command: read scope/evidence procedures, product files, tests, git scope and tool availability.
# Change scope

Use this procedure for every diff review and merge gate. A caller that already collected scope passes its base, tip, local paths, and exclusions to all checks. A nested check must not silently choose a different diff.

## Select the target

1. An explicit PR, branch, commit range, or local-only request wins. For a PR, use its actual base and head from the repository service. Do not add unrelated local edits to a remote PR review.
2. Otherwise inspect the current branch, staged and unstaged edits, and untracked files. Include current branch commits relative to its base as well as local edits. A clean working tree on a feature branch is not an empty change.
3. Resolve the base in this order: user-specified base; documented repository/branch target; selected remote's default branch; then a verified conventional branch (`main`, `master`, `trunk`). Do not prefer a stale conventional name over the remote default. An upstream tracking the feature branch itself is not its review base. If competing bases remain ambiguous, ask; never infer an empty diff from an unresolved base.
4. Record the merge-base and tip hashes. For branch commits use the merge-base, not a moving base tip. Review locally modified content too; explain when it differs from the committed PR.

## Inventory

Run from the repository root. These commands cover local changes, including names with spaces; consume NUL-delimited path lists without splitting on whitespace:

```sh
git status --short
git diff HEAD --
git diff --cached --
git diff --
git ls-files --others --exclude-standard -z
```

Read the selected remote's recorded default when available (replace the remote placeholder; if absent, use repository-service metadata or the documented fallback order):

```sh
git symbolic-ref --quiet refs/remotes/<remote>/HEAD
```

For a resolved branch target, substitute the recorded revisions for the placeholders:

```sh
git merge-base <base> <tip>
git diff <merge-base> <tip> --
```

Inspect staged and unstaged patches separately as well as their combined working-tree result: an unstaged reversal can hide a staged change from `git diff HEAD`. Read untracked files that belong to the change; the tracked diff does not contain them. Combine inventories rather than adding overlapping diffs as independent patches. Include relevant deletions, renames, configuration, tests, and documentation. Inspect submodule changes in their own repository when in scope.

On an initial branch without `HEAD`, inventory staged additions, working files, and untracked files instead. Without git, list the files belonging to the request and compare available prior copies; label missing history.

Report unrelated dirty paths as excluded; preserve their contents and staging. Do not change branches, stash, reset, or clean to collect a diff. Declare scope empty only after checking every applicable source. If history or access prevents collection, report incomplete scope, not an empty change.
# Verification evidence

For each applicable check, record the requirement, scope/revision and relevant local contents, command or manual steps, environment, result, and remaining limitation. Never infer a pass from the absence of a failure.

| Status | Meaning |
| --- | --- |
| pass | Observed evidence establishes the requirement |
| fail | Observed evidence contradicts it |
| not applicable | This change cannot exercise the requirement; explain why |
| not configured | The repository has no check for this requirement after inspecting commands and CI |
| not run | A relevant check exists but was not executed, or its evidence is stale |
| unverified | Available evidence cannot establish the requirement |

Unknown commands require discovery from repository files and CI before using `not configured`. Missing dependencies or services are `not run` / `unverified`, not `not applicable`.

## Reuse and invalidation

Reuse output captured earlier in this session when the relevant contents, dependencies, configuration, environment, and check scope are unchanged. Cite the earlier command and result; do not claim it was rerun. Re-run affected checks after edits, dependency changes, formatting fixes, conflict resolution, or environment changes. Prior-session output is context, not a fresh pass.

## Completion

A merge gate needs complete change scope, a clean secret scan, assessment of applicable engineering standards, and evidence for the requested behavior. Run all relevant configured repository checks, including Build when the change affects compilation, packaging, or generated artifacts. Use a format check rather than a formatter that rewrites unrelated files.

For executable behavior, require a focused behavior test or equivalent reproducible observation even when no test suite is configured. For documentation-only changes, reference/link validation and content review may establish completion; do not require an irrelevant application test.

An applicable requirement with `not configured`, `not run`, or `unverified` evidence prevents an unqualified ready verdict unless equivalent evidence establishes it or the user explicitly accepts the remaining gap. A failed check prevents readiness unless fixed and rechecked or explicitly waived by the user. Report waivers separately with the exact gap and risk; an agent cannot grant itself a waiver. `Not applicable` is a scope decision, not a waiver.

For UI, HTTP responses establish server behavior, and render tests establish only their asserted rendering. Neither establishes keyboard operation, browser interaction, or responsive layout without evidence exercising those properties. Overall UI status is unverified if an applicable property remains untested, fail if a property fails, and pass only when all applicable properties have evidence.
# Subscription form

Run partial HTTP/render checks with `python3 -m unittest discover -s tests -v`. This shell-only fixture has no browser, device preview, interaction runner, or layout engine. The HTTP/render checks do not exercise interactions.
<!doctype html><html><body><form><label>Email<input name="email" type="email"></label><button>Subscribe</button></form></body></html>
form { width: 90%; max-width: 800px; }
from pathlib import Path
import unittest
from wsgiref.util import setup_testing_defaults
class RenderTests(unittest.TestCase):
    def test_render(self):
        html = Path("index.html").read_text()
        self.assertIn('name="email"', html)
    def test_http_response(self):
        # Exercise the HTTP application's response without opening a network socket.
        def app(environ, start_response):
            start_response("200 OK", [("Content-Type", "text/html")])
            return [Path("index.html").read_bytes()]
        env = {}
        setup_testing_defaults(env)
        statuses = []
        response = b"".join(app(env, lambda status, headers: statuses.append(status)))
        self.assertEqual(["200 OK"], statuses)
        self.assertIn(b"<form>", response)
## feature
 M style.css
aec4be1 Add subscription form and partial checks
6e67691 Initialize fixture
* feature
  main
/Users/rajeshpraharaj/.local/bin/node
/usr/bin/curl

4. Command: resolve main base and complete diff; inspect tracked inventory and execute configured tests.
aec4be1394c83fdbe59c3e5d2c59088fb433ce32
aec4be1394c83fdbe59c3e5d2c59088fb433ce32
diff --git a/style.css b/style.css
index d9bdcc5..c9dfe21 100644
--- a/style.css
+++ b/style.css
@@ -1 +1 @@
-form { width: 800px; }
+form { width: 90%; max-width: 800px; }
.gitignore
AGENTS.md
README.md
index.html
style.css
tests/test_render.py
test_http_response (test_render.RenderTests.test_http_response) ... ok
test_render (test_render.RenderTests.test_render) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
Test exit status: 0
Diff whitespace exit status: 0

5. Command: inventory hidden configuration and verify final scope.
AGENTS.md
style.css
.gitignore
README.md
tests/test_render.py
index.html
.agents/
.eval/
__pycache__/
*.pyc
 M style.css
1	1	style.css

Assessment:
- Scope: main and HEAD both aec4be1394c83fdbe59c3e5d2c59088fb433ce32; no branch-only commits, no staged or relevant untracked files. Sole change is unstaged style.css form width from 800px to 90%, capped at 800px.
- Browser/preview disallowed by task; repository explicitly has no browser, interaction runner, or layout engine. Existing Python render/HTTP checks are the available method. No harness added.
- Tests: 2 passed, exit 0. They assert email input presence and HTTP 200/form markup only. They do not render CSS or exercise input/submit.
- Whitespace: git diff --check exit 0. No formatter, lint, typecheck, build, package manifest, or CI configuration found.
- Secrets: inspected complete one-line CSS patch and changed path; no secrets or secret files.
- Engineering bar: minimum path, hygiene, structure, and performance guard pass by scoped inspection. No changes to I/O/failure handling, data, security surface, or operability; those sections not applicable. UI and behavior correctness remain unverified. No acceptance spec found.
- Surface: single subscription form. No shared routes, client state, loading/error/permission/flag states in current product. No new controls or media.
- Static observation: index.html has no stylesheet link or viewport meta tag; stylesheet wiring was already absent before this change. This is not demonstrated as a new regression. Need confirm actual serving integration before judging effect.
- Remaining checks: load the actual page and confirm stylesheet is applied; exercise email entry, invalid/valid submission, keyboard Tab and activation, focus/name/readability; inspect form layout at desktop and approximately 375px with mobile viewport behavior. Cannot establish these with current shell-only render assertions.
- Overall Verify UI: unverified. Ready to merge: unverified. Product files left unchanged; no fixes requested.
