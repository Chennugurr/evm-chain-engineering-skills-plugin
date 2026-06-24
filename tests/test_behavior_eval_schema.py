import subprocess
import sys
from conftest import ROOT


def test_behavior_eval_schema_passes_strict():
    result = subprocess.run([sys.executable, "scripts/run_behavior_evals.py", "--evals", "evals/skill-trigger-matrix.yaml", "--strict", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stdout + result.stderr


def test_behavior_eval_markdown_report(tmp_path):
    report = tmp_path / "report.md"
    result = subprocess.run([sys.executable, "scripts/run_behavior_evals.py", "--evals", "evals/skill-trigger-matrix.yaml", "--markdown-report", str(report)], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0
    assert "Behavior Eval Report" in report.read_text()
