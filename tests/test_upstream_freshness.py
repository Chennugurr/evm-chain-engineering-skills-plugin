import subprocess
import sys
from conftest import ROOT


def test_upstream_freshness_offline_report(tmp_path):
    report = tmp_path / "freshness.md"
    result = subprocess.run([sys.executable, "scripts/check_upstream_freshness.py", "--sources", "docs/upstream-sources.md", "--markdown-report", str(report), "--allow-offline", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Upstream Freshness Report" in report.read_text()


def test_upstream_source_records_reference_known_skills():
    text = (ROOT / "docs" / "upstream-sources.md").read_text()
    assert "## Structured Source Records" in text
    assert "op-stack-engineer" in text
    assert "zksync-zk-stack-engineer" in text
