---
name: start-project
description: Start a new project from an empty or near-empty directory using the stack the user named. Use when there is no existing app, or the user says new project, scaffold, greenfield, or from scratch. Do not invent a stack they did not choose. Do not run this inside a repo that already has a product.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Start project

Create the **smallest runnable project** the user asked for. Do not pick a framework for them. Do not add a product feature beyond hello + the checks needed to prove it runs.

## Is this the right skill?

Stop and use `explore-codebase` / `implement-change` if the workspace already has an application: a source tree with a manifest, lockfile, or more than bootstrap files (`README`, `LICENSE`, `.gitignore`, `AGENTS.md`).

If they asked to add an app inside a monorepo, stay in the package they named and match sibling packages.

## Stack

Use the language, kind (app / lib / CLI / service), and tools the user named.

If any of those are missing, ask **one** blocking question that lists the gaps. Do not recommend a trendy stack. Do not run a third-party `create-*` scaffolder unless they named that exact tool.

Prefer the official init for the named toolchain (`cargo init`, `go mod init`, `dotnet new`, language-native module init). Match the package manager they named.

## Create

1. Init the project with that official tool (or a minimal manifest if no init exists).
2. One entry point that runs.
3. One test that fails if the entry is broken, in the runner that toolchain already uses.
4. A root `README` with Install / Run / Test from commands you actually used.
5. Copy the first readable `AGENTS.md` template: `../explore-codebase/references/agents-template.md`, else `../../templates/AGENTS.md` when this pack's layout is intact. If neither is readable, write the Agent defaults list (verify before claiming; no secrets; match the repo; smallest change; no shared-history rewrite; no skipped tests) plus `## This repo` and `## Glossary`. Fill **This repo** from the commands you ran.

Load `engineering-bar` (paths in that skill). Climb **Minimum path**. No extra dependencies, no extra folders, no CI you were not asked for.

Do not commit secrets. Do not commit unless asked.

## Prove

Run **Install** if needed, then **Test**, then **Run** as a one-shot if that is cheap. Keep the output. Unverified if you could not run them.

## Done

1. Stack and kind
2. Files created
3. Commands run and results
4. Path of `AGENTS.md` / `README`

Next is `write-prd` if the product is still open, `shape-work` or `implement-change` for the first real feature — not a drive-by architecture.
