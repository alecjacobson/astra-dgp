"""Side-by-side source/render evidence, preserving each image's full frame."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('render');p.add_argument('output');p.add_argument('--time',default='14:52');p.add_argument('--revision',default='Video revision');p.add_argument('--note',default='Camera and dimensions inferred. Presenter omitted from modeled architecture.');a=p.parse_args()
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,24);small=ImageFont.truetype(font,18)
out=Image.new('RGB',(1920,660),'#17252a');d=ImageDraw.Draw(out)
for i,(path,label) in enumerate([(a.source,f'SOURCE VIDEO  {a.time}  |  GGaJsGu_5zA'),(a.render,a.revision)]):
 im=Image.open(path).convert('RGB');im.thumbnail((950,535));out.paste(im,(i*960+(960-im.width)//2,62+(535-im.height)//2));d.text((i*960+18,18),label,font=f,fill='white')
d.text((18,610),a.note,font=small,fill='#d5e6e5');Path(a.output).parent.mkdir(exist_ok=True,parents=True);out.save(a.output)
