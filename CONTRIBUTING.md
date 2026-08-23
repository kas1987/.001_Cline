# Contributing to .001_Cline

## Operating Standard

Every change should be versioned, validated, and documented. A complete contribution answers:

1. What changed?
2. Why does it matter?
3. How was it validated?
4. Does it keep the repo clean (no orphan files, no root clutter)?

## Local Validation

```bash
python scripts/validate_repo.py
```

This is the same gate CI runs on every PR and push to `main`.

## Pull Request Rules

Before opening a PR:

- Run `python scripts/validate_repo.py` and make it pass.
- Update docs when structure or rules change.
- Use the PR template and tick every quality gate that applies.
- One logical change per PR. Small PRs merge faster and stay reviewable.
- Branch from `main`, name branches by topic (e.g. `feat/clinepass-guide`, `fix/ignore-rules`).

## Workflow Rules (this is a Cline workspace)

- Cline tasks in this repo follow `.clinerules/01-workflow.md`.
- Never commit secrets, tokens, API keys, or credentials — CI scans for common patterns.
- Keep working notes in `_Per_Cline_Chat/`, not scattered at the root.

## Governance Rule

No orphan magic. If it matters, it becomes code, docs, a rule, a workflow, or a tracked issue.
