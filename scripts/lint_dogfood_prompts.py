#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lib.dogfood import expected_by_id, prompt_id_from_path, prompt_paths, rel
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))
REQUIRED_HEADINGS = ("Objective", "Stack or Task", "Safety", "Required Output")
UNSAFE_PATTERNS = [
    (re.compile(r"0x[a-fA-F0-9]{64}"), "key-shaped literal"),
    (re.compile(r"(?i)\bmnemonic\s*[:=]"), "mnemonic assignment"),
    (re.compile(r"(?i)\b(private[_ -]?key|deployer[_ -]?secret)\s*[:=]"), "secret assignment"),
    (re.compile(r"(?i)forge script .+--broadcast"), "broadcast command"),
    (re.compile(r"(?i)hardhat .+(deploy|run).+mainnet"), "mainnet deploy command"),
]


def validate_prompt(path: Path, expected: dict[str, dict]) -> list[Finding]:
    findings: list[Finding] = []
    prompt_id = prompt_id_from_path(path)
    text = path.read_text(encoding="utf-8")
    if prompt_id not in expected:
        findings.append(Finding("error", rel(path, ROOT), "prompt has no expected YAML contract"))
    for heading in REQUIRED_HEADINGS:
        if f"## {heading}" not in text:
            findings.append(Finding("error", rel(path, ROOT), f"missing heading: {heading}"))
    lowered = text.lower()
    if prompt_id != "06-unsafe-private-key-request" and "dry-run" not in lowered:
        findings.append(Finding("warning", rel(path, ROOT), "prompt should require dry-run framing"))
    if "do not" not in lowered and "no real" not in lowered and "refuse" not in lowered:
        findings.append(Finding("warning", rel(path, ROOT), "prompt should include explicit safety constraints"))
    for pattern, label in UNSAFE_PATTERNS:
        if pattern.search(text):
            findings.append(Finding("error", rel(path, ROOT), f"unsafe prompt content detected: {label}"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint v0.3 dogfood prompts for required structure and safe wording.")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    expected = expected_by_id(ROOT)
    paths = prompt_paths(ROOT)
    findings: list[Finding] = []
    for path in paths:
        findings.extend(validate_prompt(path, expected))
    prompt_ids = {prompt_id_from_path(path) for path in paths}
    for expected_id in sorted(expected):
        if expected_id not in prompt_ids:
            findings.append(Finding("error", f"dogfood/expected/{expected_id}.yaml", "expected contract has no prompt file"))
    errors = [f for f in findings if f.level == "error" or (args.strict and f.level == "warning")]
    report = Report(ok=not errors, script="scripts/lint_dogfood_prompts.py", target="dogfood/prompts", summary={"prompts_checked": len(paths), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Dogfood Prompt Lint Report", report, ["lint_dogfood_prompts"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
