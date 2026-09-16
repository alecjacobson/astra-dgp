"""Acquire requested tour as an MP4. Try yt-dlp, then archived original media.
The fallback is an archived Googlevideo video-only track for the same YouTube ID.
No source video is committed to Git. Existing usable files are preserved.
"""
from pathlib import Path
import subprocess,sys,requests,cv2,hashlib
P=Path(__file__).resolve().parents[1];dst=P/'references/tour.mp4';dst.parent.mkdir(exist_ok=True)
def valid(p):
 cap=cv2.VideoCapture(str(p));ok=cap.isOpened() and cap.get(cv2.CAP_PROP_FRAME_COUNT)>77000 and cap.get(cv2.CAP_PROP_FPS)>0;cap.release();return ok
if not dst.exists():
 r=subprocess.run([sys.executable,'-m','yt_dlp','--no-playlist','--socket-timeout','15','--retries','1','-f','bv[ext=mp4][height<=720]/b[ext=mp4]','-o',str(dst),'https://www.youtube.com/watch?v=GGaJsGu_5zA'])
 if r.returncode!=0 or not valid(dst):
  url='https://web.archive.org/web/2oe_/http://wayback-fakeurl.archive.org/yt/GGaJsGu_5zA'
  temp=dst.with_suffix('.download.mp4')
  with requests.get(url,stream=True,timeout=45) as response:
   response.raise_for_status();assert response.headers.get('content-type','').startswith('video/'),'Archive did not return video'
   with temp.open('wb') as f:
    for block in response.iter_content(1024*1024):f.write(block)
  assert valid(temp),'Archived video failed metadata validation';temp.replace(dst)
assert valid(dst),f'Existing {dst} does not contain the full expected tour'
print(dst, dst.stat().st_size,'bytes; sha256',hashlib.sha256(dst.read_bytes()).hexdigest())
