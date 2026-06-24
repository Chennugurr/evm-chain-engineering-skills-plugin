import subprocess
import sys
from conftest import ROOT


def test_stack_profiles_validate():
    result = subprocess.run([sys.executable, "scripts/validate_stack_profiles.py", "--strict", "--all", "profiles", "--json"], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode == 0, result.stdout


def test_profile_missing_security_required_fails(tmp_path):
    profile = tmp_path / "bad-stack.yaml"
    profile.write_text("""stack_id: bad-stack
display_name: Bad Stack
status: supported-alpha
chain_types: [l2]
execution: {evm: true, clients: []}
settlement: {supported: [ethereum], notes: []}
data_availability: {supported: [ethereum], notes: []}
proof_models: {supported: [optimistic], notes: []}
required_roles: [sequencer]
optional_roles: []
security_required: []
forbidden_defaults: []
source_refs: [docs/upstream-sources.md]
notes: [test]
""")
    result = subprocess.run([sys.executable, "scripts/validate_stack_profiles.py", "--strict", "--path", str(profile)], cwd=ROOT, text=True, stdout=subprocess.PIPE)
    assert result.returncode != 0
