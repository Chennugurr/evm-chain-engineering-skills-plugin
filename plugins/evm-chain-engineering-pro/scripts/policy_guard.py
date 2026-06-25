#!/usr/bin/env python3
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def candidate_roots() -> list[Path]:
    roots: list[Path] = []
    for env_name in ("PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT"):
        value = os.environ.get(env_name)
        if value:
            roots.append(Path(value))
    here = Path(__file__).resolve()
    roots.extend([here.parents[1], here.parents[3] / "plugins" / "evm-chain-engineering-pro"])
    return roots


def find_impl() -> Path:
    for root in candidate_roots():
        impl = root / "scripts" / "_policy_guard_impl.py"
        if impl.exists():
            return impl
    print("policy guard implementation not found", file=sys.stderr)
    raise SystemExit(2)


if __name__ == "__main__":
    runpy.run_path(str(find_impl()), run_name="__main__")
