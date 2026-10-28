# ai-engineer: Portable Skills for AI Coding Agents

**33 reusable agent skills for software engineering: understand a codebase, plan a change, implement it, test it, review it, and ship it.**

ai-engineer is an open-source collection of `SKILL.md` workflows for AI coding agents. Each skill gives an agent a specific job, a procedure to follow, boundaries to respect, and evidence to provide before calling the work complete. Use the pack across languages and repositories with an agent that supports loading skill folders.

[![MIT license](https://img.shields.io/badge/license-MIT-0B6E4F.svg)](LICENSE)
[![33 agent skills](https://img.shields.io/badge/agent_skills-33-1B4D89.svg)](#skill-catalog)
[![Portable Markdown skills](https://img.shields.io/badge/format-SKILL.md-5C4D7D.svg)](#how-agent-skills-work)

[Quick start](#quick-start) · [Choose a skill](#choose-your-first-skill) · [All 33 skills](#skill-catalog) · [Troubleshooting](#troubleshooting) · [Contribute](#contributing)

## What does ai-engineer help you do?

Use it when you want an AI coding agent to:

- **Understand your repository before editing.** Discover the actual stack, entry points, conventions, and check commands.
- **Turn an unclear request into implementable work.** Write requirements, technical designs, or a small task with verifiable acceptance checks.
- **Make and verify a focused change.** Reproduce bugs, preserve unrelated work, add useful tests, and check the result.
- **Review and deliver with evidence.** Assess security, performance, compatibility, and production concerns relevant to the change, then commit or publish when requested.

The procedures adapt to the repository rather than prescribing a framework or a test runner. Small, clear changes can go straight to implementation; you do not need a PRD for a typo fix.

The pack supplies instructions. Your coding agent supplies the model, permissions, shell, and any integrations needed for the task. Installing it does not start a service or provision infrastructure.

## Quick start

### 1. Check the requirements

| Requirement | When you need it |
| --- | --- |
| An agent that can load `SKILL.md` folders | To use the skills; discovery paths and invocation syntax depend on your agent |
| Git and a POSIX-compatible shell | To clone this repository and run the installation script |
| Python 3 | To run the pack's validator and automated tests; no third-party Python packages are required |
| Your product's existing toolchain | To build, test, or run the product you ask the agent to work on |

### 2. Install the skills on your machine

```sh
git clone https://github.com/rpraharaj/ai-engineer.git
cd ai-engineer
python3 scripts/validate.py
./scripts/install.sh
```

Successful validation prints:

```text
ok: 33 skills
```

The installer creates one symlink per skill in `~/.agents/skills/`, pointing to this checkout. It skips an existing regular file or directory with the same name and replaces an existing symlink. Keep the checkout at its installed location so the links remain valid.

If your agent scans a different skills directory, follow its skill-discovery instructions and link the installed skill folders there. Start a new session or reload skills as your agent requires. See [troubleshooting](#troubleshooting) if the skills are not discovered.

### 3. Open your product repository and try one task

Ask your agent:

> Use explore-codebase to map this repository. Discover its real install, run, test, format, lint, typecheck, and build commands. Preserve existing instructions when updating AGENTS.md.

The result should identify the stack, important paths, available commands, and what was actually run. Unknown commands should be labeled as unknown.

Then try a small, concrete request:

> Use implement-change to add the requested behavior using this repository's patterns. Add appropriate tests and show the commands and results. Do not commit yet.

Replace “the requested behavior” with your actual task. You can request a skill by name in plain language; use a special invocation only if your agent supports it.

### 4. Keep repository instructions alongside the code

[`templates/AGENTS.md`](templates/AGENTS.md) contains the defaults and repository-facts sections used by the pack. The `explore-codebase` skill can create this file or update its managed sections while preserving your existing prose.

If you maintain the file manually, merge the relevant sections into an existing `AGENTS.md` and fill commands from your repository. Keep your team's instructions; avoid replacing the file wholesale with a starter template.

## Choose your first skill

You can describe the task naturally or name a skill explicitly. These examples show both the request and the result to expect.

| Your situation | Example request | Expected result |
| --- | --- | --- |
| You are new to a repository | “Use explore-codebase before we change anything.” | A repository map, real commands, and updated managed facts in AGENTS.md |
| The request is vague | “Use shape-work to scope password reset. Do not implement yet.” | Scope, acceptance checks, an approach, and blocking questions if needed |
| One small behavior needs changing | “Use implement-change to reject empty titles.” | A focused change with appropriate verification |
| A bug needs a cause | “Use debug to reproduce and fix this error.” | A reproduction or incident baseline, cause, fix, and regression evidence |
| You want a review without edits | “Use review-change on this branch. Report findings only.” | Findings tied to the actual change, including relevant local files |
| You want to know whether work is complete | “Use ready-to-merge and report any missing verification.” | Ready, not ready, or unverified, supported by check results |
| Production is affected | “Use incident-triage with these logs and deployment details.” | Impact, evidence, a stabilization action, and the next step |
| Someone else needs to continue | “Use handoff to capture what is done and what remains.” | A continuation brief with state, commands, risks, and next steps |

Name the target branch, files, error, or acceptance criteria when you know them. State whether you want advice, a read-only review, implementation, a commit, or publication so the agent can stay within your request.

## Recommended software engineering workflows

Use only the steps relevant to your task. These are common paths through the skills, rather than a mandatory sequence for every change.

| Work | Suggested path |
| --- | --- |
| Existing repository, clear change | `explore-codebase` if unfamiliar → `implement-change` → appropriate tests → `ready-to-merge` |
| Large or unclear initiative | `write-prd` → `write-architecture` if boundaries change → `write-design` → `write-dev-tasks` → implement one slice |
| Bug or failing CI | `debug` or `fix-ci` → regression verification → `ready-to-merge` |
| New project | `start-project` with your named stack → plan and implement the first feature |
| Review and delivery | `review-change` → address findings → `commit` → `open-pr`, when requested |
| Release or incident | `ship-notes` → `cut-release` for a requested release; `incident-triage` → `revert-change` or `debug` for an incident |

UI changes also need `verify-ui`. The merge gate calls for security, performance, production, and data checks when the change warrants them. A commit, pull request, or release requires the corresponding authorization; requesting a plan or review does not authorize publication.

## Skill catalog

Every skill below links to its full procedure. Install the whole pack to retain shared standards, referenced skills, and supporting templates.

### Requirements, design, and planning

| Skill | Use it to | Deliverable |
| --- | --- | --- |
| [`write-prd`](skills/write-prd/SKILL.md) | Define the user problem, audience, goals, and requirements | Product requirements with testable success checks |
| [`write-architecture`](skills/write-architecture/SKILL.md) | Describe durable system boundaries, data, and control flow | System architecture document |
| [`write-design`](skills/write-design/SKILL.md) | Design one initiative using the repository's actual patterns | Technical design with contracts, risks, and delivery slices |
| [`write-dev-tasks`](skills/write-dev-tasks/SKILL.md) | Break agreed work into ordered implementation tasks | Tasks with dependencies, scope, and acceptance checks |
| [`record-decision`](skills/record-decision/SKILL.md) | Capture one expensive-to-reverse technical choice | Short architecture decision record (ADR) |

### Codebase exploration and implementation

| Skill | Use it to | Deliverable |
| --- | --- | --- |
| [`explore-codebase`](skills/explore-codebase/SKILL.md) | Understand an unfamiliar repository | Map, real commands, and managed AGENTS.md facts |
| [`start-project`](skills/start-project/SKILL.md) | Start an empty project using the stack you name | Minimal runnable entry point, test, and setup documentation |
| [`shape-work`](skills/shape-work/SKILL.md) | Scope one change before implementation | In/out of scope, acceptance checks, approach, and first slice |
| [`implement-change`](skills/implement-change/SKILL.md) | Apply a scoped feature or code change | Focused implementation with verification results |
| [`explain-code`](skills/explain-code/SKILL.md) | Understand how one existing feature or path works | Entry points, data flow, tests, and likely edit locations |
| [`debug`](skills/debug/SKILL.md) | Diagnose and fix a known failure | Reproduction or incident evidence, cause, fix, and proof |
| [`write-tests`](skills/write-tests/SKILL.md) | Add tests at the interfaces callers actually use | Focused behavior tests with independent expected results |
| [`refactor-safely`](skills/refactor-safely/SKILL.md) | Clean up structure while preserving behavior | Mechanical changes checked against a passing baseline |
| [`write-docs`](skills/write-docs/SKILL.md) | Document existing behavior and operations | README, API documentation, or runbook grounded in code |
| [`upgrade-deps`](skills/upgrade-deps/SKILL.md) | Update existing dependencies with the repository's manager | Version changes, compatibility fixes, and check results |

### Quality checks and code review

| Skill | Use it to | Deliverable |
| --- | --- | --- |
| [`engineering-bar`](skills/engineering-bar/SKILL.md) | Apply the shared engineering standards | Assessment of relevant correctness, hygiene, safety, and operability requirements |
| [`ready-to-merge`](skills/ready-to-merge/SKILL.md) | Decide whether the current change has enough verification | Readiness verdict with evidence, gaps, and any user-approved waivers |
| [`review-change`](skills/review-change/SKILL.md) | Review a local, branch, or pull request change | Read-only findings with locations and suggestions |
| [`lean-review`](skills/lean-review/SKILL.md) | Find unnecessary complexity in a diff or repository | Ranked simplifications and what would replace them |
| [`performance`](skills/performance/SKILL.md) | Investigate slowness or guard a change against regressions | Measured before/after results or a focused regression assessment |
| [`security-pass`](skills/security-pass/SKILL.md) | Review changed trust boundaries and reachable surfaces | Concrete authorization, injection, secret, or privacy findings |
| [`production-pass`](skills/production-pass/SKILL.md) | Check operational risks in a change | Timeout, retry, idempotency, bounds, visibility, rollback, and compatibility assessment |
| [`data-change`](skills/data-change/SKILL.md) | Plan, implement, or assess a staged schema/API migration | Expand/backfill/contract plan and verification for the current step |
| [`verify-ui`](skills/verify-ui/SKILL.md) | Exercise changed screens, shared surfaces, and states | Interaction, layout, accessibility, and remaining-verification results |
| [`fix-ci`](skills/fix-ci/SKILL.md) | Reproduce and repair a failing pipeline check | Cause-level fix and rerun of the failing check |

### Delivery, operations, and continuation

| Skill | Use it to | Deliverable |
| --- | --- | --- |
| [`commit`](skills/commit/SKILL.md) | Commit the requested changes, or draft a message when that is all you ask for | Reviewed commit or message draft; unrelated staging preserved |
| [`open-pr`](skills/open-pr/SKILL.md) | Prepare or publish a pull request or merge request | Change summary, test plan, risk, and PR/MR link when published |
| [`resolve-conflicts`](skills/resolve-conflicts/SKILL.md) | Complete an in-progress merge or rebase | Resolved conflicts, intent trade-offs, and check results |
| [`ship-notes`](skills/ship-notes/SKILL.md) | Describe changes in a real commit range | Changelog entry or release notes with migration callouts |
| [`cut-release`](skills/cut-release/SKILL.md) | Run a requested release using existing repository machinery | Release command, version/tag, output, and publication status |
| [`incident-triage`](skills/incident-triage/SKILL.md) | Respond to a production or customer-facing incident | Impact snapshot, stabilization choice, evidence, and next action |
| [`revert-change`](skills/revert-change/SKILL.md) | Undo a known source change or perform an operational rollback | Verified undo or service recovery, with remaining limits stated |
| [`handoff`](skills/handoff/SKILL.md) | Continue work with another person or session | Goal, completed work, open tasks, real checks, and landmines |

## How agent skills work

A skill is a folder containing a `SKILL.md` file with `name` and `description` frontmatter followed by a Markdown procedure. Supporting resources travel with the folder:

```text
skills/
  debug/
    SKILL.md
  engineering-bar/
    SKILL.md
    references/
      change-scope.md
      evidence.md
  write-prd/
    SKILL.md
    references/
      prd-template.md
```

Agents with skill discovery can use the name and description to select a matching procedure. Exact loading behavior depends on the agent. Without automatic discovery, an agent that can read files can still follow a procedure you explicitly point it to.

The pack keeps shared information in specific places:

| Source | Owns |
| --- | --- |
| [`templates/AGENTS.md`](templates/AGENTS.md) | Persistent defaults and repository facts |
| [`engineering-bar`](skills/engineering-bar/SKILL.md) | Quality standards and secret-file rules |
| [Change scope](skills/engineering-bar/references/change-scope.md) | Branch/base selection, local edits, and untracked-file coverage |
| [Verification evidence](skills/engineering-bar/references/evidence.md) | Result statuses, evidence reuse, and readiness requirements |
| Individual skill folders | Task procedures and their supporting resources |

A passing command is evidence for what it tests. For example, HTTP or render tests cannot establish keyboard behavior or responsive layout on their own. Missing evidence should remain visible as unverified.

## Install for a team, update, or remove

### Install in one product repository

For a first installation, run these commands from your product repository. Replace `/path/to/ai-engineer` with the pack checkout:

```sh
mkdir -p .agents/skills
cp -R /path/to/ai-engineer/skills/* .agents/skills/
```

If `.agents/skills/` already contains skills with the same names, review and merge those folders before copying. This command can overwrite matching files. Use `explore-codebase` to create or update `AGENTS.md`, or merge the [template](templates/AGENTS.md) manually.

Commit the copied skills with your product if you want teammates to share a reviewed version. Copies remain on that version until you deliberately update them; machine-wide symlinks follow the source checkout. A submodule is another option if your team already manages dependencies that way.

### Update a machine-wide installation

From the ai-engineer checkout, review any local edits before updating:

```sh
git pull --ff-only
python3 scripts/validate.py
./scripts/install.sh
```

Existing symlinks see updated skill content in the checkout. Rerunning the installer also links any newly added skills. Reload skills in your agent when needed. Repository-local copies require a separate reviewed update.

### Remove an installation

For a machine-wide installation, remove only the symlinks that point to this pack, including any mirrors you created in agent-specific directories. Keep the checkout until you have removed or updated those references. There is no background service to stop.

For a repository-local installation, remove only the skill folders you copied from this pack and review the change in Git. Keep your product's `AGENTS.md`; it may contain team instructions and useful repository facts.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| The agent cannot find a skill | Confirm its configured discovery directory contains the skill folder and SKILL.md. Reload skills or start a new session if needed. |
| The installer says “skip” | A regular file or directory already occupies that skill name. Inspect it and decide whether to keep, merge, or replace it; the installer leaves it alone. |
| A skill link is broken | The source checkout may have moved or been deleted. Run the installer from the intended checkout, then verify any agent-specific mirrors. |
| The agent chooses the wrong workflow | Name the skill and target explicitly. Report the request and the skill it selected so the routing description can be improved. |
| Commands in AGENTS.md are unknown or stale | Ask explore-codebase to rediscover commands from the current repository and update its managed facts. |
| The result is “unverified” | Read the stated gap: a missing runtime, service, browser, or test can prevent a supported completion claim. Run the missing check or supply the required evidence. |
| A review includes unrelated work | Identify the requested branch/files and exclusions. The shared scope procedure requires preserving unrelated files and staging. |

For reproducible problems, [open an issue](https://github.com/rpraharaj/ai-engineer/issues) with the skill name, request, expected result, actual result, and relevant redacted output.

## Validation, tests, and evaluation results

From the pack root:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

| Check | What it establishes |
| --- | --- |
| Structural validator | Frontmatter, names, length limits, concrete bundled-resource references, portability checks, README coverage, and identical shared templates |
| 30 automated tests | Validation failure cases, documented Git command behavior, and evaluation-fixture preconditions/state capture |
| 12 agent-evaluation scenarios | Observed agent behavior against required actions, forbidden actions, and independent state checks in a recorded run |

Read the [scenario rubrics](tests/scenarios.md) and the [2026-10-28 evaluation report](tests/evaluation-results/2026-10-28/README.md). The report includes command traces, before/after state, and corrected-fixture reruns. These observations describe that run; they do not guarantee behavior for every agent or input.

To prepare fresh disposable fixtures, choose a destination that does not already exist:

```sh
python3 tests/agent_evaluations.py prepare /tmp/ai-engineer-agent-evaluations-new
```

Fixture generation does not invoke an agent. Follow the rubrics to run and grade each case separately. Expected failures inside deliberately broken fixtures are part of the evaluations; the pack's own automated suite must pass.

## Frequently asked questions

### Does this work with my coding agent?

Use the pack with an agent that loads SKILL.md folders, or explicitly point a file-reading agent to a skill. Check your agent's discovery and invocation settings. The pack's bodies use filesystem, shell, and Git procedures without requiring a particular agent product.

### Do I need an API key or a paid service?

The pack's installer, validator, and tests require no API key or paid service. Your chosen agent has its own access requirements. Individual tasks may need the accounts or integrations your product already uses, such as access to a Git hosting service to publish a pull request.

### Can I use only a few skills?

You can ask for only the skills relevant to your work. Install the whole pack so shared standards, linked procedures, and templates remain available. If distributing a subset, include its referenced skills and resources and disclose anything missing.

### How is AGENTS.md different from SKILL.md?

AGENTS.md holds persistent repository instructions and known commands. SKILL.md describes how to perform one kind of task. The two work together: a debugging procedure uses your repository's actual test command rather than inventing one.

### Will the agent commit, push, or deploy automatically?

The skills distinguish drafting, reviewing, editing, committing, and publishing. A message-draft request should produce a draft; a read-only review should preserve files. Commit and publication actions depend on what you authorize. Review the agent's actual actions and permissions when using it.

### Can I adapt the skills for my team?

Yes. The [MIT license](LICENSE) permits use and modification, including commercial use, with its license conditions. Keep team-specific commands in AGENTS.md and shared quality standards in their existing home so changes are easier to maintain.

## Contributing

Contribute a real engineering task, a reproducible routing problem, a useful template improvement, or a clearer procedure. Start with [AGENTS.md](AGENTS.md), the pack's authoring contract.

1. Use one folder per skill under `skills/<name>/`, with a matching frontmatter name and a description saying what it does and when to use it.
2. Keep SKILL.md under 500 lines. Put longer resources in the skill's supporting folders; reference shared defaults and standards instead of duplicating them.
3. Keep procedures portable: no host-only frontmatter, product-specific tool names, or mandatory multi-agent orchestration in skill bodies.
4. Add the skill to this catalog and include focused tests or evaluation cases when behavior changes.
5. Run the validator and full test suite shown above. For skill-policy or routing changes, rerun the affected agent evaluations as well.
6. Open a pull request explaining the task, scope, behavior change, and verification.

The validator uses a dependency-free YAML subset: plain strings, JSON-compatible double-quoted strings, YAML single-quoted strings, and a two-space-indented `metadata` mapping of strings. Quote numeric/boolean values and strings containing a colon followed by whitespace. Use single-line descriptions; block scalars, anchors, and flow collections are outside this pack's authoring subset.

Keep [`templates/AGENTS.md`](templates/AGENTS.md) and [the bundled exploration template](skills/explore-codebase/references/agents-template.md) byte-identical. Add tests for validator or installation behavior without weakening existing checks.

If you are unsure whether something belongs, [open an issue](https://github.com/rpraharaj/ai-engineer/issues) with the job you want an agent to perform.

## Project home and license

Project home: [rajeshpraharaj.com](https://rajeshpraharaj.com/). Contributions are welcome through [the repository](https://github.com/rpraharaj/ai-engineer).

Released under the [MIT license](LICENSE). You can use, adapt, and share the pack under its terms.
