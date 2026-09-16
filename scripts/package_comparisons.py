"""Publish source/render pairs from a completed, named Blender render revision."""
from pathlib import Path
import argparse,subprocess,shutil,json
P=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('revision');a=ap.parse_args()
rows=[('0030','0030.jpg','00:30'),('0330','0210.jpg','03:30'),('0630','0390.jpg','06:30'),('0730','0450.jpg','07:30'),('1430','0870.jpg','14:30'),('1452',None,'14:52')]
manifest=[]
for key,source,time in rows:
 src=P/'references/partial'/source if source else P/'references/decoded/00892.00s.jpg'
 render=P/'renders'/f'{a.revision}-video_{key}.png';assert render.exists(),render
 final=P/'renders'/f'final-video_{key}.png';shutil.copy2(render,final)
 out=P/'renders'/f'comparison-{key}.png'
 subprocess.run(['python',str(P/'scripts/compare_frames.py'),str(src),str(final),str(out),'--time',time,'--revision',a.revision+' — modeled architecture','--note','Source: U of T APS162 tour, GGaJsGu_5zA. Dimensions/layout inferred; presenter omitted.'],check=True)
 manifest.append({'timestamp':time,'source':str(src.relative_to(P)),'render':str(final.relative_to(P)),'comparison':str(out.relative_to(P)),'revision':a.revision})
for name in ['exterior','atrium_east','atrium_west','audit_lobby_offset','video_1452_offset']:
 src=P/'renders'/f'{a.revision}-{name}.png'
 if src.exists():shutil.copy2(src,P/'renders'/f'final-{name}.png')
shutil.copy2(P/'renders/final-video_1430.png',P/'renders/final-landing.png')
(P/'review/comparison-manifest.json').write_text(json.dumps(manifest,indent=2))
