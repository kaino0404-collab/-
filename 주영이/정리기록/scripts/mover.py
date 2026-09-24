import json, os, shutil, sys
S=r"./work"
SRC="E:/주영이/요딩이"; DST="E:/주영이/주영이"
idx=json.load(open(S+"/sheet_index.json",encoding='utf-8'))
prefix=sys.argv[1]
moved=kept=0; log=open(S+"/moved_log.txt","a",encoding='utf-8')
seen=set()
for line in open(S+"/decisions.txt",encoding='utf-8'):
    line=line.strip()
    if not line.startswith(prefix): continue
    sid,sel=line.split(":"); seen.add(sid)
    picks={int(x) for x in sel.split(",") if x}
    for i,name in enumerate(idx[sid],1):
        if i not in picks: kept+=1; continue
        src=os.path.join(SRC,name)
        if not os.path.exists(src): print("MISSING",name); continue
        dst=os.path.join(DST,name)
        if os.path.exists(dst):
            b,e=os.path.splitext(name); dst=os.path.join(DST,b+"_dup2"+e); print("RENAMED",name)
            if os.path.exists(dst): print("SKIP collision",name); continue
        shutil.move(src,dst); log.write(name+"\n"); moved+=1
missing=[s for s in idx if s.startswith(prefix) and s not in seen]
print("moved",moved,"kept",kept,"sheets without decision:",missing)
