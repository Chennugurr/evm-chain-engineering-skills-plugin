import json
import subprocess
import sys
from conftest import PLUGIN, ROOT


def test_secret_scan_passes():
    script = PLUGIN / "scripts" / "scan_secrets.py"
    result = subprocess.run([sys.executable, str(script), "--path", str(ROOT), "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["findings"] == []
