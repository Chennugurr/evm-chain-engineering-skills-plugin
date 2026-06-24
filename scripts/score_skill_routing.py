#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.dogfood import expected_by_id, load_json_file, transcript_paths, write_json
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))


def build_scorecard(platform: str | None) -> tuple[dict, list[Finding]]:
    expected = expected_by_id(ROOT)
    paths = transcript_paths(ROOT, platform)
    findings: list[Finding] = []
    prompt_scores: dict[str, dict] = {}
    platform_scores: dict[str, dict] = {"codex": {"score": 0, "confidence": "low", "runs": 0}, "claude": {"score": 0, "confidence": "low", "runs": 0}}
    total = 0
    count = 0
    for path in paths:
        data = load_json_file(path)
        if data.get("failures"):
            continue
        prompt_id = str(data.get("prompt_id"))
        contract = expected.get(prompt_id, {})
        observed = set(data.get("skills_observed", []) or [])
        expected_skills = set(contract.get("expected_skills", []) or [])
        forbidden = set(contract.get("forbidden_skills", []) or [])
        missing = sorted(expected_skills - observed)
        irrelevant = sorted(forbidden & observed)
        denom = max(len(expected_skills) + len(forbidden), 1)
        score = max(0, round(100 * (denom - len(missing) - len(irrelevant)) / denom))
        prompt_scores[prompt_id] = {"score": score, "missing_expected_skills": missing, "irrelevant_skills": irrelevant, "notes": []}
        platform_name = str(data.get("platform"))
        if platform_name in platform_scores:
            prev_runs = int(platform_scores[platform_name]["runs"])
            prev_total = int(platform_scores[platform_name]["score"]) * prev_runs
            platform_scores[platform_name]["runs"] = prev_runs + 1
            platform_scores[platform_name]["score"] = round((prev_total + score) / (prev_runs + 1))
            platform_scores[platform_name]["confidence"] = "medium"
        total += score
        count += 1
    overall = round(total / count) if count else 0
    confidence = "medium" if count else "low"
    scorecard = {
        "overall_score": overall,
        "confidence": confidence,
        "platforms": platform_scores,
        "prompts": prompt_scores,
        "recommendations": [{"skill": "chain-security-reviewer", "reason": "Keep security review required for sensitive live workflows."}],
    }
    return scorecard, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score v0.3 live skill routing from transcript metadata.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--platform", choices=["codex", "claude"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    strict = args.strict and not args.bootstrap
    scorecard, findings = build_scorecard(args.platform)
    if strict and not transcript_paths(ROOT, args.platform):
        findings.append(Finding("error", "dogfood/transcripts", "strict mode requires transcripts before scoring skill routing"))
    if strict:
        for path in transcript_paths(ROOT, args.platform):
            data = load_json_file(path)
            if data.get("failures"):
                findings.append(Finding("error", str(path), "strict mode does not score transcripts with unresolved failures"))
        if scorecard["overall_score"] < 85:
            findings.append(Finding("error", "dogfood/transcripts", "strict mode requires skill routing score >= 85"))
    if args.json_out:
        write_json(Path(args.json_out), scorecard)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Skill Routing Scorecard", {"ok": not findings, "summary": {"overall_score": scorecard["overall_score"], "confidence": scorecard["confidence"]}, "findings": [f.__dict__ for f in findings]}, ["score_skill_routing"])
    report = Report(ok=not findings, script="scripts/score_skill_routing.py", target=args.platform or "dogfood/transcripts", summary={"mode": "strict" if strict else "bootstrap", "overall_score": scorecard["overall_score"], "confidence": scorecard["confidence"], "transcripts_scored": len(transcript_paths(ROOT, args.platform))}, findings=findings)
    if args.json:
        print(json.dumps(scorecard if args.json_out else report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
