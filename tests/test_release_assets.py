import subprocess
import sys
from conftest import ROOT


def test_release_assets_exist_and_readme_sections():
    for path in ["RELEASE_CHECKLIST.md", "CHANGELOG.md", "README.md", "docs/dogfood-plan.md", "docs/usage-review.md"]:
        assert (ROOT / path).exists(), path
    readme = (ROOT / "README.md").read_text()
    for term in ["Dogfood workflow", "Behavior evals", "Golden demos", "Safety model", "Release validation"]:
        assert f"## {term}" in readme


def test_docs_quality_passes_without_errors():
    result = subprocess.run([sys.executable, "scripts/check_docs_quality.py", "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_unexpected_local_absolute_paths():
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        if "/home/iljanemesis" in text and "/home/iljanemesis/blockchain-engineering" not in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders
