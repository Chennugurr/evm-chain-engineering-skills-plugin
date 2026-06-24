#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from evm_chain_engineering_plugin.cli import main

if __name__ == "__main__":
    raise SystemExit(main(Path(__file__).name))
