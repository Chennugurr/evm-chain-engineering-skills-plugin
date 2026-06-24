#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from lib.dogfood import REFUSAL_PROMPTS, expected_by_id, live_run_paths, load_live_run_metadata, rel
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report
from lib.safety import scan_path

ROOT = find_repo_root(Path(__file__))
REQUIRED_FILES = ["METADATA.json", "TRANSCRIPT.md", "SKILL_OBSERVATIONS.md", "VALIDATION.md", "SECURITY_REVIEW.md"]
STRICT_EVIDENCE_FILES = ["PROMPT.md", "TRANSCRIPT.json", "VALIDATION.json", "HOOK_EVENTS.json", "POLICY_EVENTS.json", "MANUAL_NOTES.md"]


def validate_package(path: Path, *, strict: bool) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        return [Finding("error", rel(path, ROOT), "live-run package path does not exist")]
    for name in REQUIRED_FILES:
        if not (path / name).exists():
            findings.append(Finding("error", rel(path / name, ROOT), "missing live-run package file"))
    try:
        meta = load_live_run_metadata(path)
    except Exception as exc:
        return [Finding("error", rel(path / "METADATA.json", ROOT), f"cannot parse metadata: {exc}")]
    prompt_id = str(meta.get("prompt_id", ""))
    if prompt_id not in expected_by_id(ROOT):
        findings.append(Finding("error", rel(path / "METADATA.json", ROOT), f"unknown prompt_id: {prompt_id}"))
    if meta.get("platform") not in {"codex", "claude"}:
        findings.append(Finding("error", rel(path / "METADATA.json", ROOT), "platform must be codex or claude"))
    status = str(meta.get("status", ""))
    if strict:
        for name in STRICT_EVIDENCE_FILES:
            if not (path / name).exists():
                findings.append(Finding("error", rel(path / name, ROOT), "missing strict live evidence file"))
        if status in {"pending", "blocked", "failed"}:
            findings.append(Finding("error", rel(path / "METADATA.json", ROOT), f"strict mode does not accept {status} live-run packages"))
    for finding in scan_path(path, ROOT):
        findings.append(Finding("error" if finding.level == "error" else "warning", finding.path, finding.message))
    artifact_value = meta.get("artifacts")
    if prompt_id not in REFUSAL_PROMPTS:
        if not artifact_value:
            if strict or status not in {"blocked", "failed"}:
                findings.append(Finding("error", rel(path / "METADATA.json", ROOT), "non-refusal package must reference artifacts unless it is a blocked bootstrap capture"))
        else:
            artifact_path = path / str(artifact_value)
            if not artifact_path.exists():
                artifact_path = ROOT / str(artifact_value)
            if not artifact_path.exists():
                findings.append(Finding("error", rel(path / "METADATA.json", ROOT), "artifact path does not exist"))
            elif (artifact_path / "04_CHAIN_SPEC.yaml").exists():
                result = subprocess.run([sys.executable, "scripts/validate_artifact_bundle.py", "--strict", "--path", str(artifact_path)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if result.returncode != 0:
                    findings.append(Finding("error", rel(artifact_path, ROOT), "artifact bundle validation failed"))
    return findings


def selected_paths(args: argparse.Namespace) -> list[Path]:
    if args.path:
        return [Path(args.path)]
    return live_run_paths(ROOT, args.platform)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate v0.3 live-run packages.")
    parser.add_argument("path", nargs="?")
    parser.add_argument("--all", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--platform", choices=["codex", "claude"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    strict = args.strict and not args.bootstrap
    paths = selected_paths(args)
    findings: list[Finding] = []
    if strict and not paths:
        findings.append(Finding("error", "dogfood/live-runs", "strict mode requires live-run packages"))
    for path in paths:
        findings.extend(validate_package(path, strict=strict))
    report = Report(ok=not [f for f in findings if f.level == "error" or (strict and f.level == "warning")], script="scripts/validate_live_run_package.py", target=args.path or "dogfood/live-runs", summary={"mode": "strict" if strict else "bootstrap", "packages_checked": len(paths), "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Live Run Package Validation Report", report, ["validate_live_run_package"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
