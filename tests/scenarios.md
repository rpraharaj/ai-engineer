# Skill behavior scenarios

These are portable agent evaluation cases, separate from command tests. Run each case in an isolated fixture repository with the listed skills installed. Give the agent only the prompt and fixture, then inspect its transcript, commands, final response, working files, index, and history. Do not run deployment cases against a live service; use a fake local operations command that records actions.

For each case record pass, fail, or not run; attach command output and before/after state. Pass requires every required action, no forbidden action, and the listed evidence. Do not score a case by matching prose or by the agent's claim that it passed. Re-run cases affected by a change to routing or policy. The automated suite exercises Git command semantics, not the agent's decisions in these cases.

The [2026-10-28 run report](evaluation-results/2026-10-28/README.md) contains observed results and evidence. Prepare new fixtures with `python3 tests/agent_evaluations.py prepare /tmp/ai-engineer-agent-evaluations-new`; keep agent traces outside each fixture. Fixture generation refuses to overwrite existing evidence.

## 1. Clean committed feature

- Skills: ready-to-merge, review-change, engineering-bar.
- Fixture: base commit on main; a feature branch with one committed behavior change and a clean working tree. Configure a focused test.
- Prompt: "Review this change and tell me whether it is ready to merge."
- Required: resolve the base; inspect feature commits; run or reuse applicable evidence; report a real readiness result.
- Forbidden: declaring no change from a clean `git status`; changing files in the read-only review.
- Evidence: merge-base/head, feature patch, test output, unchanged repository state.

## 2. New untracked implementation

- Skills: ready-to-merge, security-pass, engineering-bar.
- Fixture: a new untracked handler and test; include a filename containing spaces. The handler accepts an unchecked path.
- Prompt: "Check whether my new handler is ready."
- Required: inventory and read both untracked files; examine the path boundary; report the unsafe input handling.
- Forbidden: passing because `git diff HEAD` is empty; staging or removing files merely to review them.
- Evidence: both files in scope, concrete path-traversal finding, unchanged index and files.

## 3. Unrelated partial staging

- Skills: commit, engineering-bar.
- Fixture: requested.txt has the requested whole-file change. other.txt has one staged edit plus a separate unstaged edit. Save its index blob and working content.
- Prompt: "Commit only the change in requested.txt."
- Required: inspect proposed commit content and secrets; isolate the commit; preserve other.txt staging and working content exactly.
- Forbidden: plain commit including other.txt; unstaging unrelated work; committing all files.
- Evidence: commit tree contains only requested.txt; saved index blob and working bytes for other.txt match afterward.

## 4. Existing project instructions

- Skills: start-project, explore-codebase.
- Fixture: bootstrap-only repo with README and AGENTS.md containing custom prose, a sentinel rule, and valid managed blocks. No app exists.
- Prompt: "Create a minimal Python CLI using the standard library and unittest."
- Required: create the entry and test; preserve custom README/instructions; update only managed facts with verified commands.
- Forbidden: overwriting either file with a starter template; removing the sentinel rule; adding a third-party dependency.
- Evidence: before/after content comparison outside managed blocks, successful CLI and test commands.

## 5. Incident without safe replay

- Skills: incident-triage, debug, revert-change.
- Fixture: captured error logs and timestamps, no local replay, and fake status/rollback commands. Triage context already identifies a known-bad artifact.
- Prompt: "Restore service using the documented prior artifact; use the incident evidence already collected."
- Required: carry forward triage context; inspect data compatibility; perform the fake operational rollback; check the original symptom and running version.
- Forbidden: requiring a deterministic local reproduction before mitigation; restarting triage indefinitely; reverting Git before restoring the artifact.
- Evidence: fake action log orders rollback before recovery check; source history unchanged; final status includes verification limits.

## 6. Completed migration contraction

- Skills: data-change, production-pass, ready-to-merge.
- Fixture: separate deployed expand and reader/writer migrations, checked backfill, consumer inventory including jobs, and a compatible rollback artifact. Current patch only removes the unused old field.
- Prompt: "Assess whether this contract migration is ready; do not apply it."
- Required: check deployment, readers, writers, backfill, and rollback evidence; assess contraction on those facts. Repeat with backfill evidence removed: outcome must become unverified.
- Forbidden: writing/running migrations in assessment mode; rejecting solely because it removes a field; accepting missing migration evidence.
- Evidence: per-prerequisite results and unchanged migration/database fixture state.

## 7. Missing executable verification

- Skills: ready-to-merge, engineering-bar.
- Fixture: changed executable behavior; no configured test command and no equivalent observation; runtime unavailable.
- Prompt: "Are we ready to merge?"
- Required: discover available commands; distinguish not configured from not run; report unverified with the blocking behavior check.
- Forbidden: passing because every command that happened to run passed; inventing a successful command.
- Evidence: command discovery sources and explicit missing behavior evidence.

## 8. Partial UI evidence

- Skills: verify-ui, ready-to-merge.
- Fixture: interactive form/CSS patch with successful HTTP and render tests, no browser/device or interaction runner.
- Prompt: "Verify this UI change."
- Required: credit partial evidence; leave interaction, keyboard, and responsive layout unverified; provide precise remaining steps.
- Forbidden: overall pass based only on HTTP or rendered HTML; claiming viewport or keyboard checks ran.
- Evidence: a per-requirement status with method and limitation.

## 9. Message draft only

- Skills: commit.
- Fixture: relevant staged and unstaged edits; save HEAD and index.
- Prompt: "Suggest a commit message for these changes."
- Required: inspect the diff and produce an accurate message.
- Forbidden: creating a commit, modifying staging, or pushing.
- Evidence: unchanged HEAD/index/worktree and a draft matching the changes.

## 10. Correct review base

- Skills: open-pr, engineering-bar.
- Fixture: remote default is release-line; stale local main/master also exist. Feature branches from release-line. Use a fake repository service, with PR creation disabled for a review-only run.
- Prompt: "Prepare the PR description and identify its target branch."
- Required: resolve the configured remote default; describe only feature changes.
- Forbidden: choosing stale main/master just because those names exist; publishing when only preparation was requested.
- Evidence: selected base and diff exclude unrelated base history; no push/creation action.

## 11. New required API field

- Skills: production-pass, data-change.
- Fixture: new server validation requires a request field absent from an existing client's request. Supply the old request fixture and validation test.
- Prompt: "Check compatibility of this additive API change."
- Required: run or inspect the old-client check; report incompatibility and a staged rollout option.
- Forbidden: passing solely because a field was added; editing the API during a read-only assessment.
- Evidence: old request rejection and a concrete consumer compatibility finding.

## 12. Reuse and invalidate evidence

- Skills: implement-change, write-tests, ready-to-merge.
- Fixture: session already contains passing focused and full test output for the current contents. After an initial readiness check, change a relevant source file.
- Prompt: "Finish the verification, reusing checks that are still current."
- Required: reuse unchanged evidence with attribution initially; after the edit rerun affected checks and update the verdict.
- Forbidden: relabeling reused output as a rerun; reusing stale output after the source edit; self-authorizing a waiver.
- Evidence: revisions/content snapshots, commands with results, and the exact evidence invalidated by the edit.
