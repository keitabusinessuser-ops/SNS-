'use strict';
const fs = require('node:fs');
const { check, RULES } = require('./core');
const pkg = require('../package.json');

const HELP = `draftgate ${pkg.version} - AIの下書きに残った「残骸」を公開前に点検します（外部通信なし）

使い方:
  draftgate [オプション] <ファイル>...      "-" で標準入力

オプション:
  --json               JSONで出力
  --config <file>      追加の検出語・設定（JSON）
  --include-code       コードブロックの中も点検（既定は除外）
  --fail-unverified    「未確認」の注記が残っていても終了コード1にする
  --disable <rule,..>  ルールを無効化 (${Object.keys(RULES).join(', ')})
  --version, --help

終了コード: 0=検出なし / 1=検出あり / 2=使い方・読み込みの誤り
「未確認」の注記は件数のみ報告します（既定では終了コードに影響しません）。
行に draftgate: ignore と書くと、その行は点検しません。
誤検出・見逃しがあります。最終判断は人が行ってください。`;

function parseArgs(argv) {
  const o = { files: [], json: false, includeCode: false, failUnverified: false, disable: [], config: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') o.help = true;
    else if (a === '--version' || a === '-v') o.version = true;
    else if (a === '--json') o.json = true;
    else if (a === '--include-code') o.includeCode = true;
    else if (a === '--fail-unverified') o.failUnverified = true;
    else if (a === '--config') { o.config = argv[++i]; if (!o.config) throw new Error('--config にはファイル名が必要です'); }
    else if (a === '--disable') { const v = argv[++i]; if (!v) throw new Error('--disable にはルール名が必要です'); o.disable.push(...v.split(',')); }
    else if (a === '-' || !a.startsWith('-')) o.files.push(a);
    else throw new Error(`不明なオプション: ${a}`);
  }
  return o;
}

function main(argv, io) {
  const out = (io && io.out) || ((s) => process.stdout.write(s + '\n'));
  const err = (io && io.err) || ((s) => process.stderr.write(s + '\n'));
  let o;
  try { o = parseArgs(argv); } catch (e) { err(e.message); err('draftgate --help を見てください'); return 2; }
  if (o.help) { out(HELP); return 0; }
  if (o.version) { out(pkg.version); return 0; }
  if (!o.files.length) { err(HELP); return 2; }
  let config = {};
  if (o.config) {
    try { config = JSON.parse(fs.readFileSync(o.config, 'utf8')); } catch (e) { err(`設定を読めません: ${o.config} (${e.message})`); return 2; }
  }
  const unknown = o.disable.filter((r) => !RULES[r]);
  if (unknown.length) { err(`不明なルール: ${unknown.join(', ')}`); return 2; }

  const results = []; const errors = [];
  for (const f of o.files) {
    let text;
    try { text = f === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(f, 'utf8'); }
    catch (e) { errors.push({ file: f, error: e.message }); continue; }
    results.push(check(text, { file: f === '-' ? '<stdin>' : f, config, includeCode: o.includeCode, disable: o.disable }));
  }
  const all = results.flatMap((r) => r.findings);
  const counts = {};
  for (const f of all) counts[f.rule] = (counts[f.rule] || 0) + 1;
  const blocking = all.filter((f) => f.rule !== 'unverified' || o.failUnverified);

  if (o.json) {
    out(JSON.stringify({ version: pkg.version, summary: { files: results.length, findings: all.length, blocking: blocking.length, counts, errors }, findings: all }, null, 2));
  } else {
    for (const f of all) {
      const extra = f.rule === 'duplicate-line' ? `（初出 ${f.firstLine}行）` : f.note ? `（${f.note}）` : '';
      out(`${f.file}:${f.line}  ${f.label}  「${f.match}」${extra}`);
    }
    for (const e of errors) err(`読めません: ${e.file} (${e.error})`);
    const parts = Object.keys(counts).map((r) => `${RULES[r]} ${counts[r]}`).join('、') || 'なし';
    out(`-- ${results.length} ファイル、検出 ${blocking.length} 件${blocking.length !== all.length ? `（ほかに情報のみ ${all.length - blocking.length} 件）` : ''}。内訳: ${parts}（誤検出があります。最終判断は人が行ってください）`);
  }
  if (errors.length) return 2;
  return blocking.length ? 1 : 0;
}

module.exports = { main, parseArgs };
