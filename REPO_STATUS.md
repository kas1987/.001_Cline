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
| Usage tracking (persistent CSV log) | ✅ `scripts/Track-ClineUsage.py` |
| Budget tracker + free tier optimizer | ✅ `scripts/BudgetTracker.py` |

## Scripts

| Script | Purpose | Run |
|---|---|---|
| `scripts/Track-ClineUsage.py` | Append usage snapshot to persistent CSV log | `python scripts/Track-ClineUsage.py` |
| `scripts/Track-ClineUsage.py --trend` | View last 10 snapshots | `python scripts/Track-ClineUsage.py --trend` |
| `scripts/BudgetTracker.py` | Full budget dashboard + burn rate forecast | `python scripts/BudgetTracker.py` |
| `scripts/BudgetTracker.py --daily` | Daily breakdown only | `python scripts/BudgetTracker.py --daily` |
| `scripts/BudgetTracker.py --configure 20` | Set monthly budget | `python scripts/BudgetTracker.py --configure <amt>` |
| `scripts/Check-ClineAuth.ps1` | Verify ClinePass login + token health | `powershell scripts/Check-ClineAuth.ps1` |
| `scripts/validate_repo.py` | CI quality gate | `python scripts/validate_repo.py` |

## Budget Snapshot (2026-08-27)

| Metric | Value |
|---|---|
| Monthly budget | $9.99 |
| MTD spent | $1.34 (13.4%) |
| Daily avg burn | $0.27/day |
| Projected month-end | $1.54 (under budget by $8.45) |
| Free tier utilization | 62% (13/21 sessions) |
| ClinePass sessions in quota | 7 (within window, $0) |
| ClinePass overflow | 6 (real cost incurred) |

## Free Tier Strategy

**Available free models:**
- `stealth/ox-alpha` — free, reasoning capable
- `poolside/laguna-s-2.1:free` — free, fast

**Recommendation:** Use free models for 80% of tasks (exploration, simple edits, debugging). Reserve ClinePass for 20% (complex refactors, multi-file architecture).

## Known Gaps / Next Work

- [ ] Add per-repo Cline rule packs as they evolve
- [ ] Move `_Per_Cline_Chat` notes into structured `docs/` once they stabilize
- [ ] Consider model pairing upgrade (currently on cheapest tier)
- [ ] Automate daily usage snapshot (Task Scheduler)
- [ ] Consider switching default model to free tier
