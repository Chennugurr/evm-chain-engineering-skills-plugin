#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Render only 04_CHAIN_SPEC.yaml from a stack profile and CLI options.')
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--stack", required=True)
    parser.add_argument("--chain-type", default="l2")
    parser.add_argument("--environment", default="public-testnet")
    parser.add_argument("--settlement", default="VERIFY_CURRENT_DOCS")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / args.workflow
        cmd = [sys.executable, "scripts/render_artifact_bundle.py", "--workflow", args.workflow, "--stack", args.stack, "--chain-type", args.chain_type, "--environment", args.environment, "--settlement", args.settlement, "--output", str(out), "--overwrite", "--skip-validate"]
        result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            print(result.stdout)
            return result.returncode
        mapping = {"chain": "04_CHAIN_SPEC.yaml", "infra": "05_INFRASTRUCTURE_PLAN.md", "gates": "08_LAUNCH_GATES.md", "security": "06_SECURITY_REVIEW.md"}
        text = (out / mapping['chain']).read_text(encoding="utf-8")
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
