from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

VERSION = "v0.2.0-alpha"


@dataclass
class Finding:
    level: str
    path: str
    message: str


@dataclass
class Report:
    ok: bool
    script: str
    target: str
    version: str = VERSION
    checked_at: None = None
    summary: dict[str, Any] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def payload(self) -> dict[str, Any]:
        return asdict(self)


def write_json_report(path: str | Path, report: Report | dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = report.payload() if isinstance(report, Report) else report
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown_report(path: str | Path, title: str, report: Report | dict[str, Any], commands: list[str] | None = None) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = report.payload() if isinstance(report, Report) else report
    findings = payload.get("findings", []) or []
    skipped = payload.get("skipped", []) or []
    ok = bool(payload.get("ok", False))
    lines = [f"# {title}", "", f"Status: {'PASS' if ok else 'FAIL'}", "", "## Summary", ""]
    for key, value in sorted((payload.get("summary") or {}).items()):
        lines.append(f"- {key}: {value}")
    if not (payload.get("summary") or {}):
        lines.append("- No summary fields recorded.")
    lines.extend(["", "## Findings", ""])
    if findings:
        lines.append("| Level | Path | Message |")
        lines.append("|---|---|---|")
        for item in findings:
            level = item.get("level", "info") if isinstance(item, dict) else getattr(item, "level", "info")
            path_value = item.get("path", "") if isinstance(item, dict) else getattr(item, "path", "")
            message = item.get("message", "") if isinstance(item, dict) else getattr(item, "message", "")
            lines.append(f"| {level} | {path_value} | {message} |")
    else:
        lines.append("None.")
    lines.extend(["", "## Skipped Checks", ""])
    if skipped:
        lines.extend([f"- {item}" for item in skipped])
    else:
        lines.append("None.")
    lines.extend(["", "## Commands", ""])
    if commands:
        lines.extend([f"- `{item}`" for item in commands])
    else:
        lines.append("Not recorded.")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_human(report: Report) -> None:
    print(f"status: {'pass' if report.ok else 'fail'}")
    for key, value in sorted(report.summary.items()):
        print(f"{key}: {value}")
    for finding in report.findings:
        print(f"{finding.level}: {finding.path}: {finding.message}")
    for item in report.skipped:
        print(f"skipped: {item}")
