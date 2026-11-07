#!/usr/bin/env python3
"""秘書: 移動時間の計算。予定（場所・到着したい時刻・終了時刻）を並べると、
出発時刻・帰宅時刻・予定間の移動を出す。所要時間は companies/secretary/travel.md の表。

使い方:
  python3 -I scripts/travel_plan.py 2026-11-10 "四谷,18:00,19:45" ["有楽町,20:30,22:00" ...]
  各予定は "エリア,到着したい時刻,終了時刻[,駅から徒歩の分]"。終了が不明なら "?" （帰りは出さない）
"""
import re, sys, urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "companies/secretary/travel.md"
SETTINGS = ROOT / "companies/secretary/settings.md"
HOME = "柏"


def load_table():
    """柏からの表と、都内どうしの区間表を読む。"""
    t, pairs, section = {}, {}, ""
    for line in TABLE.read_text().splitlines():
        if line.startswith("## "):
            section = line
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "区間" in section and len(cells) >= 3 and cells[2].isdigit():
            pairs[(cells[0], cells[1])] = pairs[(cells[1], cells[0])] = int(cells[2])
        elif "区間" not in section and len(cells) >= 3 and cells[2].isdigit():
            t[cells[0]] = (cells[1], int(cells[2]))
    t["_pairs"] = pairs
    return t


def setting(name, default):
    m = re.search(rf"{name}[^0-9]*(\d+)\s*分", SETTINGS.read_text())
    return int(m.group(1)) if m else default


def minutes(table, a, b):
    """エリア間の分数。柏を経由した値で近似（直接の値が無いため。上限の目安）。"""
    if a == b:
        return 0
    if (a, b) in table["_pairs"]:
        return table["_pairs"][(a, b)]
    ta, tb = table[a][1], table[b][1]
    if HOME in (a, b):
        return ta + tb
    # 都内どうしは柏経由だと過大になるので、差＋20分を目安にする
    return min(ta + tb, abs(ta - tb) + 20)


def maps_link(dest_station):
    q = urllib.parse.urlencode({"api": 1, "origin": "柏駅", "destination": dest_station + "駅", "travelmode": "transit"})
    return "https://www.google.com/maps/dir/?" + q


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    table = load_table()
    day = sys.argv[1]
    walk = setting("自宅→柏駅", 10)       # 自宅から柏駅まで
    buf = setting("早め到着", 10)          # 到着の余裕
    gap_home = setting("一度帰る条件", 60)  # 予定の間に、往復＋この分数より長く空けば一度帰る
    plans = []
    for arg in sys.argv[2:]:
        f = [x.strip() for x in arg.split(",")]
        area, arrive, end = f[:3]
        foot = int(f[3]) if len(f) > 3 else 0
        if area not in table or area == "_pairs":
            print(f"!! 表に無いエリア: {area}（travel.md に追加するか、近いエリアで指定）")
            sys.exit(2)
        a = datetime.fromisoformat(f"{day}T{arrive}")
        e = None if end == "?" else datetime.fromisoformat(f"{day}T{end}")
        plans.append((area, a, e, foot))
    plans.sort(key=lambda p: p[1])

    out, here, free_at, prev_foot = [], HOME, None, 0
    for i, (area, arrive, end, foot) in enumerate(plans):
        mv = minutes(table, here, area) + foot + prev_foot
        if here == HOME:
            mv += walk
        depart = arrive - timedelta(minutes=mv + buf)
        if free_at and here != HOME:
            # 前の予定から直行するか、一度帰るか
            back = minutes(table, here, HOME) + walk + prev_foot
            go = minutes(table, HOME, area) + walk + foot
            if depart - free_at > timedelta(minutes=back + go + gap_home):
                out.append(("帰宅", free_at, free_at + timedelta(minutes=back), f"{here}→柏（{back}分）"))
                mv = go
                depart = arrive - timedelta(minutes=mv + buf)
                here = HOME
        out.append(("移動", depart, arrive - timedelta(minutes=buf), f"{here}→{area}（{mv}分＋余裕{buf}分）"))
        if end is None:
            here, free_at = area, None
            break
        here, free_at, prev_foot = area, end, foot
    if free_at and here != HOME:
        back = minutes(table, here, HOME) + walk + prev_foot
        out.append(("帰宅", free_at, free_at + timedelta(minutes=back), f"{here}→柏（{back}分）"))

    for kind, s, e, note in out:
        print(f"{kind}\t{s:%H:%M}-{e:%H:%M}\t{note}")
    for area, *_ in plans:
        print(f"確認リンク({area}): {maps_link(table[area][0])}")
    print("注意: 所要時間は推定（未確認）。Googleマップで確かめ、ずれたら travel.md を直す")


if __name__ == "__main__":
    main()
