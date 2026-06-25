# Validation Report: Example Orbit L3 AnyTrust

## Validators Run

- artifact bundle validator: expected pass
- generated config validator: expected pass
- strict secret scan: expected pass
- policy guard: expected pass

## Pass/Fail Summary

Pending local execution.

## Skipped Checks and Why

Live Codex/Claude dogfood is deferred to v0.3.

## Warnings

Version-sensitive facts remain `VERIFY_CURRENT_DOCS`.

## Next Required Validations

Run `python3 scripts/validate_artifact_bundle.py --strict --path <bundle>`.
