# Behavior Evals

Behavior evals are deterministic routing and safety specifications for manual or saved-response testing. They are not LLM judges and do not prove semantic correctness by themselves.

Run them with:

```bash
python3 scripts/run_behavior_evals.py --evals evals/skill-trigger-matrix.yaml --strict
```

To score saved responses, place `<eval-id>.md` or `<eval-id>.txt` files in a response directory and pass `--responses`. The runner checks required fragments, forbidden fragments, skill-name validity, coverage, and key-shaped unsafe test data.

Add new cases by including `id`, `prompt`, `expected_skills`, optional `forbidden_skills`, `must_include`, `must_not_include`, `required_behavior`, `safety_level`, and `review_notes`. Do not add fake private keys, mnemonics, cloud keys, or credential-shaped examples. If evals reveal false positives or false negatives, update skill descriptions and the trigger collision analysis in `docs/skill-inventory.md`.
