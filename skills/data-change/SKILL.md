---
name: data-change
description: Plan and apply a schema, API, or data migration using expand-then-contract. Use when adding or changing columns, indexes, events, protobuf or OpenAPI shapes, or backfills, and when ready-to-merge sees a contract change. Do not expand and contract in the same change.
license: MIT
metadata:
  pack: ai-engineer
  version: "1.1"
---

# Data change

Change stored or published shape **without breaking current readers**. Do not mix a destructive contract change with the code that requires the new shape.

Read `AGENTS.md` if present.

## Mode

When invoked by a review or `ready-to-merge`, assess the existing plan, migration, and evidence only; do not write or execute migrations. In implementation mode, apply only the authorized current step. Reuse the caller's scope through `engineering-bar` **Shared procedures**.

## Detect how this repo migrates

From existing folders and manifests, use the tool already here. Do not add a new migrator.

Look for (first match that already exists): `prisma/migrations`, `alembic`, Django `migrations/`, `db/migrate`, `supabase/migrations`, `flyway`, `goose`, `liquibase`, `knex`, TypeORM/SQLAlchemy migrations, `sqlx`, `golang-migrate`, raw SQL next to existing SQL migrations, OpenAPI/protobuf/avro/json-schema generators this repo already runs.

If none exist and the user really needs a schema change, stop and say so. Do not invent a framework.

## Classify the step

| Kind | Examples | This change may |
| --- | --- | --- |
| **Expand** | add nullable column, add table, add index concurrently if the DB allows, add field to a response, add event field with a default | yes |
| **Backfill** | populate the new column/field for old rows | yes, after expand is deployed or in the same expand if it is online-safe and bounded |
| **Contract** | drop column, make NOT NULL, rename, remove field, change meaning | **not** in the same change as the code that still needs the old shape, and not with expand |

If the user asked for a rename or drop, split the work:

1. Expand (add the new name, write both)
2. Later change: readers use the new name
3. Later change: contract (drop the old)

Say that plan and only implement the step they are on (default: expand).

## Contract prerequisites

Before contraction, require evidence that expand is deployed, the backfill is complete and checked, and all supported readers and writers have migrated (including jobs and external consumers). Verify old fields no longer receive writes. Document a rollback that does not redeploy code requiring the removed shape. If any of these are unknown, contraction is unverified and must not run. An accepted versioned breaking API change still needs an explicit consumer and rollout plan.

## Plan before files

Write this (reply is enough unless the user asked for a file):

```markdown
## Data change plan
- Tool:
- Step: expand | backfill | contract
- Online?: <locks, rewrite risk, estimated size>
- Expand:
- Backfill: <bounded batches / pause / how to resume, or n/a>
- Contract (later):
- Rollback:
- Verification: <query or test that proves old and new readers work>
```

Destructive contract in the same change as expand is a fail. Unbounded backfill on a large table without batches is a fail.

## Apply (only the current step)

- Match existing migration naming, directory, and review comments in this repo.
- Prefer additive, reversible operations the existing migrations use.
- Do not run a destructive migration against a shared or production database unless the user explicitly asked and the plan says so.
- For API/event contracts, keep old fields until the contract step; add new ones alongside.
- Load `engineering-bar` (paths in that skill). For a backfill job, also load `production-pass` and apply only Timeouts, Bounds, and Visibility. Do not let `production-pass` start a new migration plan.

Prove with this repo's tests (`write-tests` if a migration test pattern exists) plus the verification query/check from the plan.

## Done

1. Mode (assessment or implementation), plan, and step assessed or executed; report missing evidence as unverified
2. Files added
3. Commands run (including migrate/test only when authorized) and results
4. What must happen in a later change (contract, leftover dual-write)

Do not commit unless asked.
