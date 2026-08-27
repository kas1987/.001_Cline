# ClinePass Usage Estimation

> **Snapshot Date:** August 25, 2026  
> **Model in Use:** `cline-pass/mimo-v2.5` (cheapest in bundle)  
> **Subscription:** $9.99/month ($4.99 first month)

---

## Current Usage (from Dashboard)

| Window | Used | Remaining | Resets In |
|--------|------|-----------|-----------|
| **5-Hour Limit** | 1% | 99% | 4 hours |
| **Weekly Limit** | 6% | 94% | 4 days 23 hours |
| **Monthly Limit** | 3% | 97% | 27 days 23 hours |

**Observation:** This is a very fresh subscription. Usage is minimal — you've barely scratched the quota.

---

## How ClinePass Quota Works

ClinePass uses **reference pricing** to measure your usage against the quota. The three rolling windows (5-hour, weekly, monthly) each have an **undisclosed token allowance**. Cline states the allowance is **2–5× the standard API rate** for each model, but the exact numbers are not published.

**Key insight:** The percentages shown on the dashboard represent how much of your **total available quota** you've consumed — not dollars spent. The same interaction costs different amounts of quota depending on which model you use.

---

## Estimating Your Capacity

### Reference Pricing (what Cline uses to measure quota)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Relative Cost |
|-------|----------------------|------------------------|---------------|
| **MiMo-V2.5** | $0.14 | $0.28 | **1×** (baseline) |
| DeepSeek V4 Flash | $0.22–0.44 | $0.66–1.32 | 1.6–3.1× |
| Qwen3.7 Plus | $0.40 | $1.60 | 2.9–5.7× |
| MiniMax M3 | $0.30 | $1.20 | 2.1–4.3× |
| Kimi K2.7 Code | $0.95 | $4.00 | 6.8–14.3× |
| Qwen3.8 Max | $2.00 | $6.00 | 14.3–21.4× |
| Qwen3.7 Max | $2.50 | $7.50 | 17.9–26.8× |
| Kimi K3 | $3.00 | $15.00 | 21.4–53.6× |

### What This Means

Using **MiMo-V2.5** (your current model) gives you **maximum quota efficiency** — every interaction costs the least amount of quota. Switching to a more expensive model like Kimi K3 would consume **20–50× more quota per interaction**.

---

## Practical Estimates (MiMo-V2.5)

### Per-Interaction Cost (Standard API Rates)

A typical agentic interaction involves:
- **Input:** ~8,000–15,000 tokens (system prompt + context + user message + tool results)
- **Output:** ~1,000–3,000 tokens (assistant response + tool calls)

| Scenario | Input Tokens | Output Tokens | Standard API Cost |
|----------|-------------|---------------|-------------------|
| Quick question | 5,000 | 500 | $0.00084 |
| Code edit | 10,000 | 2,000 | $0.00196 |
| Multi-file refactor | 25,000 | 5,000 | $0.00490 |
| Full agent session (10 turns) | 100,000 | 20,000 | $0.01960 |

### Monthly Capacity Estimates

Based on the 2–5× multiplier and typical usage patterns:

| Usage Level | Interactions/Month | Hours/Day | Best For |
|-------------|-------------------|-----------|----------|
| **Light** | 3,000–5,000 | 1–2 hrs | Occasional code edits, questions |
| **Moderate** | 8,000–15,000 | 3–5 hrs | Daily development, feature work |
| **Heavy** | 20,000–30,000 | 6–8 hrs | Full-time AI-assisted development |
| **Intensive** | 40,000–50,000+ | 8+ hrs | Power user, multiple sessions |

> **Note:** These are estimates based on the 2–5× claim and reference pricing. Actual capacity depends on Cline's internal quota formula, which is not published.

---

## Your Current Trajectory

### What You've Used So Far

| Metric | Value |
|--------|-------|
| Monthly usage | 3% |
| Days into month | ~3 days (27 days remaining) |
| Estimated daily burn rate | ~1% per day |
| Projected monthly usage | ~30% by month end |

### What's Left

| Window | Available | Estimated Capacity |
|--------|-----------|-------------------|
| **5-Hour** | 99% remaining | ~100 more interactions in next 4 hours |
| **Weekly** | 94% remaining | ~1,500+ more interactions this week |
| **Monthly** | 97% remaining | ~30,000+ more interactions this month |

---

## Model-Specific Estimates

If you stick with **MiMo-V2.5** (cheapest):

| Timeframe | Estimated Interactions | What You Could Do |
|-----------|----------------------|-------------------|
| **Per day** | ~1,000 | Full day of coding assistance |
| **Per week** | ~5,000 | Multiple feature implementations |
| **Per month** | ~20,000–30,000 | Entire project development |

If you switch to **Qwen3.7 Max** (most expensive):

| Timeframe | Estimated Interactions | What You Could Do |
|-----------|----------------------|-------------------|
| **Per day** | ~50–100 | Heavy reasoning tasks |
| **Per week** | ~300–500 | Complex architecture work |
| **Per month** | ~1,000–2,000 | Selective high-complexity tasks |

---

## Recommendations

### Maximize Usage

1. **Stick with MiMo-V2.5** for routine work — it's 20–50× cheaper per interaction than Kimi K3
2. **Use model pairing** (Plan → Act): expensive model for planning, cheap model for execution
3. **Batch related tasks** in one session to amortize system prompt costs
4. **Monitor the dashboard** weekly to understand your actual burn rate

### Budget Your Quota

| Task Type | Recommended Model | Quota Cost |
|-----------|-------------------|------------|
| Quick questions | MiMo-V2.5 | Minimal |
| Code edits | MiMo-V2.5 or DeepSeek V4 Flash | Low |
| Feature implementation | Kimi K2.7 Code or Qwen3.7 Max | Medium |
| Architecture / planning | GLM-5.2 or DeepSeek V4 Pro | High |
| Complex debugging | Qwen3.8 Max | High |

### Track Your Usage

Check the dashboard weekly:
- **5-Hour limit** → resets fast, use it freely
- **Weekly limit** → watch for heavy sessions
- **Monthly limit** → this is your real budget constraint

---

## Sources

- [ClinePass Docs](https://docs.cline.bot/getting-started/clinepass)
- [CLINEPASS_PRICING.md](./CLINEPASS_PRICING.md)
- [Kingy AI Review](https://kingy.ai/news/clinepass-guide/)
- [Volanea Pricing Deep-Dive](https://www.volanea.com/blog/clinepass-pricing)
- [Emergent.sh Cline Pricing](https://emergent.sh/learn/cline-pricing)
