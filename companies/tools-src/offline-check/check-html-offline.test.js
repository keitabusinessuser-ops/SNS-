'use strict';
const test = require('node:test');
const assert = require('node:assert');
const { check } = require('./check-html-offline');

test('検査自体の動作: 問題のあるHTMLを検出する', () => {
  assert.deepStrictEqual(check('<p>a</p><script>var x=1;</script>'), []);
  assert.ok(check('<script>fetch("a")</script>').length);
  assert.ok(check('<script>navigator.sendBeacon("a")</script>').length);
  assert.ok(check('<script>import("./a.js")</script>').length);
  assert.ok(check('<script>new WebSocket("wss://a")</script>').length);
  assert.ok(check('<script>var r=new XMLHttpRequest()</script>').length);
  assert.ok(check('<img src="https://a/b.png">').length);
  assert.deepStrictEqual(check('<a href="https://a/b">x</a>'), []); // クリック時のみ移動するリンクは通信ではない
  assert.ok(check('<link rel="stylesheet" href="https://a/b.css">').length);
  assert.ok(check('<form action="https://a/b"></form>').length);
  assert.ok(check('<script src="a.js"></script>').length);
  assert.deepStrictEqual(check('<a href="../../">top</a><a href="#x">x</a><a href="mailto:a@b">m</a>'), []);
});
