#!/usr/bin/env python3
"""Run internal release readiness checks for evm-chain-engineering-pro."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def run(name: str, command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout
    if len(output) > 4000:
        output = "[truncated]\n" + output[-4000:]
    return {"name": name, "command": " ".join(command), "returncode": result.returncode, "output": output}


def scripts_help() -> dict[str, Any]:
    scripts = sorted((ROOT / "scripts").glob("*.py")) + sorted((ROOT / "plugins" / "evm-chain-engineering-pro" / "scripts").glob("*.py"))
    failures: list[str] = []
    for script in scripts:
        result = subprocess.run([sys.executable, str(script), "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            failures.append(str(script.relative_to(ROOT)))
    return {"name": "scripts --help", "command": "all scripts --help", "returncode": 1 if failures else 0, "output": "failures: " + ", ".join(failures)}


def local_path_check() -> dict[str, Any]:
    allowed = {str(ROOT)}
    home = str(Path.home())
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        rel = str(path.relative_to(ROOT))
        if rel.startswith("tests/") or rel == "scripts/clean_install_test.py":
            continue
        if rel.startswith("docs/") or rel in {"README.md", "FINAL_REPORT.md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if home in text and not any(item in text for item in allowed):
            offenders.append(rel)
    return {"name": "local-only paths", "command": "scan text files", "returncode": 1 if offenders else 0, "output": "\n".join(offenders)}


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = ["# Release Readiness Report", "", f"- Status: {payload['status']}", f"- Checks: {len(payload['checks'])}", ""]
    for check in payload["checks"]:
        mark = "PASS" if check["returncode"] == 0 else "FAIL"
        lines.extend([f"## {check['name']}", "", f"- Result: {mark}", f"- Command: `{check['command']}`", ""])
        if check.get("output"):
            lines.extend(["```txt", str(check["output"]).strip(), "```", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run release readiness checks without publishing or deploying.")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    checks = [
        run("pytest", [sys.executable, "-m", "pytest"]),
        run("make validate", ["make", "validate"]),
        run("hook validation", [sys.executable, "scripts/validate_hooks.py", "--plugin-root", "plugins/evm-chain-engineering-pro", "--strict"]),
        run("behavior eval schema", [sys.executable, "scripts/run_behavior_evals.py", "--evals", "evals/skill-trigger-matrix.yaml", "--strict"]),
        run("secret scan", [sys.executable, "plugins/evm-chain-engineering-pro/scripts/scan_secrets.py", "--path", ".", "--strict", "--json"]),
        run("docs quality", [sys.executable, "scripts/check_docs_quality.py", "--strict"]),
        scripts_help(),
        local_path_check(),
    ]
    if shutil.which("claude"):
        checks.append(run("claude plugin validate", ["claude", "plugin", "validate", "plugins/evm-chain-engineering-pro", "--strict"]))
    else:
        checks.append({"name": "claude plugin validate", "command": "claude plugin validate plugins/evm-chain-engineering-pro --strict", "returncode": 0, "output": "skipped: claude CLI not installed"})
    for required in ["RELEASE_CHECKLIST.md", "CHANGELOG.md", "FINAL_REPORT.md"]:
        exists = (ROOT / required).exists()
        checks.append({"name": f"asset {required}", "command": f"test -f {required}", "returncode": 0 if exists else 1, "output": "" if exists else "missing"})
    failed = [check for check in checks if check["returncode"] != 0]
    status = "fail" if failed else "pass"
    payload = {"status": status, "checks": checks, "next_actions": [f"Fix {c['name']}" for c in failed]}
    if args.markdown_report:
        write_markdown(Path(args.markdown_report), payload)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status: {status}")
        for check in checks:
            print(f"{'PASS' if check['returncode'] == 0 else 'FAIL'} {check['name']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
