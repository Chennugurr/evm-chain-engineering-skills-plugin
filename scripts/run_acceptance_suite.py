#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from lib.repo import find_repo_root, relpath, skill_names
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report
from lib.yaml_json import load_yaml, load_json

ROOT = find_repo_root(Path(__file__))


def expected_paths(case: str | None) -> list[Path]:
    base = ROOT / "acceptance" / "expected"
    if case:
        return [base / f"{case}.yaml"]
    return sorted(base.glob("*.yaml"))


def all_text(path: Path | None, extra: Path | None = None) -> str:
    text = ""
    for base in [path, extra]:
        if base and base.exists():
            files = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
            for file_path in files:
                try:
                    text += "\n" + file_path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    pass
    return text


def validate_case(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = relpath(path, ROOT)
    try:
        data = load_yaml(path)
    except Exception as exc:
        return [Finding("error", rel, f"cannot parse expected YAML: {exc}")]
    if not isinstance(data, dict):
        return [Finding("error", rel, "expected file must be a mapping")]
    case_id = str(data.get("id", path.stem))
    prompt = ROOT / str(data.get("prompt_file", ""))
    if not prompt.exists():
        findings.append(Finding("error", rel, "prompt_file does not exist"))
    known = skill_names(ROOT)
    for field in ["expected_skills", "forbidden_skills"]:
        for skill in data.get(field, []) or []:
            if skill not in known:
                findings.append(Finding("error", rel, f"{field} contains unknown skill: {skill}"))
    fixture_value = data.get("fixture_bundle")
    fixture = ROOT / fixture_value if fixture_value else None
    if fixture_value:
        if not fixture or not fixture.exists():
            findings.append(Finding("error", rel, "fixture bundle does not exist"))
        else:
            result = subprocess.run([sys.executable, "scripts/validate_artifact_bundle.py", "--strict", "--path", str(fixture)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if result.returncode != 0:
                findings.append(Finding("error", rel, f"fixture bundle failed validation: {fixture_value}"))
            for artifact in data.get("required_artifacts", []) or []:
                if not (fixture / artifact).exists():
                    findings.append(Finding("error", rel, f"required artifact missing: {artifact}"))
            policy_path = fixture / "evidence" / "policy-check.json"
            if policy_path.exists():
                policy = load_json(policy_path)
                expected = data.get("expected_policy", {}) or {}
                for key, value in expected.items():
                    if key == "human_approval_required":
                        spec = load_yaml(fixture / "04_CHAIN_SPEC.yaml")
                        actual = spec.get("human_approval_required") if isinstance(spec, dict) else None
                    else:
                        actual = policy.get(key)
                    if actual != value:
                        findings.append(Finding("error", rel, f"policy expectation mismatch for {key}: expected {value}, got {actual}"))
    refusal = ROOT / "acceptance" / "reports" / f"{case_id}.expected-refusal.md"
    corpus = all_text(fixture, refusal)
    for term in data.get("must_include", []) or []:
        if term.lower() not in corpus.lower():
            findings.append(Finding("error", rel, f"must_include not found: {term}"))
    for term in data.get("must_not_include", []) or []:
        if term.lower() in corpus.lower():
            findings.append(Finding("error", rel, f"must_not_include found: {term}"))
    if data.get("expected_policy", {}).get("refusal_required") and not refusal.exists():
        findings.append(Finding("error", rel, "refusal case requires expected refusal document"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate v0.2 workflow acceptance prompt contracts and fixtures.")
    parser.add_argument("--case")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    args = parser.parse_args(argv)
    paths = expected_paths(args.case)
    findings: list[Finding] = []
    for path in paths:
        findings.extend(validate_case(path))
    errors = [f for f in findings if f.level == "error" or (args.strict and f.level == "warning")]
    report = Report(ok=not errors, script="scripts/run_acceptance_suite.py", target=args.case or "acceptance/expected", summary={"cases_checked": len(paths), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_out:
        write_markdown_report(args.markdown_out, "Acceptance Suite Report", report, ["run_acceptance_suite"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
