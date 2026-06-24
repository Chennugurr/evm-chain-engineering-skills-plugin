import subprocess
import sys
from conftest import ROOT


def test_renderer_creates_valid_bundle(tmp_path):
    out = tmp_path / "rendered"
    result = subprocess.run([sys.executable, "scripts/render_artifact_bundle.py", "--workflow", "tmp-op", "--stack", "op-stack", "--chain-type", "l2", "--environment", "public-testnet", "--settlement", "ethereum-sepolia", "--output", str(out), "--overwrite"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
    assert (out / "04_CHAIN_SPEC.yaml").exists()


def test_renderer_dry_run_writes_nothing(tmp_path):
    out = tmp_path / "dry"
    result = subprocess.run([sys.executable, "scripts/render_artifact_bundle.py", "--workflow", "tmp-op", "--stack", "op-stack", "--chain-type", "l2", "--environment", "public-testnet", "--settlement", "ethereum-sepolia", "--output", str(out), "--dry-run"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout
    assert not out.exists()
