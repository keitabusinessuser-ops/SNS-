'use strict';
// 外部通信系 require を無効化した状態で全テストを走らせる。 使い方: node test/run-offline.js
// NODE_OPTIONS 経由なので、テストが起動する CLI の子プロセスにもガードが効く。
const { spawnSync } = require('node:child_process');
const path = require('node:path');
const guard = path.join(__dirname, 'helpers', 'block-network.js');
const r = spawnSync(process.execPath, ['--test'], {
  cwd: path.join(__dirname, '..'),
  stdio: 'inherit',
  env: { ...process.env, NODE_OPTIONS: `--require=${guard}` },
});
process.exit(r.status === null ? 1 : r.status);
