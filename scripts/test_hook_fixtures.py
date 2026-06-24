#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from lib.repo import find_repo_root, relpath
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))


def fixtures(path: str | None) -> list[Path]:
    if path:
        return [Path(path)]
    return sorted((ROOT / "tests" / "fixtures" / "hooks").glob("*.json"))


def validate_fixture(path: Path) -> list[Finding]:
    rel = relpath(path, ROOT)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [Finding("error", rel, f"cannot parse fixture: {exc}")]
    event = data.get("event", {})
    expected = data.get("expected_status")
    result = subprocess.run([sys.executable, "scripts/policy_guard.py", "--stdin", "--json", "--strict"], cwd=ROOT, input=json.dumps(event), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return [Finding("error", rel, "policy guard did not emit JSON")]
    actual = payload.get("status")
    if actual != expected:
        return [Finding("error", rel, f"expected {expected}, got {actual}")]
    if expected == "allow" and result.returncode != 0:
        return [Finding("error", rel, "allow fixture returned nonzero")]
    if expected == "block" and result.returncode == 0:
        return [Finding("error", rel, "block fixture returned zero")]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Codex/Claude hook policy fixtures.")
    parser.add_argument("--fixture")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    args = parser.parse_args(argv)
    paths = fixtures(args.fixture)
    findings: list[Finding] = []
    for path in paths:
        findings.extend(validate_fixture(path))
    report = Report(ok=not findings, script="scripts/test_hook_fixtures.py", target=args.fixture or "tests/fixtures/hooks", summary={"fixtures_checked": len(paths), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_out:
        write_markdown_report(args.markdown_out, "Hook Fixture Report", report, ["test_hook_fixtures"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
