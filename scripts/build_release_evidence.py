#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from lib.repo import find_repo_root
from lib.reports import Finding, Report, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))

CHECKS = [
    ("behavior-evals", [sys.executable, "scripts/run_behavior_evals.py", "--evals", "evals/skill-trigger-matrix.yaml", "--strict", "--json-out", "{out}/behavior-evals.json"]),
    ("artifact-bundle", [sys.executable, "scripts/validate_artifact_bundle.py", "--strict", "--all", "fixtures/artifact-bundles", "--json-out", "{out}/artifact-bundle-report.json"]),
    ("stack-profile", [sys.executable, "scripts/validate_stack_profiles.py", "--strict", "--all", "profiles", "--json-out", "{out}/stack-profile-report.json"]),
    ("generated-config", [sys.executable, "scripts/validate_generated_configs.py", "--strict", "--all", "fixtures/artifact-bundles", "--json-out", "{out}/generated-config-report.json"]),
    ("acceptance", [sys.executable, "scripts/run_acceptance_suite.py", "--strict", "--json-out", "{out}/acceptance-report.json"]),
    ("hook-fixture", [sys.executable, "scripts/test_hook_fixtures.py", "--strict", "--json-out", "{out}/hook-fixture-report.json"]),
    ("upstream-freshness", [sys.executable, "scripts/check_upstream_freshness.py", "--sources", "docs/upstream-sources.md", "--markdown-report", "{out}/upstream-freshness-report.md", "--allow-offline", "--json"]),
    ("secret-scan", [sys.executable, "plugins/evm-chain-engineering-pro/scripts/scan_secrets.py", "--path", ".", "--strict", "--json"]),
    ("clean-install", [sys.executable, "scripts/clean_install_test.py", "--json-out", "{out}/clean-install-report.json", "--skip-claude-plugin-validate"]),
]


def git_value(args: list[str], default: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.stdout.strip() or default


def run_checks(out: Path, collect_only: bool) -> tuple[dict[str, str], list[Finding], list[str]]:
    checks: dict[str, str] = {}
    findings: list[Finding] = []
    command_log: list[str] = []
    for name, template in CHECKS:
        if collect_only:
            checks[name] = "collected" if any(out.glob(f"{name}*")) else "missing"
            if checks[name] == "missing":
                findings.append(Finding("error", name, "required report missing in collect-only mode"))
            continue
        cmd = [part.format(out=str(out)) for part in template]
        result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        checks[name] = "pass" if result.returncode == 0 else "fail"
        command_log.append("$ " + " ".join(cmd))
        command_log.append(f"exit_code={result.returncode}")
        if name in {"upstream-freshness", "secret-scan"}:
            report_name = "upstream-freshness-report.json" if name == "upstream-freshness" else "secret-scan-report.json"
            try:
                (out / report_name).write_text(result.stdout if result.stdout.strip().startswith("{") else json.dumps({"ok": result.returncode == 0, "output": result.stdout[-1000:]}, indent=2), encoding="utf-8")
            except Exception:
                pass
        if result.returncode != 0:
            findings.append(Finding("error", name, "release evidence check failed"))
    (out / "command-log.txt").write_text("\n".join(command_log) + "\n", encoding="utf-8")
    return checks, findings, command_log


def write_summary(out: Path, version: str, checks: dict[str, str], findings: list[Finding]) -> None:
    branch = git_value(["branch", "--show-current"], "unknown")
    tag_status = version
    summary = {
        "version": version,
        "ok": not findings and all(value in {"pass", "collected"} for value in checks.values()),
        "git": {"branch": branch, "commit": "HEAD", "tag": tag_status, "working_tree_clean": git_value(["status", "--short"], "dirty") == ""},
        "checks": checks,
        "known_limitations": [
            "No live chain deployment performed.",
            "No mainnet approval workflow implemented.",
            "Live Codex/Claude hook activation must be manually verified.",
            "Tracked evidence uses reproducible git labels; final response records exact commit hash.",
        ],
    }
    write_json_report(out / "summary.json", summary)
    lines = [
        f"# {version} Release Evidence", "",
        f"- Version: {version}",
        f"- Git branch: {branch}",
        "- Git commit: HEAD (exact hash recorded in FINAL_REPORT/final response)",
        f"- Git tag status: {tag_status}",
        f"- Validation summary: {'PASS' if summary['ok'] else 'FAIL'}", "",
        "## Checks", "",
    ]
    for key, value in sorted(checks.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Known Limitations", ""])
    lines.extend([f"- {item}" for item in summary["known_limitations"]])
    lines.extend(["", "## Unsafe Capabilities Intentionally Excluded", "", "- No deployment, transaction sending, key generation, cloud API calls, MCP servers, or mainnet approval marker.", "", "## Manual Checks Still Required", "", "- Live Codex/Claude dogfood, platform hook activation, external protocol/security review, and upstream release verification."])
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build reproducible v0.2-alpha release evidence without publishing or deploying.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--output")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--collect-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    out = Path(args.output or f"release/evidence/{args.version}")
    out.mkdir(parents=True, exist_ok=True)
    checks, findings, command_log = run_checks(out, args.collect_only)
    write_summary(out, args.version, checks, findings)
    report = Report(ok=not findings, script="scripts/build_release_evidence.py", target=str(out), summary={"checks": len(checks), "findings": len(findings)}, findings=findings)
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print(f"status: {'pass' if report.ok else 'fail'}")
        for key, value in sorted(checks.items()):
            print(f"{key}: {value}")
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
