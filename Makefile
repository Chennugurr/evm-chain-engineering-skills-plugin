.PHONY: test validate scripts-help scan-secrets validate-all behavior-evals hooks-validate upstream-check release-check golden-demos-check scripts-help-check validate-profiles validate-artifacts validate-configs acceptance hook-fixtures clean-install-test release-evidence validate-v02 validate-v02-full lint-dogfood-prompts validate-dogfood-transcripts-bootstrap validate-dogfood-transcripts validate-live-runs-bootstrap validate-live-runs validate-live-hooks-bootstrap validate-live-hooks live-acceptance-bootstrap live-acceptance score-skill-routing-bootstrap score-skill-routing validate-subagent-dogfood-bootstrap validate-subagent-dogfood compare-live-to-fixture-bootstrap compare-live-to-fixture check-known-bad-outputs validate-v03-bootstrap validate-v03

test:
	PYTHONPATH=src python3 -m pytest

validate: test scripts-help scan-secrets
	python3 "$$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/evm-chain-engineering-pro

scripts-help:
	PYTHONPATH=src python3 -m evm_chain_engineering_plugin.devcheck --scripts-help

scan-secrets:
	PYTHONPATH=src python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path . --strict --json

validate-all:
	python3 -m pytest
	$(MAKE) validate
	python3 scripts/validate_hooks.py --plugin-root plugins/evm-chain-engineering-pro --strict
	python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict
	python3 scripts/release_check.py --strict

behavior-evals:
	python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --markdown-report docs/behavior-eval-report.md

hooks-validate:
	python3 scripts/validate_hooks.py --plugin-root plugins/evm-chain-engineering-pro --strict

upstream-check:
	python3 scripts/check_upstream_freshness.py --sources docs/upstream-sources.md --markdown-report docs/upstream-freshness-report.md --allow-offline

release-check:
	python3 scripts/release_check.py --strict --markdown-report docs/release-readiness-report.md

golden-demos-check:
	python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict

scripts-help-check:
	for f in plugins/evm-chain-engineering-pro/scripts/*.py scripts/*.py; do [ -f "$$f" ] && python3 "$$f" --help >/dev/null; done

validate-profiles:
	python3 scripts/validate_stack_profiles.py --strict --all profiles

validate-artifacts:
	python3 scripts/validate_artifact_bundle.py --strict --all fixtures/artifact-bundles

validate-configs:
	python3 scripts/validate_generated_configs.py --strict --all fixtures/artifact-bundles

acceptance:
	python3 scripts/run_acceptance_suite.py --strict

hook-fixtures:
	python3 scripts/test_hook_fixtures.py --strict

clean-install-test:
	python3 scripts/clean_install_test.py

release-evidence:
	python3 scripts/build_release_evidence.py --version v0.2.0-alpha --strict

validate-v02:
	$(MAKE) validate
	$(MAKE) validate-profiles
	$(MAKE) validate-artifacts
	$(MAKE) validate-configs
	$(MAKE) acceptance
	$(MAKE) hook-fixtures
	$(MAKE) release-evidence
	$(MAKE) clean-install-test

validate-v02-full:
	$(MAKE) validate-v02

lint-dogfood-prompts:
	python3 scripts/lint_dogfood_prompts.py --strict

validate-dogfood-transcripts-bootstrap:
	python3 scripts/validate_dogfood_transcripts.py --bootstrap

validate-dogfood-transcripts:
	python3 scripts/validate_dogfood_transcripts.py --strict

validate-live-runs-bootstrap:
	python3 scripts/validate_live_run_package.py --all --bootstrap

validate-live-runs:
	python3 scripts/validate_live_run_package.py --all --strict

validate-live-hooks-bootstrap:
	python3 scripts/validate_live_hook_observations.py --bootstrap

validate-live-hooks:
	python3 scripts/validate_live_hook_observations.py --strict

live-acceptance-bootstrap:
	python3 scripts/run_live_acceptance_suite.py --bootstrap

live-acceptance:
	python3 scripts/run_live_acceptance_suite.py --strict

score-skill-routing-bootstrap:
	python3 scripts/score_skill_routing.py --bootstrap

score-skill-routing:
	python3 scripts/score_skill_routing.py --strict

validate-subagent-dogfood-bootstrap:
	python3 scripts/validate_subagent_dogfood.py --bootstrap

validate-subagent-dogfood:
	python3 scripts/validate_subagent_dogfood.py --strict

compare-live-to-fixture-bootstrap:
	python3 scripts/compare_live_to_fixture.py --bootstrap

compare-live-to-fixture:
	python3 scripts/compare_live_to_fixture.py --strict

check-known-bad-outputs:
	python3 scripts/check_bad_output_patterns.py --path tests/known_bad_outputs --expect-bad
	python3 scripts/check_bad_output_patterns.py --path dogfood/live-runs --strict

validate-v03-bootstrap:
	$(MAKE) validate-v02
	$(MAKE) lint-dogfood-prompts
	$(MAKE) validate-dogfood-transcripts-bootstrap
	$(MAKE) validate-live-runs-bootstrap
	$(MAKE) validate-live-hooks-bootstrap
	$(MAKE) live-acceptance-bootstrap
	$(MAKE) score-skill-routing-bootstrap
	$(MAKE) validate-subagent-dogfood-bootstrap
	$(MAKE) compare-live-to-fixture-bootstrap
	$(MAKE) check-known-bad-outputs
	$(MAKE) clean-install-test
	python3 scripts/build_release_evidence.py --version v0.3.0-beta --bootstrap

validate-v03:
	$(MAKE) validate-v02
	$(MAKE) lint-dogfood-prompts
	$(MAKE) validate-dogfood-transcripts
	$(MAKE) validate-live-runs
	$(MAKE) validate-live-hooks
	$(MAKE) live-acceptance
	$(MAKE) score-skill-routing
	$(MAKE) validate-subagent-dogfood
	$(MAKE) compare-live-to-fixture
	$(MAKE) check-known-bad-outputs
	$(MAKE) clean-install-test
	python3 scripts/build_release_evidence.py --version v0.3.0-beta --strict
