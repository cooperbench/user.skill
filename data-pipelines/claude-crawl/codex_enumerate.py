import json, subprocess, os, time
BASE="/data/claude-crawl"; REG=f"{BASE}/meta/registry.json"; DONE=f"{BASE}/meta/enum_done.json"
registry=set(json.load(open(REG))); done=set(json.load(open(DONE))) if os.path.exists(DONE) else set()
SIZE=["0..1999","2000..7999","8000..31999","32000..127999","128000..511999","512000..2097151",">2097151"]
PATHQ=['path:.codex/sessions extension:jsonl','filename:rollout- extension:jsonl',
       '"response_item" "session_meta" extension:jsonl']
def sc(q):
    repos=set()
    for page in range(1,11):
        try:
            r=subprocess.run(["gh","api","-X","GET","search/code","-f",f"q={q}","-f","per_page=100","-f",f"page={page}",
                              "--jq",".items[].repository.full_name"],capture_output=True,timeout=40)
            time.sleep(6.5)
            if r.returncode!=0:
                if "rate limit" in r.stderr.decode().lower(): time.sleep(60); continue
                break
            names=[x for x in r.stdout.decode().split("\n") if x]
            if not names: break
            repos.update(names)
            if len(names)<100: break
        except Exception: break
    return repos
def save(): json.dump(sorted(registry),open(REG,"w")); json.dump(sorted(done),open(DONE,"w"))
for pq in PATHQ:
    for sz in SIZE:
        key=f"codex::{pq}::size:{sz}"
        if key in done: continue
        b=len(registry); registry|=sc(f"{pq} size:{sz}"); done.add(key)
        print(f"[{len(registry)} (+{len(registry)-b})] {key}",flush=True); save()
for name in ["codex-sessions","codex-backup","codex-history",".codex","codex-rollouts","codex-cli-sessions"]:
    key=f"repo::{name}"
    if key in done: continue
    b=len(registry)
    try:
        r=subprocess.run(["gh","api","-X","GET","search/repositories","-f",f"q={name}","-f","per_page=100","--jq",".items[].full_name"],capture_output=True,timeout=40)
        time.sleep(2.5); registry|=set(x for x in r.stdout.decode().split("\n") if x)
    except Exception: pass
    done.add(key); print(f"[{len(registry)} (+{len(registry)-b})] {key}",flush=True); save()
save(); print(f"DONE codex enum. registry {len(registry)}")
