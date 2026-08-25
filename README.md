# .001_Cline

[![Validate](https://github.com/kas1987/.001_Cline/actions/workflows/validate.yml/badge.svg)](https://github.com/kas1987/.001_Cline/actions/workflows/validate.yml)

A workspace repo for [Cline](https://cline.bot) setup, best practices, and autonomous-execution
configuration across VS Code and VS Code Insiders.

## Repo Structure

```
.001_Cline/
├── .clinerules/            # Rules Cline auto-loads for every task in this repo
├── .github/
│   ├── ISSUE_TEMPLATE/     # Triage-labeled bug & feature forms
│   ├── workflows/          # CI: validate.yml (required check on main)
│   └── pull_request_template.md
├── scripts/
│   └── validate_repo.py    # Local/CI quality gate
├── _Per_Cline_Chat/        # Working notes and chat artifacts
├── CONTRIBUTING.md         # Operating standard + PR rules
├── REPO_STATUS.md          # Living status board
└── SECURITY.md             # Vulnerability reporting policy
```

## Contents

| Path | Purpose |
|---|---|
| `.clinerules/` | Project rules Cline follows in every task (workflow, safety, conventions) |
| `_Per_Cline_Chat/` | Working notes and chat artifacts |

## Recommended ClinePass model pairings (Plan → Act)

> **Per-token reference pricing** and full model catalog: see
> [CLINEPASS_PRICING.md](./CLINEPASS_PRICING.md).

| Scenario | Plan Mode | Act Mode |
|---|---|---|
| Default daily driver | `cline-pass/qwen3.8-max` | `cline-pass/kimi-k2.7-code` |
| Large refactors / big repos | `cline-pass/deepseek-v4-pro` (1M ctx) | `cline-pass/mimo-v2.5-pro` |
| Speed & cost conscious | `cline-pass/qwen3.7-max` | `cline-pass/deepseek-v4-flash` |
| Unattended / YOLO sessions | n/a | `cline-pass/mimo-v2.5-pro` |
| UI work from screenshots | `cline-pass/qwen3.8-max` | `cline-pass/qwen3.7-plus` |

> **Rule of thumb:** Plan mode rewards raw reasoning + large context (read-only, mistakes are cheap).
> Act mode rewards instruction-following, reliability, and speed (it executes tools — mistakes cost real files).
> Avoid `cline-pass/kimi-k3` in unattended sessions (documented reliability instability).

## Autonomous execution safety tiers

1. **Baseline:** Auto-approve *Read project files* only. Checkpoints always on.
2. **Autonomous:** + *Edit project files* and *Execute safe commands* — git-tracked repos only.
3. **YOLO:** Everything auto-approved — throwaway experiments, dev containers, or sandboxes only.

## Setup checklist (per VS Code install)

- [x] Cline extension installed (Stable + Insiders, same version)
- [x] ClinePass provider signed in
- [x] Separate models enabled for Plan / Act
- [ ] Auto-approve tier configured to taste
- [ ] `.clinerules/` reviewed per repo
