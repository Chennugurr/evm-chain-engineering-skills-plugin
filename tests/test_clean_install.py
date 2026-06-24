import subprocess
import sys
from conftest import ROOT


def test_clean_install_help():
    result = subprocess.run([sys.executable, "scripts/clean_install_test.py", "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0
