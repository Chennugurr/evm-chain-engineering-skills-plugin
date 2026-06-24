# Transcript Capture Policy

Live transcripts must be redacted before commit.

Never include:

- real private material
- mnemonic phrases
- cloud credentials
- API credentials
- signed transactions
- deployable production commands
- approval marker files

Record:

- platform and prompt ID
- plugin version and git commit
- installation method
- observed skills and subagents
- hook observations
- generated artifact bundle path
- validation commands and results
- policy events, redactions, failures, and notes

Do not claim a live run, hook event, or subagent execution happened unless the transcript metadata contains evidence.
