# Release Process

1. Refresh `docs/upstream-sources.md`.
2. Replace or preserve `VERIFY_CURRENT_DOCS` notes based on verified official docs.
3. Run `python3 -m pytest`.
4. Run Codex plugin validation.
5. Run Claude plugin validation when Claude CLI is installed.
6. Update `CHANGELOG.md` and `FINAL_REPORT.md`.
7. Bump plugin versions in both manifests.
