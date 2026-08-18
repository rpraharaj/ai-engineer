---
name: explore-codebase
description: Map an unfamiliar repository — stack, install/run/test/lint commands, layout, entry points, and local conventions. Write or update AGENTS.md from evidence. Use when starting in a new repo, onboarding, or before changing code you have not read.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Explore codebase

Goal: a stranger (human or agent) can run, test, and change this repo without guessing. Do not implement product features. Do not invent commands you did not see in a file or run successfully.

## Load

If `AGENTS.md` exists at the workspace root, read it first.

## Step 1 — Find the root

- Prefer the git root (`git rev-parse --show-toplevel`). If git is missing or this is not a repo, use the current workspace directory.
- Record that path as **Root**.

## Step 2 — Detect the stack from files (do not guess)

Scan the root (and obvious packages in a monorepo) for evidence. Record only what exists:

| Evidence | Means |
| --- | --- |
| `package.json` | JS/TS (lockfile names the manager: `pnpm-lock.yaml`, `yarn.lock`, `bun.lock` / `bun.lockb`, `package-lock.json`) |
| `pyproject.toml`, `requirements.txt`, `Pipfile`, `environment.yml` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle` | JVM (Java/Kotlin) |
| `build.sbt` | Scala |
| `Gemfile` | Ruby |
| `mix.exs` | Elixir |
| `composer.json` | PHP |
| `*.csproj`, `*.sln` | .NET |
| `Package.swift`, `*.xcodeproj` | Swift |
| `pubspec.yaml` | Dart / Flutter |
| `CMakeLists.txt` | C/C++ |
| `*.tf`, `.terraform.lock.hcl` | Terraform |
| `flake.nix`, `flake.lock`, `default.nix` | Nix |
| `deno.json`, `deno.lock` | Deno |
| `nx.json`, `pnpm-workspace.yaml`, `turbo.json` | JS/TS monorepo |
| `Makefile`, `justfile`, `Taskfile.yml` | task runner |
| `docker-compose.yml`, `compose.yml`, `Dockerfile` | containers |
| `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml` | CI |

Read the manifest scripts and CI jobs. Those are the source of truth for commands.

## Step 3 — Resolve commands

For each of **Install**, **Run**, **Test**, **Lint**, **Typecheck**, **Build**:

1. Take the command from a manifest script, Makefile target, or CI step that clearly matches that job.
2. If several match, prefer the one CI uses.
3. If none match, write `(unknown)`. Never substitute a generic `npm test` / `pytest` unless that exact command appears or you ran it successfully.

Install only if needed to run tests or the app, and only with the lockfile's package manager.

## Step 4 — Run what you can

- Run **Test** if known. If **Test** is unknown, try **Lint** or **Build**.
- If a command fails because dependencies are missing, run **Install** once, then retry.
- Capture the command and its exit status. A failed test run is still useful evidence (the command exists).
- Do not start long-lived servers unless you need a one-shot health check; prefer a unit test or build.

## Step 5 — Map the tree

From README, manifests, and a shallow directory listing (not a full dump of `node_modules` / `vendor` / `dist` / `.git`):

- Languages and major frameworks actually imported, not every tool in lockfile history.
- Layout: where apps, libraries, tests, and infra live.
- Entry points: `main`, server bootstrap, CLI, mobile apps, jobs.
- Generated or vendored paths that agents must not edit.
- How errors are returned and how tests are named — from 2–3 existing files, not from style guides you invent.
- Domain terms the code and docs already use (type names, module names, comments). Do not invent a glossary.

## Step 6 — Write AGENTS.md

**If `AGENTS.md` does not exist:** copy the first readable template:

1. `references/agents-template.md` next to this skill (always ships with the skill folder)
2. `../../templates/AGENTS.md` when this pack's repo layout is intact

If neither is readable, write an "Agent defaults" list (verify before claiming; no secrets; match the repo; smallest change; no shared-history rewrite; no skipped tests) plus `## This repo` and `## Glossary` managed sections.

**If `AGENTS.md` exists:** replace only the matching managed blocks below. If a marker pair is missing, append that section. Do not rewrite the user's other prose.

Fill every field from evidence. Use `(unknown)` when you could not prove a command.

```markdown
## This repo

<!-- managed-by: explore-codebase -->

- **Root:** <absolute or repo-relative root>
- **Languages:** <list>
- **Install:** `<command or (unknown)>`
- **Run:** `<command or (unknown)>`
- **Test:** `<command or (unknown)>`
- **Lint:** `<command or (unknown)>`
- **Typecheck:** `<command or (unknown)>`
- **Build:** `<command or (unknown)>`
- **Layout:** <one short paragraph>
- **Do not edit:** <generated/vendored paths, or (none found)>

<!-- end-managed-by: explore-codebase -->

## Glossary

<!-- managed-by: explore-codebase-glossary -->

- `<Term>` — <one-line meaning as this repo uses it>

<!-- end-managed-by: explore-codebase-glossary -->
```

Glossary: 5–20 terms taken from this repo. If you cannot find real terms, write `- (none yet)`. Never invent product jargon.

## Done

Report:

1. Root and languages
2. The commands (and which ones you actually ran, with pass/fail)
3. Layout + do-not-edit
4. Path of the `AGENTS.md` you created or updated
5. Anything still `(unknown)` and where a human should look
6. Glossary term count (or none yet)

Stop. Next skill is usually `shape-work` or `debug`, not a drive-by refactor. If the tree has no application yet, next is `start-project`. If they asked how a feature works, that is `explain-code`.
