# ClinePass Model Pricing & Reference

Companion reference to the [model pairing guide in README.md](./README.md#recommended-clinepass-model-pairings-plan--act).
ClinePass is a **flat $9.99/month** subscription (often **$4.99 for the first month**). All included models
run on that single plan — there are no tiers. The per-token rates below are *reference pricing* (what
you would pay at standard API rates); Cline uses them to measure your 2–5× usage quota across three
rolling windows: **5-hour**, **weekly**, and **monthly**.

> **Key take-away:** ClinePass is the only plan Cline offers — $9.99/month after a $4.99 intro month.
> Exact numerical quota caps are **not published**; Cline only discloses the 2–5× multiplier relative
> to standard API rate limits.

## Quick Picks

| Goal | Model | Input | Output | Why |
|---|---|---|---|---|
| **Abs. cheapest per token** | **MiMo-V2.5** | $0.14 | $0.28 | Lowest rates in the bundle; 1 M context |
| **Speed + cost** | DeepSeek V4 Flash | $0.22–0.44 | $0.66–1.32 | Tiny cost per edit-test loop |
| **Best reasoning value** | Qwen3.7 Max | $2.50 | $7.50 | Strong multi-file / difficult work |
| **Best cost × context** | Qwen3.7 Plus | $0.40 | $1.60 | Good value up to 256 K tokens |

---

## Full Model Table

Reference prices per 1 M tokens (USD). Sorted by input cost (cheapest first).

| # | Model | Slug | Input | Output | Context | Notes |
|---|-------|------|-------|--------|---------|-------|
| 1 | **MiMo-V2.5** | `cline-pass/mimo-v2.5` | **$0.14** | **$0.28** | 1 M | Cheapest in bundle |
| 2 | DeepSeek V4 Flash (off-peak) | `cline-pass/deepseek-v4-flash` | $0.22 | $0.66 | 1 M | Peak: $0.44 / $1.32 |
| 3 | DeepSeek V4 Flash (peak) | — | $0.44 | $1.32 | 1 M | |
| 4 | Qwen3.7 Plus (≤256 K) | `cline-pass/qwen3.7-plus` | $0.40 | $1.60 | 1 M | Scales to $1.20 / $4.80 above 256 K |
| 5 | MiniMax M3 | `cline-pass/minimax-m3` | $0.30 | $1.20 | 512 K | |
| 6 | Kimi K2.6 | `cline-pass/kimi-k2.6` | $0.95 | $4.00 | 256 K | |
| 7 | Kimi K2.7 Code | `cline-pass/kimi-k2.7-code` | $0.95 | $4.00 | 256 K | Code-specialised |
| 8 | DeepSeek V4 Pro (off-peak) | `cline-pass/deepseek-v4-pro` | $0.66 | $1.98 | 1 M | Peak: $1.32 / $3.96 |
| 9 | DeepSeek V4 Pro (peak) | — | $1.32 | $3.96 | 1 M | |
| 10 | GLM-5.2 | `cline-pass/glm-5.2` | $1.40 | $4.40 | 1 M | Reasoning-heavy tasks |
| 11 | GLM-5.3 | `cline-pass/glm-5.3` | $1.40 | $4.40 | 1 M | Latest GLM line |
| 12 | MiMo-V2.5-Pro | `cline-pass/mimo-v2.5-pro` | $1.74 | $3.48 | 1 M | Pro variant |
| 13 | Qwen3.8 Max | `cline-pass/qwen3.8-max` | $2.00 | $6.00 | 1 M | |
| 14 | Qwen3.7 Max | `cline-pass/qwen3.7-max` | $2.50 | $7.50 | 1 M | Highest-end model |
| 15 | Kimi K3 | `cline-pass/kimi-k3` | $3.00 | $15.00 | 1 M | **Most expensive**; known reliability concerns |

---

## Usage Limits (Three Rolling Windows)

| Window | Measurement |
|---|---|
| **5-hour rolling** | Usage within any trailing 5-hour period |
| **Weekly** | Calendar-week usage |
| **Monthly** | Calendar-month usage |

> Cline states these quotas are **2–5× the standard API rate** for each model, but the absolute token
> allowances are not published. Check your real-time consumption on the [Cline dashboard](https://app.cline.bot).

## Cautions

- **Opaque caps:** No public numerical limits — test your workloads before production use.
- **Model rotation:** The lineup can change; verify the live model selector in Cline settings.
- **Data path:** Six of the model providers are based in China — review data-handling and residency policies for sensitive work.
- **Kimi K3:** Documented reliability instability; avoid in unattended sessions.

## Sources

- [ClinePass docs — cline.bot/docs](https://docs.cline.bot/getting-started/clinepass)
- [Cline model directory](https://cline.bot/models)
- [LLM Directory — ClinePass models](https://llmdir.com/providers/cline-pass-models)
- [Kingy AI review](https://kingy.ai/news/clinepass-guide/)
- [Awesome Agents coverage](https://awesomeagents.ai/news/clinepass-open-weight-bundle/)
- [Volanea pricing deep-dive](https://www.volanea.com/blog/clinepass-pricing)
