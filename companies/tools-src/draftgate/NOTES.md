# NOTES（draftgate 0.1.0 実装メモ、2026-10-13）

環境: Node v22.22.0、外部通信なし、npm publish 未実施。

## node --test
```
# tests 25
# suites 0
# pass 25
# fail 0
```

## npm pack --dry-run（抜粋）
```
npm notice
npm notice package: draftgate@0.1.0
npm notice Tarball Contents
npm notice 1.1kB LICENSE
npm notice 5.3kB README.md
npm notice 104B bin/draftgate.js
npm notice 659B package.json
npm notice 4.4kB src/cli.js
npm notice 6.2kB src/core.js
npm notice 105B src/index.js
npm notice Tarball Details
npm notice name: draftgate
```
含まれるのは LICENSE README.md bin src package.json の7ファイルのみ。bin src README LICENSE package.json を grep し、メール・本名らしき文字列・ローカルパスが無いことを確認（作者は hitori-to-ai のみ）。

## CLI 実行記録（samples/ は全て架空）
```
### node bin/draftgate.js samples/sample.md
samples/sample.md:2  未解決マーカー  「【要確認】」
samples/sample.md:2  穴埋め  「○○」
samples/sample.md:3  AI定型の前置き  「以下に記事を示します。」
samples/sample.md:5  ダミーURL  「https://example.com」
samples/sample.md:6  TODO系  「TODO」
samples/sample.md:7  穴埋め  「ここに事例を入れる」
samples/sample.md:11  重複行  「この行は重複して出てきます。」（初出 10行）
samples/sample.md:17  未確認の注記  「未確認」
samples/sample.md:19  閉じていないコードブロック  「```」（19行目で開いたコードブロックが閉じていません）
-- 1 ファイル、検出 8 件（ほかに情報のみ 1 件）。内訳: 未解決マーカー 1、穴埋め 2、AI定型の前置き 1、ダミーURL 1、TODO系 1、重複行 1、未確認の注記 1、閉じていないコードブロック 1（誤検出があります。最終判断は人が行ってください）
```

## 実際の文章にかけた結果（修正後の再実行。1行90字で切って記載）
```
### ../../site/drafts/e-a-01-approval-gates.md
../../site/drafts/e-a-01-approval-gates.md:27  未解決マーカー  「【運営者確認：経緯の書き方】」
../../site/drafts/e-a-01-approval-gates.md:76  未解決マーカー  「【運営者確認】」
../../site/drafts/e-a-01-approval-gates.md:84  未解決マーカー  「【運営者確認】」
../../site/drafts/e-a-01-approval-gates.md:85  未解決マーカー  「【運営者確認】」
../../site/drafts/e-a-01-approval-gates.md:89  未解決マーカー  「【運営者確認】」
-- 1 ファイル、検出 5 件。内訳: 未解決マーカー 5（誤検出があります。最終判断は人が行ってください）
exit=1
### ../../publish-queue/note/2026-10-10-ai-sugiru.md
../../publish-queue/note/2026-10-10-ai-sugiru.md:79  未解決マーカー  「【公開しない注記】」
../../publish-queue/note/2026-10-10-ai-sugiru.md:84  未確認の注記  「未確認」
-- 1 ファイル、検出 1 件（ほかに情報のみ 1 件）。内訳: 未解決マーカー 1、未確認の注記 1（誤検出があります。最終判断は人が行ってください）
exit=1
### ../../publish-queue/note/2026-10-13-ai-eigyo-reisetsu.md
../../publish-queue/note/2026-10-13-ai-eigyo-reisetsu.md:42  未解決マーカー  「【担当者確認：AIの営業案の具体（
../../publish-queue/note/2026-10-13-ai-eigyo-reisetsu.md:55  未解決マーカー  「【担当者確認：止めると決めた瞬間の
../../publish-queue/note/2026-10-13-ai-eigyo-reisetsu.md:103  未解決マーカー  「【公開しない注記】」
../../publish-queue/note/2026-10-13-ai-eigyo-reisetsu.md:108  未解決マーカー  「【担当者確認】」
../../publish-queue/note/2026-10-13-ai-eigyo-reisetsu.md:112  未確認の注記  「未確認」
-- 1 ファイル、検出 4 件（ほかに情報のみ 1 件）。内訳: 未解決マーカー 4、未確認の注記 1（誤検出があります。最終判断は人が行ってください）
exit=1
```
評価:
- site/drafts/e-a-01-approval-gates.md: 5件すべて【運営者確認】系（grep で一致を確認）。妥当
- note/2026-10-10: 初回は【公開しない注記】の見出しを見逃した。ルールに「公開しない」を追加して拾うようにした。「未確認」1件は情報のみ（終了コード0扱い）
- note/2026-10-13: 初回は40字超の【担当者確認：…】（55行）を見逃した。上限を120字に広げて修正。これはテストにも追加
- 誤検出は上の実文では見当たらなかった（サンプル数3、少ない）。公開用の記事に添える「【公開しない注記】」の節は意図どおり拾うが、そこだけ分けて扱いたい場合は設定が要る（未対応）
未解決: 4スペース字下げのコードブロック未対応、重複行は完全一致のみ、npm上の名前の空きは担当確認済みとの連絡を信頼（私は未確認）、Windows未検証。
