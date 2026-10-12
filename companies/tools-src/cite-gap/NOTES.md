# NOTES（cite-gap 0.1.0 実装メモ、2026-10-12）

実行環境: Python 3.13、外部通信なし、pip install なし。PyPI 未公開。wheel のビルドは未実施（ビルドに通信が要るため）。

## python3 -m unittest
```
.................................
----------------------------------------------------------------------
Ran 33 tests in 0.609s

OK
```

## python3 -m compileall -q src tests
```
exit=0
```

## CLI 実行記録（`PYTHONPATH=src python3 -m cite_gap ...`）
サンプルは `samples/`（全て架空）。
```
## 1. README の例
samples/readme-example.md:1  出典なし  「国内の副業人口は2割に達した。」  理由: 割合(2割)
-- 数字・断定を含む文 3 件のうち、出典なし 1 件（出典の有無のみを見ています。真偽は判定していません）
exit=1

## 2. サンプル（誤検出しやすい文を含む）
samples/sample.md:8  出典なし  「国内の副業人口は2割に達した。」  理由: 割合(2割)
samples/sample.md:27  出典なし  「成約率は50%だった」  理由: 割合(50%)
-- 数字・断定を含む文 6 件のうち、出典なし 2 件（出典の有無のみを見ています。真偽は判定していません）
exit=1

## 3. --strict
samples/sample.md:8  出典なし  「国内の副業人口は2割に達した。」  理由: 割合(2割)
samples/sample.md:12  出典なし  「この方法なら必ず稼げる。」  理由: 断定(必ず)
samples/sample.md:14  出典なし  「月に約1,200円かかると言われている。」  理由: 金額(1,200円)、伝聞(と言われ)
samples/sample.md:27  出典なし  「成約率は50%だった」  理由: 割合(50%)
-- 数字・断定を含む文 6 件のうち、出典なし 4 件（出典の有無のみを見ています。真偽は判定していません）
exit=1

## 4. --json（readme-example）
{
  "version": "0.1.0",
  "strict": false,
  "summary": {
    "files": 1,
    "claim_sentences": 3,
    "gaps": 1,
    "errors": []
  },
  "findings": [
    {
      "file": "samples/readme-example.md",
      "line": 1,
      "sentence": "国内の副業人口は2割に達した。",
      "label": "出典なし",
      "reasons": [
        {
          "kind": "割合",
          "text": "2割"
        }
      ]
    }
  ]
}
exit=1

## 5. ギャップなし
-- 数字・断定を含む文 1 件のうち、出典なし 0 件（出典の有無のみを見ています。真偽は判定していません）
exit=0

## 6. 存在しないファイル
nope.md: 読めません (FileNotFoundError)
-- 数字・断定を含む文 0 件のうち、出典なし 0 件（出典の有無のみを見ています。真偽は判定していません）
exit=2
```

## 未解決・要確認
- 実世界の文章での誤検出率は未計測。サンプルは作者が作った少数の例のみ
- 見出しは点検しない（「売上3倍の方法」のような見出しは見逃す）
- 字下げコードブロック、複数行にまたがる行内コードは未対応
- 「参考」「出典」の語だけでOKにする。出典が数字を支えているかは見ない
- Python 3.9〜3.12 での動作は未確認。pyproject の `license = "MIT"` 形式は setuptools>=77 が必要（ビルド未確認）
- `project.urls` は公開用リポジトリ決定後に追加
- ペンネームでの権利表示（LICENSE）の可否は専門家確認が必要（DESIGN.md③）
- compliance 審査は未実施
