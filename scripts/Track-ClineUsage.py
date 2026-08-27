#!/usr/bin/env python3
"""ClinePass Usage Logger — independent of Cline's own logs.

Appends a usage snapshot to a persistent CSV log.
Run daily to build trend data.

Usage:
    python Track-ClineUsage.py           # Log snapshot + show trend
    python Track-ClineUsage.py --trend   # Trend only (no new snapshot)
    python Track-ClineUsage.py --csv     # Dump CSV to stdout
"""
import csv, json, os, sys
from datetime import datetime
from pathlib import Path

SESSIONS_DIR = Path(os.path.expanduser("~")) / ".cline" / "data" / "sessions"
_REPO_ROOT = Path(os.path.abspath(__file__)).parent.parent
LOG_DIR = _REPO_ROOT / "_Per_Cline_Chat"
LOG_FILE = LOG_DIR / "usage_log.csv"
CSV_FIELDS = [
    "timestamp", "total_sessions", "total_input_tokens",
    "total_output_tokens", "total_cache_tokens", "total_reference_cost",
    "clinepass_sessions", "clinepass_cost", "model_breakdown",
]


def scan_sessions():
    """Parse all Cline session JSON files and aggregate usage."""
    report = {
        "total_sessions": 0, "total_input": 0, "total_output": 0,
        "total_cache": 0, "total_cost": 0,
        "clinepass_sessions": 0, "clinepass_cost": 0,
        "by_model": {},
    }
    if not SESSIONS_DIR.exists():
        return report
    for name in sorted(os.listdir(SESSIONS_DIR)):
        json_path = SESSIONS_DIR / name / f"{name}.json"
        if not json_path.is_file():
            continue
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        usage = data.get("metadata", {}).get("usage")
        if not usage:
            continue
        model = data.get("model", "unknown")
        inp = usage.get("inputTokens", 0)
        out = usage.get("outputTokens", 0)
        cache = usage.get("cacheReadTokens", 0)
        cost = usage.get("totalCost", 0)
        report["total_sessions"] += 1
        report["total_input"] += inp
        report["total_output"] += out
        report["total_cache"] += cache
        report["total_cost"] += cost
        if model not in report["by_model"]:
            report["by_model"][model] = {"sessions": 0, "input": 0, "output": 0, "cache": 0, "cost": 0.0}
        m = report["by_model"][model]
        m["sessions"] += 1; m["input"] += inp; m["output"] += out
        m["cache"] += cache; m["cost"] += cost
        if model.startswith("cline-pass/"):
            report["clinepass_sessions"] += 1
            report["clinepass_cost"] += cost
    return report


def log_snapshot(report):
    """Append one row to the CSV log."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    write_header = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            writer.writeheader()
        breakdown = {}
        for model, v in report["by_model"].items():
            breakdown[model] = {k: (round(v[k], 6) if k == "cost" else v[k]) for k in v}
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_sessions": report["total_sessions"],
            "total_input_tokens": report["total_input"],
            "total_output_tokens": report["total_output"],
            "total_cache_tokens": report["total_cache"],
            "total_reference_cost": round(report["total_cost"], 6),
            "clinepass_sessions": report["clinepass_sessions"],
            "clinepass_cost": round(report["clinepass_cost"], 6),
            "model_breakdown": json.dumps(breakdown),
        })


def show_trend(n=10):
    """Display the last N snapshots from the log."""
    if not LOG_FILE.exists():
        print("No usage log found."); return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    recent = rows[-n:]
    print(f"=== Trend (last {len(recent)} snapshots) ===")
    for r in recent:
        print(f"  {r['timestamp']} | {r['total_sessions']} sessions | ${r['total_reference_cost']} | ClinePass: {r['clinepass_sessions']}")


def print_csv():
    if LOG_FILE.exists():
        print(LOG_FILE.read_text(encoding="utf-8"), end="")


def print_report(report):
    def fmt_m(v): return f"{v / 1e6:.1f}M"
    def fmt_d(v): return f"${v:.4f}"
    print("=== Usage Snapshot Logged ===")
    print(f"Timestamp:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sessions:   {report['total_sessions']}")
    print(f"Input:      {fmt_m(report['total_input'])} tokens")
    print(f"Output:     {fmt_m(report['total_output'])} tokens")
    print(f"Cache:      {fmt_m(report['total_cache'])} tokens")
    print(f"Cost:       {fmt_d(report['total_cost'])}")
    print(f"ClinePass:  {report['clinepass_sessions']} sessions / {fmt_d(report['clinepass_cost'])}")
    print()
    print("=== By Model ===")
    for model in sorted(report["by_model"]):
        v = report["by_model"][model]
        print(f"  {model}: {v['sessions']} sessions | In:{fmt_m(v['input'])} Out:{fmt_m(v['output'])} | {fmt_d(v['cost'])}")
    print()
    print(f"Log file:   {LOG_FILE}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--csv" in args:
        print_csv()
    elif "--trend" in args:
        show_trend()
    else:
        report = scan_sessions()
        log_snapshot(report)
        print_report(report)
        show_trend()
