#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from lib.repo import find_repo_root, relpath
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report
from lib.safety import scan_text
from lib.yaml_json import load_yaml

ROOT = find_repo_root(Path(__file__))
REQUIRED = {"stack_id","display_name","status","chain_types","execution","settlement","data_availability","proof_models","required_roles","optional_roles","security_required","forbidden_defaults","source_refs","notes"}
STATUSES = {"supported-alpha", "reference-alpha", "experimental-alpha"}
OVERCLAIM_RE = re.compile(r"(?i)production ready by default|audit approved|mainnet certified|guaranteed secure")


def profile_paths(args: argparse.Namespace) -> list[Path]:
    if args.path:
        return [Path(args.path)]
    base = Path(args.all or "profiles")
    return sorted(base.glob("*.yaml"))


def validate_profile(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = relpath(path, ROOT)
    try:
        data = load_yaml(path)
    except Exception as exc:
        return [Finding("error", rel, f"cannot parse YAML: {exc}")]
    if not isinstance(data, dict):
        return [Finding("error", rel, "profile must be a mapping")]
    missing = REQUIRED - set(data)
    for key in sorted(missing):
        findings.append(Finding("error", rel, f"missing required field: {key}"))
    stack_id = str(data.get("stack_id", ""))
    if stack_id != path.stem:
        findings.append(Finding("error", rel, "stack_id must match filename stem"))
    if data.get("status") not in STATUSES:
        findings.append(Finding("error", rel, "status must be supported-alpha, reference-alpha, or experimental-alpha"))
    for field in ["chain_types", "required_roles", "security_required", "forbidden_defaults", "source_refs", "notes"]:
        if not isinstance(data.get(field), list) or not data.get(field):
            findings.append(Finding("error", rel, f"{field} must be a non-empty list"))
    for ref in data.get("source_refs", []) if isinstance(data.get("source_refs"), list) else []:
        ref_path = str(ref).split("#", 1)[0]
        if ref_path and not (ROOT / ref_path).exists():
            findings.append(Finding("warning", rel, f"source_ref does not resolve locally: {ref}"))
    text = path.read_text(encoding="utf-8")
    if OVERCLAIM_RE.search(text):
        findings.append(Finding("error", rel, "unsupported production/security overclaim detected"))
    for finding in scan_text(text, rel):
        findings.append(finding)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate v0.2 stack profile YAML files.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path")
    group.add_argument("--all")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    args = parser.parse_args(argv)
    paths = profile_paths(args)
    findings: list[Finding] = []
    for path in paths:
        findings.extend(validate_profile(path))
    errors = [f for f in findings if f.level == "error" or (args.strict and f.level == "warning")]
    report = Report(ok=not errors, script="scripts/validate_stack_profiles.py", target=args.path or args.all, summary={"profiles_checked": len(paths), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_out:
        write_markdown_report(args.markdown_out, "Stack Profile Validation Report", report, ["validate_stack_profiles"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
