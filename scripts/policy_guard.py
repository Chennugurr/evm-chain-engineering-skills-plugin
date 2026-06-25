#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "plugins" / "evm-chain-engineering-pro" / "scripts" / "_policy_guard_impl.py"

if __name__ == "__main__":
    runpy.run_path(str(IMPL), run_name="__main__")
