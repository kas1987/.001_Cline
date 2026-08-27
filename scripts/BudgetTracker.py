#!/usr/bin/env python3
"""ClinePass Budget Tracker -- forecast usage against monthly/weekly/daily budgets.

Usage:
    python BudgetTracker.py                  # Full dashboard
    python BudgetTracker.py --daily          # Daily breakdown table
    python BudgetTracker.py --configure 20   # Set monthly budget to $20
"""
import json, os, sys, csv
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

SESSIONS_DIR = Path.home() / ".cline" / "data" / "sessions"
_REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = _REPO_ROOT / "_Per_Cline_Chat" / "budget_config.json"
USAGE_LOG = _REPO_ROOT / "_Per_Cline_Chat" / "usage_log.csv"

FREE_MODELS = ("stealth/ox-alpha",)
MONTHLY_BUDGET_DEFAULT = 9.99

CONFIG_DEFAULTS = {
    "monthly_budget_usd": MONTHLY_BUDGET_DEFAULT,
    "weekly_budget_usd": None,
    "daily_budget_usd": None,
    "alert_threshold_pct": 80,
}


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        for k, v in CONFIG_DEFAULTS.items():
            cfg.setdefault(k, v)
        return cfg
    return CONFIG_DEFAULTS.copy()


def save_config(cfg):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def scan_sessions():
    sessions = []
    if not SESSIONS_DIR.exists():
        return sessions
    for name in sorted(os.listdir(SESSIONS_DIR)):
        jp = SESSIONS_DIR / name / f"{name}.json"
        if not jp.is_file():
            continue
        try:
            data = json.loads(jp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        usage = data.get("metadata", {}).get("usage")
        if not usage:
            continue
        model = data.get("model", "unknown")
        date = data.get("started_at", "")[:10]
        cost = usage.get("totalCost", 0)
        is_free = model in FREE_MODELS or ":free" in model or cost == 0
        sessions.append({
            "date": date, "model": model, "cost": cost, "is_free": is_free,
            "input_tokens": usage.get("inputTokens", 0),
            "output_tokens": usage.get("outputTokens", 0),
            "cache_tokens": usage.get("cacheReadTokens", 0),
        })
    return sessions


def daily_agg(sessions):
    by_date = defaultdict(lambda: {
        "total": 0.0, "free": 0, "paid": 0, "sessions": 0, "tokens_in": 0, "models": set(),
    })
    for s in sessions:
        d = by_date[s["date"]]
        d["sessions"] += 1
        d["tokens_in"] += s["input_tokens"]
        d["models"].add(s["model"])
        if s["is_free"]:
            d["free"] += 1
        else:
            d["paid"] += 1
        d["total"] += s["cost"]
    return dict(sorted(by_date.items()))


def forecast(sessions, cfg):
    daily = daily_agg(sessions)
    dates = sorted(daily.keys())
    if not dates:
        return None

    first = datetime.strptime(dates[0], "%Y-%m-%d")
    last = datetime.strptime(dates[-1], "%Y-%m-%d")
    total_days = max((last - first).days + 1, 1)
    total_cost = sum(s["cost"] for s in sessions)
    total_free = sum(1 for s in sessions if s["is_free"])
    total_paid = len(sessions) - total_free

    daily_avg = total_cost / total_days
    weekly_avg = daily_avg * 7

    today = datetime.now()
    m_start = today.replace(day=1)
    m_end = (m_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    days_in_month = m_end.day
    days_elapsed = (today - m_start).days + 1
    days_remaining = days_in_month - days_elapsed

    mtd = [s for s in sessions if m_start.strftime("%Y-%m-%d") <= s["date"] <= today.strftime("%Y-%m-%d")]
    mtd_cost = sum(s["cost"] for s in mtd)
    mtd_free = sum(1 for s in mtd if s["is_free"])
    mtd_paid = len(mtd) - mtd_free

    budget = cfg["monthly_budget_usd"]
    wk_budget = cfg["weekly_budget_usd"] or budget / 4.33
    dy_budget = cfg["daily_budget_usd"] or budget / days_in_month

    used_pct = (mtd_cost / budget * 100) if budget > 0 else 0
    projected = (mtd_cost / days_elapsed * days_in_month) if days_elapsed > 0 else 0
    remaining = budget - mtd_cost
    days_left = (remaining / daily_avg) if daily_avg > 0 else float("inf")

    # Count how many cline-pass sessions hit quota vs overflow
    cp_quota = sum(1 for s in sessions if s["model"].startswith("cline-pass/") and s["cost"] == 0)
    cp_overflow = sum(1 for s in sessions if s["model"].startswith("cline-pass/") and s["cost"] > 0)

    return {
        "total_days": total_days, "total_sessions": len(sessions),
        "total_cost": total_cost, "total_free": total_free, "total_paid": total_paid,
        "daily_avg": daily_avg, "weekly_avg": weekly_avg, "free_pct": (total_free / len(sessions) * 100) if sessions else 0,
        "today": today.strftime("%Y-%m-%d"), "days_in_month": days_in_month,
        "days_elapsed": days_elapsed, "days_remaining": days_remaining,
        "mtd_cost": mtd_cost, "mtd_sessions": len(mtd), "mtd_free": mtd_free, "mtd_paid": mtd_paid,
        "budget": budget, "wk_budget": wk_budget, "dy_budget": dy_budget,
        "used_pct": used_pct, "projected": projected, "remaining": remaining,
        "days_left": days_left, "cp_quota": cp_quota, "cp_overflow": cp_overflow,
        "over": used_pct > 100, "near": used_pct > cfg.get("alert_threshold_pct", 80),
    }


def bar(pct, width=30):
    filled = min(int(pct / 100 * width), width)
    return "#" * filled + "-" * (width - filled)


def status_icon(fc):
    if fc["over"]:
        return "[!!!] OVER BUDGET"
    if fc["near"]:
        return "[!] NEAR LIMIT"
    return "[OK] ON TRACK"


def print_dashboard(fc):
    print("=" * 62)
    print(f"  CLINEPASS BUDGET DASHBOARD  --  {fc['today']}")
    print("=" * 62)
    print()
    print(f"  Status: {status_icon(fc)}")
    print()

    print(f"  MONTHLY BUDGET: ${fc['budget']:.2f}")
    print(f"  [{bar(fc['used_pct'])}] {fc['used_pct']:.1f}%")
    print(f"   ${fc['mtd_cost']:.4f} spent  /  ${fc['remaining']:.4f} remaining")
    print(f"   {fc['days_elapsed']}/{fc['days_in_month']} days elapsed, {fc['days_remaining']} remaining")
    print()

    print("  BURN RATE")
    print(f"   Daily avg:      ${fc['daily_avg']:.4f} (over {fc['total_days']} tracked days)")
    print(f"   Weekly avg:     ${fc['weekly_avg']:.4f}")
    print(f"   Daily budget:   ${fc['dy_budget']:.4f}")
    print(f"   Weekly budget:  ${fc['wk_budget']:.4f}")
    print()

    print("  STRAIGHT-LINE FORECAST")
    print(f"   Projected month-end:  ${fc['projected']:.4f}")
    if fc["projected"] <= fc["budget"]:
        print(f"   [OK] Under budget by:   ${fc['budget'] - fc['projected']:.4f}")
    else:
        print(f"   [!!] Over budget by:    ${fc['projected'] - fc['budget']:.4f}")
    if fc["days_left"] < float("inf"):
        print(f"   Days of budget left:  {fc['days_left']:.1f} at current burn rate")
    print()

    print("  FREE vs PAID")
    print(f"   Free sessions:     {fc['total_free']}/{fc['total_sessions']} ({fc['free_pct']:.0f}%)")
    print(f"   Paid sessions:     {fc['total_paid']}")
    print(f"   ClinePass (quota): {fc['cp_quota']} (within quota, $0 cost)")
    print(f"   ClinePass (over):  {fc['cp_overflow']} (overflow, actual cost)")
    print()

    print("  MONTH-TO-DATE")
    print(f"   Sessions: {fc['mtd_sessions']} ({fc['mtd_free']} free, {fc['mtd_paid']} paid)")
    print(f"   Cost:     ${fc['mtd_cost']:.4f}")
    print()

    # Smart recommendations
    print("  RECOMMENDATIONS")
    recs = []
    if fc["free_pct"] < 50:
        recs.append("1. SWITCH TO FREE MODELS -- you're using <50% free tiers")
        recs.append("   -> Set default model to stealth/ox-alpha or poolside/laguna-s-2.1:free")
        recs.append("   -> Reserve ClinePass for complex tasks only")
    if fc["cp_overflow"] > 0:
        recs.append(f"2. {fc['cp_overflow']} sessions exceeded ClinePass quota window")
        recs.append("   -> These incurred real cost - space sessions apart to stay within quota")
    if fc["near"] and not fc["over"]:
        recs.append(f"3. At {fc['used_pct']:.0f}% with {fc['days_remaining']} days left -- slow down or go free-only")
    if fc["over"]:
        recs.append("3. OVER BUDGET -- switch to free models for rest of month")
    if not recs:
        headroom = fc["dy_budget"] - fc["daily_avg"]
        recs.append(f"1. Healthy headroom: ${headroom:.4f}/day under budget")
        recs.append(f"2. Free tier at {fc['free_pct']:.0f}% -- {'good' if fc['free_pct'] > 50 else 'room to improve'}")

    for r in recs:
        print(f"   {r}")
    print()

    # How to switch to free
    print("  HOW TO SWITCH TO FREE MODEL")
    print("   In Cline CLI/VS Code, change model to one of:")
    print("     stealth/ox-alpha              (free, reasoning capable)")
    print("     poolside/laguna-s-2.1:free    (free, fast)")
    print("   Or in Cline settings: model ? select from dropdown")
    print()
    print("   Tip: Use free models for 80% of tasks (exploration, simple edits,")
    print("   debugging). Reserve ClinePass/mimo-v2.5 for 20% (complex refactors,")
    print("   multi-file architecture, performance-critical code).")
    print()


def print_daily(sessions):
    daily = daily_agg(sessions)
    print(f"\n{'Date':<12} {'Sess':>5} {'Free':>5} {'Paid':>5} {'Cost':>10}  Models")
    print("-" * 72)
    for date, d in daily.items():
        models = ", ".join(sorted(d["models"]))
        print(f"{date:<12} {d['sessions']:>5} {d['free']:>5} {d['paid']:>5} ${d['total']:>9.4f}  {models}")
    print(f"\n{'TOTAL':<12} {sum(d['sessions'] for d in daily.values()):>5} "
          f"{sum(d['free'] for d in daily.values()):>5} "
          f"{sum(d['paid'] for d in daily.values()):>5} "
          f"${sum(d['total'] for d in daily.values()):>9.4f}")


def main():
    args = sys.argv[1:]

    if "--configure" in args:
        idx = args.index("--configure")
        if idx + 1 < len(args):
            cfg = load_config()
            cfg["monthly_budget_usd"] = float(args[idx + 1])
            save_config(cfg)
            print(f"Monthly budget set to ${cfg['monthly_budget_usd']:.2f}")
        else:
            print("Usage: python BudgetTracker.py --configure <amount>")
        return

    sessions = scan_sessions()
    cfg = load_config()
    fc = forecast(sessions, cfg)

    if not fc:
        print("No session data found."); return

    if "--daily" in args:
        print_daily(sessions)
    else:
        print_dashboard(fc)
        print("DAILY BREAKDOWN")
        print("-" * 72)
        print_daily(sessions)


if __name__ == "__main__":
    main()
