# Usage Review

Maintain an internal review loop after dogfooding. Do not collect secrets or store prompts that contain secrets. Redact chain credentials, sensitive addresses, internal RPC URLs, cloud identifiers, and organization names when needed.

## Categories

Skill trigger quality: false positives, false negatives, direct invocation frequency, and prompts that require multiple skills.

Output quality: missing ADRs, missing assumptions, missing server roles, missing security caveats, stale-doc warnings, and scripts/templates that fail validation.

Safety: blocked secret writes, blocked mainnet-like actions, warnings about exposed admin/debug RPC, warnings about unpinned images, and unsafe user requests that were redirected safely.

Docs: missing examples, confusing install steps, stale upstream source records, and stack-specific claims needing citations or source updates.

| Date | Platform | Prompt id | Expected skill(s) | Observed skill(s) | Result | Issue | Fix PR/commit |
|---|---|---|---|---|---|---|---|
