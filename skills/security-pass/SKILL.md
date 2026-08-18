---
name: security-pass
description: Threat-model this diff only — new reachable surface, authorization, injection, secrets, and PII. Use when the change touches auth, input, files, HTML, URLs, or secrets, when ready-to-merge dispatches a security pass, or when the user asks for a security review of the change.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Security pass

Adversarial review of **this delta**, not a company-wide audit. Do not edit product code unless the user asked you to fix what you found.

Read `AGENTS.md` if present. Load `engineering-bar` (paths in that skill) for Security + Secret files; this skill is the method for walking them.

## Collect

Diff vs `HEAD` or the branch the user named. Inventory:

- New or changed reachable surfaces (HTTP routes, RPC, jobs that consume untrusted payloads, CLI flags, UI actions)
- Trust boundaries crossed (client → server, webhook → app, file → parser, query → HTML)
- Authn/authz code paths
- Secret and PII handling (logs, fixtures, client bundles, storage)

If the inventory is empty, report **no new reachable surface** and stop (still scan the diff for leaked secrets).

## For each new or changed surface

Walk in order. A "fail" needs `file:line` and a one-line attack or leak.

1. **Authorization** — Is the action allowed for this principal? Authn alone is a fail if this repo uses auth. IDOR: can the caller swap an id?
2. **Untrusted input** — Query, path, header, body, file name, HTML, URL. Follow it to sinks: SQL/ORM, command, path join, template/HTML, redirect, deserializer, eval.
3. **Injection / traversal** — Parameterized queries or the repo's equivalent. No shell string concat. No path built from user input without a jail. No HTML from user input without the repo's encoder.
4. **SSRF / outbound** — User-controlled URLs must not hit internal networks unless this repo already has a checked allow-list.
5. **Uploads** — Type, size, path, and execution risk (stored where the server might serve or run them).
6. **Secrets** — No new secrets in source, logs, errors, or client bundles. Compare to how this repo already loads secrets.
7. **PII** — New personal data is minimized, access-controlled, and not logged in full.

Skip items the diff cannot hit. Do not file theoretical issues with no path from this change.

## Severity

- **bug** — exploitable or a secret/PII leak
- **suggestion** — missing defense this repo already uses elsewhere
- **nit** — hardening with no current path

## Output

```markdown
## Security pass: pass | fail

### Inventory
- Surfaces:
- Boundaries:

### Findings
### Finding 1 — Severity: bug
- File: path:line
- Description:
- Suggestion:

### Secrets
pass | fail
```

If the user asked you to fix fails, use `implement-change` (smallest fix, tests via `write-tests`). Do not "fix" security by deleting the check or broadening authz.
