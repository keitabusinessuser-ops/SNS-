'use strict';
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs'); const path = require('node:path');
const { spawnSync } = require('node:child_process');
const root = path.join(__dirname, '..');
const BANNED = ['net', 'http', 'https', 'http2', 'tls', 'dns', 'dgram', 'child_process', 'cluster', 'worker_threads'];

const files = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
  e.isDirectory() ? files(path.join(dir, e.name)) : /\.(js|cjs|mjs)$/.test(e.name) ? [path.join(dir, e.name)] : []);
const sources = [...files(path.join(root, 'src')), ...files(path.join(root, 'bin'))];

test('src/ と bin/ に通信系の require/import が無い', () => {
  assert.ok(sources.length > 0);
  const re = /(?:require\s*\(\s*|import\s*\(\s*|from\s+|import\s+)['"`](?:node:)?([a-z_0-9]+)(?:\/[^'"`]*)?['"`]/g;
  for (const f of sources) {
    const s = fs.readFileSync(f, 'utf8');
    for (const m of s.matchAll(re)) assert.ok(!BANNED.includes(m[1]), `${path.relative(root, f)}: ${m[0]}`);
    assert.ok(!/\b(fetch|XMLHttpRequest|WebSocket)\s*\(/.test(s) && !/new\s+(WebSocket|XMLHttpRequest)/.test(s), `${f}: fetch 等`);
    assert.ok(!/process\.binding|require\s*\(\s*[^'"`\s]/.test(s), `${f}: 動的 require`);
  }
});

test('ガードが実際に効く（net/http/dns/child_process を src 側から require すると失敗）', () => {
  const guard = path.join(__dirname, 'helpers', 'block-network.js');
  const code = (mod, file) => `require(${JSON.stringify(guard)});
    const Module=require('node:module');
    const m=new Module(${JSON.stringify(file)}); m.filename=${JSON.stringify(file)};
    try{ m.require(${JSON.stringify(mod)}); process.exit(0);}catch(e){ process.exit(/検出/.test(e.message)?42:1);}`;
  for (const mod of ['net', 'node:http', 'https', 'dns', 'node:dns']) {
    assert.strictEqual(spawnSync(process.execPath, ['-e', code(mod, path.join(root, 'test', 'x.js'))]).status, 42, mod);
  }
  assert.strictEqual(spawnSync(process.execPath, ['-e', code('child_process', path.join(root, 'src', 'x.js'))]).status, 42);
  assert.strictEqual(spawnSync(process.execPath, ['-e', code('child_process', path.join(root, 'test', 'x.js'))]).status, 0);
});
