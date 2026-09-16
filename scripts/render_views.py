import bpy,sys,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
views=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['atrium_east','atrium_west','exterior']
s.render.use_persistent_data=True;s.cycles.samples=int(os.getenv('BAHEN_SAMPLES','48'));s.render.resolution_x=int(os.getenv('BAHEN_WIDTH','1400'));s.render.resolution_y=round(s.render.resolution_x*5/7)
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 s.cycles.device='GPU'
except Exception:pass
for v in views:
 s.camera=bpy.data.objects[v];s.view_settings.exposure=.35 if v not in ['exterior','street','overview'] else -.5
 s.render.filepath=str(P/'renders'/f'{os.getenv("BAHEN_REV","r01")}-{v}.png');bpy.ops.render.render(write_still=True)
