# Skill Design Standard

Skills must be focused, activation-ready, and safe.

- Keep frontmatter to `name` and `description` for portable Agent Skills compatibility.
- Put specific trigger terms and exclusions in the description because agents see metadata before the body.
- Keep body instructions concise and imperative.
- Link only directly relevant reference files from each skill.
- Route production, mainnet, bridge, admin, validator, sequencer, prover, relayer, and custom precompile requests through `chain-security-reviewer`.
- Do not place commands that deploy, sign, move funds, generate keys, or mutate live infrastructure inside skill bodies.
