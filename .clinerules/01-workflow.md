# Cline Workflow Rules — apply to every task in this repo

## Planning
- Use Plan mode for anything touching more than 3 files, new architecture, or unclear requirements.
- In Plan mode: read-only exploration. Present the plan as a numbered checklist and wait for approval
  before switching to Act.

## Execution (Act mode)
- Make small, focused edits. One logical change per commit.
- Run builds/tests after changes when a test command is discoverable (package.json scripts, etc.).
- Never force-push, never rewrite history on shared branches.
- Never commit secrets, tokens, API keys, or credentials. If found, stop and report.

## Git
- Commit messages: imperative mood, concise summary line (e.g. "Add retry logic to API client").
- Checkpoint/rollback is the safety net — do not disable checkpoints.

## Safety
- Destructive commands (delete, move-overwrite, in-place edits via sed) always require approval.
- Prefer additive changes over destructive rewrites.
- If a task requires actions outside this workspace, ask first.
