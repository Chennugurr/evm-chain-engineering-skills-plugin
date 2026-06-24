# Release Process

## Validation

Run:

```bash
python3 -m pytest
make validate
python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict --markdown-report docs/behavior-eval-report.md
python3 scripts/validate_hooks.py --plugin-root plugins/evm-chain-engineering-pro --strict
python3 scripts/check_upstream_freshness.py --sources docs/upstream-sources.md --markdown-report docs/upstream-freshness-report.md --allow-offline
python3 scripts/release_check.py --strict --markdown-report docs/release-readiness-report.md
```

## Dogfood

Use `docs/dogfood-plan.md` in Codex and Claude Code. Record results in `docs/usage-review.md` and update evals for false positives or false negatives.

## Upstream Freshness

Update `docs/upstream-sources.md` structured records with last checked dates, volatility, dependent skills, and notes. Run the freshness checker offline by default; use online checks only as an explicit release review step.

## Internal Tag

Create an internal tag only after validation is green:

```bash
git tag -a v0.1.0-internal -m "Internal v0.1.0 dogfood-ready release"
```

If the tag exists, use `v0.1.0-internal.1`. Do not push, publish, or share externally without explicit human instruction.
