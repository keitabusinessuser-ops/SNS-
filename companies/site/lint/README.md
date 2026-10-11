# 文章を校正ツール（textlint）に通す手順（コンテナ内で動く。Keitaの作業なし）
2026-10-11 動作確認済み（Node v22、npm経由。外部サイトへの送信なし。文章はローカルで処理される）。

```
mkdir -p /tmp/lint && cd /tmp/lint && npm init -y
npm install textlint textlint-rule-preset-japanese textlint-rule-preset-ja-technical-writing @textlint-ja/textlint-rule-preset-ai-writing
cp <repo>/companies/site/lint/extract.py <repo>/companies/site/lint/.textlintrc.json .
python3 extract.py <repo>/companies/site/<ver>/index.html > page.txt
npx textlint --config .textlintrc.json page.txt
```
- 使うルール: preset-japanese（助詞の重複・長文・読点など）、ai-writing（AIに多い書き癖の検出）。ja-technical-writing は厳しめなので、必要なときだけ追加
- **指摘は参考。自然な言い回しも指摘される**（例:「売上も記事も」は助詞「も」の重複と出る）。直すかは人が判断する
- 目的は読みやすさの校正。**AI検出の回避ではない**（MISSION.md）。AI利用の明記は続ける
- 流れ: AIが下書き → 文体ガイド（`knowledge/voice-guide.md`）で書き直し → textlintで確認 → Keitaが確認 → 公開
