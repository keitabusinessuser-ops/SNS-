# 校正・言い換えツール調査（scout、2026-10-11）

目的: 日本語の文章を読みやすく整える。対象は、校正（誤字・表記ゆれ・読みにくさの指摘）、言い換え、文体の整え。
方針: `MISSION.md` v2「外部ツールの利用ルール」と `voice-guide.md` に従う。人間らしさは、Keitaの実体験・具体的な数字・口調で作る。
前提: コンテナは外部サイトに出られない（npm / PyPI / GitHub API のみ到達可）。Web版ツールはKeitaがMacのブラウザでコピペする。公開予定の文章だけ入れる。機密・個人情報は入れない。

## 先に: この調査でできなかったこと
- 調査担当（私）の環境にシェルが無く、`npm install` と textlint の実行は**していない**。バージョン・依存・使い方は npm レジストリとGitHubのREADMEの記載を読んだだけ。「実際に動く」は未検証。CEO側で下の手順を1回実行して確認すること。
- Enno、DeepL、Shodoの公式ページ（規約・プライバシー）にはコンテナから到達できなかった。規約の記述は全て「未確認」か、第三者の検索結果の要約。

## 対象外（不採用）
- AI検出を回避する目的のツール・手法（言い換えで検出を逃れる系、AI利用を隠す運用）: **不採用: 規約・方針に反する**。名前の調査もしない。
- AI利用の明記は、これまでどおり続ける。

## 比較表

| ツール | 用途 | 日本語・品質(根拠のある範囲) | 無料枠 | 入力データの扱い(公式) | ログイン | 結論 |
|---|---|---|---|---|---|---|
| textlint + 日本語ルール(npm) | 校正の指摘。一部は自動修正 | 日本語向けルール群が公式プリセットとして存在。品質の客観評価は未確認。指摘は機械的で、読みやすさの判断は人が必要 | 全部無料(MIT)。コンテナで実行できる | ローカル実行。外部送信の明記は未確認だが、プリセットの依存一覧に外部API系は見当たらない | 不要 | **採用(最適解)** |
| AI文章パターン検出プリセット(@textlint-ja/preset-ai-writing) | AIに多い書き癖の指摘 | 誇張表現、太字の多用、絵文字リスト、コロン直後のリストなどを検出。効果の検証は未確認 | 無料(MIT) | ローカル | 不要 | 保留(試験導入。下に注意) |
| Claudeで推敲(別の指示) | 言い換え、文体調整、読みにくさの指摘 | 日本語の自然さは高い(一般的な実感。数値の根拠は未確認)。ただし事実や体験を足してしまう危険がある | 既存の月3,000円の中 | 新しい送信先は増えない | 既存 | 採用(併用。指示は下) |
| Enno | 誤字・変換ミス・二重敬語の指摘 | AIではなくパターン照合(第三者記事)。書き換えはしない。指摘中心 | 無料・登録不要(第三者記事) | 公式は未確認。第三者記事では「送信文は保存せず件数だけ保存」とあるが、公式の裏取りなし | 不要 | 保留(補助。Keita本人が規約を確認) |
| DeepL Write | 言い換え | 公式の説明で確認できた対応言語は英独西仏伊葡。日本語は確認できず(日本語対応とする第三者記事は公式と食い違う) | 無料版あり。上限の公式数値は未確認 | 未確認 | 未確認 | 不採用(日本語未確認。確認できたら再評価) |
| Shodo | 生成AIによる校正 | 日本語特化のサービス(第三者記事) | 無料プランあり(制限あり)。有料は月1,000円(税込、第三者記事) | 学習利用・保持期間は未確認 | 要(Keita本人作業) | 保留(アカウント作成が要る) |
| 文章校正ツール(uravation) | 誤字チェック | 品質は未確認 | 無料・登録不要。1日の全体枠と、10分あたり10回の制限(運営の説明) | 「入力文は保存しない」は運営者自身の説明。第三者の検証なし | 不要 | 保留(Ennoと重複するので優先度低) |

## 出典(取得日 2026-10-11)
- textlint 15.8.0, Node.js 20.18以上, MIT: https://registry.npmjs.org/textlint/latest
- textlint-rule-preset-ja-technical-writing 12.0.2(23ルール): https://registry.npmjs.org/textlint-rule-preset-ja-technical-writing/latest / README: https://raw.githubusercontent.com/textlint-ja/textlint-rule-preset-ja-technical-writing/master/README.md
- textlint-rule-preset-japanese 10.0.4: https://registry.npmjs.org/textlint-rule-preset-japanese/latest
- textlint-rule-preset-ja-spacing 3.0.3: https://registry.npmjs.org/textlint-rule-preset-ja-spacing/latest
- textlint-rule-prh 6.1.0: https://registry.npmjs.org/textlint-rule-prh/latest
- textlint-rule-ja-no-orthographic-variants 2.0.0(表記ゆれ): https://registry.npmjs.org/textlint-rule-ja-no-orthographic-variants/latest
- textlint-rule-ja-no-abusage 3.0.0(誤用): https://registry.npmjs.org/textlint-rule-ja-no-abusage/latest
- @textlint-ja/textlint-rule-preset-ai-writing 1.7.0 / README: https://registry.npmjs.org/@textlint-ja/textlint-rule-preset-ai-writing/latest / https://github.com/textlint-ja/textlint-rule-preset-ai-writing
- textlint 使い方(README): https://raw.githubusercontent.com/textlint/textlint/master/README.md
- ja-no-redundant-expression: https://raw.githubusercontent.com/textlint-ja/textlint-rule-ja-no-redundant-expression/master/README.md (--fix対応はREADMEに記載なし。未確認)
- DeepL Write 対応言語(公式ページへの検索結果): https://www.deepl.com/ja/features/write (コンテナから直接は未到達。検索結果の要約)
- Enno(検索結果の要約のみ): https://gigazine.net/news/20140830-enno / https://www.sungrove.co.jp/proofreading-tool
- Shodo(第三者記事): https://saas.imitsu.jp/cate-generative-ai/service/4819/price
- 文章校正ツール(運営の説明): https://uravation.com/tools/bunsho-kousei/

## textlint の詳細(最適解)

### 何ができるか
文章を読んで、決めたルールに合わない箇所を行番号つきで指摘する。本体にルールは入っておらず、ルールを別に入れる。書き換えは、`--fix` に対応したルールだけ。多くは「指摘のみ」で、直すのは人。

### 入れるパッケージ(全部npm、MIT。バージョンは取得日時点)
| パッケージ | 役割 |
|---|---|
| textlint 15.8.0 | 本体。Node.js 20.18以上 |
| textlint-rule-preset-japanese 10.0.4 | 一般向けの日本語。1文の長さ、読点の数、助詞の重複、ですます/である混在、ら抜き、二重否定、同じ接続詞の連続、逆接「が」の重複、見えない文字など |
| textlint-rule-preset-ja-technical-writing 12.0.2 | 上に加え、曖昧な表現(「かもしれない」「と思います」等)、冗長表現、誤用、表記の揺れ、感嘆符、連続する漢字、全角半角など。名前は技術文書向けだが、デフォルトは厳しめ。READMEも「文章に合わせて調整」と書いている |
| textlint-rule-preset-ja-spacing 3.0.3 | 日本語と英数字の間のスペース等。取り込み先の文体に合わせて使う |
| textlint-rule-prh 6.1.0 | 自分の辞書(YAML)で表記ゆれ・禁止語を指摘。`voice-guide.md` の「避ける語」を辞書にできる |
| textlint-rule-ja-no-orthographic-variants 2.0.0 | 表記ゆれ(例: 同じ語の漢字/ひらがな混在) |

2つのプリセットは一部重複する(同じルールが両方に入っている)。**まず ja-technical-writing 1本で始める**のが無難(仮説。重複の影響は未検証)。

### 手順(CEO側。コンテナで実行。Keita作業なし)
作業フォルダは新しい空ディレクトリを使う(リポジトリ直下に node_modules を作らない)。
1. `mkdir <作業フォルダ> && cd <作業フォルダ> && npm init -y`
2. `npm install --save-dev textlint textlint-rule-preset-ja-technical-writing textlint-rule-prh`
3. 設定ファイル `.textlintrc.json` を作る(下の例)
4. 実行: `npx textlint 校正したい.md`
5. 自動修正のプレビュー: `npx textlint --dry-run --format diff 校正したい.md` → 良ければ `npx textlint --fix 校正したい.md`(--fixは対応ルールだけ。実行前に必ず _backup へ複製)

設定例(READMEの記載にもとづく。この環境では未実行):
```json
{
  "rules": {
    "preset-ja-technical-writing": {
      "sentence-length": { "max": 90 },
      "ja-no-weak-phrase": false,
      "no-exclamation-question-mark": false
    },
    "prh": { "rulePaths": ["./prh-keita.yml"] }
  }
}
```
- 注意: ルール名を個別に書く形式は、READMEの例(`"max": 120`、`"no-mix-dearu-desumasu": false`)から外れる。**READMEにあるのは、プリセット直下に `max` や `ルール名: false` を書く形。上の入れ子形式が通るかは未検証。** 通らなければREADMEの形に直す。
- 「ja-no-weak-phrase」(〜かもしれない、〜と思います)は、voice-guide の「〜かも」を混ぜる方針と衝突するので切る候補。ルールを入れ過ぎると、くだけた口調まで全部指摘される。
- `prh-keita.yml`(辞書)の例は、形式を確認してから作る(prhの書式は一般知識で、この調査では未確認)。中身の候補は voice-guide の「避ける語」(大切です、重要です、していきます、しっかり、ぜひ、さまざまな)。

### 判定基準(試験導入)
- 3本の既存下書きで実行し、指摘のうち「直して良かった」が半分以上なら定着。無意味な指摘が多いルールは切る。
- 失敗の判定: 指摘が多すぎてKeitaの口調(短文・体言止め・〜かも)を潰すなら、ルールを減らす。直した結果が硬くなったら元に戻す。

### preset-ai-writing の扱い
- READMEの要約では、目的は「AIが書いた文章に出やすいパターンを見つけて、自然な日本語にする」で、検出の回避は謳っていない。MITで、textlint 15.1以上が必要。
- 運用: **品質の指摘として使う。** 指摘を見て、Keitaの体験・数字・口調を足す方向で直す。「検出を逃れるために直す」「AI利用の明記を消す」使い方はしない。後者に寄ってきたら不採用に切り替える。
- 判定は保留。1回試して、指摘が voice-guide の「AIっぽい癖」と一致するかを見る。

### 限界
- textlint は形式の指摘しかしない。体験・数字・本音は足せない。voice-guide の「AIっぽい癖」のうち、抽象語の連発、三点セット、すべて「です・ます」は、一部だけ機械で拾える(prh辞書、ですます混在など)。見出しの味、本音の1文は人が書く。
- 機械の指摘に従うほど、文章は均一になる。均一さは「AIっぽさ」の一因なので、全部は直さない。

## Claudeで推敲する場合との比較
| 観点 | textlint | Claude(別の指示) |
|---|---|---|
| 何を見るか | 決めたルールだけ | 文脈、リズム、言い換え |
| 再現性 | 高い(同じ入力で同じ指摘) | 低い(毎回違う) |
| 危険 | 少ない | 体験や数字を創作する。口調がなめらかな「AI調」に寄る |
| Keitaの作業 | なし | なし |
| 費用 | 0円 | 既存の月3,000円 |

結論: 先にtextlintで形式を洗い、次にClaudeに「言い換え案を出させ」、最後にKeitaが自分の言葉に直す。

### Claudeに渡す指示(コピペ用)
```
次の文章を推敲して。条件:
1. 事実、数字、体験は一切足さない・変えない。足りない所は【Keita確認】と書く
2. 直す所は「元 → 案 → 理由」で一覧にする(全文の書き直しはしない)
3. 一文は30〜40字を目安に。文末は「です・ます」だけにせず、「だ」「かも」「体言止め」を混ぜる(くだけ過ぎない)
4. 抽象語(仕組み、価値、最適化など)は、具体的な場面に置き換える案を出す
5. AIを使ったことの明記は消さない
```

## Keitaがコピペで使う手順(Mac)
Web版は補助。**メインはCEO側のtextlint(Keita作業なし)**。Keitaは、最後の確認だけ。

### A. Enno で誤字を見る(補助。公開予定の文章のみ)
注意: 画面のボタン名は公式未到達のため**未確認**。画面の指示に従う。
1. Safari を開き、「Enno 日本語 校正」で検索して、公式サイトを開く(URLは検索結果で確認。偽サイトに注意)
2. 画面に、規約やプライバシーの記載があれば読む。「入力文を保存・学習に使う」と読める場合は使わない
3. 校正したい文章を選んで、`command + C` でコピー
4. Enno の入力欄をクリックして、`command + V` で貼り付け
5. チェックのボタンを押す(名前は未確認)
6. 赤や色が付いた所を確認する。**全部は直さない。** 誤字・変換ミスだけ直す
7. 個人名、店名、取引先、メールアドレス、電話番号が入った文章は貼らない

### B. Claude に推敲させる(上の指示をコピペ)
1. Claude を開く → 新しいチャット
2. 上の「Claudeに渡す指示」を貼り付け、その下に文章を貼る(`command + V`)
3. 返ってきた「元 → 案 → 理由」を読み、自分が言いたいことに近いものだけ採る

### C. Keita自身のMacにtextlintを入れる場合(任意。普通は不要)
- Node.js(20.18以上)が要る。入っていなければ、Node.js公式のインストーラを使う。インストール作業はKeita本人。
- ターミナルで `node -v` と入力して `Enter`。`v20.` 以上が出れば可。
- 以降はCEO側の手順1〜4と同じ。ただし、CEO側で回せるので、Keitaは入れなくてよい。

## 推奨
- **最適解: textlint(ja-technical-writing + prh の自作辞書)をCEO側で回し、そのあとClaudeに言い換え案を出させ、Keitaが自分の言葉に直す。** 理由: 0円、Keita作業なし、外部にデータを出さない、再現性が高い。Keita以外にも手順を渡せる(母親・学生向けの横展開は、実数が出てから)。
- **普通はやらない案: 自分(Keita)の文章サンプル500〜1,000字から、prh辞書とルール設定を作る。** voice-guide が待っている「口癖・文末の癖」を、辞書として機械でチェックできる形にする。「Keitaらしさ」を指摘する自前の校正器になり、真似されにくい。サンプルが無いと作れない(未受領)。

## 次の一手
1. CEO側で上の手順1〜5を1回実行し、動くか確認(未検証の解消)。動かなければ、この文書の「採用」を「保留」に直す
2. 既存の下書き3本に実行して、判定基準で残すルールを決める
3. Keitaの文章サンプル(500〜1,000字)を受け取り、prh辞書を作る
4. Keitaに依頼(任意): Enno の公式規約を読み、入力文の扱いの記載を教えてもらう。Shodoのアカウント作成は、textlintで足りなければ検討
