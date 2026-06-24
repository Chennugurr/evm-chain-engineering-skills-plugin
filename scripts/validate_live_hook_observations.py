#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.dogfood import hook_observation_paths, load_json_file, rel
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))


def validate_observation(path: Path, *, strict: bool) -> list[Finding]:
    findings: list[Finding] = []
    if not path.exists():
        return [Finding("error" if strict else "warning", rel(path, ROOT), "hook observation file missing")]
    try:
        data = load_json_file(path)
    except Exception as exc:
        return [Finding("error", rel(path, ROOT), f"cannot parse hook observation: {exc}")]
    status = data.get("status")
    if data.get("platform") not in {"codex", "claude"}:
        findings.append(Finding("error", rel(path, ROOT), "platform must be codex or claude"))
    if not (ROOT / str(data.get("hook_manifest_path", ""))).exists():
        findings.append(Finding("error", rel(path, ROOT), "hook_manifest_path does not exist"))
    if status == "fail":
        findings.append(Finding("error", rel(path, ROOT), "hook observation status is fail"))
    if strict:
        if status == "pending":
            findings.append(Finding("error", rel(path, ROOT), "strict mode requires real hook observation"))
        elif status == "pass" and not data.get("evidence"):
            findings.append(Finding("error", rel(path, ROOT), "passing hook observation requires evidence"))
        elif status == "not-supported" and (not data.get("platform_limitation") or not data.get("evidence")):
            findings.append(Finding("error", rel(path, ROOT), "platform limitation requires evidence in strict mode"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate live Codex/Claude hook observation evidence.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--platform", choices=["codex", "claude"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    strict = args.strict and not args.bootstrap
    paths = hook_observation_paths(ROOT, args.platform)
    findings: list[Finding] = []
    for path in paths:
        findings.extend(validate_observation(path, strict=strict))
    report = Report(ok=not [f for f in findings if f.level == "error" or (strict and f.level == "warning")], script="scripts/validate_live_hook_observations.py", target=args.platform or "dogfood/hooks", summary={"mode": "strict" if strict else "bootstrap", "observations_checked": len(paths), "live_hook_observations": "pending" if any("pending" in path.read_text(encoding="utf-8") for path in paths if path.exists()) else "recorded", "findings": len(findings)}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Live Hook Observation Report", report, ["validate_live_hook_observations"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
