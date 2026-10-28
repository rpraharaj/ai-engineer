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
