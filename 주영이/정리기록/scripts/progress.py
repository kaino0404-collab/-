import json,glob,os,re
S=r"./work"
decided=set()
for f in sorted(glob.glob(r"./work_prev/subagents/agent-*.jsonl")):
  reads=[]; mv_ids={}; last_done=0
  for line in open(f,encoding='utf-8'):
    try:d=json.loads(line)
    except:continue
    cs=d.get('message',{}).get('content',[])
    if not isinstance(cs,list): continue
    for c in cs:
      if not isinstance(c,dict):continue
      if c.get('type')=='tool_use':
        i=c['input']
        if c['name']=='Read':
          reads.append(os.path.basename(i.get('file_path','').replace(chr(92),'/')))
        elif c['name']=='Bash' and re.search(r'\bmv\b|while IFS',i.get('command','')):
          mv_ids[c['id']]=len(reads)
      if c.get('type')=='tool_result' and c.get('tool_use_id') in mv_ids:
        last_done=max(last_done,mv_ids[c['tool_use_id']])
  imgs=[r for r in reads if not r.startswith('chunk')]
  dec=[r for r in reads[:last_done] if not r.startswith('chunk')]
  decided|=set(dec)
  print(os.path.basename(f)[:16],'read',len(imgs),'decided',len(dec))
cur=set(os.listdir('E:/주영이/요딩이'))
rem_img=sorted(x for x in cur if x.lower().endswith(('.jpg','.jpeg','.png')) and x not in decided)
rem_vid=sorted(x for x in cur if x.lower().endswith(('.mp4','.mov')))
print('decided',len(decided),'decided-not-baby still here',len([x for x in decided if x in cur]))
print('images to classify',len(rem_img),'videos',len(rem_vid))
open(S+'/todo_images.txt','w',encoding='utf-8').write('\n'.join(rem_img))
open(S+'/todo_videos.txt','w',encoding='utf-8').write('\n'.join(rem_vid))
