"""Validate native deliverable and set explicit metric display units."""
import bpy,json
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.length_unit='METERS';s.unit_settings.scale_length=1
meshes=[o for o in bpy.data.objects if o.type=='MESH'];assert len(meshes)>4000
for name in ['atrium_east','atrium_west','landing','exterior']:assert bpy.data.objects[name].type=='CAMERA'
assert all(o.data for o in meshes);assert not [im for im in bpy.data.images if im.source=='FILE' and not im.packed_file]
report={'mesh_objects':len(meshes),'cameras':[o.name for o in bpy.data.objects if o.type=='CAMERA'],'units':'metres','external_image_dependencies':False,'saved_revision':s['revision'],'passed':True};(P/'review/native-scene-check.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(P/'bahen-centre.blend'),compress=True);print(json.dumps(report))
