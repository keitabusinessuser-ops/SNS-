#!/usr/bin/env python3
"""experiments.json の期限を読み、今日の判定対象を出す。判定は人(CEO)が行う補助。標準ライブラリのみ。"""
import json, sys, datetime, pathlib, glob
root = pathlib.Path(__file__).resolve().parent.parent
today = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
data = json.loads((root / "companies/experiments.json").read_text(encoding="utf-8"))
for e in data["experiments"]:
    print(f'## {e["id"]} {e["name"]}（起点 {e["start"]}）')
    for c in e["checks"]:
        left = (datetime.date.fromisoformat(c["due"]) - today).days
        mark = "【期限到達・判定する】" if left <= 0 else f"あと{left}日"
        print(f'- {c["due"]} {mark}: 失敗条件={c["fail_if"]} → {c["action"]}')
latest = sorted(glob.glob(str(root / "companies/metrics/github-*.json")))
print("\n最新の計測:", latest[-1].split("/")[-1] if latest else "なし")
