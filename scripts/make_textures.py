"""Deterministic procedural PBR color tiles for portable glTF material support.
These are authored surface approximations, not photographic textures.
"""
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'textures';P.mkdir(exist_ok=True)
rng=np.random.default_rng(12);N=1024
for name,col in [('cream-brick',(205,198,175)),('heritage-brick',(179,166,121)),('red-brick',(153,91,62))]:
 im=Image.new('RGB',(N,N),(142,138,119));d=ImageDraw.Draw(im)
 # 8 bricks by 16 rows in a 2.08 x 1.36 metre tile.
 for j in range(16):
  for i in range(-1,9):
   x=i*128+(64 if j%2 else 0);y=j*64;v=float(rng.uniform(.88,1.08));c=tuple(int(min(255,a*v)) for a in col);d.rectangle((x+2,y+2,x+125,y+61),fill=c)
 a=np.array(im).astype(float);a+=rng.normal(0,1.8,(N,N,1));Image.fromarray(np.uint8(np.clip(a,0,255))).save(P/f'{name}.jpg',quality=94)
for name,col,std in [('concrete',(189,187,176),2.5),('terrazzo',(166,173,170),15),('limestone',(190,185,163),2),('wood',(85,57,40),4)]:
 a=np.ones((N,N,3))*np.array(col);noise=rng.normal(0,std,(N,N,1))
 if name=='wood':noise=np.repeat(rng.normal(0,std,(N,1,1)),N,axis=1)+rng.normal(0,1,(N,N,1))
 a+=noise
 if name=='terrazzo':
  for k in range(26000):
   x,y=rng.integers(0,N,2);r=int(rng.integers(1,3));a[y:y+r,x:x+r]=rng.choice([72,103,216,235])
 Image.fromarray(np.uint8(np.clip(a,0,255))).save(P/f'{name}.jpg',quality=94)
