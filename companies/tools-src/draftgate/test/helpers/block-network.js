'use strict';
// テスト専用。--require で読み込み、外部通信系モジュールの require を失敗させる。
// net/http/https/http2/tls/dns/dgram は全員禁止。
// child_process は src/ と bin/ からの require だけ禁止（テスト側が CLI を起動するのに使うため）。
const Module = require('node:module');
const path = require('node:path');
const root = path.resolve(__dirname, '..', '..');
const srcDirs = [path.join(root, 'src') + path.sep, path.join(root, 'bin') + path.sep];
const ALWAYS = new Set(['net', 'http', 'https', 'http2', 'tls', 'dns', 'dgram']);
const SRC_ONLY = new Set(['child_process', 'cluster', 'worker_threads']);
const origLoad = Module._load;
Module._load = function (request, parent, isMain) {
  const name = String(request).replace(/^node:/, '').split('/')[0];
  const from = parent && parent.filename ? parent.filename : '';
  if (ALWAYS.has(name) && !from.startsWith('node:') && from) {
    throw new Error(`外部通信モジュールの require を検出: ${request} (from ${from})`);
  }
  if (SRC_ONLY.has(name) && srcDirs.some((d) => from.startsWith(d))) {
    throw new Error(`外部通信/子プロセス系モジュールの require を検出: ${request} (from ${from})`);
  }
  return origLoad.apply(this, arguments);
};
process.env.DRAFTGATE_OFFLINE_GUARD = '1';
