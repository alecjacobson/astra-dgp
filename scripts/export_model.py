"""Portable textured GLB. Evaluates modifiers, preserves named layer groups.
The native .blend retains procedural Cycles materials. GLB uses authored tiled
color approximations; glazing is simplified in the browser for performance.
"""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1]
# Replace unsupported procedural colors with tiling image maps.
texture_map={'Brick':'cream-brick','Heritage brick':'heritage-brick','Red brick':'red-brick','Concrete':'concrete','Floor':'terrazzo','Wood':'wood','Door wood':'wood','Limestone':'limestone'}
imgs={}
for m in bpy.data.materials:
 base=m.name.replace(' XZ','').replace(' YZ','');key=texture_map.get(base)
 if not key:continue
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 if not p:continue
 for sock in ['Base Color','Normal']:
  for li in list(p.inputs[sock].links):l.remove(li)
 t=n.new('ShaderNodeTexImage');im=imgs.setdefault(key,bpy.data.images.load(str(P/'textures'/f'{key}.jpg'),check_existing=True));t.image=im;l.new(t.outputs['Color'],p.inputs['Base Color'])
for o in list(bpy.data.objects):
 if o.type=='FONT' or o.type=='CURVE':
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
for o in bpy.data.objects:
 if o.type!='MESH':continue
 uv=o.data.uv_layers.new(name='UVMap') if not o.data.uv_layers else o.data.uv_layers.active
 for poly in o.data.polygons:
  normal=(o.matrix_world.to_3x3()@poly.normal).normalized();axis=max(range(3),key=lambda i:abs(normal[i]));mat=o.data.materials[poly.material_index] if o.data.materials else None
  brick=mat and 'brick' in mat.name.lower();sx,sy=(2.08,1.36) if brick else (2,2)
  for li in poly.loop_indices:
   v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   u,w=(v.y,v.z) if axis==0 else ((v.x,v.z) if axis==1 else (v.x,v.y));uv.data[li].uv=(u/sx,w/sy)
# Collection grouping permits intuitive visibility and cutaways in any viewer.
for c in bpy.data.collections:
 if c.name=='Collection':continue
 empty=bpy.data.objects.new(c.name,None);bpy.context.scene.collection.objects.link(empty)
 for o in list(c.objects):o.parent=empty
# Keep browser lights independent from Cycles area lights.
for o in list(bpy.data.objects):
 if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.export_scene.gltf(filepath=str(P/'bahen-centre.glb'),export_format='GLB',export_apply=True,export_cameras=False,export_lights=False,export_extras=True,export_yup=True)
report={'bytes':(P/'bahen-centre.glb').stat().st_size,'objects':len(bpy.data.objects),'material_tiles':list(imgs),'native_materials':'Procedural in .blend','portable_materials':'Authored tiled base color; no photographic textures or baked lighting'}
(P/'review/export-report.json').write_text(json.dumps(report,indent=2))
