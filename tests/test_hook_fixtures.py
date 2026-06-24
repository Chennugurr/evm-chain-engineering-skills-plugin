import subprocess
import sys
from conftest import ROOT


def test_hook_fixtures_pass():
    result = subprocess.run([sys.executable, "scripts/test_hook_fixtures.py", "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout


def test_secret_fixture_blocks():
    fixture = ROOT / "tests/fixtures/hooks/codex-pre-command-secret.json"
    result = subprocess.run([sys.executable, "scripts/test_hook_fixtures.py", "--fixture", str(fixture), "--strict"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
