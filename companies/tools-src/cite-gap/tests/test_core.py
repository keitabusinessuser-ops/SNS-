import unittest

from cite_gap import check_text


def gaps(text, strict=False):
    return check_text(text, "t.md", strict=strict).findings


class DetectTests(unittest.TestCase):
    def test_ratio_without_source(self):
        f = gaps("国内の副業人口は2割に達した。")
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].line, 1)
        self.assertEqual(f[0].reasons[0].label(), "割合(2割)")

    def test_various_numbers(self):
        for s in ["売上は3倍になった。", "月に約1,200円かかる。", "成約率は50%だった。",
                  "利用者は1,500人いる。", "全体の3分の1が該当する。", "価格は二十万円だ。",
                  "売上が3000万円になった。", "売上は12,000になった。", "ＶＩＰは５０％引き。"]:
            with self.subTest(s=s):
                self.assertEqual(len(gaps(s)), 1)

    def test_assertions(self):
        for s in ["この方法なら必ず稼げる。", "絶対に成功する。", "副業は儲かると言われている。",
                  "専門家によると効果がある。"]:
            with self.subTest(s=s):
                self.assertEqual(len(gaps(s)), 1)

    def test_english_assertion(self):
        self.assertEqual(len(gaps("This is guaranteed to work.")), 1)


class OkTests(unittest.TestCase):
    def test_source_in_same_sentence(self):
        self.assertEqual(gaps("調査では売上が3倍になった（出典: https://example.com/x 取得日2026-10-01）。"), [])

    def test_unverified_mark(self):
        self.assertEqual(gaps("売上は3倍になった（未確認）。"), [])
        self.assertEqual(gaps("これは仮説だが、2割が離脱する。"), [])

    def test_source_in_same_paragraph(self):
        self.assertEqual(gaps("利用者は50%増えた。\n別の文。\n出典: https://example.com/a"), [])

    def test_paragraph_mark_does_not_cross_blank_line(self):
        f = gaps("利用者は50%増えた。\n\n出典: https://example.com/a")
        self.assertEqual(len(f), 1)

    def test_each_list_item_is_own_scope(self):
        f = gaps("- 成約率は50%だった\n- 成約率は50%だった（仮説）")
        self.assertEqual([x.line for x in f], [1])

    def test_strict_needs_same_sentence(self):
        text = "利用者は50%増えた。出典: https://example.com/a"
        self.assertEqual(gaps(text), [])
        self.assertEqual(len(gaps("利用者は50%増えた。\n出典: https://example.com/a", strict=True)), 1)

    def test_strict_flags_bare_numbers(self):
        self.assertEqual(gaps("売上が300になった。"), [])
        self.assertEqual(len(gaps("売上が300になった。", strict=True)), 1)

    def test_ignore_comment(self):
        self.assertEqual(gaps("売上は3倍だった。 <!-- cite-gap: ignore -->"), [])


class FalsePositiveTests(unittest.TestCase):
    """誤検出しやすい文。人が先に見るべきテスト。"""

    def test_dates_times_versions_phone(self):
        s = "2026年10月1日の10:30に v1.2.3 を出した。電話は090-0000-0000。2026-10-01 取得。"
        self.assertEqual(gaps(s), [])

    def test_headings_and_ordinals(self):
        self.assertEqual(gaps("# 第3章 副業の話 2割の壁\n\n## 1. 手順\n\n第2章で書いた。3ページ目を見る。"), [])

    def test_number_inside_url(self):
        self.assertEqual(gaps("詳細は https://example.com/a/2割/3倍/50% を見る。"), [])

    def test_code_block_and_inline_code(self):
        self.assertEqual(gaps("```\n絶対に3倍 50%\n```\n\n`50%` はコード。\n"), [])
        self.assertEqual(gaps("~~~~\n必ず2割\n```\n必ず2割\n~~~~\n"), [])

    def test_front_matter(self):
        self.assertEqual(gaps("---\ntitle: 50%\n---\n\n本文だけ。"), [])

    def test_small_counts(self):
        self.assertEqual(gaps("1人の人間とAIで進める。二人で話した。2人でも可。"), [])

    def test_absolute_value(self):
        self.assertEqual(gaps("絶対値は0以上になる。"), [])

    def test_url_with_question_mark_does_not_split(self):
        self.assertEqual(gaps("50%は多い（https://example.com/a?b=1&c=2）。"), [])

    def test_html_comment_block(self):
        self.assertEqual(gaps("<!--\n必ず3倍\n-->\n本文。"), [])

    def test_markdown_link_target(self):
        self.assertEqual(gaps("[詳細](https://example.com/50%25)を見る。"), [])


class LineNumberTests(unittest.TestCase):
    def test_line_of_sentence_start(self):
        f = gaps("前置き。\n\n本文です。\n売上は3倍になった。")
        self.assertEqual(f[0].line, 4)

    def test_multiline_sentence_uses_first_line(self):
        f = gaps("売上は\n3倍になった。")
        self.assertEqual(f[0].line, 1)

    def test_stats_counts(self):
        r = check_text("売上は3倍だった（仮説）。\n\n利用者は2割いる。")
        self.assertEqual((r.sentences_checked, r.ok_count, len(r.findings)), (2, 1, 1))


if __name__ == "__main__":
    unittest.main()
