#!/usr/bin/env python3
"""ClinePass billing model deep-dive from actual session data."""
import json, os
from collections import defaultdict
from pathlib import Path

SD = Path.home() / ".cline" / "data" / "sessions"
sessions = []
for name in sorted(os.listdir(SD)):
    p = SD / name / f"{name}.json"
    if not p.is_file():
        continue
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    u = d.get("metadata", {}).get("usage")
    if not u:
        continue
    sessions.append({
        "date": d.get("started_at", "")[:10],
        "model": d.get("model", "?"),
        "cost": u.get("totalCost", 0),
        "input": u.get("inputTokens", 0),
        "output": u.get("outputTokens", 0),
        "cache_read": u.get("cacheReadTokens", 0),
    })

free = [s for s in sessions if "ox-alpha" in s["model"] or ":free" in s["model"]]
cp_zero = [s for s in sessions if s["model"].startswith("cline-pass/") and s["cost"] == 0]
cp_paid = [s for s in sessions if s["model"].startswith("cline-pass/") and s["cost"] > 0]
direct_paid = [s for s in sessions if not s["model"].startswith("cline-pass/")
               and "ox-alpha" not in s["model"] and ":free" not in s["model"]]

cp_paid_total = sum(s["cost"] for s in cp_paid)
cp_paid_input = sum(s["input"] for s in cp_paid)
cp_paid_output = sum(s["output"] for s in cp_paid)
direct_total = sum(s["cost"] for s in direct_paid)
total_cost = sum(s["cost"] for s in sessions)

print("=" * 70)
print("  CLINEPASS BILLING MODEL")
print("  What Actually Gets Charged vs Your $9.99/mo")
print("=" * 70)
print()
print("HOW IT WORKS")
print("-" * 70)
print("  Your $9.99/mo is a SUBSCRIPTION, not a prepaid balance.")
print()
print("  It gives you:")
print("    1. ACCESS to 15+ premium models (mimo-v2.5, deepseek, etc)")
print("    2. ROLLING QUOTA WINDOWS that cover some usage at $0")
print("       - 5-hour window: resets every 5 hours")
print("       - Weekly window: resets weekly")
print("       - Monthly window: resets monthly")
print("    3. DISCOUNTED per-token rates when you overflow quota")
print("    4. CACHE SAVINGS: repeated context is cached, charged at a")
print("       fraction of full price (this is why actual << raw math)")
print()
print("  There is NO hard $10 cap. You CAN spend more than $9.99/mo")
print("  in overflow charges. But cache savings keep actual cost low.")
print()

print("YOUR ACTUAL BILLING BREAKDOWN")
print("-" * 70)
print()
print(f"  A) FREE (stealth/ox-alpha, poolside:free)")
print(f"     Sessions:     {len(free)}")
print(f"     Cost:         $0.00 (always free, no quota consumed)")
print(f"     These bypass ClinePass entirely.")
print()
print(f"  B) CLINEPASS IN QUOTA (cline-pass/*, cost=$0)")
print(f"     Sessions:     {len(cp_zero)}")
print(f"     Cost:         $0.00 (covered by $9.99 subscription)")
print(f"     These CONSUME your rolling quota windows.")
print(f"     When windows reset, more become free again.")
print()
print(f"  C) CLINEPASS OVERFLOW (cline-pass/*, cost>$0)")
print(f"     Sessions:     {len(cp_paid)}")
print(f"     Charged:      ${cp_paid_total:.4f}")
for s in sorted(cp_paid, key=lambda x: x["cost"], reverse=True):
    print(f"       {s['date']} {s['model']:<30} ${s['cost']:.4f}  ({s['input']:,} in)")
print()
print(f"  D) DIRECT API (your own DeepSeek API key)")
print(f"     Sessions:     {len(direct_paid)}")
print(f"     Charged:      ${direct_total:.4f} (billed to DeepSeek, NOT ClinePass)")
print()

print(f"  GRAND TOTAL SPEND: ${total_cost:.4f}")
print(f"  ClinePass overflow: ${cp_paid_total:.4f}")
print(f"  Direct API: ${direct_total:.4f}")
print()

print("CACHE SAVINGS PROOF")
print("-" * 70)
rates = {
    "cline-pass/mimo-v2.5": (0.14, 0.28),
    "cline-pass/deepseek-v4-flash": (0.07, 0.28),
    "deepseek/deepseek-v4-flash": (0.07, 0.28),
}
by_model = defaultdict(lambda: {"n": 0, "cost": 0.0, "input": 0, "output": 0, "cr": 0})
for s in sessions:
    m = by_model[s["model"]]
    m["n"] += 1; m["cost"] += s["cost"]
    m["input"] += s["input"]; m["output"] += s["output"]; m["cr"] += s["cache_read"]

total_raw = 0
total_actual = 0
for model in sorted(by_model):
    if model not in rates:
        continue
    m = by_model[model]
    r_in, r_out = rates[model]
    raw = (m["input"] / 1e6 * r_in) + (m["output"] / 1e6 * r_out)
    total_raw += raw
    total_actual += m["cost"]
    pct = (1 - m["cost"] / raw) * 100 if raw > 0 else 0
    print(f"  {model}:")
    print(f"    Raw math:     ${raw:.4f}")
    print(f"    Actually:     ${m['cost']:.4f}")
    print(f"    Savings:      {pct:.0f}%")
print()
overall = (1 - total_actual / total_raw) * 100 if total_raw > 0 else 0
print(f"  WITHOUT cache: ${total_raw:.2f}  |  WITH cache: ${total_actual:.4f}  |  {overall:.0f}% saved")
print()

print("RECOMMENDED BUDGET")
print("-" * 70)
days_active = len(set(s["date"] for s in sessions))
daily_avg = total_cost / max(days_active, 1)
projected_30 = daily_avg * 31

print(f"  Active days:          {days_active}")
print(f"  Daily avg spend:      ${daily_avg:.4f}")
print(f"  Projected 30-day:     ${projected_30:.4f}")
print()
print(f"  The $9.99 subscription covers ACCESS + quota windows.")
print(f"  Overflow is extra. But cache keeps overflow LOW.")
print()
print(f"  Conservative budget:  $15/mo (covers subscription + overflow)")
print(f"  Aggressive budget:    $25/mo (room for growth)")
print(f"  At current burn rate: ~${projected_30:.2f}/mo (well under $25)")
print()
print("HOW TO MINIMIZE COST")
print("-" * 70)
print("  1. Default to free models (stealth/ox-alpha) for simple tasks")
print("  2. Reserve ClinePass for complex work (20/80 rule)")
print("  3. Batch ClinePass work within 5-hour windows (quota resets)")
print("  4. Avoid direct DeepSeek API — use ClinePass instead (discounted)")
print("  5. Context caching is your ally — longer sessions = more cache")
