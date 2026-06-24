#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.dogfood import expected_by_id, load_json_file, rel, transcript_paths, write_json
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_markdown_report

ROOT = find_repo_root(Path(__file__))
REQUIRED_HEADINGS = ("# ", "## ")


def compare_bundle(prompt_id: str, live: Path, fixture: Path) -> list[Finding]:
    findings: list[Finding] = []
    required = ["02_ARCHITECTURE_DECISION_RECORD.md", "04_CHAIN_SPEC.yaml", "05_INFRASTRUCTURE_PLAN.md", "06_SECURITY_REVIEW.md", "08_LAUNCH_GATES.md"]
    for name in required:
        if not (live / name).exists():
            findings.append(Finding("error", rel(live / name, ROOT), "live bundle missing required file"))
        if not (fixture / name).exists():
            findings.append(Finding("error", rel(fixture / name, ROOT), "fixture bundle missing required file"))
    for directory in ["configs", "evidence"]:
        if not (live / directory).exists():
            findings.append(Finding("warning", rel(live / directory, ROOT), "live bundle missing structural directory"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare live generated artifact bundles to checked-in fixture structure.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--platform", choices=["codex", "claude"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    strict = args.strict and not args.bootstrap
    expected = expected_by_id(ROOT)
    findings: list[Finding] = []
    comparisons: list[dict] = []
    for path in transcript_paths(ROOT, args.platform):
        data = load_json_file(path)
        prompt_id = str(data.get("prompt_id"))
        fixture_value = expected.get(prompt_id, {}).get("fixture_bundle")
        live_value = data.get("generated_artifact_bundle")
        if fixture_value and live_value:
            live = ROOT / str(live_value)
            fixture = ROOT / str(fixture_value)
            bundle_findings = compare_bundle(prompt_id, live, fixture)
            findings.extend(bundle_findings)
            comparisons.append({"prompt_id": prompt_id, "live": str(live_value), "fixture": str(fixture_value), "findings": len(bundle_findings)})
    if strict and not comparisons:
        findings.append(Finding("error", "dogfood/transcripts", "strict mode requires live artifact bundle comparisons"))
    payload = {"status": "pass" if not findings else "fail", "comparisons": comparisons, "findings": [f.__dict__ for f in findings]}
    if args.json_out:
        write_json(Path(args.json_out), payload)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Live vs Fixture Diff", {"ok": not findings, "summary": {"comparisons": len(comparisons)}, "findings": [f.__dict__ for f in findings]}, ["compare_live_to_fixture"])
    report = Report(ok=not [f for f in findings if f.level == "error" or (strict and f.level == "warning")], script="scripts/compare_live_to_fixture.py", target=args.platform or "dogfood/transcripts", summary={"mode": "strict" if strict else "bootstrap", "comparisons": len(comparisons), "findings": len(findings)}, findings=findings)
    if args.json:
        print(json.dumps(payload if args.json_out else report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
