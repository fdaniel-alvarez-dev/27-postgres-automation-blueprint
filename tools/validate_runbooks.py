#!/usr/bin/env python3
import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Finding:
    severity: str  # ERROR | WARN | INFO
    rule_id: str
    message: str
    path: str | None = None


REQUIRED_SECTIONS = [
    "Goal",
    "When to use",
    "Prechecks",
    "Procedure",
    "Rollback",
    "Verification",
]


def add(findings: list[Finding], severity: str, rule_id: str, message: str, path: Path | None = None) -> None:
    findings.append(
        Finding(
            severity=severity,
            rule_id=rule_id,
            message=message,
            path=str(path.relative_to(REPO_ROOT)) if path else None,
        )
    )


def headings(md: str) -> set[str]:
    found: set[str] = set()
    for line in md.splitlines():
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not m:
            continue
        title = m.group(1).strip()
        found.add(title)
    return found


def validate_runbook(path: Path, findings: list[Finding]) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    hs = headings(text)

    for s in REQUIRED_SECTIONS:
        if s not in hs:
            add(findings, "ERROR", "runbook.section_missing", f"Missing required section heading: '{s}'", path)

    if "TODO" in text or "TBD" in text:
        add(findings, "WARN", "runbook.placeholders", "Runbook contains TODO/TBD placeholders; ensure it is actionable.", path)

    if "```bash" not in text and "```sh" not in text:
        add(findings, "WARN", "runbook.no_commands", "Runbook has no shell command examples; consider adding concrete steps.", path)


def summarize(findings: list[Finding]) -> dict:
    return {
        "errors": sum(1 for f in findings if f.severity == "ERROR"),
        "warnings": sum(1 for f in findings if f.severity == "WARN"),
        "info": sum(1 for f in findings if f.severity == "INFO"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runbooks for completeness and actionability.")
    parser.add_argument("--out", default="artifacts/runbook_validation.json")
    args = parser.parse_args()

    runbooks_dir = REPO_ROOT / "docs" / "runbooks"
    findings: list[Finding] = []

    if not runbooks_dir.exists():
        add(findings, "ERROR", "runbooks.missing", "docs/runbooks directory is missing.", runbooks_dir)
    else:
        candidates = sorted(p for p in runbooks_dir.glob("*.md") if p.name.lower() != "readme.md")
        if not candidates:
            add(findings, "ERROR", "runbooks.empty", "No runbooks found under docs/runbooks (excluding README).", runbooks_dir)
        for rb in candidates:
            validate_runbook(rb, findings)

    report = {"summary": summarize(findings), "findings": [asdict(f) for f in findings]}
    out_path = (REPO_ROOT / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
