# バックログ（優先順。CEOが毎サイクル見直す。更新: 2026-10-11 夜・日曜週次）

最重要ミッション: 1人の人間とAIで月収50万（`MISSION.md` v2）。AIメイン・模倣困難・初期費用ゼロ・再現性。
状態: 新規 / 進行 / 完了 / 保留

| 優先 | タスク | 状態 | 担当 | 成果物 |
|---|---|---|---|---|
| P0 | E-D: experiments.json+check-experiments.py 稼働中。E-F(通信しない事務ライブラリ群): 既存3ツールに「通信ゼロ」検証テストを追加し実行確認（公開しない）。選別: ideas/selection-2,3.md | 新規 | CEO＋general-purpose | tools-src/ |
| P0 | E-A: 承認ゲート設計テンプレ（最初の公開物）。下書き→compliance→Keita確認→サイトに掲載 | 進行（下書き作成中） | media-editor＋compliance | `site/drafts/e-a-01-approval-gates.md` |
| P0 | 法務部の蓄積: 優先1（広告・表示）済 → 優先2（個人情報）済 → 優先1〜8済み（広告・個人情報・著作権・名誉・契約・税務・営業・AI関連）→ 次は優先9（業種別、必要時）と、既存ファイルの確認度の底上げ（一次情報に到達できたとき）。**一次情報に到達できないため、すべて二次情報。ドメイン追加（Drive 08）がボトルネック** | 進行 | legal | `legal/laws/`、`legal/issues/` |
| P0 | 計測: GitHub指標の自動保存（済）。サイト訪問の解析は、導入前の法務確認（外部送信規律・通知）とKeita作業が要る。推奨はCloudflare Web Analytics（`knowledge/analytics-plan.md`）。Keitaの未確認が多いので、依頼は後ろに回す | 進行（保存は稼働） | scout＋legal | `metrics/`、`knowledge/analytics-plan.md` |
| P0 | サイト文章v3の公開（Keita確認 Drive 10 の後）。文章サンプル（Drive 11）で口調を寄せ直す | 待ち（Keita） | media-editor | `site/draft-v3/` |
| P1 | E-B: 題材選定は完了（推奨5本: 文字数カウント／和暦西暦／日数計算／トークン概算／AI用語集）。2本制作・動作確認・審査済み（文字数カウント `site/e-b/moji-count/`、和暦西暦 `site/e-b/wareki/`）。公開は、Keita確認（Drive 13）の後。3本目以降（日数計算・トークン概算・AI用語集）は、Keitaが公開OKを出して流れを確認してから | 待ち（Keita） | media-editor＋compliance | `site/e-b-topics-01.md` |
| P1 | E-C: cite-gap 0.1.0 を実装済み（テスト33件OK、wheelビルドOK、compliance「修正後可」を反映。`tools-src/cite-gap/`）。draftgate 0.1.0 も実装済み（テスト25件OK、npm packの中身OK、compliance「修正後可」を反映）。名前は npm/PyPI とも空き（私が直接確認、2026-10-13）。**公開（PyPI/npmのアカウント作成・2FA・規約同意）はKeita本人作業のため、未確認が減ってから** | 進行 | CEO | `tools-src/` |
| P1 | noteの名前変更（Keita、Drive 07）と、note記事2本の確認（Drive 03/04の旧版→再確認） | 待ち（Keita） | — | — |
| P1 | 思考ログ: 判断を毎回追記。週次で `keita-model.md` 更新 | 進行（v0作成） | CEO | `thinking-log/` |
| P2 | 事実ログを毎週作る（第0週を作成） | 進行 | analyst | `niche-media/log/` |
| P2 | 日曜週次: knowledge更新、kpi更新、ポートフォリオ判定（4週時点は11/7） | 進行 | CEO | `knowledge/` |
| 保留 | G6 変化検知配信（要ドメイン）、G5 手順カード（土台）、アフィリエイト（法務確認後）、C社（営業はしない） | 保留 | — | — |

## 保留・待ち（Keita）
`companies/keita-todo.md` と、Drive「要確認」フォルダを参照。
