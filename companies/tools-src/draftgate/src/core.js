'use strict';
// draftgate core: pure functions, no I/O, no network.

const RULES = {
  'unresolved-marker': '未解決マーカー',
  'todo': 'TODO系',
  'placeholder': '穴埋め',
  'ai-preamble': 'AI定型の前置き',
  'duplicate-line': '重複行',
  'unclosed-fence': '閉じていないコードブロック',
  'dummy-url': 'ダミーURL',
  'custom': '追加検出語',
  'unverified': '未確認の注記',
};

const LINE_RULES = [
  { rule: 'unresolved-marker', re: /【[^】\n]{0,120}(?:確認|要修正|要対応|未定|仮|公開しない)[^】\n]{0,120}】/g },
  { rule: 'unresolved-marker', re: /\[(?:要確認|要修正|要対応)\]/g },
  { rule: 'todo', re: /(?<![A-Za-z0-9_])(?:TODO|TBD|FIXME|XXX)(?![A-Za-z0-9_])/g },
  { rule: 'placeholder', re: /[○〇◯]{2,}|□{2,}|△{2,}|＿{3,}|_{4,}(?![A-Za-z0-9])/g },
  { rule: 'placeholder', re: /[\[［【（(]ここに[^\]］】）)\n]{0,40}[\]］】）)]/g },
  { rule: 'placeholder', re: /ここに[^。\n]{0,30}(?:を入れる|を入れ|を記載|を書く|を挿入|を追加|を貼る|を貼り付け)/g },
  { rule: 'placeholder', re: /\{\{[^}\n]{1,40}\}\}/g },
  { rule: 'placeholder', re: /lorem ipsum/gi },
  { rule: 'placeholder', re: /\[(?:Your|YOUR|insert|INSERT)[^\]\n]{0,30}\]/g },
  { rule: 'dummy-url', re: /(?<![a-z0-9.-])(?:https?:\/\/)?(?:[a-z0-9-]+\.)*(?:example\.(?:com|org|net)|yourdomain\.[a-z]+|your-domain\.[a-z]+)(?![a-z0-9-])/gi },
  { rule: 'dummy-url', re: /https?:\/\/(?:localhost|127\.0\.0\.1)(?::\d+)?[^\s)]*/g },
];

// AI preambles are only checked at line start (after optional quote/list marks).
const PREAMBLE_RES = [
  /^(?:承知(?:いた)?しました|かしこまりました|了解しました|もちろんです|もちろん、)/,
  /^以下(?:の|に|が|は)[^。\n]{0,30}(?:とおり|通り|示します|示しま|まとめ|下書き|案|です|ます)/,
  /^(?:こちらが|こちらに)[^。\n]{0,30}(?:下書き|案|記事|文面|ご用意)/,
  /^(?:Sure|Certainly|Of course)[,!.]/i,
  /^Here(?:'s| is| are)\b/i,
  /^As an AI\b/i,
  /^I(?:'ve| have) (?:drafted|written|prepared)\b/i,
];
const UNVERIFIED_RE = /未確認/g;

function maskInline(line) {
  // blank out inline code spans so their content is not matched
  return line.replace(/(`+)[^`\n]*?\1/g, (m) => ' '.repeat(m.length));
}

function parseFence(line) {
  const m = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(line);
  if (!m) return null;
  if (m[1][0] === '`' && m[2].includes('`')) return null;
  return { ch: m[1][0], len: m[1].length, rest: m[2].trim() };
}

function check(text, opts = {}) {
  const cfg = opts.config || {};
  const includeCode = Boolean(opts.includeCode || cfg.includeCode);
  const disabled = new Set([...(cfg.disable || []), ...(opts.disable || [])]);
  const file = opts.file || '<stdin>';
  const findings = [];
  const add = (line, rule, match, extra) => {
    if (disabled.has(rule)) return;
    findings.push(Object.assign({ file, line, rule, label: RULES[rule], match }, extra || {}));
  };

  const customWords = (cfg.markers || []).filter((s) => typeof s === 'string' && s);
  const customRes = (cfg.patterns || []).map((p) => {
    try { return { name: p.name || 'custom', re: new RegExp(p.regex, 'g') }; } catch (e) { return null; }
  }).filter(Boolean);

  const lines = text.replace(/^﻿/, '').split(/\r?\n/);
  let fence = null; // {ch,len,line}
  const seen = new Map();
  let inFront = lines[0] === '---';
  let inComment = false;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const n = i + 1;
    if (inFront) { if (i > 0 && raw === '---') inFront = false; continue; }

    const f = parseFence(raw);
    if (fence) {
      if (f && f.ch === fence.ch && f.len >= fence.len && f.rest === '') fence = null;
      else if (includeCode) scanLine(raw, n, true);
      continue;
    }
    if (f) { fence = { ch: f.ch, len: f.len, line: n }; continue; }

    if (/draftgate:\s*ignore/.test(raw)) continue;
    // HTML comments are skipped (often intentional notes), single or multi-line
    let work = raw;
    if (inComment) {
      const e = work.indexOf('-->');
      if (e < 0) continue;
      work = ' '.repeat(e + 3) + work.slice(e + 3); inComment = false;
    }
    work = work.replace(/<!--.*?-->/g, (m) => ' '.repeat(m.length));
    const o = work.indexOf('<!--');
    if (o >= 0) { work = work.slice(0, o); inComment = true; }
    scanLine(work, n, false, raw);
  }
  if (fence) add(fence.line, 'unclosed-fence', '```'.slice(0, 3), { note: `${fence.line}行目で開いたコードブロックが閉じていません` });

  function scanLine(line, n, inCode, rawLine) {
    const s = maskInline(line);
    const hit = new Set();
    const push = (rule, m, idx) => {
      const k = rule + ':' + idx + ':' + m;
      if (hit.has(k)) return; hit.add(k); add(n, rule, m);
    };
    for (const { rule, re } of LINE_RULES) {
      re.lastIndex = 0; let m;
      while ((m = re.exec(s))) { push(rule, m[0], m.index); if (m[0] === '') re.lastIndex++; }
    }
    const body = s.replace(/^[\s>*+\-]+(?:\d+[.)]\s+)?/, '');
    if (!inCode) for (const re of PREAMBLE_RES) { const m = re.exec(body); if (m) { add(n, 'ai-preamble', body.slice(0, 30)); break; } }
    for (const w of customWords) { let p = 0, q; while ((q = s.indexOf(w, p)) >= 0) { push('custom', w, q); p = q + w.length; } }
    for (const { name, re } of customRes) { re.lastIndex = 0; let m; while ((m = re.exec(s))) { push('custom', m[0], m.index); if (m[0] === '') re.lastIndex++; } }
    UNVERIFIED_RE.lastIndex = 0; let um;
    while ((um = UNVERIFIED_RE.exec(s))) add(n, 'unverified', um[0]);
    // duplicates: meaningful lines only (not code, not tables/rules/short)
    if (!inCode) {
      const t = s.trim();
      if (t.length >= 8 && !/^[|\-=*_#\s>]+$/.test(t) && !/^\|/.test(t)) {
        if (seen.has(t)) add(n, 'duplicate-line', t.slice(0, 40), { firstLine: seen.get(t) });
        else seen.set(t, n);
      }
    }
  }

  const counts = {};
  for (const f of findings) counts[f.rule] = (counts[f.rule] || 0) + 1;
  findings.sort((a, b) => a.line - b.line);
  return { file, findings, counts };
}

module.exports = { check, RULES };
