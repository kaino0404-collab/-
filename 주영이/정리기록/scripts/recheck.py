import json, subprocess, os
from PIL import Image, ImageDraw, ImageFont
S=r"./work"
idx=json.load(open(S+"/sheet_index.json",encoding='utf-8'))
font=ImageFont.truetype("arial.ttf",32)
for line in open(S+"/recheck.txt"):
    sid,n=line.strip().split(":"); name=idx[sid][int(n)-1]; p="E:/주영이/요딩이/"+name
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
    cells=[]
    for k in range(12):
        o=f"{S}/vframes/re_{k}.jpg"
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(dur*(k+0.5)/12),'-i',p,'-frames:v','1','-vf','scale=300:300:force_original_aspect_ratio=decrease',o])
        cells.append(Image.open(o).convert('RGB'))
    sh=Image.new('RGB',(1200,900),(40,40,40)); d=ImageDraw.Draw(sh)
    for i,c in enumerate(cells): sh.paste(c,((i%4)*300,(i//4)*300))
    d.text((5,5),f"{sid}-{n} {dur:.0f}s",fill=(255,255,0),font=font)
    sh.save(f"{S}/sheets/R_{sid}_{n}.jpg"); print(sid,n,name,round(dur))
