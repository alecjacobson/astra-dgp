"""Project a few manually identified source anchors; diagnostic, not a survey fit.
Image points use1280x720. Presenter, blur, exposure and hidden geometry excluded.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
points={
 'video_1452':[
  ('2133 numeral centre',(1.53,-2.365,5.8),(372,279)),
  ('lever midpoint',(1.72,-2.457,5.215),(445,455)),
 ],
 'video_1430':[
  ('left round handrail cap',(-10.955,-10.24,5.25),(234,489)),
  ('right round handrail cap',(-9.045,-10.24,5.25),(730,440)),
  ('right front newel foot',(-9.045,-10,4.2),(687,660)),
 ]}
r={'reference':'YouTube GGaJsGu_5zA, manually identified pixels in frames870/892s','resolution':[1280,720],'limitations':'Selected local anchors only. Camera pose, dimensions and source pixels approximate; no full-image or overall-building accuracy claim.','cameras':{}}
for cam,pts in points.items():
 s.camera=bpy.data.objects[cam];bpy.context.view_layer.update();rows=[]
 for name,world,pixel in pts:
  co=world_to_camera_view(s,s.camera,Vector(world));u,v=co.x*1280,(1-co.y)*720
  rows.append({'anchor':name,'source_pixel':pixel,'projected_pixel':[round(u,1),round(v,1)],'distance_pixels':round(math.hypot(u-pixel[0],v-pixel[1]),1)})
 r['cameras'][cam]=rows
(P/'review/camera-anchor-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
