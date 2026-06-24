#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from lib.repo import find_repo_root
from lib.reports import Finding, Report, write_json_report

ROOT = find_repo_root(Path(__file__))

V02_CHECKS = [
    ("clean-install", [sys.executable, "scripts/clean_install_test.py", "--json-out", "{out}/clean-install-report.json", "--skip-claude-plugin-validate"]),
    ("behavior-evals", [sys.executable, "scripts/run_behavior_evals.py", "--evals", "evals/skill-trigger-matrix.yaml", "--strict", "--json"]),
    ("artifact-bundle", [sys.executable, "scripts/validate_artifact_bundle.py", "--strict", "--all", "fixtures/artifact-bundles", "--json-out", "{out}/artifact-bundle-report.json"]),
    ("stack-profile", [sys.executable, "scripts/validate_stack_profiles.py", "--strict", "--all", "profiles", "--json-out", "{out}/stack-profile-report.json"]),
    ("generated-config", [sys.executable, "scripts/validate_generated_configs.py", "--strict", "--all", "fixtures/artifact-bundles", "--json-out", "{out}/generated-config-report.json"]),
    ("acceptance", [sys.executable, "scripts/run_acceptance_suite.py", "--strict", "--json-out", "{out}/acceptance-report.json"]),
    ("hook-fixture", [sys.executable, "scripts/test_hook_fixtures.py", "--strict", "--json-out", "{out}/hook-fixture-report.json"]),
    ("upstream-freshness", [sys.executable, "scripts/check_upstream_freshness.py", "--sources", "docs/upstream-sources.md", "--markdown-report", "{out}/upstream-freshness-report.md", "--allow-offline", "--json"]),
    ("secret-scan", [sys.executable, "plugins/evm-chain-engineering-pro/scripts/scan_secrets.py", "--path", ".", "--strict", "--json"]),
]

V03_CHECKS = [
    ("clean-install", [sys.executable, "scripts/clean_install_test.py", "--json-out", "{out}/clean-install-report.json", "--skip-claude-plugin-validate"]),
    ("dogfood-prompt-lint", [sys.executable, "scripts/lint_dogfood_prompts.py", "--strict", "--json-out", "{out}/dogfood-prompt-lint-report.json"]),
    ("dogfood-transcripts", [sys.executable, "scripts/validate_dogfood_transcripts.py", "{mode}", "--json-out", "{out}/dogfood-transcript-report.json"]),
    ("live-runs", [sys.executable, "scripts/validate_live_run_package.py", "--all", "{mode}", "--json-out", "{out}/live-run-package-report.json"]),
    ("live-acceptance", [sys.executable, "scripts/run_live_acceptance_suite.py", "{mode}", "--json-out", "{out}/live-acceptance-report.json"]),
    ("live-hooks", [sys.executable, "scripts/validate_live_hook_observations.py", "{mode}", "--json-out", "{out}/live-hook-observation-report.json"]),
    ("skill-routing", [sys.executable, "scripts/score_skill_routing.py", "{mode}", "--json-out", "{out}/skill-routing-scorecard.json"]),
    ("subagent-dogfood", [sys.executable, "scripts/validate_subagent_dogfood.py", "{mode}", "--json-out", "{out}/subagent-dogfood-report.json"]),
    ("live-vs-fixture", [sys.executable, "scripts/compare_live_to_fixture.py", "{mode}", "--json-out", "{out}/live-vs-fixture-diff.json"]),
    ("known-bad-output", [sys.executable, "scripts/check_bad_output_patterns.py", "--path", "tests/known_bad_outputs", "--expect-bad", "--json-out", "{out}/known-bad-output-check.json"]),
    ("live-output-safety", [sys.executable, "scripts/check_bad_output_patterns.py", "--path", "dogfood/live-runs", "--strict", "--json-out", "{out}/live-output-safety-check.json"]),
    ("secret-scan", [sys.executable, "plugins/evm-chain-engineering-pro/scripts/scan_secrets.py", "--path", ".", "--strict", "--json"]),
]


def git_value(args: list[str], default: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.stdout.strip() or default


def is_v03(version: str) -> bool:
    return version.startswith("v0.3")


def command_for(template: list[str], out: Path, mode: str) -> list[str]:
    return [part.format(out=str(out), mode=mode) for part in template]


def run_checks(out: Path, checks_spec: list[tuple[str, list[str]]], *, mode: str, collect_only: bool) -> tuple[dict[str, str], list[Finding], list[str]]:
    checks: dict[str, str] = {}
    findings: list[Finding] = []
    command_log: list[str] = []
    for name, template in checks_spec:
        if collect_only:
            checks[name] = "collected" if any(out.glob(f"{name}*")) else "missing"
            if checks[name] == "missing":
                findings.append(Finding("error", name, "required report missing in collect-only mode"))
            continue
        cmd = command_for(template, out, mode)
        result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        checks[name] = "pass" if result.returncode == 0 else "fail"
        command_log.append("$ " + " ".join(cmd))
        command_log.append(f"exit_code={result.returncode}")
        if name in {"behavior-evals", "upstream-freshness", "secret-scan"}:
            report_name = {
                "behavior-evals": "behavior-evals.json",
                "upstream-freshness": "upstream-freshness-report.json",
                "secret-scan": "secret-scan-report.json",
            }[name]
            payload = result.stdout if result.stdout.strip().startswith("{") else json.dumps({"ok": result.returncode == 0, "output": result.stdout[-1000:]}, indent=2)
            (out / report_name).write_text(payload, encoding="utf-8")
        if result.returncode != 0:
            findings.append(Finding("error", name, "release evidence check failed"))
    (out / "command-log.txt").write_text("\n".join(command_log) + "\n", encoding="utf-8")
    return checks, findings, command_log


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def write_v03_auxiliary(out: Path, mode_name: str, checks: dict[str, str], findings: list[Finding]) -> None:
    copy_if_exists(ROOT / "docs" / "platform-compatibility-matrix.md", out / "platform-compatibility-matrix.md")
    unresolved = sorted((ROOT / "dogfood" / "issues" / "open").glob("*.md"))
    issue_lines = ["# Unresolved Dogfood Issues", ""]
    issue_lines.extend([f"- {path.name}" for path in unresolved] or ["None recorded."])
    (out / "unresolved-dogfood-issues.md").write_text("\n".join(issue_lines) + "\n", encoding="utf-8")
    ready = mode_name == "strict" and not findings and all(value in {"pass", "collected"} for value in checks.values())
    readiness_lines = [
        "# v0.3.0-beta Release Readiness",
        "",
        f"- Mode: {mode_name}",
        f"- Release ready: {str(ready).lower()}",
        "- Reason: strict live evidence is required for readiness." if not ready else "- Reason: strict validation passed with live evidence.",
        "- Excluded capabilities: push, publish, deploy, real secrets, MCP servers, mainnet approval marker.",
    ]
    (out / "release-readiness.md").write_text("\n".join(readiness_lines) + "\n", encoding="utf-8")


def write_summary(out: Path, version: str, checks: dict[str, str], findings: list[Finding], *, mode_name: str) -> None:
    branch = git_value(["branch", "--show-current"], "unknown")
    commit = git_value(["rev-parse", "--short", "HEAD"], "HEAD")
    working_tree_clean = git_value(["status", "--short"], "dirty") == ""
    v03 = is_v03(version)
    release_ready = (not findings and all(value in {"pass", "collected"} for value in checks.values()) and mode_name == "strict") if v03 else (not findings and all(value in {"pass", "collected"} for value in checks.values()))
    transcript_report = read_json(out / "dogfood-transcript-report.json")
    hook_report = read_json(out / "live-hook-observation-report.json")
    scorecard = read_json(out / "skill-routing-scorecard.json")
    tag_status = "not created" if v03 and not release_ready else version
    summary = {
        "version": version,
        "ok": not findings and all(value in {"pass", "collected"} for value in checks.values()),
        "mode": mode_name,
        "release_ready": release_ready,
        "v0_3_release_ready": release_ready if v03 else None,
        "git": {"branch": branch, "commit": commit, "tag": tag_status, "working_tree_clean": working_tree_clean},
        "checks": checks,
        "live_codex_transcripts": (transcript_report.get("summary") or {}).get("live_codex_transcripts", "pending") if v03 else None,
        "live_claude_transcripts": (transcript_report.get("summary") or {}).get("live_claude_transcripts", "pending") if v03 else None,
        "live_hook_observations": (hook_report.get("summary") or {}).get("live_hook_observations", "pending") if v03 else None,
        "skill_routing_score": scorecard.get("overall_score", 0) if v03 else None,
        "known_limitations": [
            "No live chain deployment performed.",
            "No mainnet approval workflow implemented.",
            "No MCP servers included.",
            "v0.3 strict release requires real Codex/Claude dogfood transcripts and live hook observations.",
        ],
    }
    write_json_report(out / "summary.json", summary)
    lines = [
        f"# {version} Release Evidence",
        "",
        f"- Version: {version}",
        f"- Mode: {mode_name}",
        f"- Git branch: {branch}",
        f"- Git commit: {commit}",
        f"- Git tag status: {tag_status}",
        f"- Validation summary: {'PASS' if summary['ok'] else 'FAIL'}",
        f"- Release ready: {str(release_ready).lower()}",
        "",
        "## Checks",
        "",
    ]
    for key, value in sorted(checks.items()):
        lines.append(f"- {key}: {value}")
    if v03:
        lines.extend([
            "",
            "## Live Evidence",
            "",
            f"- Codex transcripts: {summary['live_codex_transcripts']}",
            f"- Claude transcripts: {summary['live_claude_transcripts']}",
            f"- Hook observations: {summary['live_hook_observations']}",
            f"- Skill routing score: {summary['skill_routing_score']}",
        ])
    lines.extend(["", "## Known Limitations", ""])
    lines.extend([f"- {item}" for item in summary["known_limitations"]])
    lines.extend(["", "## Unsafe Capabilities Intentionally Excluded", "", "- No push, publish, deploy, transaction sending, key generation, cloud API calls, MCP servers, or mainnet approval marker."])
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if v03:
        write_v03_auxiliary(out, mode_name, checks, findings)
        report = Report(ok=summary["ok"], script="scripts/build_release_evidence.py", target=str(out), summary=summary, findings=findings)
        write_json_report(out / "validate-v03-report.json", report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build reproducible release evidence without publishing or deploying.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--output")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--collect-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    mode_name = "strict" if args.strict and not args.bootstrap else "bootstrap" if args.bootstrap else "strict"
    mode_flag = "--strict" if mode_name == "strict" else "--bootstrap"
    out = Path(args.output or f"release/evidence/{args.version}")
    out.mkdir(parents=True, exist_ok=True)
    checks_spec = V03_CHECKS if is_v03(args.version) else V02_CHECKS
    checks, findings, _command_log = run_checks(out, checks_spec, mode=mode_flag, collect_only=args.collect_only)
    write_summary(out, args.version, checks, findings, mode_name=mode_name)
    report = Report(ok=not findings, script="scripts/build_release_evidence.py", target=str(out), summary={"checks": len(checks), "findings": len(findings), "mode": mode_name}, findings=findings)
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print(f"status: {'pass' if report.ok else 'fail'}")
        for key, value in sorted(checks.items()):
            print(f"{key}: {value}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
