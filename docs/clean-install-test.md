# Clean Install Test

The clean install test proves that committed repository files are sufficient to run validation in an offline local clone. It does not prove live Codex/Claude behavior, real deployment readiness, or production infrastructure correctness.

Run:

```bash
python3 scripts/clean_install_test.py
```

Expected output is `status: pass`. Claude plugin validation is skipped unless the CLI is installed and not skipped. Troubleshoot failures by checking whether the working tree is clean, scripts assume local paths, or generated reports depend on untracked files.
