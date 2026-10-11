# efficiency

## 2026-10-10 定期ルーティンの作り方（横展開できる知見）
- **ルーティンで新規セッションを起動すると、リポジトリが付かない。**（診断テストで確認: 作業場所が空、`.claude/agents/` も見えない）
- **回避策:** リポジトリを付けた専用の運用セッションを作り（`create_session` の `source_url`）、定期トリガーをそのセッションに向ける（`persistent_session_id`）。手順書（`OPS_RUNBOOK.md`）とバックログ（`BACKLOG.md`）をリポジトリに置き、毎回それを読んで動く
- 運用セッションは permission_mode が auto で作成された。ツールは Bash、Agent、WebSearch、WebFetch、トリガー操作などが使え、GitHub MCPは無し（`git` で push する）
- 朝9時・夜21時の報告に合わせ、起動は8:40・20:40（日本時間）。cron は `CRON_TZ=Asia/Tokyo` を付けて指定する
- 1回の診断で約0.07ドル相当、セットアップ確認で約0.17ドル相当（list価格換算）。サイクルはこれより大きい。5時間枠の使用状況は `get_session` の `rate_limit_info` で見える

## 2026-10-10 画像・動画の自動生成は、このコンテナで可能
- Pillow（PyPI経由で取得可）、日本語フォント（IPAゴシック）、ffmpeg が利用可能。カルーセル画像や字幕つき動画を、API無しで生成できる
- 投稿そのもの（X、Threads、Instagram）は、ドメイン遮断のため私からはできない。予約投稿はKeitaの端末で行う
