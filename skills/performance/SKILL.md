---
name: performance
description: Investigate slowness with measure-first profiling, or guard a diff for regressions (N+1, unbounded work, heavy imports). Use when something is slow, latency or p99 is high, the user asks to profile or optimize, or ready-to-merge asks for a performance guard.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Performance

Two modes. Pick one and say which.

| Mode | When |
| --- | --- |
| **Investigate** | User says it is slow, names a page/API/job/query, or asks to profile |
| **Guard** | `ready-to-merge` dispatched you, or the user asks whether this change will make things slower |

Do not rewrite code on a hunch. Guess-caching is a fail (`engineering-bar`).

Read `AGENTS.md` if present.

## Guard

Collect the current diff (working tree vs `HEAD`, or the branch the user named).

Fail the guard if the diff introduces any of these without a matching bound, index, or existing repo pattern that already does the same thing safely:

- Query, RPC, or file I/O inside a loop over an unbounded or request-sized list (N+1)
- Missing pagination / limit on a newly exposed list
- Full-table or full-collection scan (filter after fetch, `SELECT *` over a large set with no predicate the DB can use)
- New heavy import or bundle on a hot route or first paint
- Sync work on a request/UI path that this repo usually defers
- UI layout jump from images/embeds/fonts with no reserved size

If none apply, **pass** and list what you checked. Do not suggest micro-optimizations (memoization, extra indexes, caches) unless the diff already created the problem.

Output:

```markdown
## Performance guard: pass | fail
- Checked: …
- Fails: <file:line + why, or none>
```

## Investigate

### 1. Name the surface

Page, API route, query, job, screen, or pipeline. If the user did not name one, pick the hottest path in the complaint and say so.

### 2. Measure first

Establish a baseline **number** with whatever this repo already has:

- Existing benchmark or load test
- Database `EXPLAIN` / query plan
- Language profiler already in the repo
- Server/access logs with durations
- Metrics the service already emits
- If the surface is a URL **and** a browser or tracing tool is available in this session, use it

If you cannot measure, say **unverified** and collect the cheapest signal (one timed request, one query plan). Do not optimize yet.

Write: surface, metric, baseline value, how you measured.

### 3. Classify

One primary class: network, parse/render, CPU, I/O, lock/contention, N+1, payload size, cold start, GC. Evidence or it is a guess — label guesses.

### 4. One change

Change one thing aimed at that class. Load `engineering-bar` (paths in that skill) so the fix stays small and correct.

Add a regression pin when this repo has a place for it (benchmark, test assertion on query count, budget file). Use `write-tests` for that pin.

### 5. Measure again

Same method as the baseline. Stop if the metric is inside the budget the user named, or inside this repo's documented budget. Otherwise report the next cheapest win — do not stack three optimizations.

## Done (investigate)

1. Surface + metric + before/after + method
2. Bottleneck class
3. What you changed (or why you changed nothing)
4. Commands/output

Do not commit unless asked.
