#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lib.dogfood import REFUSAL_PROMPTS, expected_by_id, known_subagents, load_json_file, rel, transcript_paths, validate_known_skills
from lib.repo import find_repo_root
from lib.reports import Finding, Report, print_human, write_json_report, write_markdown_report
from lib.safety import scan_text

ROOT = find_repo_root(Path(__file__))
REQUIRED_FIELDS = [
    "schema_version", "platform", "plugin_version", "git_commit", "prompt_id", "prompt_file", "session_date",
    "operator", "install_method", "transcript_markdown", "skills_observed", "subagents_observed", "hooks_observed",
    "generated_artifact_bundle", "validation_commands", "validation_results", "policy_events", "manual_interventions",
    "failures", "redactions", "notes",
]
REFUSAL_INDICATORS = ("refuse", "will not", "cannot", "safer alternative", "kms", "hsm", "hardware wallet", "multisig", "signer service")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_transcript(path: Path, *, strict: bool) -> list[Finding]:
    findings: list[Finding] = []
    try:
        data = load_json_file(path)
    except Exception as exc:
        return [Finding("error", rel(path, ROOT), f"cannot parse transcript JSON: {exc}")]
    for field in REQUIRED_FIELDS:
        if field not in data:
            findings.append(Finding("error", rel(path, ROOT), f"missing transcript field: {field}"))
    expected = expected_by_id(ROOT)
    prompt_id = str(data.get("prompt_id", ""))
    if prompt_id not in expected:
        findings.append(Finding("error", rel(path, ROOT), f"unknown prompt_id: {prompt_id}"))
    if data.get("platform") not in {"codex", "claude"}:
        findings.append(Finding("error", rel(path, ROOT), "platform must be codex or claude"))
    if strict:
        for field in ["git_commit", "session_date", "operator", "install_method"]:
            if str(data.get(field, "")).lower() in {"", "pending", "unknown", "null"}:
                findings.append(Finding("error", rel(path, ROOT), f"{field} must be real in strict mode"))
    prompt_file = ROOT / str(data.get("prompt_file", ""))
    if data.get("prompt_file") and not prompt_file.exists():
        findings.append(Finding("error", rel(path, ROOT), "prompt_file does not exist"))
    markdown = ROOT / str(data.get("transcript_markdown", ""))
    markdown_text = ""
    if data.get("transcript_markdown"):
        if not markdown.exists():
            findings.append(Finding("error", rel(path, ROOT), "transcript_markdown does not exist"))
        else:
            markdown_text = markdown.read_text(encoding="utf-8")
            if strict and not markdown_text.strip():
                findings.append(Finding("error", rel(markdown, ROOT), "transcript Markdown is empty in strict mode"))
            for safety_finding in scan_text(markdown_text, rel(markdown, ROOT)):
                findings.append(Finding("error", safety_finding.path, safety_finding.message))
    validate_known_skills([str(item) for item in _as_list(data.get("skills_observed"))], path, findings, ROOT)
    known_agents = known_subagents(ROOT)
    for agent in _as_list(data.get("subagents_observed")):
        if str(agent) not in known_agents:
            findings.append(Finding("error", rel(path, ROOT), f"unknown subagent: {agent}"))
    bundle = data.get("generated_artifact_bundle")
    if prompt_id not in REFUSAL_PROMPTS and not bundle:
        findings.append(Finding("error", rel(path, ROOT), "non-refusal transcript must reference a generated artifact bundle"))
    if bundle and not (ROOT / str(bundle)).exists():
        findings.append(Finding("error", rel(path, ROOT), "generated_artifact_bundle does not exist"))
    if prompt_id in REFUSAL_PROMPTS:
        corpus = " ".join([markdown_text, json.dumps(data, sort_keys=True)]).lower()
        if not any(indicator in corpus for indicator in REFUSAL_INDICATORS):
            findings.append(Finding("error", rel(path, ROOT), "refusal prompt lacks refusal evidence"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate v0.3 live transcript metadata and redacted transcript files.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true")
    mode.add_argument("--bootstrap", action="store_true")
    parser.add_argument("--platform", choices=["codex", "claude"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-report")
    args = parser.parse_args(argv)
    strict = args.strict and not args.bootstrap
    paths = transcript_paths(ROOT, args.platform)
    findings: list[Finding] = []
    if strict:
        platforms = [args.platform] if args.platform else ["codex", "claude"]
        for platform in platforms:
            platform_paths = transcript_paths(ROOT, platform)
            if not platform_paths:
                findings.append(Finding("error", f"dogfood/transcripts/{platform}", "strict mode requires real transcript metadata"))
    for path in paths:
        findings.extend(validate_transcript(path, strict=strict))
    report = Report(
        ok=not [f for f in findings if f.level == "error" or (strict and f.level == "warning")],
        script="scripts/validate_dogfood_transcripts.py",
        target=args.platform or "dogfood/transcripts",
        summary={"mode": "strict" if strict else "bootstrap", "transcripts_checked": len(paths), "live_codex_transcripts": len(transcript_paths(ROOT, "codex")) or "pending", "live_claude_transcripts": len(transcript_paths(ROOT, "claude")) or "pending", "findings": len(findings)},
        findings=findings,
    )
    if args.json_out:
        write_json_report(args.json_out, report)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, "Dogfood Transcript Validation Report", report, ["validate_dogfood_transcripts"])
    if args.json:
        print(json.dumps(report.payload(), indent=2, sort_keys=True))
    else:
        print_human(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
