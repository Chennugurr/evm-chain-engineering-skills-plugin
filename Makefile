.PHONY: test validate scripts-help scan-secrets validate-all behavior-evals hooks-validate upstream-check release-check golden-demos-check scripts-help-check validate-profiles validate-artifacts validate-configs acceptance hook-fixtures clean-install-test release-evidence validate-v02 validate-v02-full

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
