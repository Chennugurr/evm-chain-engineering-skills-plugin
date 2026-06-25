#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.dogfood import known_subagents, load_json_file, transcript_paths
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report

ROOT = find_repo_root(Path(__file__))
LIMITATION_PATH = ROOT / "dogfood" / "reports" / "subagent-dogfood-limitation.md"


def observed_prompt_11(platform: str | None) -> tuple[int, int]:
    prompt_11 = 0
    subagent_runs = 0
    for path in transcript_paths(ROOT, platform):
        try:
            data = load_json_file(path)
        except Exception:
            continue
        if data.get("prompt_id") == "11-multi-agent-chain-review":
            prompt_11 += 1
            if data.get("subagents_observed"):
                subagent_runs += 1
    return prompt_11, subagent_runs


def documented_limitation() -> bool:
    if not LIMITATION_PATH.exists():
        return False
    text = LIMITATION_PATH.read_text(encoding="utf-8").lower()
    required = ["subagent", "limitation", "no live subagent claim"]
    return all(term in text for term in required)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate v0.3 multi-agent dogfood evidence without accepting fake subagent claims.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--platform", choices=["codex", "claude"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    strict = args.strict and not args.bootstrap
    known = known_subagents(ROOT)
    prompt_11, subagent_runs = observed_prompt_11(args.platform)
    limitation_recorded = documented_limitation()
    findings: list[Finding] = []
    if strict and prompt_11 == 0 and not limitation_recorded:
        findings.append(Finding("error", "dogfood/transcripts", "strict mode requires prompt 11 transcript or documented limitation"))
    if strict and prompt_11 and subagent_runs == 0 and not limitation_recorded:
        findings.append(Finding("error", "dogfood/transcripts", "prompt 11 transcript exists but no subagent evidence was observed"))
    report = Report(ok=not findings, script="scripts/validate_subagent_dogfood.py", target=args.platform or "dogfood/transcripts", summary={"mode": "strict" if strict else "bootstrap", "known_subagents": len(known), "prompt_11_transcripts": prompt_11, "subagent_runs": subagent_runs, "documented_limitation": limitation_recorded, "limitation_path": str(LIMITATION_PATH.relative_to(ROOT)) if limitation_recorded else None}, findings=findings)
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Subagent Dogfood Report", report, ["validate_subagent_dogfood"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
