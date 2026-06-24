#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from lib.repo import find_repo_root
from lib.reports import Report, Finding, print_human, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))
COMMANDS = [
    [sys.executable, "-m", "pytest"],
    ["make", "validate"],
    [sys.executable, "scripts/run_behavior_evals.py", "--evals", "evals/skill-trigger-matrix.yaml", "--strict"],
    [sys.executable, "scripts/validate_hooks.py", "--plugin-root", "plugins/evm-chain-engineering-pro", "--strict"],
    [sys.executable, "scripts/check_upstream_freshness.py", "--sources", "docs/upstream-sources.md", "--allow-offline"],
    [sys.executable, "scripts/release_check.py", "--strict"],
    [sys.executable, "scripts/validate_stack_profiles.py", "--strict", "--all", "profiles"],
    [sys.executable, "scripts/validate_artifact_bundle.py", "--strict", "--all", "fixtures/artifact-bundles"],
    [sys.executable, "scripts/validate_generated_configs.py", "--strict", "--all", "fixtures/artifact-bundles"],
    [sys.executable, "scripts/run_acceptance_suite.py", "--strict"],
    [sys.executable, "scripts/test_hook_fixtures.py", "--strict"],
]


def git_clean() -> bool:
    result = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    dirty = []
    for line in result.stdout.splitlines():
        path = line[3:] if len(line) > 3 else line
        if path.startswith("release/evidence/"):
            continue
        dirty.append(line)
    return not dirty


def clone_repo(target: Path, mode: str) -> tuple[Path, list[str]]:
    skipped: list[str] = []
    dest = target / "repo"
    if mode == "committed-only":
        if not git_clean():
            raise RuntimeError("committed-only clean install requires a clean working tree")
        result = subprocess.run(["git", "clone", "--no-hardlinks", str(ROOT), str(dest)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            raise RuntimeError("git clone failed: " + result.stdout[-400:])
        return dest, skipped
    shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    skipped.append("working-tree-copy mode is a simulation, not a committed clean clone")
    return dest, skipped


def run_commands(repo: Path, skip_claude: bool) -> tuple[list[dict[str, object]], list[str]]:
    results = []
    skipped: list[str] = []
    for cmd in COMMANDS:
        result = subprocess.run(cmd, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results.append({"command": " ".join(cmd), "returncode": result.returncode})
    if not skip_claude and shutil.which("claude"):
        result = subprocess.run(["claude", "plugin", "validate", "plugins/evm-chain-engineering-pro", "--strict"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results.append({"command": "claude plugin validate plugins/evm-chain-engineering-pro --strict", "returncode": result.returncode})
    else:
        skipped.append("claude plugin validate skipped")
    return results, skipped


def local_path_findings(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    patterns = [str(Path.home()), "/Users/", "C:\\Users\\"]
    for path in repo.rglob("*"):
        if not path.is_file() or any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern in text for pattern in patterns):
            rel = str(path.relative_to(repo))
            if rel.startswith(("docs/", "README.md", "FINAL_REPORT.md")):
                continue
            findings.append(Finding("error", rel, "unexpected absolute local path"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run offline clean install validation from a local clone or working-tree simulation.")
    parser.add_argument("--mode", choices=["committed-only", "working-tree-copy"], default="committed-only")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--skip-claude-plugin-validate", action="store_true")
    parser.add_argument("--require-claude", action="store_true")
    args = parser.parse_args(argv)
    temp = Path(tempfile.mkdtemp(prefix="v02-clean-install-"))
    findings: list[Finding] = []
    skipped: list[str] = []
    results: list[dict[str, object]] = []
    try:
        repo, clone_skips = clone_repo(temp, args.mode)
        skipped.extend(clone_skips)
        results, run_skips = run_commands(repo, args.skip_claude_plugin_validate)
        skipped.extend(run_skips)
        findings.extend(local_path_findings(repo))
        for item in results:
            if item["returncode"] != 0:
                findings.append(Finding("error", str(item["command"]), f"exit code {item['returncode']}"))
        if args.require_claude and any("claude" in item for item in skipped):
            findings.append(Finding("error", "claude", "Claude validation required but skipped"))
    except Exception as exc:
        findings.append(Finding("error", "clean-install", str(exc)))
    finally:
        if not args.keep_temp:
            shutil.rmtree(temp, ignore_errors=True)
    report = Report(ok=not findings, script="scripts/clean_install_test.py", target=args.mode, summary={"commands_checked": len(results), "findings": len(findings)}, findings=findings, skipped=skipped)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_out:
        write_markdown_report(args.markdown_out, "Clean Install Test Report", report, [str(item["command"]) for item in results])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
