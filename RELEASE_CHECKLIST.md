# Release Checklist

## Repository state
- [ ] Working tree is clean or all intended changes are staged.
- [ ] No split repos, submodules, or duplicated plugin roots were introduced.
- [ ] No accidental local-only absolute paths are present except documented examples.
- [ ] Version is bumped consistently in all manifests.
- [ ] CHANGELOG.md has an entry for the release.
- [ ] FINAL_REPORT.md is updated or superseded by a release report.

## Validation
- [ ] `python3 -m pytest` passes.
- [ ] `make validate` passes.
- [ ] Codex plugin validator passes.
- [ ] Claude plugin validate --strict passes.
- [ ] All skills pass quick validation.
- [ ] All scripts support `--help`.
- [ ] Hook validation passes.
- [ ] Behavior eval schema validation passes.
- [ ] Golden demo validation passes.
- [ ] Strict secret scan has zero unapproved findings.

## Safety
- [ ] Mainnet-like deployment commands are approval-gated.
- [ ] No skill recommends committing secrets.
- [ ] No script prints unredacted secrets.
- [ ] No demo contains a key-shaped fake secret.
- [ ] Admin/debug RPC exposure warnings are present.
- [ ] Unpinned Docker image warnings are present.
- [ ] Destructive commands require dry-run or explicit approval.
- [ ] Bridge, DA, sequencer, prover, and governance trust assumptions are documented.

## Behavior dogfooding
- [ ] Architecture router prompt passes.
- [ ] OP Stack public testnet prompt passes.
- [ ] Arbitrum Orbit L3 prompt passes.
- [ ] Polygon CDK enterprise prompt passes.
- [ ] ZKsync ZK Stack prompt passes.
- [ ] EVM L1 validator network prompt passes.
- [ ] Bridge risk prompt passes.
- [ ] Unsafe secret prompt is refused safely.
- [ ] False-positive and false-negative skill triggers are recorded.

## Documentation
- [ ] README quickstart works from a clean clone.
- [ ] docs/dogfood-plan.md exists.
- [ ] docs/behavior-eval-report.md exists or can be generated.
- [ ] docs/upstream-sources.md is current enough for internal release.
- [ ] docs/usage-review.md explains telemetry/feedback review without collecting secrets.
- [ ] Golden demos are readable and complete.
- [ ] Known limitations are documented.

## Release
- [ ] Release branch is named clearly.
- [ ] Internal tag is created.
- [ ] Install test completed in Codex.
- [ ] Install test completed in Claude Code.
- [ ] No publish/share action is taken without explicit user instruction.
