'use strict';
const test = require('node:test');
const assert = require('node:assert');
const { check } = require('../src/core');

const rules = (t, o) => check(t, o).findings.map((f) => `${f.line}:${f.rule}`);

test('README例: 未解決マーカー・穴埋め・前置き', () => {
  const r = rules('## 料金\n【要確認】月額は○○円です。\n以下に記事を示します。');
  assert.deepStrictEqual(r, ['2:unresolved-marker', '2:placeholder', '3:ai-preamble']);
});
test('【担当者確認】【運営者確認：経緯】を拾う', () => {
  assert.deepStrictEqual(rules('a【担当者確認】b\nc【運営者確認：経緯の書き方】'), ['1:unresolved-marker', '2:unresolved-marker']);
});
test('TODO/TBD/XXX は単語として拾い、部分一致は拾わない', () => {
  assert.deepStrictEqual(rules('TODO x\nTBD\nXXX'), ['1:todo', '2:todo', '3:todo']);
  assert.deepStrictEqual(rules('TODOLIST and MAXXXL'), []);
});
test('穴埋め: ここに〇〇を入れる / {{var}} / lorem ipsum', () => {
  assert.deepStrictEqual(rules('ここに事例を入れる\n{{name}}さん\nLorem Ipsum'), ['1:placeholder', '2:placeholder', '3:placeholder']);
});
test('AI前置き: 承知しました / 以下のとおりです / 以下が下書きです / As an AI', () => {
  for (const s of ['承知しました。', '以下のとおりです。', '以下が下書きです。', 'As an AI language model', '- 承知しました']) {
    assert.deepStrictEqual(rules(s), ['1:ai-preamble'], s);
  }
});
test('前置きは行頭のみ。文中の「以下のとおり」は拾わない', () => {
  assert.deepStrictEqual(rules('結果は以下のとおりです。'), []);
});
test('重複行は2回目以降を報告。短い行・表の区切りは対象外', () => {
  const r = check('これは同じ行です。\n---\nこれは同じ行です。\n|a|b|\n|a|b|\nok\nok');
  assert.deepStrictEqual(r.findings.map((f) => f.line), [3]);
  assert.strictEqual(r.findings[0].firstLine, 1);
});
test('閉じていないコードブロック', () => {
  const r = check('a\n```\nコード');
  assert.deepStrictEqual(r.findings.map((f) => `${f.line}:${f.rule}`), ['2:unclosed-fence']);
});
test('閉じたコードブロック内は既定で除外、--include-code で点検', () => {
  const t = '```\nTODO x\n```\n';
  assert.deepStrictEqual(rules(t), []);
  assert.deepStrictEqual(rules(t, { includeCode: true }), ['2:todo']);
});
test('長いフェンスの中の短いフェンスは閉じない', () => {
  assert.deepStrictEqual(rules('````\n```\nTODO\n````\n'), []);
});
test('インラインコード・HTMLコメント・ignore行・front matter は除外', () => {
  assert.deepStrictEqual(rules('`TODO` と `【要確認】`'), []);
  assert.deepStrictEqual(rules('<!-- TODO -->\n<!--\nTODO\n-->\n'), []);
  assert.deepStrictEqual(rules('TODO draftgate: ignore'), []);
  assert.deepStrictEqual(rules('---\ntitle: TODO\n---\n本文'), []);
});
test('ダミーURL', () => {
  assert.deepStrictEqual(rules('https://example.com/x と https://www.example.org と http://localhost:3000/a'), ['1:dummy-url', '1:dummy-url', '1:dummy-url']);
  assert.deepStrictEqual(rules('https://notexample.com/'), []);
});
test('未確認は件数用に報告（unverified）', () => {
  assert.deepStrictEqual(rules('未確認です。未確認。'), ['1:unverified', '1:unverified']);
});
test('設定: markers と patterns で追加、disable で無効化', () => {
  const cfg = { markers: ['社内ペンディング'], patterns: [{ regex: '20XX年' }] };
  assert.deepStrictEqual(rules('社内ペンディング20XX年', { config: cfg }), ['1:custom', '1:custom']);
  assert.deepStrictEqual(rules('TODO', { disable: ['todo'] }), []);
});
test('CRLF と BOM', () => {
  assert.deepStrictEqual(rules('﻿a\r\nTODO\r\n'), ['2:todo']);
});
test('誤検出の例(既知): 引用中の「承知しました」は拾う', () => {
  assert.deepStrictEqual(rules('承知しました、と返した。'), ['1:ai-preamble']);
});
test('コードに通信モジュールが含まれない', () => {
  const fs = require('node:fs'); const path = require('node:path');
  for (const f of ['core.js', 'cli.js', 'index.js']) {
    const s = fs.readFileSync(path.join(__dirname, '..', 'src', f), 'utf8');
    assert.ok(!/require\(['"](?:node:)?(?:http|https|net|dns|dgram|tls|child_process)['"]\)|fetch\(/.test(s), f);
  }
});
test('長い【担当者確認：…】と【公開しない注記】を拾う', () => {
  assert.deepStrictEqual(rules('【担当者確認：' + 'あ'.repeat(60) + '】\n## 【公開しない注記】'), ['1:unresolved-marker', '2:unresolved-marker']);
});
