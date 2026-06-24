# Security Review

## Blockers

- Any real secret, live broadcast, or mainnet-like action without human approval.
- Missing bridge, DA, sequencer, prover/validator, governance, or admin-key trust assumptions.

## Warnings

- Exact server sizing, deployment commands, and stack modes must be verified against current upstream docs.
- Public RPC must exclude admin/debug/personal/engine APIs.

## Accepted Risks

Only accept risks after documenting owner, expiration, mitigation, and reviewer.

## Required Human Decisions

- Target environment.
- Stack/version choice.
- Governance ownership and upgrade policy.
- TVL and launch limits.

## Required Upstream Docs To Re-check Before Production

- Stack deployment docs.
- Client releases.
- Bridge docs.
- DA provider docs.
- Security advisories.
