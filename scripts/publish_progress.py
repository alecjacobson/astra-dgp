"""Publish a NEW model render every 600 s during this modeling session.
Only explicit progress paths are staged; never publishes reference media.
"""
import time,subprocess,shutil,json
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parents[1]; seen=set(); start=time.time()
while not (P/'.stop-publisher').exists():
 if time.time()-start>=600:
  candidates=sorted((P/'renders').glob('*.png'),key=lambda p:p.stat().st_mtime)
  candidates=[p for p in candidates if (str(p),p.stat().st_mtime) not in seen and time.time()-p.stat().st_mtime>3]
  if candidates:
   src=candidates[-1];stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S');dest=P/'progress'/f'{stamp}.png';dest.parent.mkdir(exist_ok=True);shutil.copy2(src,dest);shutil.copy2(src,P/'progress/latest.png');seen.add((str(src),src.stat().st_mtime))
   with (P/'progress/history.md').open('a') as f:f.write(f'\n- {stamp} UTC — [{src.name}]({stamp}.png)\n')
   subprocess.run(['git','add','progress'],cwd=P,check=True);subprocess.run(['git','commit','-m',f'Progress render {stamp}'],cwd=P,check=True);
   for attempt in range(6):
    if subprocess.run(['git','push'],cwd=P).returncode==0:break
    time.sleep(5)
   else:raise RuntimeError('Progress push failed after retries')
   print('PUBLISHED',dest,flush=True);start=time.time()
 time.sleep(5)
