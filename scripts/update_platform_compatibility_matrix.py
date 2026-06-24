#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.dogfood import hook_observation_paths, load_json_file, transcript_paths
from lib.repo import find_repo_root

ROOT = find_repo_root(Path(__file__))


def platform_status(platform: str) -> dict[str, str]:
    transcripts = transcript_paths(ROOT, platform)
    hook_path = hook_observation_paths(ROOT, platform)[0]
    hook_status = "pending"
    if hook_path.exists():
        try:
            hook_status = str(load_json_file(hook_path).get("status", "pending"))
        except Exception:
            hook_status = "invalid"
    return {
        "live_transcripts": "yes" if transcripts else "pending",
        "hook_activation": hook_status,
        "skill_observation": "pending" if not transcripts else "partial",
        "artifact_generation": "pending" if not transcripts else "partial",
    }


def render() -> str:
    lines = [
        "# Platform Compatibility Matrix",
        "",
        "Generated from v0.3 local evidence. `pending` means bootstrap-compatible but not strict-release-ready.",
        "",
        "| Platform | Live Transcripts | Hook Activation | Skill Observation | Artifact Generation |",
        "|---|---|---|---|---|",
    ]
    for platform in ["codex", "claude"]:
        status = platform_status(platform)
        lines.append(f"| {platform} | {status['live_transcripts']} | {status['hook_activation']} | {status['skill_observation']} | {status['artifact_generation']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update or print the v0.3 platform compatibility matrix from local evidence.")
    parser.add_argument("--output", default="docs/platform-compatibility-matrix.md")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    content = render()
    out = ROOT / args.output
    if args.check:
        ok = out.exists() and out.read_text(encoding="utf-8") == content
        if args.json:
            print(json.dumps({"ok": ok, "path": args.output}, indent=2, sort_keys=True))
        else:
            print("status: pass" if ok else "status: fail")
        return 0 if ok else 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    if args.json:
        print(json.dumps({"ok": True, "path": args.output}, indent=2, sort_keys=True))
    else:
        print(f"updated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
