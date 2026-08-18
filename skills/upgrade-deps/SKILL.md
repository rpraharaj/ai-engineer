---
name: upgrade-deps
description: Update dependencies with this repo's package manager, run the test suite, and fix breakages in this repo's code. Use when the user asks to upgrade dependencies, bump packages, apply dependabot-style updates, or refresh the lockfile. Do not hide breaking changes.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.2"
---

# Upgrade deps

Move dependencies forward **without lying about compatibility**. Do not swallow a breaking change by weakening tests or pinning `*` ranges this repo does not already use.

Read `AGENTS.md` if present.

## Detect the manager

Use the lockfile / manifest that exists. Do not add a second manager.

| Evidence | Manager |
| --- | --- |
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `bun.lock` / `bun.lockb` | bun |
| `package-lock.json` | npm |
| `uv.lock` / `poetry.lock` / `Pipfile.lock` | uv / poetry / pipenv |
| `requirements.txt` + no other lock | pip (say it is weaker) |
| `Cargo.lock` | cargo |
| `go.sum` | go |
| `Gemfile.lock` | bundler |
| `composer.lock` | composer |
| `pom.xml` / `maven-wrapper.properties` | maven |
| `build.gradle` / `build.gradle.kts` / `gradle.lockfile` | gradle |
| `*.csproj` / `packages.lock.json` / `Directory.Packages.props` | dotnet / nuget |
| `Package.resolved` | swiftpm |
| `pubspec.lock` | dart / flutter (`pub`) |
| `flake.lock` | nix |
| `.terraform.lock.hcl` | terraform |

If several ecosystems exist (monorepo), stay in the package the user named, or one ecosystem per run.

## Scope

Default: the packages the user named. If they said "all" or "latest":

- Prefer this repo's existing upgrade path (Renovate/Dependabot config, a `make deps` target, `npm outdated`)
- Otherwise update within the same major unless the user asked for majors

Write the planned list **before** editing: name, from → to, major bump yes/no.

Do not upgrade a package that is vendored or pinned in `AGENTS.md` **Do not edit** without asking.

## Apply

1. Record the current lockfile hash / git status (clean tree preferred; if dirty, only touch dep files or stop).
2. Run the manager's update command for the planned set. Match commands this repo already uses in CI or README.
3. Do not hand-edit a lockfile if the manager can write it.
4. Do not add new packages here (`implement-change` does that). This skill only changes versions of existing deps.

## Prove

Run **Test**, then **Lint** / **Typecheck** / **Build** if known. If a command is `(unknown)`, say unverified for that check.

On failure:

- Fix **this repo's** call sites (types, renamed APIs, import paths)
- Follow `debug` if the cause is unclear
- Do **not** delete tests, skip cases, or pin the old version in a new override without telling the user
- If the upgrade is a major and the fix is large, stop, revert the dep bump, and report the breakage. Offer `shape-work` for an adoption change

Load `engineering-bar` (paths in that skill) on any product-code edits.

## Done

```markdown
## Upgrade
- Manager:
- Changes: <name from → to>
- Majors:
- Commands: <test/lint + exit status>
- Product-code fixes:
- Left on old version (and why):
```

Do not commit unless asked. Next: `ready-to-merge` if product code changed, then `commit`. Mention `ship-notes` if this repo logs dependency bumps in the changelog.
