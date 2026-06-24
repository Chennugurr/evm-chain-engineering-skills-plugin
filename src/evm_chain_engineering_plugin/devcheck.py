from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = sorted((ROOT / "plugins" / "evm-chain-engineering-pro" / "scripts").glob("*.py"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Developer checks for the plugin repository.")
    parser.add_argument("--scripts-help", action="store_true")
    args = parser.parse_args()
    if args.scripts_help:
        for script in SCRIPTS:
            result = subprocess.run([sys.executable, str(script), "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(result.stderr)
                return result.returncode
        print(f"checked {len(SCRIPTS)} script help pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
