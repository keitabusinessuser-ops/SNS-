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
