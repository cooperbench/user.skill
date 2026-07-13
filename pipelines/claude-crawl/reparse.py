import json, os, sys
sys.path.insert(0,"/data/swesimbench-v2-mini"); import parse_claude as P
BASE="/data/claude-crawl"; CL=f"{BASE}/clones"; CO=f"{BASE}/corpus"
import shutil; shutil.rmtree(CO,ignore_errors=True); os.makedirs(CO)
owners={}
clones=sorted(os.listdir(CL))
for i,cd in enumerate(clones):
    d=os.path.join(CL,cd)
    if not os.path.isdir(d): continue
    owner=cd.split("__")[0]
    try: sess=P.parse_agent_clone(d)
    except Exception as e: print("ERR",cd,str(e)[:50]); continue
    if not sess: continue
    out=open(os.path.join(CO,owner+".jsonl"),"a")
    for sid,ts,turns,proj,harness in sess:
        nu=sum(1 for t in turns if t["role"]=="user")
        if nu==0: continue
        # repo = owner/name from clone dir
        repo=cd.replace("__","/",1)
        out.write(json.dumps({"user":"gh:"+owner,"repo":repo,"session_id":f"{repo}|{sid}",
            "start_time":ts,"harness":harness,"n_user_turns":nu,"turns":turns},ensure_ascii=False)+"\n")
    out.close()
    if (i+1)%40==0: print(f"{i+1}/{len(clones)} clones reparsed",flush=True)
print("reparse done:",len(os.listdir(CO)),"owner corpus files")
