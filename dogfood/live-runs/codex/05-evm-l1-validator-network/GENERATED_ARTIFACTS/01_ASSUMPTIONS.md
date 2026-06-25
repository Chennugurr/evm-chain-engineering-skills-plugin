# Assumptions: Example EVM L1 PoSA Testnet

## User-Omitted Assumptions

- Selected stack profile: `bnb-style-posa`.
- Selected chain type: `l1`. Validator and consensus design are in scope.
- Server sizing and exact commands are `VERIFY_CURRENT_DOCS`.

## Must Verify Before Deployment

- Current upstream docs, supported releases, chain ID collision status, bridge contracts, and signer custody.

## Safety-Critical Assumptions

- Sensitive signer material stays outside git and is provided only by approved runtime custody.
- Admin/debug RPC remains private.
- Validator and consensus assumptions must be explicit when this is an L1/appchain.
- This bundle is dry-run planning evidence only.
