import json, subprocess, os, time
BASE="/data/claude-crawl"; REG=f"{BASE}/meta/registry.json"; DONE=f"{BASE}/meta/enum_done.json"
registry=set(json.load(open(REG))); done=set(json.load(open(DONE))) if os.path.exists(DONE) else set()
SIZE=["0..3999","4000..15999","16000..63999","64000..255999","256000..1048575",">1048575"]
Q=['"parentUuid" "isSidechain" extension:jsonl','"parentUuid" "toolUseResult" extension:jsonl']
def sc(q):
    r=set()
    for page in range(1,11):
        try:
            p=subprocess.run(["gh","api","-X","GET","search/code","-f",f"q={q}","-f","per_page=100","-f",f"page={page}","--jq",".items[].repository.full_name"],capture_output=True,timeout=40)
            time.sleep(6.5)
            if p.returncode!=0:
                if "rate limit" in p.stderr.decode().lower(): time.sleep(60); continue
                break
            n=[x for x in p.stdout.decode().split("\n") if x]
            if not n: break
            r.update(n)
            if len(n)<100: break
        except: break
    return r
for q in Q:
    for sz in SIZE:
        k=f"content::{q}::size:{sz}"
        if k in done: continue
        b=len(registry); registry|=sc(f"{q} size:{sz}"); done.add(k)
        print(f"[{len(registry)} (+{len(registry)-b})] {k}",flush=True)
        json.dump(sorted(registry),open(REG,"w")); json.dump(sorted(done),open(DONE,"w"))
print("DONE content enum. registry",len(registry))
