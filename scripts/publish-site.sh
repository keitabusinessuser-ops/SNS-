#!/usr/bin/env bash
# サイトの公開スクリプト（既定は点検のみ。公開しない）。
#   scripts/publish-site.sh [--with-tools]            点検だけ実行（公開しない）
#   PUBLISH_OK=1 scripts/publish-site.sh --push ...    Keitaの「公開OK」が出た後だけ。公開用リポジトリのmainへ通常のpush（強制pushはしない）
# 点検: 名前・メールの漏れ、JS構文、U+2028/2029、外部URL、ツールの自己テスト（ヘッドレスChromium）
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/companies/site"
OUT="${TMPDIR:-/tmp}/site-out"
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
PUB="${PUB_REPO_DIR:-/home/user/hitori-site}"
WITH_TOOLS=0; PUSH=0
for a in "$@"; do case "$a" in --with-tools) WITH_TOOLS=1;; --push) PUSH=1;; esac; done
fail=0; ng(){ echo "NG: $*"; fail=1; }; ok(){ echo "OK: $*"; }

rm -rf "$OUT"; mkdir -p "$OUT"
cp "$SRC/draft-v3/index.html" "$SRC/draft-v3/feed.xml" "$OUT/"
cp "$PUB/README.md" "$OUT/" 2>/dev/null || true
if [ $WITH_TOOLS = 1 ]; then
  for t in moji-count wareki; do mkdir -p "$OUT/e-b/$t"; cp "$SRC/e-b/$t/index.html" "$OUT/e-b/$t/"; done
fi
echo "--- 公開予定のファイル"; (cd "$OUT" && find . -type f | sort | while read f; do printf "%8s  %s\n" "$(wc -c <"$f")" "$f"; done)

echo "--- 点検"
if grep -rniE "keita|keitabusiness|gmail|@[a-z0-9-]+\.[a-z]{2,}" "$OUT" | grep -v "@media" | grep -q .; then ng "名前・メールらしき文字列が見つかった"; grep -rniE "keita|keitabusiness|gmail|@[a-z0-9-]+\.[a-z]{2,}" "$OUT" | grep -v "@media" | head -3; else ok "名前・メールの文字列なし"; fi
python3 - "$OUT" <<'PY' || fail=1
import sys,re,subprocess,pathlib,tempfile,os
bad=0
for p in pathlib.Path(sys.argv[1]).rglob('*.html'):
    s=p.read_text(encoding='utf-8')
    if ' ' in s or ' ' in s: print('NG: 生のU+2028/2029',p); bad=1
    for m in re.finditer(r'<script>(.*?)</script>',s,re.S):
        f=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8'); f.write(m.group(1)); f.close()
        r=subprocess.run(['node','--check',f.name],capture_output=True,text=True); os.unlink(f.name)
        if r.returncode: print('NG: JS構文エラー',p,r.stderr[:200]); bad=1
        else: print('OK: JS構文',p.relative_to(sys.argv[1]))
    ext=set(re.findall(r'(?:src|href)="(https?://[^"]+)"',s))
    allowed=('https://github.com/hitori-to-ai/','https://hitori-to-ai.github.io/')
    for u in ext:
        if not u.startswith(allowed): print('NG: 外部URL',p,u); bad=1
    if re.search(r'<script[^>]+src=',s): print('NG: 外部script',p); bad=1
sys.exit(bad)
PY
# ツールの自己テスト
if [ $WITH_TOOLS = 1 ] && [ -x "$CHROME" ]; then
  for t in moji-count wareki; do
    obj=$([ $t = moji-count ] && echo mojiCount || echo wareki)
    T="$OUT/_t-$t.html"
    python3 - "$OUT/e-b/$t/index.html" "$T" "$obj" <<'PY'
import sys
s=open(sys.argv[1],encoding='utf-8').read()
inj="<script>setTimeout(function(){var o={};try{o.r=JSON.stringify(window.%s.selfTest())}catch(e){o.e=String(e)}var p=document.createElement('pre');p.id='res';p.textContent='RESULT:'+JSON.stringify(o);document.body.appendChild(p)},800)</script></body>"%sys.argv[3]
open(sys.argv[2],'w',encoding='utf-8').write(s.replace('</body>',inj))
PY
    res=$("$CHROME" --headless --no-sandbox --disable-gpu --virtual-time-budget=5000 --dump-dom "file://$T" 2>/dev/null | grep -o 'id="res">[^<]*' | head -c 400)
    echo "$res" | grep -q '"ok\\":true' && ok "自己テスト $t: $res" || ng "自己テスト $t: $res"
    rm -f "$T"
  done
fi
[ $fail = 0 ] && echo "=== 点検: すべてOK" || echo "=== 点検: NGあり（公開しない）"

if [ $PUSH = 1 ]; then
  [ "${PUBLISH_OK:-0}" = 1 ] || { echo "公開しません: PUBLISH_OK=1 が無い（Keitaの公開OKが必要）"; exit 2; }
  [ $fail = 0 ] || { echo "公開しません: 点検NG"; exit 3; }
  cd "$PUB" || exit 4
  git fetch -q origin main && git merge -q --ff-only origin/main || { echo "ff-onlyで取り込めない。強制pushはしない"; exit 5; }
  rsync -a --delete --exclude .git --exclude README.md "$OUT/" "$PUB/" 2>/dev/null || cp -r "$OUT/." "$PUB/"
  rm -f "$PUB"/_t-*.html
  git add -A && git -c user.name="hitori-to-ai" -c user.email="hitori-to-ai@users.noreply.github.com" commit -q -m "サイトを更新" && git push -q origin main && echo "公開（push）しました" || echo "変更なし、またはpush失敗"
else
  echo "（点検のみ。公開していません）"
fi
exit $fail
