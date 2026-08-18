# Working on this pack

This repository is **ai-engineer**, a portable skill pack (home: https://rajeshpraharaj.com/). Skills must work in any coding agent that loads a `SKILL.md` folder (name + description frontmatter, markdown body).

## Format

- One directory per skill under `skills/<name>/`.
- `name` in frontmatter must match the directory name.
- Frontmatter fields allowed: `name`, `description`, `license`, `metadata`. Optional `compatibility` only for real environment needs (e.g. `git`).
- Do not add host-only frontmatter (`when-to-use`, `argument-hint`, `disable-model-invocation`, `model`, `allowed-tools`).
- Do not name host products, host tools, or host slash commands in skill bodies.
- Write procedures for one agent with a filesystem, a shell, and (usually) git.
- Keep each `SKILL.md` under 500 lines. Put long checklists and copy-templates in `references/`.
- `description` must say what the skill does and when to use it (max 1024 characters).

## One home per fact

- Always-on defaults live in `templates/AGENTS.md`. Keep `skills/explore-codebase/references/agents-template.md` byte-identical (`python3 scripts/validate.py` checks).
- Quality checks and secret-file patterns live in `skills/engineering-bar/SKILL.md`.
- Other skills point at those by name. Do not paste them in full.

## Validation

```bash
python3 scripts/validate.py
```

## Install locally

```bash
./scripts/install.sh
```
