# Live Transcript (claude)

- Platform: claude
- Prompt ID: 03-polygon-cdk-enterprise-validium
- Capture date: 2026-06-25
- Raw stream retained outside repo: /tmp/v03-claude-03.raw.jsonl
- Committed stream: CLAUDE_STREAM_REDACTED.jsonl

## Assistant Response

# 03 Polygon CDK Enterprise Validium — Planning-Only Package

## Selected skills

- `blockchain-architect`
- `polygon-cdk-engineer`
- `chain-infra-ops`
- `bridge-interop-engineer`
- `chain-security-reviewer`

---

## Planning answer

### ADR-001 — Stack and mode selection

**Status:** Proposed (planning only — not approved for production).

**Context.** An enterprise sponsor wants a permissioned, high-throughput EVM chain with predictable fees, strong settlement guarantees on Ethereum, and the ability to keep transaction data off the public L1 for cost and confidentiality reasons. The chain should be able to join a shared interoperability layer over time.

**Decision.** Plan a **Polygon CDK** chain operating in **validium** mode, with **Agglayer** connectivity treated as a forward-looking option rather than a launch requirement. Validity (zk) proofs settle to Ethereum L1 while transaction data is held off-chain by a Data Availability Committee (DAC). **Sovereign mode** is documented as a fallback/alternative posture for teams that want looser coupling to a shared bridge and unified liquidity layer.

**Consequences.**
- Enterprise gets low data-publishing cost and the option of a **private validium** posture for confidential workloads.
- Trust shifts: with **validium**, data availability is guaranteed by the DAC, *not* by Ethereum. This is the dominant risk and is treated as a first-class security concern below.
- Choosing validium over a pure **zkRollup** trades stronger data guarantees (calldata/blobs on L1) for lower cost and confidentiality. The decision is reversible at the config/policy level before genesis but expensive to change after launch.

### Stack decision matrix

| Dimension | zkRollup (CDK) | **Validium (CDK) — selected** | Sovereign mode (CDK) |
|---|---|---|---|
| Settlement | Ethereum L1 (validity proofs) | Ethereum L1 (validity proofs) | Self-settled / chosen settlement |
| Data availability | Ethereum calldata/blobs | **Off-chain DAC** | Operator/committee defined |
| Cost profile | Higher (L1 data) | **Lowest L1 data cost** | Variable |
| Confidentiality | Low (public data) | **High (private validium option)** | Configurable |
| Withdrawal safety if DA fails | Strong | **Weaker — depends on DAC liveness** | Depends |
| Agglayer unified bridge fit | Native | **Native (with DA caveats)** | Looser / optional |
| Best for | Public, value-heavy | **Enterprise, throughput, confidential** | Independent appchains |

### Chain spec (planning placeholders — values to be finalized in review)

- **Mode:** validium (CDK), zk validity proofs to Ethereum L1.
- **Chain ID / network name:** to be reserved; avoid collisions with existing registries before any public exposure.
- **Gas token:** enterprise policy decision — native ETH-equivalent vs. custom token; default to a non-custom token for launch simplicity unless treasury requires otherwise.
- **Block/batch cadence:** tuned to prover throughput and DAC signing latency; placeholder pending load modeling.
- **Roles:** **sequencer** (ordering/execution), **prover** (validity proof generation), aggregator/proposer (proof submission to L1), DAC members (data availability attestations).
- **Access model:** permissioned RPC and permissioned sequencing for the **enterprise** tenant at launch; public read endpoints gated behind review.

### Infrastructure plan (topology, not commands)

- **Sequencer:** single sequencer at launch with a documented promotion path to redundancy/decentralization; isolated network segment, dedicated keys under HSM/KMS policy (no key material handled here).
- **Prover:** capacity-planned compute (GPU/large-memory class) sized to target TPS and proof latency; queue depth and proof-lag alerts are launch-blocking signals. Plan for burst headroom and a backlog drain runbook.
- **DA / DAC:** ≥N independent committee members across distinct operators and failure domains; signed availability attestations; retention, replication, and retrieval SLAs defined. Document the exact DA trust assumption in writing.
- **Bridge operations:** canonical **bridge** between L1 and the CDK chain; monitoring for deposit/withdrawal flow, message relaying, and claim liveness. **Agglayer** participation, if pursued, adds shared-bridge/unified-liquidity considerations and a pessimistic-proof/soundness review before connection — treated as a separate gated workstream.
- **Supporting services:** RPC/archive nodes, explorer, indexer, status page. All exposed surfaces behind TLS, rate limits, and firewalling.
- **IaC posture:** reproducible provisioning (Docker Compose for dev, Kubernetes/Terraform/Ansible for higher environments), with config-as-code and peer-reviewed change control. No secrets in repos or images.

---

## Security review

**Posture: NOT production-ready. Planning artifact only.** No contracts deployed, no keys created, no bridge commands published, no secrets stored.

Key findings and required controls:

1. **Data availability is the primary risk (validium).** With **validium**, withdrawals and proving depend on the DAC actually serving data. A DAC that goes offline or withholds data can freeze user exits even though state is proven. Required: ≥N-of-M independent members, diverse operators/jurisdictions, attestation monitoring, retention/replication SLAs, and a documented DA-failure incident runbook. Consider a fallback to on-chain data (validium→rollup escape) policy.
2. **Sequencer centralization.** A single **sequencer** is a censorship and liveness single point of failure. Require a forced-inclusion / L1 escape-hatch mechanism, sequencer monitoring, and a decentralization roadmap.
3. **Prover integrity and liveness.** The **prover**/aggregator is trusted for liveness; proof bugs are catastrophic. Require audited proving stack versions, proof-lag alerting, deterministic builds, and a verified circuit/contract pin.
4. **Bridge and Agglayer trust.** The canonical **bridge** and any **Agglayer** unified-bridge connection concentrate value and cross-chain message trust. No TVL-bearing or public-testnet bridge work without a dedicated bridge security review (interop engineer + security reviewer jointly).
5. **Admin keys / upgradeability.** Upgrade and admin controls must use multisig + timelock, with documented key custody (HSM/KMS), least privilege, and rotation policy. No keys generated here.
6. **Access control (enterprise).** Permissioned RPC/sequencing and any **private validium** confidentiality controls must be explicitly threat-modeled; "private" is a policy + network control, not a cryptographic guarantee unless stated.

**Mandatory before any non-dev environment:** independent audits (contracts, bridge, DA), external pen test of exposed surfaces, dry-run validation on devnet then public testnet, and human go/no-go sign-off.

### Launch gates (go/no-go)

- **Gate 0 — Devnet:** stack stands up; DAC, prover, sequencer, bridge function in dry-run; runbooks drafted.
- **Gate 1 — Public testnet:** monitoring/alerting live; DA-failure, sequencer-down, prover-backlog, and bridge-halt runbooks exercised; security audit in progress.
- **Gate 2 — Production-network candidate:** audits closed with remediations verified; bridge review complete; key custody and pause/rollback procedures tested; **launch gates** signed off by security + ops + sponsor.
- **Gate 3 — Production-network / Agglayer connect:** separate gated decision; pessimistic-proof/soundness and unified-bridge review required before joining shared liquidity.

---

## Validation notes

- This is a **planning-only** deliverable. No contracts were deployed, no keys created, no secrets stored, no live deployment or bridge commands issued.
- All chain-spec values are placeholders requiring human finalization and review.
- **Required validation path:** internal review → independent audits (protocol, **bridge**, **data availability**) → external pen test → devnet dry-run → public testnet exercise of failure runbooks → documented go/no-go at each of the **launch gates** above.
- Production readiness is **not** claimed and cannot be claimed until all gates above are passed with human sign-off.
- **Agglayer** connection and any **sovereign mode** repositioning are explicitly out of scope for initial launch and are handled as separate, independently gated workstreams.
