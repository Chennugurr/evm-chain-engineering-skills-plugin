import subprocess
import sys
import shutil
from conftest import ROOT


def test_generated_configs_validate():
    result = subprocess.run([sys.executable, "scripts/validate_generated_configs.py", "--strict", "--all", "fixtures/artifact-bundles", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout


def test_latest_image_fails(tmp_path):
    src = ROOT / "fixtures/artifact-bundles/op-stack-public-testnet"
    dst = tmp_path / "bundle"
    shutil.copytree(src, dst)
    compose = dst / "configs/docker-compose/docker-compose.yaml"
    compose.write_text(compose.read_text().replace(":v0.0.0-placeholder", ":latest"))
    result = subprocess.run([sys.executable, "scripts/validate_generated_configs.py", "--strict", "--path", str(dst)], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode != 0


def test_inline_secret_env_fails(tmp_path):
    src = ROOT / "fixtures/artifact-bundles/op-stack-public-testnet"
    dst = tmp_path / "bundle"
    shutil.copytree(src, dst)
    compose = dst / "configs/docker-compose/docker-compose.yaml"
    compose.write_text(compose.read_text() + "      PRIVATE_KEY: not-safe-placeholder\n")
    result = subprocess.run([sys.executable, "scripts/validate_generated_configs.py", "--strict", "--path", str(dst)], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode != 0
