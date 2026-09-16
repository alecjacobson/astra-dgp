"""Validate the fully embedded, lighting-baked interactive deliverable."""
from pathlib import Path
import json,struct,math,hashlib
P=Path(__file__).resolve().parents[1];f=P/'viewer/bahen-lit.glb';raw=f.read_bytes()
magic,version,size=struct.unpack_from('<4sII',raw);assert magic==b'glTF' and version==2 and size==len(raw)
n,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a;j=json.loads(raw[20:20+n]);identity=j['asset']['extras']
native=json.loads((P/'review/native-scene-check.json').read_text());editable=json.loads((P/'review/glb-audit.json').read_text())
assert identity['source_revision']==native['saved_revision']
assert identity['source_components']==editable['meshes']
assert identity['source_blend_sha256']==hashlib.sha256((P/'bahen-centre.blend').read_bytes()).hexdigest()
assert all('uri' not in x for x in j['buffers'])
assert all('bufferView' in x for x in j['images'])
for a in j['accessors']:
 for key in ['min','max']:
  assert all(math.isfinite(v) for v in a.get(key,[]))
baked=[m for m in j['materials'] if m.get('name','').startswith('Baked / ')]
assert len(baked)>50
for m in baked:
 assert 'KHR_materials_unlit' in m['extensions']
 assert 'baseColorTexture' in m['pbrMetallicRoughness']
for name in ['Source monitor','Source notices','Source lobby notices','Source recycling labels']:
 m=next(m for m in j['materials'] if m.get('name')==name);assert 'baseColorTexture' in m['pbrMetallicRoughness']
seat=next(m for m in j['materials'] if m.get('name')=='Theatre seat')
assert 'KHR_materials_unlit' not in seat.get('extensions',{})
assert 'baseColorTexture' not in seat['pbrMetallicRoughness']
assert min(seat['pbrMetallicRoughness']['baseColorFactor'][:3])>.5,'White chairs lost their plain PBR material'
assert f.stat().st_size<65*1024*1024,'Lighting package exceeds portable size budget'
r={**identity,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'mesh_nodes':len(j['meshes']),'baked_atlases':len(baked),'materials':len(j['materials']),'embedded_images':len(j['images']),'all_resources_embedded':True,'all_accessor_bounds_finite':True,'source_detail_textures_preserved':True,'unlit_atlas_materials':True,'plain_white_seats_preserved':True,'passed':True}
(P/'review/baked-glb-audit.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
