import subprocess
import sys
import shutil
from conftest import ROOT


def test_acceptance_suite_passes():
    result = subprocess.run([sys.executable, "scripts/run_acceptance_suite.py", "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout


def test_acceptance_case_passes_single():
    result = subprocess.run([sys.executable, "scripts/run_acceptance_suite.py", "--case", "unsafe-private-key-request", "--strict"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
