"""コマンドライン。終了コード: 0=ギャップなし / 1=ギャップあり / 2=使い方・読み込みの誤り。"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from .core import Report, __version__, check_text

MAX_SHOWN = 80

EPILOG = """\
終了コード: 0=ギャップなし 1=ギャップあり 2=使い方・読み込みの誤り
このツールは出典の「有無」だけを見ます。内容の真偽は判定しません。
誤検出・見逃しがあります。最終判断は人が行ってください。法的助言ではありません。
行ごとに除外: 行内に  cite-gap: ignore  と書く(HTMLコメント可)。
"""


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cite-gap",
        description="文章中の数字・割合・倍率・断定に、出典か「未確認」の印があるかを点検します。"
                    "外部通信はしません。",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("files", nargs="+", metavar="FILE",
                   help="Markdown/テキストのファイル。 - で標準入力")
    p.add_argument("--json", action="store_true", help="JSONで出力する")
    p.add_argument("--strict", action="store_true",
                   help="印は同じ文の中だけ有効にする。2桁以上の数字も対象にする")
    p.add_argument("--version", action="version", version=f"cite-gap {__version__}")
    return p


def _short(s: str) -> str:
    return s if len(s) <= MAX_SHOWN else s[: MAX_SHOWN - 1] + "…"


def _read(path: str) -> str:
    if path == "-":
        return sys.stdin.buffer.read().decode("utf-8")
    with open(path, "rb") as f:
        return f.read().decode("utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    reports: List[Report] = []
    errors: List[str] = []
    for path in args.files:
        try:
            text = _read(path)
        except (OSError, UnicodeDecodeError) as e:
            errors.append(f"{path}: 読めません ({type(e).__name__})")
            continue
        name = "<stdin>" if path == "-" else path
        reports.append(check_text(text, filename=name, strict=args.strict))

    findings = [f for r in reports for f in r.findings]
    checked = sum(r.sentences_checked for r in reports)

    if args.json:
        out = {
            "version": __version__,
            "strict": args.strict,
            "summary": {
                "files": len(reports),
                "claim_sentences": checked,
                "gaps": len(findings),
                "errors": errors,
            },
            "findings": [
                {
                    "file": f.file,
                    "line": f.line,
                    "sentence": f.sentence,
                    "label": "出典なし",
                    "reasons": [{"kind": r.kind, "text": r.text} for r in f.reasons],
                }
                for f in findings
            ],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            why = "、".join(r.label() for r in f.reasons)
            print(f"{f.file}:{f.line}  出典なし  「{_short(f.sentence)}」  理由: {why}")
        for e in errors:
            print(e, file=sys.stderr)
        print(f"-- 数字・断定を含む文 {checked} 件のうち、出典なし {len(findings)} 件"
              f"（出典の有無のみを見ています。真偽は判定していません）")

    if errors:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
