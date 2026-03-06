# Performance triage (query + database)

## Goal

Reduce time-to-diagnosis for slow queries by following a repeatable workflow and capturing evidence that supports a safe fix.

## When to use

- p95/p99 latency spikes (API or batch jobs)
- CPU saturation on the database host
- sudden increase in query runtimes after a deployment or migration

## Prechecks

- Confirm user impact and scope (which endpoints/jobs, which tenants, which time window).
- Record the baseline: p95/p99 latency, QPS, error rate, and current resource utilization.
- Ensure you can run read-only diagnostics safely.

## Procedure

1) Identify the top offenders:
- start with slow query logs / top statements / most time-consuming queries
- capture query text, parameters (if safe), and frequency

2) Get an execution plan (example for PostgreSQL):

```bash
# Replace with your query. Use EXPLAIN ANALYZE carefully in production.
psql "$PG_TEST_DSN" -c "EXPLAIN (ANALYZE, BUFFERS) SELECT 1;"
```

3) Check for common causes:
- missing or stale statistics
- missing indexes on join/filter columns
- sequential scans on large tables
- N+1 query patterns in application code
- lock contention (long-running transactions, blocking DDL)

4) Apply the smallest safe fix first:
- add or adjust an index (validate write amplification + storage impact)
- update statistics (`ANALYZE`) where appropriate
- reduce lock duration (split migrations, use safe DDL patterns)

## Rollback

- Prefer changes that are reversible (e.g., drop an index if it causes unacceptable write overhead).
- If a change increases latency or error rate, revert quickly and capture the evidence for a safer follow-up.

## Verification

- Confirm the improvement using the same metric you used to detect the issue (p95/p99 latency, runtime, CPU).
- Re-run the plan capture and ensure the execution plan changed in the expected direction.
- Document the fix and add a regression test or guardrail when possible.

