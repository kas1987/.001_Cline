# Cline CLI Usage Report

> **Generated:** August 27, 2026 11:04  
> **Data Source:** `~/.cline/data/sessions/` (Cline CLI local sessions)

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Sessions** | 21 |
| **Total Input Tokens** | 99,590,000 (~99.6M) |
| **Total Output Tokens** | 620,000 (~0.62M) |
| **Total Cache Read** | 90,100,000 (~90.1M) |
| **Total Cache Write** | 0 |
| **Total Cost (Reference)** | $1.3417 |

---

## Usage by Model

| Model | Input | Output | Cache Read | Cost | Sessions |
|-------|-------|--------|------------|------|----------|
| **cline-pass/mimo-v2.5** | 43,800,000 | 250,000 | 40,200,000 | $0.8382 | 12 |
| **cline-pass/deepseek-v4-flash** | 8,350,000 | 60,000 | 7,800,000 | $0.1837 | 1 |
| **deepseek/deepseek-v4-flash** | 40,780,000 | 200,000 | 35,360,000 | $0.3198 | 3 |
| **stealth/ox-alpha** | 4,250,000 | 80,000 | 3,000,000 | $0.0000 | 4 |
| **poolside/laguna-s-2.1:free** | 2,390,000 | 20,000 | 1,880,000 | $0.0000 | 1 |

---

## ClinePass Usage

| Metric | Value |
|--------|-------|
| **Sessions** | 13 (of 21 total) |
| **Total Cost (Reference)** | $1.0219 |
| **Models Used** | `mimo-v2.5`, `deepseek-v4-flash` |
| **Non-ClinePass Models** | `deepseek/deepseek-v4-flash`, `stealth/ox-alpha`, `poolside/laguna-s-2.1:free` |

---

## Growth Since Last Report (Aug 25 → Aug 27)

| Metric | Aug 25 | Aug 27 | Delta |
|--------|--------|--------|-------|
| Sessions | 12 | 21 | +9 |
| Input tokens | 61.3M | 99.6M | +38.3M (+62%) |
| ClinePass sessions | 3 | 13 | +10 |
| ClinePass cost | $0.1487 | $1.0219 | +$0.87 |

---

## Key Observations

1. **ClinePass adoption increasing** — 13 of 21 sessions now use ClinePass models (62%)
2. **Cache hit rate excellent** — ~90% of input tokens are cache reads (90.1M / 99.6M)
3. **Cost efficiency** — ClinePass sessions average ~$0.08 per session
4. **Monthly budget utilization** — $1.02 of ~$4.50 monthly reference capacity used (~23%)
5. **Active auth token expires today** — run `cline auth` if it lapses

---

## Auth Status (Aug 27 11:04)

| Provider | Token Status | Expires |
|----------|-------------|---------|
| `cline` (active) | ⚠️ EXPIRING SOON | 4.8 hours remaining |
| `cline-pass` | ❌ EXPIRED | 40.7 hours ago |

> **Action needed:** Run `cline auth` before the active token expires.

---

*Report generated from local Cline CLI session data.*
