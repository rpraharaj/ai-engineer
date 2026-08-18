---
name: cut-release
description: Cut a version and run this repository's existing release or deploy path. Use when the user asks to release, deploy, tag, publish, or ship to production. Detect the path from the repo. Do not invent a pipeline. Do not publish unless asked.
license: MIT
compatibility: Requires git
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Cut release

Publish **this version** using machinery this repo already has. Do not invent a deploy system. Do not enable paid cloud plans, change billing, or buy domains. `ship-notes` writes the notes; this skill runs the release.

Read `AGENTS.md` if present. If `git` is missing, stop.

## Detect the path

Look for the first match that this repo already uses (README, Makefile, `package.json` scripts, CI job named release/deploy, existing tags):

- A documented **Release** / **Deploy** command
- `make release` / `make deploy` / `just release` (only if that target exists)
- A release script in the manifest (`release`, `deploy`) this repo's CI already runs
- A releaser already configured (goreleaser, semantic-release, changesets, cargo-release, or this repo's equivalent)
- Host CLI release (`gh release create`, `glab release create`) only if that is how this repo already ships

If you cannot find a path, write the notes with `ship-notes` if needed, print the exact commands a human should run, and **stop**. Do not guess `npm publish` or a cloud deploy.

## Preconditions

- Working tree clean enough for this repo's release (no leftover secret files — `engineering-bar` **Secret files**)
- User asked to publish / deploy / tag. Notes-only is `ship-notes`.
- If they have not run `ready-to-merge` on this change, say so. Do not block a notes+tag they insisted on.

## Run (only what they asked)

1. `ship-notes` first if the changelog is stale and this repo keeps one.
2. Version bump only if they asked **or** the existing release script does it. One version file, this repo's scheme.
3. Run the detected release/deploy command. Keep the output.
4. Tag only if they asked or the script tags. Do not `--force` a tag. Do not delete a published tag.
5. Push tags / publish only if they asked and a remote exists.

Do not `npm publish` / `pypi upload` / store submit unless that command is the detected path **and** they asked to publish. Do not change account, billing, or plan settings.

If the command would spend money or require a paid upgrade, **stop** and say what the user must do in their dashboard.

## Done

```markdown
## Release
- Path (command):
- Version / tag:
- Notes: <path or n/a>
- Published: yes | no | not asked
- Output:
```

Do not merge a PR unless they asked. Next is usually `handoff` or stop.
