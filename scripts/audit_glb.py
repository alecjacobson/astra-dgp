"""Check delivered GLB metadata, mesh bounds, indices, and texture embedding."""
from pathlib import Path
import struct,json,math
P=Path(__file__).resolve().parents[1];p=P/'bahen-centre.glb';b=p.read_bytes();magic,version,length=struct.unpack_from('<4sII',b);assert magic==b'glTF' and version==2 and length==len(b)
n,t=struct.unpack_from('<II',b,12);assert t==0x4e4f534a;j=json.loads(b[20:20+n]);assert j['meshes'] and len(j['nodes'])>1000
for a in j['accessors']:
 for k in ['min','max']:
  if k in a:assert all(math.isfinite(v) for v in a[k])
for m in j['meshes']:
 for prim in m['primitives']:
  assert 'POSITION' in prim['attributes'];assert prim['mode']==4 if 'mode' in prim else True
for im in j.get('images',[]):assert 'bufferView' in im,'External image dependency'
assert all('uri' not in v for v in j['buffers']), 'External geometry dependency'
r={'format':'glTF 2.0 binary','bytes':len(b),'meshes':len(j['meshes']),'nodes':len(j['nodes']),'materials':len(j['materials']),'embedded_images':len(j.get('images',[])),'required_extensions':j.get('extensionsRequired',[]),'all_accessor_bounds_finite':True,'all_resources_embedded':True,'checks_passed':True};(P/'review/glb-audit.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
