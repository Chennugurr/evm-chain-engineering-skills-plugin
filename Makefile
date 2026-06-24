.PHONY: test validate scripts-help scan-secrets

test:
	PYTHONPATH=src python3 -m pytest

validate: test scripts-help scan-secrets
	python3 /home/iljanemesis/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/evm-chain-engineering-pro

scripts-help:
	PYTHONPATH=src python3 -m evm_chain_engineering_plugin.devcheck --scripts-help

scan-secrets:
	PYTHONPATH=src python3 plugins/evm-chain-engineering-pro/scripts/scan_secrets.py --path . --strict --json
