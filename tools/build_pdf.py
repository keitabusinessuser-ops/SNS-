"""Turn a product Markdown draft into a styled PDF with headless Chromium.

Usage: python3 tools/build_pdf.py <input.md> <output.pdf> [--title "..."]
Drops HTML comments (internal notes) and fact IDs like [F01] before rendering.
"""
import argparse
import os
import re
import subprocess
import tempfile

import markdown

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
CSS = """
@page { size: A5; margin: 14mm 12mm 16mm; }
body { font-family: "Liberation Sans", "DejaVu Sans", sans-serif; color: #0e1b30; font-size: 10.5pt; line-height: 1.5; }
h1 { font-size: 24pt; margin: 0 0 4pt; line-height: 1.15; }
h1 + h3 { margin-top: 0; color: #5d6b82; font-weight: normal; }
h2 { font-size: 14pt; margin: 18pt 0 6pt; padding: 4pt 8pt; background: #0e1b30; color: #ffcd3c; border-radius: 4pt; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 10pt 0 4pt; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0 10pt; font-size: 9pt; page-break-inside: avoid; }
th { background: #ffcd3c; text-align: left; padding: 4pt; }
td { border-bottom: 1px solid #d9dee8; padding: 4pt; vertical-align: top; }
hr { border: 0; border-top: 1px solid #d9dee8; margin: 12pt 0; }
ul, ol { padding-left: 16pt; }
li { margin: 2pt 0; }
em { color: #5d6b82; }
strong { color: #0e1b30; }
.cover-note { color: #5d6b82; font-size: 9pt; }
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--title", default="First72 Japan")
    a = ap.parse_args()
    with open(a.src) as f:
        text = f.read()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\s?\[F\d+\](\[F\d+\])*", "", text)
    text = text.replace("- [ ]", "- ☐")
    body = markdown.markdown(text, extensions=["tables"])
    page = f"<!doctype html><html><head><meta charset='utf-8'><title>{a.title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(page)
        html_path = f.name
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={os.path.abspath(a.out)}", "file://" + html_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(html_path)
    print(a.out)


if __name__ == "__main__":
    main()
