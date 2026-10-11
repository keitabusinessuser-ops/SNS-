#!/usr/bin/env bash
# GitHubの公開指標を保存する（トラフィックは14日で消えるため、毎サイクル保存）。認証情報は使わない。
# 使い方: scripts/collect-metrics.sh  → companies/metrics/github-YYYY-MM-DD.json
set -u
REPO="hitori-to-ai/hitori-to-ai.github.io"
OUT="companies/metrics/github-$(TZ=Asia/Tokyo date +%F).json"
mkdir -p companies/metrics
get() { curl -s -m 20 "https://api.github.com/repos/$REPO$1"; }
python3 - "$OUT" <<PY
import json,subprocess,sys,datetime
repo="$REPO"
def g(p):
    r=subprocess.run(["curl","-s","-m","20","https://api.github.com/repos/"+repo+p],capture_output=True,text=True).stdout
    try: return json.loads(r)
    except Exception: return {"error":r[:200]}
base=g("")
out={"collected_at":datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
 "repo":repo,
 "stars":base.get("stargazers_count"),"forks":base.get("forks_count"),"watchers":base.get("subscribers_count"),"open_issues":base.get("open_issues_count"),"private":base.get("private"),
 "views":g("/traffic/views"),"clones":g("/traffic/clones"),"referrers":g("/traffic/popular/referrers"),"paths":g("/traffic/popular/paths")}
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("saved",sys.argv[1],"stars",out["stars"],"views",out["views"].get("count"),"clones",out["clones"].get("count"))
PY
