import json
import subprocess
import sys
from pathlib import Path
from conftest import PLUGIN, ROOT, SCRIPTS


def test_each_script_supports_help():
    scripts = sorted(SCRIPTS.glob("*.py"))
    assert len(scripts) == 13
    for script in scripts:
        result = subprocess.run([sys.executable, str(script), "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0, f"{script}: {result.stderr}"
        assert "usage:" in result.stdout.lower()


def test_representative_validators_on_fixtures(tmp_path):
    genesis = PLUGIN / "examples" / "l1-examples" / "genesis.json"
    result = subprocess.run([sys.executable, str(SCRIPTS / "validate_genesis.py"), "--genesis", str(genesis), "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["status"] == "ok"

    firewall = PLUGIN / "examples" / "public-testnet" / "firewall-policy.yml"
    result = subprocess.run([sys.executable, str(SCRIPTS / "validate_firewall_policy.py"), "--policy", str(firewall), "--environment", "public-testnet", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout

    out_dir = tmp_path / "adr"
    result = subprocess.run([
        sys.executable, str(SCRIPTS / "generate_adr.py"), "--title", "Test Chain", "--chain-type", "L2", "--stack", "op-stack", "--settlement", "Sepolia", "--data-availability", "Ethereum blobs", "--trust-assumptions", "test assumptions", "--open-questions", "none", "--output-dir", str(out_dir), "--json"
    ], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
    payload = json.loads(result.stdout)
    assert Path(payload["path"]).exists()
