"""Decode actual timestamped source frames for the render/reference loop.
Usage: python scripts/extract_video_frames.py references/tour.mp4
Produces local-only source frames, contact sheets and frame metadata. No network
or thumbnail substitution. Requested 14:52 frame must exist and decode correctly.
"""
import argparse,json,hashlib,math
from pathlib import Path
import cv2
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('--interval',type=float,default=20);a=p.parse_args()
assert a.video.is_file(),f'Missing video file: {a.video}'
cap=cv2.VideoCapture(str(a.video));assert cap.isOpened(),'Source video cannot be decoded'
fps=cap.get(cv2.CAP_PROP_FPS);count=cap.get(cv2.CAP_PROP_FRAME_COUNT);assert fps>0 and count>0
seconds=count/fps;assert seconds>892,'Source does not contain requested 14:52 timestamp'
out=P/'references/decoded';out.mkdir(exist_ok=True)
times=sorted(set([float(t) for t in range(0,math.floor(seconds),max(1,round(a.interval)))]+[872,882,892,902,912]))
frames=[]
for t in times:
 if t>=seconds:continue
 requested=round(t*fps);cap.set(cv2.CAP_PROP_POS_FRAMES,requested);ok,bgr=cap.read();assert ok,f'Cannot decode {t}s'
 actual=int(cap.get(cv2.CAP_PROP_POS_FRAMES))-1;assert abs(actual-requested)<=1
 image=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));filename=f'{t:08.2f}s.jpg';image.save(out/filename,quality=96)
 frames.append({'file':str((out/filename).relative_to(P)),'requested_seconds':t,'decoded_frame_index':actual,'decoded_seconds':actual/fps,'width':image.width,'height':image.height,'observation_status':'unreviewed'})
cap.release()
for page in range(math.ceil(len(frames)/24)):
 subset=frames[page*24:(page+1)*24];sheet=Image.new('RGB',(1600,math.ceil(len(subset)/4)*260),'#eee');d=ImageDraw.Draw(sheet)
 for i,f in enumerate(subset):
  im=Image.open(P/f['file']);im.thumbnail((390,225));x=(i%4)*400;y=(i//4)*260;sheet.paste(im,(x,y+28));t=f['requested_seconds'];d.text((x+6,y+6),f'{int(t//60):02d}:{t%60:05.2f}  /  frame {f["decoded_frame_index"]}',fill='#172c20')
 sheet.save(out/f'contact-{page+1:02d}.jpg',quality=93)
report={'video_file':str(a.video),'sha256':hashlib.sha256(a.video.read_bytes()).hexdigest(),'source_url':'https://www.youtube.com/watch?v=GGaJsGu_5zA','fps':fps,'frame_count':count,'duration_seconds':seconds,'frames':frames}
(out/'frame-catalog.json').write_text(json.dumps(report,indent=2));print(f'Decoded {len(frames)} frames from {seconds:.2f}s source; exact 14:52 included.')
