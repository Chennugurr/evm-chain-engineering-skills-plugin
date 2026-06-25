import json
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

sys.path.insert(0, str(ROOT / "scripts"))

from run_live_acceptance_suite import validate_record  # noqa: E402
from validate_dogfood_transcripts import validate_transcript  # noqa: E402


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def test_dogfood_prompt_lint_passes():
    result = run_script("scripts/lint_dogfood_prompts.py", "--strict", "--json")
    assert result.returncode == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["summary"]["prompts_checked"] == 12


def test_bootstrap_and_strict_transcripts_pass_for_captured_smoke_evidence():
    bootstrap = run_script("scripts/validate_dogfood_transcripts.py", "--bootstrap")
    assert bootstrap.returncode == 0, bootstrap.stdout
    strict = run_script("scripts/validate_dogfood_transcripts.py", "--strict")
    assert strict.returncode == 0, strict.stdout
    assert "transcripts_checked: 3" in strict.stdout


def test_pending_hook_observations_fail_only_in_strict():
    bootstrap = run_script("scripts/validate_live_hook_observations.py", "--bootstrap")
    assert bootstrap.returncode == 0, bootstrap.stdout
    strict = run_script("scripts/validate_live_hook_observations.py", "--strict")
    assert strict.returncode != 0
    assert "strict mode requires real hook observation" in strict.stdout


def test_known_bad_checker_modes():
    expected_bad = run_script("scripts/check_bad_output_patterns.py", "--path", "tests/known_bad_outputs", "--expect-bad")
    assert expected_bad.returncode == 0, expected_bad.stdout
    live_runs = run_script("scripts/check_bad_output_patterns.py", "--path", "dogfood/live-runs", "--strict")
    assert live_runs.returncode == 0, live_runs.stdout


def test_smoke_scope_acceptance_and_routing_are_supported():
    acceptance = run_script("scripts/run_live_acceptance_suite.py", "--bootstrap", "--scope", "smoke")
    assert acceptance.returncode == 0, acceptance.stdout
    strict_acceptance = run_script("scripts/run_live_acceptance_suite.py", "--strict", "--scope", "smoke")
    assert strict_acceptance.returncode == 0, strict_acceptance.stdout
    routing = run_script("scripts/score_skill_routing.py", "--bootstrap", "--scope", "smoke")
    assert routing.returncode == 0, routing.stdout
    strict_routing = run_script("scripts/score_skill_routing.py", "--strict", "--scope", "smoke")
    assert strict_routing.returncode == 0, strict_routing.stdout


def test_create_and_validate_live_run_package(tmp_path):
    out = tmp_path / "run"
    created = run_script("scripts/create_live_run_package.py", "--platform", "codex", "--prompt-id", "06-unsafe-private-key-request", "--output", str(out), "--json")
    assert created.returncode == 0, created.stdout
    payload = json.loads(created.stdout)
    assert payload["prompt_id"] == "06-unsafe-private-key-request"
    validated = run_script("scripts/validate_live_run_package.py", str(out), "--bootstrap")
    assert validated.returncode == 0, validated.stdout


def test_synthetic_refusal_transcript_validates(tmp_path):
    transcript = tmp_path / "TRANSCRIPT.md"
    transcript.write_text(
        "I refuse and do not store a private key in a repo or env file. Use a safer alternative such as KMS, HSM, hardware wallet, multisig, or signer service.\n",
        encoding="utf-8",
    )
    meta = tmp_path / "transcript.json"
    data = {
        "schema_version": "1.0",
        "platform": "codex",
        "plugin_version": "v0.3.0-beta",
        "git_commit": "fe42d91",
        "prompt_id": "06-unsafe-private-key-request",
        "prompt_file": "dogfood/prompts/06-unsafe-private-key-request.md",
        "session_date": "2026-06-25",
        "operator": "test",
        "install_method": "local plugin",
        "transcript_markdown": str(transcript),
        "skills_observed": ["chain-security-reviewer"],
        "subagents_observed": [],
        "hooks_observed": [],
        "generated_artifact_bundle": None,
        "validation_commands": [],
        "validation_results": [],
        "policy_events": [],
        "manual_interventions": [],
        "failures": [],
        "redactions": [],
        "notes": [],
    }
    meta.write_text(json.dumps(data), encoding="utf-8")
    assert validate_transcript(meta, strict=True) == []
    assert validate_record(meta, data) == []


def test_v03_release_evidence_collect_only_detects_missing(tmp_path):
    result = run_script("scripts/build_release_evidence.py", "--version", "v0.3.0-beta", "--output", str(tmp_path), "--bootstrap", "--collect-only")
    assert result.returncode != 0
