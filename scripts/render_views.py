import bpy,sys,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];s=bpy.context.scene
views=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['atrium_east','atrium_west','exterior']
s.render.use_persistent_data=True;s.cycles.samples=int(os.getenv('BAHEN_SAMPLES','48'));s.render.resolution_x=int(os.getenv('BAHEN_WIDTH','1400'));s.render.resolution_y=round(s.render.resolution_x*5/7)
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 s.cycles.device='GPU' if any(d.type=='OPTIX' for d in prefs.devices) else 'CPU'
except Exception:s.cycles.device='CPU'
for v in views:
 s.camera=bpy.data.objects[v];s.view_settings.exposure=.35 if v not in ['exterior','street','overview'] else -.5
 if v.startswith(('video_','audit_')):s.view_settings.exposure={'video_1452':-1.25,'video_1430':-1.1,'video_0330':.55,'video_0030':-.35,'video_0730':-.35,'video_1452_offset':-1.25,'audit_lobby_offset':-1.1}.get(v,-.75)
 s.render.resolution_y=round(s.render.resolution_x*(9/16 if v.startswith(('video_','audit_')) else 5/7))
 s.render.filepath=str(P/'renders'/f'{os.getenv("BAHEN_REV","r01")}-{v}.png');bpy.ops.render.render(write_still=True)
