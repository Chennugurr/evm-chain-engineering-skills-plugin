import subprocess
import sys
from conftest import PLUGIN, ROOT


def test_render_scripts_dry_run():
    scripts = [
        ["render_docker_compose.py", "--dry-run"],
        ["render_systemd_units.py", "--dry-run"],
        ["render_prometheus_alerts.py"],
    ]
    for args in scripts:
        result = subprocess.run([sys.executable, str(PLUGIN / "scripts" / args[0]), *args[1:]], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0, result.stderr
        assert "latest" not in result.stdout.lower()
        assert "external-secret-ref" in result.stdout or "runbook_url" in result.stdout or "EnvironmentFile" in result.stdout


def test_templates_do_not_use_latest_tags():
    for path in (PLUGIN / "templates").rglob("*"):
        if path.is_file():
            assert ":latest" not in path.read_text().lower(), path
