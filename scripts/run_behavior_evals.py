#!/usr/bin/env python3
"""Validate deterministic skill-routing behavior evals and optionally score saved responses."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "plugins" / "evm-chain-engineering-pro" / "skills"
SECRET_SHAPED = re.compile(r"0x[a-fA-F0-9]{64}|\bAKIA[0-9A-Z]{16}\b|-----BEGIN [A-Z ]*PRIVATE KEY-----")
REQUIRED_CASE_FIELDS = {"id", "prompt", "expected_skills", "must_include", "must_not_include", "required_behavior", "safety_level", "review_notes"}

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def load_data(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("eval file must contain an object")
    return data


def known_skills() -> set[str]:
    return {p.name for p in SKILLS_ROOT.iterdir() if p.is_dir()}


def listify(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def contains_fragment(text: str, fragment: str) -> bool:
    if fragment.startswith("regex:"):
        return re.search(fragment[6:], text, re.I | re.S) is not None
    return fragment.lower() in text.lower()


def validate_schema(data: dict[str, Any]) -> tuple[list[str], list[str], dict[str, dict[str, int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    skills = known_skills()
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["cases must be a non-empty list"], warnings, {}
    seen: set[str] = set()
    coverage = {skill: {"expected": 0, "forbidden": 0} for skill in skills}
    for idx, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"case {idx} must be an object")
            continue
        missing = REQUIRED_CASE_FIELDS - set(case)
        if missing:
            errors.append(f"{case.get('id', idx)} missing fields: {', '.join(sorted(missing))}")
        case_id = str(case.get("id", ""))
        if not case_id:
            errors.append(f"case {idx} missing id")
        elif case_id in seen:
            errors.append(f"duplicate id: {case_id}")
        seen.add(case_id)
        if SECRET_SHAPED.search(str(case.get("prompt", ""))):
            errors.append(f"{case_id} contains key-shaped test data")
        expected = [str(s) for s in listify(case.get("expected_skills"))]
        forbidden = [str(s) for s in listify(case.get("forbidden_skills"))]
        for skill in expected:
            if skill not in skills:
                errors.append(f"{case_id} expected unknown skill: {skill}")
            else:
                coverage[skill]["expected"] += 1
        for skill in forbidden:
            if skill not in skills:
                errors.append(f"{case_id} forbids unknown skill: {skill}")
            else:
                coverage[skill]["forbidden"] += 1
        if not listify(case.get("must_include")):
            errors.append(f"{case_id} must_include must be non-empty")
        if "must_not_include" in case and not listify(case.get("must_not_include")):
            errors.append(f"{case_id} must_not_include must be non-empty")
        if str(case.get("safety_level", "")) not in {"normal", "sensitive", "production", "unsafe"}:
            errors.append(f"{case_id} has invalid safety_level")
    for skill, counts in sorted(coverage.items()):
        if counts["expected"] + counts["forbidden"] < 2:
            errors.append(f"skill coverage below 2 for {skill}")
    return errors, warnings, coverage


def score_responses(data: dict[str, Any], responses: Path | None) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    scores: dict[str, Any] = {}
    if responses is None:
        return errors, warnings, scores
    for case in data.get("cases", []):
        case_id = case["id"]
        candidates = [responses / f"{case_id}.md", responses / f"{case_id}.txt"]
        response_path = next((p for p in candidates if p.exists()), None)
        if response_path is None:
            warnings.append(f"missing response for {case_id}")
            continue
        text = response_path.read_text(encoding="utf-8")
        if SECRET_SHAPED.search(text):
            errors.append(f"{case_id} response contains key-shaped test data")
        missing = [frag for frag in case.get("must_include", []) if not contains_fragment(text, str(frag))]
        forbidden = [frag for frag in case.get("must_not_include", []) if contains_fragment(text, str(frag))]
        if missing:
            errors.append(f"{case_id} response missing: {', '.join(map(str, missing))}")
        if forbidden:
            errors.append(f"{case_id} response contains forbidden: {', '.join(map(str, forbidden))}")
        if case.get("safety_level") in {"sensitive", "production", "unsafe"}:
            if not re.search(r"(?im)^#+\s*assumptions", text):
                warnings.append(f"{case_id} response lacks visible assumptions section")
            if not re.search(r"(?im)^#+\s*(security|safety|trust)", text):
                warnings.append(f"{case_id} response lacks visible security/safety section")
        if any("dry-run" in str(item).lower() or "dry run" in str(item).lower() for item in case.get("required_behavior", [])) and not re.search(r"(?i)dry[- ]run", text):
            warnings.append(f"{case_id} response lacks dry-run wording")
        scores[case_id] = {"missing": missing, "forbidden": forbidden, "response": str(response_path)}
    return errors, warnings, scores


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = ["# Behavior Eval Report", "", f"- Status: {payload['status']}", f"- Total evals: {payload['total_evals']}", f"- Errors: {len(payload['errors'])}", f"- Warnings: {len(payload['warnings'])}", "", "## Coverage", ""]
    for skill, counts in sorted(payload["coverage"].items()):
        lines.append(f"- `{skill}`: expected {counts['expected']}, forbidden {counts['forbidden']}")
    if payload["errors"]:
        lines.extend(["", "## Errors", ""] + [f"- {e}" for e in payload["errors"]])
    if payload["warnings"]:
        lines.extend(["", "## Warnings", ""] + [f"- {w}" for w in payload["warnings"]])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate behavior eval schema and optionally score saved responses.")
    parser.add_argument("--evals", required=True)
    parser.add_argument("--responses")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown-report")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load_data(Path(args.evals))
    except Exception as exc:
        payload = {"status": "fail", "errors": [str(exc)], "warnings": [], "total_evals": 0, "coverage": {}, "scores": {}}
        print(json.dumps(payload, indent=2) if args.json else f"fail: {exc}")
        return 2
    errors, warnings, coverage = validate_schema(data)
    score_errors, score_warnings, scores = score_responses(data, Path(args.responses) if args.responses else None)
    errors.extend(score_errors)
    warnings.extend(score_warnings)
    status = "fail" if errors else ("warn" if warnings else "pass")
    payload = {"status": status, "total_evals": len(data.get("cases", [])), "errors": errors, "warnings": warnings, "coverage": coverage, "scores": scores}
    if args.markdown_report:
        write_markdown(Path(args.markdown_report), payload)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status: {status}")
        print(f"total evals: {payload['total_evals']}")
        for err in errors:
            print(f"error: {err}")
        for warn in warnings:
            print(f"warning: {warn}")
    if errors:
        return 1
    if warnings and args.strict and args.responses:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
