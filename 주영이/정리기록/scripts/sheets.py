import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps
from concurrent.futures import ThreadPoolExecutor
S=r"./work"
SRC="E:/주영이/요딩이"
CELL=360
try: font=ImageFont.truetype("arial.ttf",40)
except: font=ImageFont.load_default()
os.makedirs(S+"/sheets",exist_ok=True); os.makedirs(S+"/vframes",exist_ok=True)

def thumb_img(name):
    try:
        im=Image.open(os.path.join(SRC,name)); im.draft('RGB',(CELL*2,CELL*2))
        im=ImageOps.exif_transpose(im).convert('RGB'); im.thumbnail((CELL,CELL)); return im
    except Exception as e:
        return None

def video_frames(name):
    p=os.path.join(SRC,name)
    try:
        dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
    except: dur=None
    out=[]
    for k,frac in enumerate((0.2,0.5,0.8)):
        o=f"{S}/vframes/{name}_{k}.jpg"
        t=str(dur*frac) if dur else str(k)
        subprocess.run(['ffmpeg','-y','-v','error','-ss',t,'-i',p,'-frames:v','1','-vf',f'scale={CELL}:{CELL}:force_original_aspect_ratio=decrease',o],capture_output=True)
        try: out.append(Image.open(o).convert('RGB'))
        except: out.append(None)
    return out

def draw_sheet(cells, labels, path, cols=3):
    rows=(len(cells)+cols-1)//cols
    sheet=Image.new('RGB',(cols*CELL,rows*CELL),(40,40,40)); d=ImageDraw.Draw(sheet)
    for i,(im,lab) in enumerate(zip(cells,labels)):
        x,y=(i%cols)*CELL,(i//cols)*CELL
        if im: sheet.paste(im,(x+(CELL-im.width)//2,y+(CELL-im.height)//2))
        else: d.text((x+20,y+150),"ERR",fill=(255,0,0),font=font)
        d.rectangle([x,y,x+len(lab)*24+10,y+46],fill=(255,255,0)); d.text((x+5,y+2),lab,fill=(0,0,0),font=font)
    sheet.save(path,quality=80)

index={}
imgs=[l for l in open(S+"/todo_images.txt",encoding='utf-8').read().split('\n') if l]
with ThreadPoolExecutor(8) as ex: thumbs=list(ex.map(thumb_img,imgs))
for s in range(0,len(imgs),9):
    names=imgs[s:s+9]; sid=f"I{s//9:03d}"
    draw_sheet(thumbs[s:s+9],[str(i+1) for i in range(len(names))],f"{S}/sheets/{sid}.jpg")
    index[sid]=names
vids=[l for l in open(S+"/todo_videos.txt",encoding='utf-8').read().split('\n') if l]
with ThreadPoolExecutor(6) as ex: vfr=list(ex.map(video_frames,vids))
for s in range(0,len(vids),3):
    names=vids[s:s+3]; sid=f"V{s//3:03d}"; cells=[];labs=[]
    for j,n in enumerate(names):
        cells+=vfr[s+j]; labs+=[f"{j+1}{c}" for c in "abc"]
    draw_sheet(cells,labs,f"{S}/sheets/{sid}.jpg")
    index[sid]=names
json.dump(index,open(S+"/sheet_index.json","w",encoding='utf-8'),ensure_ascii=False,indent=0)
print("sheets",len(index),"img errors",sum(t is None for t in thumbs),"vid frame errors",sum(f is None for v in vfr for f in v))
