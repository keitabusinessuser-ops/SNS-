"""Summarise reel performance from content/analytics/reels-log.csv against the T2 test thresholds.

Usage: python3 tools/analyze_reels.py [path/to/reels-log.csv]
Rows with an empty "views" column are skipped (not posted yet or no data).
"""
import csv
import sys

PASS_AVG_VIEWS = 1000   # T2 pass line: average views per reel
PASS_SAVE_SEND = 0.02   # T2 pass line: (saves + shares) / views
STOP_AVG_VIEWS = 300    # T2 stop line after 10 reels


def num(row, key):
    value = (row.get(key) or "").replace(",", "").strip()
    return float(value) if value else 0.0


def main(path):
    with open(path, newline="") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("views") or "").strip()]
    if not rows:
        print("No reels with data yet.")
        return
    print(f"{'id':<5}{'topic':<16}{'views':>8}{'save+send%':>12}{'follow%':>10}")
    for r in rows:
        views = num(r, "views") or 1
        engaged = (num(r, "saves") + num(r, "shares")) / views
        follow = num(r, "follows") / views
        print(f"{r['id']:<5}{r['topic']:<16}{num(r, 'views'):>8.0f}{engaged:>11.1%}{follow:>10.2%}")
    avg_views = sum(num(r, "views") for r in rows) / len(rows)
    total_views = sum(num(r, "views") for r in rows) or 1
    avg_engaged = sum(num(r, "saves") + num(r, "shares") for r in rows) / total_views
    best = max(rows, key=lambda r: (num(r, "saves") + num(r, "shares")) / (num(r, "views") or 1))
    print(f"\nReels with data: {len(rows)}")
    print(f"Average views: {avg_views:.0f} (pass line {PASS_AVG_VIEWS})")
    print(f"Save+send rate: {avg_engaged:.1%} (pass line {PASS_SAVE_SEND:.0%})")
    print(f"Best topic by save+send: {best['topic']} ({best['id']})")
    if avg_views >= PASS_AVG_VIEWS or avg_engaged >= PASS_SAVE_SEND:
        print("Verdict: PASS - keep going and make more of the best topic.")
    elif len(rows) >= 10 and avg_views < STOP_AVG_VIEWS:
        print("Verdict: STOP line hit - switch format or move to pattern C test.")
    else:
        print("Verdict: CONTINUE - not enough signal yet.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "content/analytics/reels-log.csv")
