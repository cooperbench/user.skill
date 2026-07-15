import json, os, sys, re
sys.path.insert(0,"/data/swesimbench-v2-mini"); import parse_claude as P
CO="/data/claude-crawl/corpus"
# (base_dir, owner_is_full_dirname)
BASES=[("/data/round2-github/clones",True),("/data/round3-github/clones",True),
       ("/data/round5-github/work",False),("/data/committed-transcripts/harvest",False)]
written=0
for base,dir_is_owner in BASES:
    if not os.path.isdir(base): continue
    for cd in sorted(os.listdir(base)):
        d=os.path.join(base,cd)
        if not os.path.isdir(d): continue
        owner = cd if dir_is_owner else re.split(r'__|_',cd)[0]
        try: sess=P.parse_agent_clone(d)
        except Exception as e: print("ERR",cd,str(e)[:40]); continue
        if not sess: continue
        out=open(os.path.join(CO,owner+".jsonl"),"a")
        for sid,ts,turns,proj,harness in sess:
            nu=sum(1 for t in turns if t["role"]=="user")
            if nu==0: continue
            out.write(json.dumps({"user":"gh:"+owner,"repo":cd,"session_id":f"reparse|{cd}|{sid}",
                "start_time":ts,"harness":harness,"n_user_turns":nu,"turns":turns},ensure_ascii=False)+"\n")
            written+=1
        out.close()
print("reparse_clones wrote",written,"full-trace sessions")
