#!/usr/bin/env python3
"""Lightweight documentation quality checks for release-critical plugin docs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SECRET_SHAPED = re.compile(r"0x[a-fA-F0-9]{64}|\bAKIA[0-9A-Z]{16}\b|-----BEGIN [A-Z ]*PRIVATE KEY-----")
RELEASE_DOCS = [Path("README.md"), Path("RELEASE_CHECKLIST.md"), Path("CHANGELOG.md"), Path("FINAL_REPORT.md")]
REQUIRED_README_SECTIONS = ["What this plugin is", "What it is not", "Supported workflows", "Safety model", "Dogfood workflow", "Behavior evals", "Golden demos", "Release validation"]


def markdown_files() -> list[Path]:
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts and "__pycache__" not in p.parts]


def check(strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for path in markdown_files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if SECRET_SHAPED.search(text):
            errors.append(f"{rel}: key-shaped test data detected")
        if rel in RELEASE_DOCS and re.search(r"TODO|FIXME", text):
            warnings.append(f"{rel}: TODO/FIXME in release-critical doc")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "codex://", "mailto:", "#")):
                continue
            local = (path.parent / target.split("#", 1)[0]).resolve()
            if not local.exists():
                warnings.append(f"{rel}: possible broken local link {target}")
        for match in re.finditer(r"(?i).{0,80}\b(production|mainnet)\b.{0,80}", text):
            window = match.group(0).lower()
            if not any(word in window for word in ["dry", "review", "approval", "human", "do not", "never", "security"]):
                warnings.append(f"{rel}: production/mainnet mention may need nearby dry-run/review language")
                break
    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for section in REQUIRED_README_SECTIONS:
            if f"## {section}" not in text:
                errors.append(f"README.md missing section: {section}")
    else:
        errors.append("README.md missing")
    for doc in RELEASE_DOCS:
        if not (ROOT / doc).exists():
            errors.append(f"missing release-critical doc: {doc}")
    if strict:
        return errors, warnings
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan markdown docs for release-critical quality issues.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    errors, warnings = check(args.strict)
    status = "fail" if errors else ("warn" if warnings else "pass")
    payload = {"status": status, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status: {status}")
        for error in errors:
            print(f"error: {error}")
        for warning in warnings:
            print(f"warning: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
