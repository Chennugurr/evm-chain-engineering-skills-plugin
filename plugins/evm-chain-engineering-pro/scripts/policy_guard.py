#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root))
runpy.run_path(str(root / "scripts" / "policy_guard.py"), run_name="__main__")
