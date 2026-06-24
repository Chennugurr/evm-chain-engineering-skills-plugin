import subprocess
import sys
from conftest import ROOT


def test_release_evidence_collect_only_detects_missing(tmp_path):
    result = subprocess.run([sys.executable, "scripts/build_release_evidence.py", "--version", "v0.2.0-alpha", "--output", str(tmp_path), "--collect-only", "--strict"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode != 0


def test_release_evidence_help():
    result = subprocess.run([sys.executable, "scripts/build_release_evidence.py", "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0
