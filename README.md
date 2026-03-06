# 27-postgres-reliability-security-runbooks

A portfolio-grade repository focused on **database runbooks**: practical operational playbooks that reduce MTTR by turning “what do we do now?” into a repeatable checklist.

This repository is intentionally generic (no employer branding). It demonstrates real engineering habits: verifiable drills, evidence artifacts, and safe validation.

## The 3 core problems this repo solves
1) **Actionable runbooks:** consistent structure, clear prechecks, and explicit verification steps.
2) **Recovery confidence:** backup/restore drills that are safe to rerun and produce evidence.
3) **Performance diagnosis discipline:** a repeatable workflow for query/database triage that leads to safer fixes.

## Quick demo (local lab)
Prereqs: Docker + Docker Compose.

```bash
make demo
```

## Tests (two explicit modes)

This repo supports exactly two test modes via `TEST_MODE`:

- `TEST_MODE=demo` (default): offline-only (validates runbooks and repo policy without Docker/cloud)
- `TEST_MODE=production`: real integrations when configured (guarded by explicit opt-in)

Run demo mode:

```bash
make test-demo
```

Run production mode (requires at least one integration to be enabled):

```bash
make test-production
```

Production integration options:
- Make Docker usable to execute local integration checks (docker-compose)
- Or set `PG_TEST_DSN` to run a real `psql` connectivity query

## Runbooks and validation

Runbooks live in `docs/runbooks/`. Demo mode runs a validator that enforces required headings and produces an evidence artifact:

```bash
python3 tools/validate_runbooks.py --out artifacts/runbook_validation.json
```

## Sponsorship and contact

Sponsored by:
CloudForgeLabs  
https://cloudforgelabs.ainextstudios.com/  
support@ainextstudios.com

Built by:
Freddy D. Alvarez  
https://www.linkedin.com/in/freddy-daniel-alvarez/

For job opportunities, contact:
it.freddy.alvarez@gmail.com

## License

Personal, educational, and non-commercial use is free. Commercial use requires paid permission.
See `LICENSE` and `COMMERCIAL_LICENSE.md`.
