import subprocess
import sys
import shutil
from conftest import ROOT


def run_validator(path):
    return subprocess.run([sys.executable, "scripts/validate_artifact_bundle.py", "--strict", "--path", str(path)], cwd=ROOT, text=True, stdout=subprocess.PIPE)


def test_valid_artifact_bundle_passes():
    result = run_validator(ROOT / "fixtures/artifact-bundles/op-stack-public-testnet")
    assert result.returncode == 0, result.stdout


def test_missing_required_file_fails(tmp_path):
    src = ROOT / "fixtures/artifact-bundles/op-stack-public-testnet"
    dst = tmp_path / "bundle"
    shutil.copytree(src, dst)
    (dst / "04_CHAIN_SPEC.yaml").unlink()
    assert run_validator(dst).returncode != 0


def test_l2_without_settlement_fails(tmp_path):
    src = ROOT / "fixtures/artifact-bundles/op-stack-public-testnet"
    dst = tmp_path / "bundle"
    shutil.copytree(src, dst)
    spec = dst / "04_CHAIN_SPEC.yaml"
    text = spec.read_text().replace("layer: ethereum-sepolia", "layer: ''")
    spec.write_text(text)
    assert run_validator(dst).returncode != 0


def test_private_key_placeholder_name_fails(tmp_path):
    src = ROOT / "fixtures/artifact-bundles/op-stack-public-testnet"
    dst = tmp_path / "bundle"
    shutil.copytree(src, dst)
    (dst / "00_REQUEST.md").write_text("PRIVATE_KEY=<unsafe-placeholder-detected-by-name>\n")
    assert run_validator(dst).returncode != 0
