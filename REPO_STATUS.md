# Repo Status — .001_Cline

Last updated: 2026-08-27

## Purpose

Workspace repo for Cline setup, best practices, and ClinePass Plan/Act model guidance.

## Current State

| Component | Status |
|---|---|
| Governance files (README, CONTRIBUTING, SECURITY, LICENSE, CODEOWNERS) | ✅ In place |
| CI validation (`validate` workflow, ubuntu + windows matrix) | ✅ In place |
| PR + issue templates (triage labels) | ✅ In place |
| Cline rules (`.clinerules/01-workflow.md`) | ✅ In place |
| Branch protection on `main` | ✅ Configured via `gh api` |
| Model pairing guide | ✅ In README |
| ClinePass per-token pricing reference | ✅ `CLINEPASS_PRICING.md` |
| ClinePass auth check script | ✅ `scripts/Check-ClineAuth.ps1` |
| Usage tracking report | ✅ Updated 2026-08-27 |

## Scripts

| Script | Purpose | Run |
|---|---|---|
| `scripts/Track-ClineUsage.ps1` | Generate usage report from CLI sessions | `.\scripts\Track-ClineUsage.ps1` |
| `scripts/Check-ClineAuth.ps1` | Verify ClinePass login + token health | `.\scripts\Check-ClineAuth.ps1` |
| `scripts/validate_repo.py` | CI quality gate (required files, secrets, markdown) | `python scripts/validate_repo.py` |

## Known Gaps / Next Work

- [ ] Add per-repo Cline rule packs as they evolve
- [ ] Move `_Per_Cline_Chat` notes into structured `docs/` once they stabilize
- [ ] Consider model pairing upgrade (currently on cheapest tier)
