#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from lib.dogfood import PLATFORMS, expected_by_id
from lib.repo import find_repo_root, relpath

ROOT = find_repo_root(Path(__file__))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a v0.3 live-run package skeleton from the checked-in template.")
    parser.add_argument("--platform", required=True, choices=list(PLATFORMS))
    parser.add_argument("--prompt-id", required=True)
    parser.add_argument("--operator", default="operator")
    parser.add_argument("--output")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    expected = expected_by_id(ROOT)
    if args.prompt_id not in expected:
        print(f"unknown prompt id: {args.prompt_id}")
        return 2
    template = ROOT / "dogfood" / "templates" / "live-run-package"
    out = Path(args.output) if args.output else ROOT / "dogfood" / "live-runs" / args.platform / args.prompt_id
    if out.exists() and not args.overwrite:
        print(f"output exists: {out}")
        return 2
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(template, out)
    meta_path = out / "METADATA.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update({"platform": args.platform, "prompt_id": args.prompt_id, "expected": "EXPECTED.yaml", "created_by": args.operator})
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    expected_path = out / "EXPECTED.yaml"
    expected_path.write_text(f"id: {args.prompt_id}\nexpected_source: dogfood/expected/{args.prompt_id}.yaml\n", encoding="utf-8")
    payload = {"status": "ok", "path": relpath(out, ROOT), "platform": args.platform, "prompt_id": args.prompt_id}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"created: {payload['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
