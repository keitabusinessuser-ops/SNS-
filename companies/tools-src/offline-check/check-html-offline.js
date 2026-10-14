#!/usr/bin/env node
'use strict';
// 単一HTMLが外部通信をしないことの静的検査（ローカル完結、依存ゼロ、HTMLは変更しない）。
// 使い方: node check-html-offline.js [HTMLファイル...]   省略時は ../../site/e-b/wareki/index.html
// 終了コード: 0=問題なし / 1=検出あり / 2=使い方の誤り
const fs = require('node:fs');
const path = require('node:path');

const DEFAULT = path.join(__dirname, '..', '..', 'site', 'e-b', 'wareki', 'index.html');
const FORBIDDEN_JS = [
  [/\bfetch\s*\(/, 'fetch('],
  [/\bXMLHttpRequest\b/, 'XMLHttpRequest'],
  [/\bWebSocket\b/, 'WebSocket'],
  [/\bsendBeacon\b/, 'sendBeacon'],
  [/\bimport\s*\(/, 'import('],
  [/\bEventSource\b/, 'EventSource'],
  [/\bimportScripts\s*\(/, 'importScripts('],
  [/\bnavigator\s*\.\s*serviceWorker\b/, 'serviceWorker'],
];
const EXTERNAL = /^\s*(?:https?:)?\/\//i;

function check(html) {
  const problems = [];
  const lineOf = (i) => html.slice(0, i).split('\n').length;
  // <script> 要素
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)) {
    if (/\bsrc\s*=/i.test(m[1])) problems.push(`${lineOf(m.index)}: <script src> がある`);
    const bodyStart = m.index + m[0].indexOf('>') + 1;
    for (const [re, label] of FORBIDDEN_JS) {
      const hit = re.exec(m[2]);
      if (hit) problems.push(`${lineOf(bodyStart + hit.index)}: <script> 内に ${label}`);
    }
  }
  // 外部URLを指す src / href / srcset / action / poster / data 等の属性
  for (const m of html.matchAll(/\b(src|href|srcset|action|formaction|poster|data|ping)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/gi)) {
    const val = m[3] ?? m[4] ?? m[5] ?? '';
    const parts = m[1].toLowerCase() === 'srcset' ? val.split(',').map((s) => s.trim().split(/\s+/)[0]) : [val];
    // <a href> は利用者がクリックしたときだけ移動するリンクで、読み込み時の通信ではない
    const tagStart = html.lastIndexOf('<', m.index);
    if (m[1].toLowerCase() === 'href' && /^<a\s/i.test(html.slice(tagStart, tagStart + 4))) continue;
    for (const p of parts) if (EXTERNAL.test(p)) problems.push(`${lineOf(m.index)}: 外部URLの ${m[1]}="${p}"`);
  }
  // CSS 内の外部読み込み
  for (const m of html.matchAll(/url\(\s*['"]?\s*((?:https?:)?\/\/[^)'"\s]+)|@import\s+(?:url\()?\s*['"]?\s*((?:https?:)?\/\/[^)'"\s;]+)/gi)) {
    problems.push(`${lineOf(m.index)}: CSSが外部を参照 ${m[1] || m[2]}`);
  }
  // <meta http-equiv=refresh>, <link rel=preconnect|dns-prefetch|prefetch>
  for (const m of html.matchAll(/<meta\b[^>]*http-equiv\s*=\s*["']?refresh[^>]*>/gi)) problems.push(`${lineOf(m.index)}: meta refresh`);
  for (const m of html.matchAll(/<link\b[^>]*rel\s*=\s*["']?(?:preconnect|dns-prefetch|prefetch|prerender)[^>]*>/gi)) problems.push(`${lineOf(m.index)}: 先読みリンク`);
  return problems;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const targets = args.length ? args : [DEFAULT];
  let bad = 0;
  for (const f of targets) {
    let html;
    try { html = fs.readFileSync(f, 'utf8'); } catch (e) { console.error(`読めません: ${f}`); process.exit(2); }
    const probs = check(html);
    if (probs.length) { bad++; console.log(`NG ${f}`); probs.forEach((p) => console.log(`  ${p}`)); }
    else console.log(`OK ${f}`);
  }
  process.exit(bad ? 1 : 0);
}
module.exports = { check };
