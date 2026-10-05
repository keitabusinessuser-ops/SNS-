"""Build the post board page (apps/post-board/index.html) from ready-to-post/02_reels.

Usage: python3 apps/post-board/build.py
Each reel needs R<n>_<MM-DD>_<topic>_{video.mp4,cover.png,caption.txt} in ready-to-post/02_reels.
The page references the media as reels/<file>; publish them with the Artifact `files` map.
"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REELS = os.path.join(ROOT, "ready-to-post", "02_reels")
OUT = os.path.join(ROOT, "apps", "post-board", "index.html")
TEMPLATE = os.path.join(ROOT, "apps", "post-board", "template.html")
YEAR = 2026
LABELS = {
    "tax-free": "免税制度の変更（11/1〜）",
    "narita": "成田から都内への行き方",
    "haneda": "羽田から都内への行き方",
    "suica": "Suica：アプリかカードか",
    "subway-ticket": "地下鉄パスは得か",
}


def main():
    reels = []
    for video in sorted(glob.glob(os.path.join(REELS, "R*_video.mp4")), key=lambda p: int(re.match(r"R(\d+)", os.path.basename(p)).group(1))):
        base = os.path.basename(video)[: -len("_video.mp4")]
        rid, mmdd, topic = base.split("_", 2)
        with open(os.path.join(REELS, base + "_caption.txt")) as f:
            caption = f.read().strip()
        reels.append({
            "id": rid,
            "date": f"{YEAR}-{mmdd}",
            "topic": LABELS.get(topic, topic),
            "video": f"reels/{base}_video.mp4",
            "cover": f"reels/{base}_cover.png",
            "caption": caption,
        })
    with open(TEMPLATE) as f:
        page = f.read()
    data = json.dumps(reels, ensure_ascii=False).replace("</", "<\\/")
    page = page.replace("__REELS_JSON__", data)
    with open(OUT, "w") as f:
        f.write(page)
    print(OUT, len(reels), "reels")
    for r in reels:
        print(r["video"])


if __name__ == "__main__":
    main()
