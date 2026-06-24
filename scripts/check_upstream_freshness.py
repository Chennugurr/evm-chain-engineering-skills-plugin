#!/usr/bin/env python3
"""Check upstream source freshness without requiring internet by default."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
THRESHOLDS = {"stable": 180, "medium": 90, "volatile": 30}

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_markdown_table(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    records: list[dict[str, Any]] = []
    headers: list[str] | None = None
    in_structured = False
    for line in lines:
        if line.strip().lower().startswith("## structured source records"):
            in_structured = True
            continue
        if not in_structured or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        if headers is None:
            headers = [re.sub(r"[^a-z0-9]+", "_", c.lower()).strip("_") for c in cells]
            continue
        if len(cells) == len(headers):
            records.append(dict(zip(headers, cells)))
    return records


def parse_sources(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML unavailable for YAML source records")
        data = yaml.safe_load(text)
        return list(data.get("sources", data)) if isinstance(data, dict) else list(data)
    records = parse_markdown_table(text)
    if records:
        return records
    fallback_date = None
    match = re.search(r"Retrieval date:\s*(\d{4}-\d{2}-\d{2})", text)
    if match:
        fallback_date = match.group(1)
    sections = re.findall(r"^##\s+(.+?)\n\n- URL:\s*(.+?)\n", text, re.M)
    return [{"stack": name, "topic": name, "url": url, "source_type": "official docs", "dependent_skills": "unknown", "volatility": "medium", "last_checked": fallback_date or "1970-01-01", "checked_by": "unknown", "notes": "Parsed from legacy free-form source section"} for name, url in sections]


def url_reachable(url: str, timeout: float = 5.0) -> tuple[str, str]:
    if url.startswith("file://"):
        return "skipped", "local file source"
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "evm-chain-engineering-freshness/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - explicit URL from maintained docs
            return "ok", str(response.status)
    except Exception as exc:  # noqa: BLE001
        return "unknown", str(exc)


def assess(records: list[dict[str, Any]], *, max_age_days: int | None, online: bool, strict_online: bool) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    today = date.today()
    warnings: list[str] = []
    errors: list[str] = []
    enriched: list[dict[str, Any]] = []
    for record in records:
        volatility = str(record.get("volatility", "medium")).strip().lower() or "medium"
        threshold = max_age_days if max_age_days is not None else THRESHOLDS.get(volatility, 90)
        last_checked = str(record.get("last_checked", "")).strip()
        parsed = parse_date(last_checked)
        status = "ok"
        age = None
        if parsed is None:
            warnings.append(f"{record.get('topic', record.get('stack', 'source'))}: missing or invalid last_checked")
            status = "unknown"
        else:
            age = (today - parsed).days
            if age > threshold:
                warnings.append(f"{record.get('topic', record.get('stack', 'source'))}: stale {volatility} source checked {age} days ago")
                status = "stale"
        if online:
            reachability, note = url_reachable(str(record.get("url", "")))
            record["reachability"] = reachability
            record["reachability_note"] = note
            if reachability == "unknown" and strict_online:
                errors.append(f"{record.get('topic', record.get('stack', 'source'))}: URL check failed: {note}")
        else:
            record["reachability"] = "offline-not-checked"
        record["freshness_status"] = status
        if age is not None:
            record["age_days"] = age
        enriched.append(record)
    return errors, warnings, enriched


def write_markdown(path: Path, status: str, errors: list[str], warnings: list[str], records: list[dict[str, Any]]) -> None:
    lines = ["# Upstream Freshness Report", "", f"- Status: {status}", f"- Sources: {len(records)}", f"- Errors: {len(errors)}", f"- Warnings: {len(warnings)}", "", "| Stack | Topic | Volatility | Last checked | Status | Reachability |", "|---|---|---|---|---|---|"]
    for r in records:
        lines.append(f"| {r.get('stack','')} | {r.get('topic','')} | {r.get('volatility','')} | {r.get('last_checked','')} | {r.get('freshness_status','')} | {r.get('reachability','')} |")
    if warnings:
        lines.extend(["", "## Warnings", ""] + [f"- {w}" for w in warnings])
    if errors:
        lines.extend(["", "## Errors", ""] + [f"- {e}" for e in errors])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check maintained upstream source records for stale dates and optional URL reachability.")
    parser.add_argument("--sources", default="docs/upstream-sources.md")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown-report")
    parser.add_argument("--max-age-days", type=int)
    parser.add_argument("--allow-offline", action="store_true")
    parser.add_argument("--strict-online", action="store_true")
    args = parser.parse_args(argv)
    records = parse_sources(Path(args.sources))
    online = not args.allow_offline
    errors, warnings, enriched = assess(records, max_age_days=args.max_age_days, online=online, strict_online=args.strict_online)
    status = "fail" if errors else ("warn" if warnings else "pass")
    payload = {"status": status, "errors": errors, "warnings": warnings, "sources": enriched}
    if args.markdown_report:
        write_markdown(Path(args.markdown_report), status, errors, warnings, enriched)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status: {status}")
        for warning in warnings:
            print(f"warning: {warning}")
        for error in errors:
            print(f"error: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
