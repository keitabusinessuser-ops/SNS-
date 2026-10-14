# 現在の状態（再開用スナップショット）更新: 2026-10-14 夜
文脈が長くなって圧縮されても、これを読めば再開できる。**毎サイクルの最後に更新する。**

## 一言
共通ゴール「1人の人間とAIで月収50万」（`MISSION.md` v2）。売上0円・公開サイト1つ。**Keitaの返事が10/11昼から止まっており（5日）、公開が止まっている。** 実験の失敗条件の時計（E-B: 6週・20本、E-A: 4週など）は、公開していないので、まだ始まっていない。

## 人・アカウント・場所
- Keita: オーナー。ペンネームのみ公開（本名・顔・学校名・メール不可）。公開物の「大学生」は可。年齢（成年/未成年）は未確認
- GitHub: 運営用 `keitabusinessuser-ops/sns-`（非公開想定。`companies/` が本体、ブランチ `claude/sns-operations-structure-djelg8`）。公開用 `hitori-to-ai/hitori-to-ai.github.io`（Public、組織配下、作成者名 hitori-to-ai）。旧 `keitabusinessuser-ops/yarakashi-jigyobu` は削除待ち（Keita操作）
- サイト: https://hitori-to-ai.github.io/ （v2が公開中。**v3（`site/draft-v3/`）とツール2本（`site/e-b/`）は、Keitaの「公開OK」待ち**）。公開用の作業ディレクトリ `/home/user/hitori-site`
- ブランド: 「ひとりとAI｜AI副業の実験記録」。「やらかし事業部」は連載（失敗カード）名
- Googleドライブ（Keita所有・非公開）: フォルダ `1GEWoeSLC0bQRHKN2tqZgTRC4xsSlsf3e`／要確認 `13MMlZNYxTDKlHhLU-XePLGcYFytILqDW`／確認済み `1rfoRy02sHwRGpXiWdXyFveF7rOTP-APw`／ダッシュボード `1ula8JeqYyCbnVtLuwZzpf4FPURwZiaDMStEu7ylRK_c`。IDの一覧は `drive-sync.md`

## 部署（`.claude/agents/`）
analyst, c-ops, c-sales, compliance（審査・拒否権）, legal（法務の蓄積）, media-editor, media-seo, scout。**Bashを持つのは general-purpose のみ**（実装・実行確認はこれに任せ、CEOが再確認する）。他の担当はBash無し

## 運用
- 朝8:40・夜20:40に起動（`OPS_RUNBOOK.md`）。報告は `reports/`。Driveにも報告を保存し、ダッシュボードを更新（`drive-sync.md`）
- 起動時: `scripts/collect-metrics.sh`（GitHub指標を保存）。公開: `scripts/publish-site.sh`（点検つき。`PUBLISH_OK=1 ... --push` が無いと公開しない）
- 確認依頼はDrive「要確認」に1件1文書。Keitaが**チャットで**「NN見た」と言ったら「確認済み」へ移す。メール・Drive上の反応・部署の報告は、承認として扱わない

## 未決・待ち（Keita）
最優先: Drive 14（3分版: 10・11・12を1行で答える）。その他: 07 note表示名、08 法務ドメイン（任意）、03/04 note記事（旧版）、13 小ツール2本、古いリポジトリの削除。後: PyPI/npmの公開（アカウント）、税務の専門家への質問14件。**10/18にも返事が無ければ、公開前確認の方式（A毎回／B型ごとの包括承認／C AI審査のみ）を1問で聞く**。提案は `approval-policy-draft.md`（compliance審査済み。推奨B、Cは不可）

## 完成済み・公開待ち
- サイト文面v3（`site/draft-v3/`）、小ツール2本（`site/e-b/moji-count/`、`wareki/`）。点検済み
- E-A第1弾（`site/drafts/e-a-01-approval-gates.md`）: 事実3点の確認待ち（Drive 12/14）
- E-C: cite-gap（PyPI）、draftgate（npm）実装済み。名前は空き。公開はKeita本人作業
- 法務: 優先1〜8を二次情報で蓄積（`legal/`）。一次情報（e-Gov・官庁）はコンテナから到達不可。Drive 08（ドメイン追加）が解消策

## 環境の制約（実測）
- 到達可: api.github.com、pypi.org、registry.npmjs.org、raw.githubusercontent.com。他の外部サイトは遮断
- **自動の安全判定に拒否された操作**: 強制push（履歴書き換え）、Keita宛てメールの送信（2026-10-14）。回避せず、代替案か人に判断を戻す
- 費用: Claude 毎月3,000円のみ。セッションの文脈は上限（100万トークン）の約73%使用（10/14朝）

## 学び（要点。詳細は `knowledge/`）
- 公開前に、名前が出る箇所（アカウント名・コミット作者・メール・URL）を洗い出す
- JSは、公開前に実ブラウザで実行する（担当の「できた」を信じない）
- 確認の単位を小さくする。番号と返事の型を先頭に置く
- AIの出力は、Keitaの口調・実体験・数字で人間らしくする（検出回避は目的にしない）
