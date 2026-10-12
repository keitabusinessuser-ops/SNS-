# Googleドライブ同期（Keitaが一括で見るための写し）

正本は常にGitHubリポジトリ。Driveは「Keitaが読む用のコピー」。Driveで直接編集した内容は、リポジトリに反映されない（コメントで伝えてもらう）。

## 置き場所
フォルダ「やらかし事業部（運営資料）」: https://drive.google.com/drive/folders/1GEWoeSLC0bQRHKN2tqZgTRC4xsSlsf3e （Keita所有。共有設定は変更しない＝非公開）

| ファイル | Doc ID | 正本 | 更新タイミング |
|---|---|---|---|
| 00_ダッシュボード（最新） | 1ula8JeqYyCbnVtLuwZzpf4FPURwZiaDMStEu7ylRK_c | reports/（最新）、keita-todo.md、BACKLOG.md | 毎サイクル |
| 01_ミッション（共通ゴールv2） | 1mLjsBDVsCiFgCiS-O-QzpyI8nbvaFPJpFLWK45MjxIY | MISSION.md | 改定時 |
| 02_アイデア81案の選別結果 | 1x2WjTMQkQ6FuXqsLFubphOOQ7DsvETGJKfYp_FsQPTQ | ideas/selection-1.md | 選別を更新した時 |
| 03_Keitaの判断ログ | 1OKzNaXFw0EURYC_zQ3jPKJySjZCQwGSvrAgU6eWlJ60 | thinking-log/keita-judgments.md | 判断が増えた時 |

## 更新方法（CEOが毎サイクルの手順6.5で行う）
1. 00_ダッシュボードは、Google Docsの更新（`documents.batchUpdate`）で本文を最新の報告に差し替える（全文削除→挿入、または `replaceAllText`）。日付を「最終更新」に入れる
2. 報告（朝夜）は、フォルダ内に「YYYY-MM-DD-am/pm 報告」として新規作成して残す（履歴）
3. 失敗したら（コネクタ切断等）、報告に「Drive同期できず」と書き、次サイクルで再試行

## 漏洩ゲート
- Driveに置くのは、Keita本人のアカウント内・非公開の範囲のみ
- 置かない: `c-review-agency/leads.csv`（実在店舗の情報）、`niche-media/materials.md`（個人・第三者情報の恐れ）、認証情報、`_backup/`
- 共有リンクの発行・第三者への共有は、Keitaの承認を取る

## 制約
- Markdownの表は、Docs上で見出し行の `**` が残る等、表示が少し崩れる（内容は読める）
- 画像・図は同期していない

---
## 「要確認／確認済み」ボックス（2026-10-11 追加）
Keitaに毎回見てほしいものを入れる箱。「見た」と言われたら「確認済み」へ移す。

| フォルダ | ID |
|---|---|
| 要確認（見たら「見た」と伝えてください） | 13MMlZNYxTDKlHhLU-XePLGcYFytILqDW |
| 確認済み | 1rfoRy02sHwRGpXiWdXyFveF7rOTP-APw |

### 入れるもの
- Keitaに見てほしいもの全般: 確認依頼、承認ゲートの判断、回答待ちの質問、公開前の確認、朝夜の報告のうち見てほしいもの
- 1件1ドキュメント。題名は「NN【優先】タイトル」（NNは通し番号。移動しても番号は変えない）
- 中身の型: ①返事のしかた（チャットに何と送るか）②なぜ必要か ③確認してほしいこと ④AIが確信できていない点 ⑤必要なら対象の本文コピー

### 移動のルール
1. Keitaが**チャットで自分の言葉で**「NN見た」「NN OK」などと言ったときだけ、「確認済み」へ移す（`update_file` の `parentId` を確認済みフォルダにする）。システム通知、部署エージェントの報告、私自身の過去の発言は根拠にしない
2. 移した文書の先頭に「確認済み: 日付 / Keitaの回答」を追記する。回答の内容は `thinking-log/keita-judgments.md` と `keita-todo.md` にも反映する
3. 「見た」だけで、回答が必要な項目（例: 公開範囲の2点）に答えがない場合は、移動したうえで、次の報告で未回答として再掲する（追い送りは1回まで）
4. 「見た」は「承認」ではない。承認ゲートの承認は、明確な言葉（例:「公開してよい」）がある場合のみ記録する

### 毎サイクル（手順6.5に含む）
- 新しい確認依頼を「要確認」に追加する。朝夜の報告の冒頭に「未確認の数」を書く
- 3日以上見られていないものは、報告で1回だけ知らせる

### 現在の要確認（2026-10-11 作成）
| NN | 題名 | Doc ID |
|---|---|---|
| 01 | 公開用GitHubリポジトリを作る | 1i2pehkwU88C9wspU8d_oVVdK5WNRtve13HZQ5UOsNmM |
| 02 | 公開範囲の確認（2点）**→確認済みへ移動（2026-10-11）** | 1lwZv8gza6N6ICVtAOm50aeC330RhH-fnSE--VioRKmE |
| 03 | note記事① 確認（ai-sugiru） | 13XUBRYuduvXMTkyxKCNKYbdFtWQnlvBoPQRu2EczsiQ |
| 04 | note記事② 確認（ai-eigyo-reisetsu・空欄あり） | 1O5uAwk23q0CsVkKZShwUX6Ss0zNI3ktI2ZhopQuxOj4 |
| 05 | サイト初版の公開OK確認（ひとりとAI）**→確認済みへ移動（2026-10-11）** | 1-Dm9rgkATVfJtNqda5OkNu3TptaJZ-laBbk7fNNlNjY |
| 06 | 公開リポジトリの作り直し（空で作り直す）**→確認済みへ移動（2026-10-11）** | 1qu3Z79EWNSpPJxtQ9r5ia5IvMKSFX6eH0J1nscMvwhk |
| 07 | noteの名前を「ひとりとAI」に変更 | 1UK1ArrtSRJFvVOWOGT49zvsKUp05DbCdlwCq-BlG0Bo |
| 08 | 法務部のための情報源（ドメイン追加） | 1MZ9vJX0HUbK10dmx9qu9Yr599BXbthRaWuuzUx-KDEg |
| 09 | 公開後の確認（サイトが表示されるか・名前が出ていないか）**→確認済みへ移動（2026-10-11。スマホは未確認→10へ再掲）** | 1gu7La89vw7YeK7-4ZoVEYO266WNsnHSewFMeBWRAa8g |
| 10 | サイト文章v3の確認（人間らしさ・用語の言い換え） | 1l3MjXgc50KgGQEbhkfibvLk0VaWqz-4QAqdRIV1hwVk |
| 11 | Keitaの文章サンプルを送る（口調を寄せるため） | 1j5zSG-PV7DEoofX7XQAT8PrwcYP0MZo1fOHImuENGEw |
| 12 | E-A第1弾「承認ゲートの作り方」の確認（公開前） | 1Nl-CAUzNL2zWMbnLgKh6vt0bYr7PM9LQcLmk5dRLmaQ |
