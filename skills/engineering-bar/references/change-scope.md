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
