---
name: lean-review
description: Review a diff or a whole repo for unnecessary complexity only — delete-list of reinvented stdlib, unneeded deps, speculative abstractions. Use when the user asks what to delete, whether this is over-engineered, a simplify review, or a bloat audit. Complements review-change. Do not edit product code.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Lean review

Read-only hunt for **complexity that does not need to exist**. Not a correctness, security, or performance review — those are `review-change`, `security-pass`, and `performance`.

Load `engineering-bar` (paths in that skill) and apply **Minimum path** + **Never cut**.

## Target

- User said "whole repo", "audit", or "what can we delete from this tree" → scan the tree (skip `node_modules`, `.git`, vendored/build output).
- Otherwise follow `engineering-bar` **Shared procedures** for scope and evidence, including branch commits and relevant untracked files.

If the target is empty, say so and stop.

## Tags

One line per finding:

`<file>:<line>: <tag> <what to cut>. <what replaces it>.`

| Tag | Means |
| --- | --- |
| `delete` | Dead code, unused flexibility, speculative feature. Replacement: nothing. |
| `stdlib` | Hand-rolled thing the language/runtime already ships. Name the function. |
| `native` | Code or dependency doing what the platform already does. Name the feature. |
| `yagni` | Abstraction with one implementation, config nobody sets, layer with one caller. |
| `shrink` | Same logic, fewer lines. Show the shorter form. |

Do not flag:

- Trust-boundary validation, data-loss error handling, authz, secrets, or accessibility
- The one focused test `write-tests` added for new logic
- Correctness/security/perf bugs — name `review-change` / `security-pass` / `performance` and leave them out of this list

## Output

Rank biggest cut first. End with `net: -<N> lines` (and `-<M> deps` if a dependency can go). Nothing to cut: `Lean already.` and stop.

Do not apply the cuts unless the user asked — that is `refactor-safely` or `implement-change`.
