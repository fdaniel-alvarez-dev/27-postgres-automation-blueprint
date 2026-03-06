# Backup & restore drill

## Goal

Make recovery predictable by practicing it end-to-end, including verification.

## When to use

- Before a risky change (schema change, upgrade, migration)
- After changing backup tooling or retention policies
- On a regular cadence (e.g., monthly) to keep muscle memory fresh

## Prechecks

- Ensure the lab is running: `make up`
- Seed deterministic data for verification: `make seed`
- Confirm a replica is healthy: `make check`

## Procedure

```bash
make backup
make restore
```

## Rollback

This drill restores into an isolated verification database (`appdb_verify`) and does not overwrite the primary lab database.

If something goes wrong:
- rerun `make restore` after fixing the root cause
- or cleanup the verification database by rerunning the restore (it drops/recreates `appdb_verify`)

## Verification

- The restore step runs a small query: `select count(*) from demo_items;`
- Treat a mismatch or missing table as a failed drill and investigate immediately.
