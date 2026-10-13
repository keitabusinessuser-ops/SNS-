'use strict';
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs'); const os = require('node:os'); const path = require('node:path');
const { spawnSync } = require('node:child_process');
const bin = path.join(__dirname, '..', 'bin', 'draftgate.js');
const run = (args, input) => spawnSync(process.execPath, [bin, ...args], { encoding: 'utf8', input });
const tmp = (name, s) => { const d = fs.mkdtempSync(path.join(os.tmpdir(), 'dg-')); const p = path.join(d, name); fs.writeFileSync(p, s); return p; };

test('検出あり=1、行番号つき', () => {
  const r = run([tmp('a.md', 'ok\n【要確認】x')]);
  assert.strictEqual(r.status, 1);
  assert.match(r.stdout, /a\.md:2 {2}未解決マーカー {2}「【要確認】」/);
});
test('検出なし=0', () => assert.strictEqual(run([tmp('b.md', 'きれいな文章です。')]).status, 0));
test('未確認のみは0。--fail-unverified で1', () => {
  const p = tmp('c.md', 'これは未確認です。');
  assert.strictEqual(run([p]).status, 0);
  assert.strictEqual(run([p, '--fail-unverified']).status, 1);
});
test('--json', () => {
  const j = JSON.parse(run(['--json', tmp('d.md', 'TODO')]).stdout);
  assert.strictEqual(j.summary.blocking, 1);
  assert.strictEqual(j.findings[0].rule, 'todo');
});
test('--config で検出語を追加', () => {
  const c = tmp('c.json', '{"markers":["保留"]}');
  assert.strictEqual(run(['--config', c, tmp('e.md', '保留中')]).status, 1);
});
test('標準入力', () => assert.strictEqual(run(['-'], 'TODO').status, 1));
test('--help は0、引数なし/不明/存在しないファイルは2', () => {
  assert.strictEqual(run(['--help']).status, 0);
  assert.strictEqual(run([]).status, 2);
  assert.strictEqual(run(['--nope']).status, 2);
  assert.strictEqual(run(['/nonexistent/x.md']).status, 2);
});
