# Assumptions: smoke-op-stack-public-testnet

## User-Omitted Assumptions

- Selected stack profile: `op-stack`.
- Selected chain type: `l2`.
- Server sizing and exact commands are `VERIFY_CURRENT_DOCS`.

## Must Verify Before Deployment

- Current upstream docs, supported releases, chain ID collision status, bridge contracts, and signer custody.

## Safety-Critical Assumptions

- Sensitive signer material stays outside git and is provided only by approved runtime custody.
- Admin/debug RPC remains private.
- This bundle is dry-run planning evidence only.
