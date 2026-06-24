# Plugin Architecture

The repository separates distribution, skill activation, deep references, scripts, templates, tests, and evals.

- Distribution: Codex metadata lives in `.agents/plugins/marketplace.json` and `.codex-plugin/plugin.json`; Claude metadata lives in `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`.
- Skills: each skill has one narrow job and a concise `SKILL.md` with portable `name` and `description` frontmatter.
- References: stack details live in `references/` files so agents load only what the task requires.
- Scripts: Python CLIs are safe by default, deterministic, importable, and testable.
- Templates: infrastructure files are rendered from placeholders and never embed real secrets.
