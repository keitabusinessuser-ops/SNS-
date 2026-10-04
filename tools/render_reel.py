"""Render a faceless text/diagram reel (1080x1920 MP4) from a JSON spec.

Usage: python3 tools/render_reel.py content/reels/specs/r1-tax-free.json

Spec format:
{
  "output": "content/reels/output/r1-tax-free.mp4",
  "cover": "content/reels/output/r1-tax-free-cover.png",
  "footer": "Source: ... | Last verified 2026-10-04",
  "slides": [
    {"seconds": 3, "blocks": [{"text": "...", "size": 96, "color": "white", "bold": true}]}
  ]
}
A block may set "box": "red" | "yellow" | "panel" to draw a filled rounded box behind its text.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
MARGIN = 90
FONT_DIR = "/usr/share/fonts/truetype/liberation"
COLORS = {
    "bg": (14, 27, 48),
    "white": (255, 255, 255),
    "muted": (170, 184, 204),
    "red": (214, 48, 49),
    "yellow": (255, 205, 60),
    "panel": (30, 48, 78),
    "dark": (14, 27, 48),
}
HANDLE = "@first72japan"
FPS = 30
FADE = 0.3


def font(size, bold):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words, line = paragraph.split(" "), ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        lines.append(line)
    return lines


def render_slide(slide, footer, path):
    img = Image.new("RGB", (W, H), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    # Measure all blocks first so the stack can be centred vertically.
    laid_out = []
    for block in slide["blocks"]:
        fnt = font(block.get("size", 72), block.get("bold", False))
        pad = 40 if block.get("box") else 0
        lines = wrap(draw, block["text"], fnt, W - 2 * MARGIN - 2 * pad)
        line_h = int(block.get("size", 72) * 1.25)
        laid_out.append((block, fnt, lines, line_h, pad, len(lines) * line_h + 2 * pad))
    gap = 56
    total = sum(item[5] for item in laid_out) + gap * (len(laid_out) - 1)
    y = max(280, (H - 560 - total) // 2 + 140)
    for block, fnt, lines, line_h, pad, height in laid_out:
        if block.get("box"):
            draw.rounded_rectangle(
                [MARGIN, y, W - MARGIN, y + height], radius=36, fill=COLORS[block["box"]]
            )
        default_color = "dark" if block.get("box") == "yellow" else "white"
        color = COLORS[block.get("color", default_color)]
        ty = y + pad
        for line in lines:
            tw = draw.textlength(line, font=fnt)
            draw.text(((W - tw) / 2, ty), line, font=fnt, fill=color)
            ty += line_h
        y += height + gap
    small = font(34, False)
    draw.text((MARGIN, 170), HANDLE, font=font(40, True), fill=COLORS["yellow"])
    for i, line in enumerate(wrap(draw, footer, small, W - 2 * MARGIN)):
        draw.text((MARGIN, H - 520 + i * 44), line, font=small, fill=COLORS["muted"])
    img.save(path)


def main(spec_path):
    with open(spec_path) as f:
        spec = json.load(f)
    os.makedirs(os.path.dirname(spec["output"]), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        clips = []
        for i, slide in enumerate(spec["slides"]):
            png = os.path.join(tmp, f"s{i}.png")
            render_slide(slide, spec["footer"], png)
            if i == 0 and spec.get("cover"):
                Image.open(png).save(spec["cover"])
            clip = os.path.join(tmp, f"s{i}.mp4")
            sec = slide["seconds"]
            vf = f"fade=t=in:st=0:d={FADE},fade=t=out:st={sec - FADE}:d={FADE},format=yuv420p"
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", png,
                 "-t", str(sec), "-r", str(FPS), "-vf", vf, "-c:v", "libx264", clip],
                check=True,
            )
            clips.append(clip)
        listing = os.path.join(tmp, "list.txt")
        with open(listing, "w") as f:
            f.writelines(f"file '{c}'\n" for c in clips)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listing,
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", spec["output"]],
            check=True,
        )
    print(spec["output"])


if __name__ == "__main__":
    main(sys.argv[1])
