"""点検の本体。標準ライブラリのみ。ネットワークは使わない。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

__version__ = "0.1.0"

# ---------------------------------------------------------------- 定数

NUM = r"(?:\d[\d,]*(?:\.\d+)?)"
KNUM = r"[〇一二三四五六七八九十百千]+(?:[万億兆][〇一二三四五六七八九十百千]*)*"

# (種類, ラベル, 正規表現)。number は後段で小さい値などを除外する。
NUMBER_PATTERNS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("割合", re.compile(rf"{NUM}\s*(?:%|パーセント)")),
    ("割合", re.compile(rf"(?:{NUM}|{KNUM})\s*割(?![りるっれ合])")),
    ("割合", re.compile(rf"(?:{NUM}|{KNUM})分の(?:{NUM}|{KNUM})")),
    ("倍率", re.compile(rf"(?:{NUM}|{KNUM})\s*倍|数倍")),
    ("金額", re.compile(rf"{NUM}\s*[万億兆千]?\s*(?:円|ドル|ユーロ)")),
    ("金額", re.compile(rf"[¥$]\s*{NUM}")),
    ("金額", re.compile(r"[〇一二三四五六七八九十百千万億]{2,}円")),
    ("人数・件数", re.compile(
        rf"(?:{NUM}|{KNUM})\s*[万億千百]?\s*(?:人|名|件|社|店舗|軒|台|世帯|位|歳)")),
    ("人数・件数", re.compile(r"数[十百千万億]+[人円件社店台]")),
]
COMMA_NUMBER = re.compile(r"(?<![0-9,.])\d{1,3}(?:,\d{3})+(?![0-9,])")
BARE_NUMBER = re.compile(r"(?<![0-9A-Za-z.,])\d{2,}(?![0-9A-Za-z])")  # --strict のみ

ASSERTION_PATTERNS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("断定", re.compile(
        r"必ず|確実|絶対(?!値|評価|零度|音感|王政|多数)|間違いなく|断言|疑いようが|例外なく"
        r"|誰でも|誰もが|唯一|世界一|日本一|業界初|最強")),
    ("断定", re.compile(r"\b(?:guaranteed?|definitely|undoubtedly|proven)\b", re.I)),
    ("伝聞", re.compile(
        r"と(?:言|い)われ|とされ(?:て|る)|と考えられて|と見られて|と報じられ"
        r"|(?:わか|分か)っている|明らかになって|実証され|証明され|によると|によれば")),
    ("伝聞", re.compile(r"studies show|research shows|experts say|it is said", re.I)),
]

# 出典の印。URL、出典、取得日、参考(語尾付き)、脚注参照
SOURCE_MARK = re.compile(
    r"https?://|www\.|出典|取得日|引用元|参考(?:文献|資料|URL|リンク|情報)|参考[:：]|【参考】|\[参考\]"
    r"|\bSources?\s*[:：]|\bretrieved\b|\baccessed\b|\[\^[^\]]+\]",
    re.I,
)
# 「確かめていない」印
UNVERIFIED_MARK = re.compile(r"未確認|仮説|要確認|未検証|unverified|unconfirmed|hypothesis", re.I)

URL_RE = re.compile(r"https?://[^\s)>\]」』）]+|www\.[^\s)>\]」』）]+")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
IMG_LINK_TARGET_RE = re.compile(r"(?<=\])\([^)\s]*\)")
HTML_TAG_RE = re.compile(r"<[^>\n]+>")

# 数字として数えない並び(日付・時刻・版・電話・条項番号など)。検出用の文字列から消す。
NON_CLAIM_RES = [
    re.compile(r"\d{4}\s*[-/.]\s*\d{1,2}\s*[-/.]\s*\d{1,2}"),
    re.compile(r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日"),
    re.compile(r"\d{4}\s*年\s*\d{1,2}\s*月"),
    re.compile(r"\d{1,2}\s*月\s*\d{1,2}\s*日"),
    re.compile(r"\d{4}\s*年"),
    re.compile(r"\d{1,2}\s*[月日]"),
    re.compile(r"\d{1,2}:\d{2}(?::\d{2})?"),
    re.compile(r"\bv?\d+\.\d+\.\d+\b"),
    re.compile(r"\d{2,4}-\d{2,4}-\d{3,4}"),
    re.compile(r"第\s*\d+\s*[章節条項回話条号]"),
    re.compile(r"\d+\s*(?:章|節|条|項|ページ|頁|行目)"),
    re.compile(r"\b[pP]\.?\s*\d+\b"),
    re.compile(r"\[\d+\]"),
]

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
LIST_RE = re.compile(r"^(\s*)(?:[-*+]|\d{1,3}[.)])\s+(?:\[[ xX]\]\s+)?")
IGNORE_MARK = "cite-gap: ignore"

FW_TRANS = str.maketrans("０１２３４５６７８９％，．", "0123456789%,.")
SENT_END = "。！？!?"
CLOSERS = "」』）)]”\"’'】"
CJK_RE = re.compile(r"[぀-ヿ㐀-鿿＀-￯]")


# ---------------------------------------------------------------- データ型

@dataclass
class Reason:
    kind: str   # 割合 / 倍率 / 金額 / 人数・件数 / 数値 / 断定 / 伝聞
    text: str

    def label(self) -> str:
        return f"{self.kind}({self.text})"


@dataclass
class Finding:
    file: str
    line: int
    sentence: str
    reasons: List[Reason] = field(default_factory=list)


@dataclass
class Report:
    file: str
    findings: List[Finding] = field(default_factory=list)
    sentences_checked: int = 0      # 数字・断定を含んだ文の数
    ok_count: int = 0               # そのうち印があった数


# ---------------------------------------------------------------- 内部処理

def _blank(pattern: "re.Pattern[str]", text: str) -> str:
    """一致部分を同じ長さの空白に置き換える(位置がずれない)。"""
    return pattern.sub(lambda m: " " * len(m.group(0)), text)


def _paragraphs(text: str) -> List[List[Tuple[int, str]]]:
    """(行番号, 本文)の段落リストを返す。コード・見出し・front matter は除く。"""
    lines = text.splitlines()
    paras: List[List[Tuple[int, str]]] = []
    cur: List[Tuple[int, str]] = []

    def flush() -> None:
        nonlocal cur
        if cur:
            paras.append(cur)
            cur = []

    i = 0
    n = len(lines)
    if n and lines[0].strip() == "---":  # front matter
        for j in range(1, n):
            if lines[j].strip() in ("---", "..."):
                i = j + 1
                break
    fence: Optional[Tuple[str, int]] = None
    in_comment = False
    while i < n:
        lineno = i + 1
        raw = lines[i]
        i += 1
        if fence:
            m = FENCE_RE.match(raw)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and raw.strip().strip(fence[0]) == "":
                fence = None
            continue
        m = FENCE_RE.match(raw)
        if m:
            flush()
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        if in_comment:
            if "-->" in raw:
                in_comment = False
            continue
        if "<!--" in raw and "-->" not in raw.split("<!--", 1)[1]:
            in_comment = True
            continue
        if IGNORE_MARK in raw:
            flush()
            continue
        raw = re.sub(r"<!--.*?-->", lambda mm: " " * len(mm.group(0)), raw)
        if not raw.strip():
            flush()
            continue
        if HEADING_RE.match(raw) or re.match(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$", raw):
            flush()
            continue
        body = raw
        while body.lstrip().startswith(">"):  # 引用
            body = body.lstrip()[1:]
        lm = LIST_RE.match(body)
        if lm:
            flush()
            body = body[lm.end():]
        cur.append((lineno, body.strip()))
    flush()
    return paras


def _join(para: List[Tuple[int, str]]) -> Tuple[str, List[int]]:
    """段落を1本の文字列にし、各文字の行番号を返す。"""
    chars: List[str] = []
    linenos: List[int] = []
    for idx, (lineno, body) in enumerate(para):
        if idx > 0 and chars:
            first = body[:1]
            if not (CJK_RE.match(chars[-1]) or (first and CJK_RE.match(first))):
                chars.append(" ")
                linenos.append(lineno)
        chars.extend(body)
        linenos.extend([lineno] * len(body))
    return "".join(chars), linenos


def _split_sentences(split_text: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    start = 0
    n = len(split_text)
    i = 0
    while i < n:
        c = split_text[i]
        end = False
        if c in SENT_END:
            end = True
        elif c == "." and (i + 1 == n or split_text[i + 1].isspace()) \
                and not (i > 0 and split_text[i - 1].isdigit()):
            end = True
        if end:
            j = i + 1
            while j < n and (split_text[j] in SENT_END or split_text[j] in CLOSERS):
                j += 1
            spans.append((start, j))
            start = j
            i = j
        else:
            i += 1
    if start < n:
        spans.append((start, n))
    return spans


def _number_ok(kind: str, matched: str) -> bool:
    """「1人」「2人」のような小さい人数・件数は統計とみなさない。"""
    if kind != "人数・件数":
        return True
    if re.search(r"[万億千百十数]|,", matched):
        return True
    m = re.search(r"\d+(?:\.\d+)?", matched)
    if m:
        return float(m.group(0)) >= 10
    k = re.match(KNUM, matched)  # 漢数字: 「一人」「二人」は除く
    return bool(k) and len(k.group(0)) >= 2


def _detect(detect_text: str, strict: bool) -> List[Reason]:
    reasons: List[Reason] = []
    seen = set()
    taken: List[Tuple[int, int]] = []

    def add(kind: str, m: "re.Match[str]") -> None:
        text = re.sub(r"\s+", "", m.group(0))
        key = (kind, text)
        if key not in seen:
            seen.add(key)
            reasons.append(Reason(kind, text))
        taken.append(m.span())

    def overlapped(span: Tuple[int, int]) -> bool:
        return any(a <= span[0] and span[1] <= b for a, b in taken)

    for kind, pat in NUMBER_PATTERNS:
        for m in pat.finditer(detect_text):
            if _number_ok(kind, m.group(0)):
                add(kind, m)
    for m in COMMA_NUMBER.finditer(detect_text):
        if not overlapped(m.span()):
            add("数値", m)
    if strict:
        for m in BARE_NUMBER.finditer(detect_text):
            if not overlapped(m.span()):
                add("数値", m)
    for kind, pat in ASSERTION_PATTERNS:
        for m in pat.finditer(detect_text):
            add(kind, m)
    return reasons


def _tidy(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def check_text(text: str, filename: str = "<stdin>", strict: bool = False) -> Report:
    """文章を点検する。

    既定: 同じ文、または同じ段落に印があれば OK。
    strict: 同じ文に印がある場合のみ OK。さらに2桁以上の数字も対象にする。
    """
    report = Report(file=filename)
    for para in _paragraphs(text):
        orig, linenos = _join(para)
        # 分割用: URL とコードを同じ長さの別文字に置換(URL 内の ? や . で文を切らない)
        masked = URL_RE.sub(lambda m: "U" * len(m.group(0)), orig)
        masked = INLINE_CODE_RE.sub(lambda m: "C" * len(m.group(0)), masked)
        # 検出用: URL・コード・リンク先・日付等を空白にする
        det = masked.translate(FW_TRANS)
        det = re.sub(r"[UC]{4,}", lambda m: " " * len(m.group(0)), det)  # 置換済みの塊
        det = _blank(IMG_LINK_TARGET_RE, det)
        det = _blank(HTML_TAG_RE, det)
        for pat in NON_CLAIM_RES:
            det = _blank(pat, det)
        para_marked = bool(SOURCE_MARK.search(orig) or UNVERIFIED_MARK.search(orig))
        for s, e in _split_sentences(masked):
            sent_det = det[s:e]
            reasons = _detect(sent_det, strict)
            if not reasons:
                continue
            report.sentences_checked += 1
            sent_orig = orig[s:e]
            sent_marked = bool(SOURCE_MARK.search(sent_orig) or UNVERIFIED_MARK.search(sent_orig))
            ok = sent_marked or (para_marked and not strict)
            if ok:
                report.ok_count += 1
                continue
            lead = len(sent_orig) - len(sent_orig.lstrip())
            line = linenos[min(s + lead, len(linenos) - 1)]
            report.findings.append(
                Finding(file=filename, line=line, sentence=_tidy(sent_orig), reasons=reasons)
            )
    return report
