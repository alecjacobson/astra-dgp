"""Source-led finish pass, run after the base scene or on the R14 baseline.
All geometry is real, viewed by the same cameras; no camera-facing backdrops.
"""
import bpy, math, sys, os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'scripts'))
import model_lib as ml
from model_lib import *
P=Path(__file__).resolve().parents[1]
M.update({m.name:m for m in bpy.data.materials})
COL.update({c.name:c for c in bpy.data.collections})
collection('11 Video central circulation')
def V(x,y,z):return (-8+x,-10+y,4.2+z)
def remove(prefixes):
 for o in list(bpy.data.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
def recolor(name,color,rough=None,metal=None):
 m=M[name];p=m.node_tree.nodes.get('Principled BSDF');m.diffuse_color=(*linear(color),1)
 for l in list(p.inputs['Base Color'].links):m.node_tree.links.remove(l)
 p.inputs['Base Color'].default_value=m.diffuse_color
 if rough is not None:p.inputs['Roughness'].default_value=rough
 if metal is not None:p.inputs['Metallic'].default_value=metal
 return m
# Neutral finishes under soft daylight, with satin metal distinct from paint.
recolor('Video wall','#d9d8cf',.8);recolor('Video cream','#dcdbcd',.56)
recolor('Metal','#b8bebd',.24,.86)
recolor('Video steel','#657073',.32,.48)
recolor('Video riser','#515757',.3,.18)
mat('Polish chrome','#d6dcdd',.19,.94)
mat('Polish ceiling','#dfdfd8',.82)
mat('Polish channel glass','#b9cbc6',.3,0,0,False,True)
M['Polish channel glass'].node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.55
for name,base,scale,low,high in [('Floor','#b9bfbc',360,.83,1.06),('Video tread','#646d6c',280,.55,1.18)]:
 m=recolor(name,base,.24);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 for q in list(p.inputs['Normal'].links):l.remove(q)
 tc=n.new('ShaderNodeTexCoord');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale;tex.inputs['Detail'].default_value=1
 l.new(tc.outputs['Object'],tex.inputs['Vector']);r=n.new('ShaderNodeValToRGB')
 r.color_ramp.elements[0].color=(*(v*low for v in m.diffuse_color[:3]),1);r.color_ramp.elements[1].color=(*(v*high for v in m.diffuse_color[:3]),1)
 l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs['Color'],p.inputs['Base Color'])
# The source rear wall is close to the guard, oblique to the onward corridor.
# Its orientation/registration is inferred from the moving sequence.
remove(['Video lobby rear wall','Video lobby bin','Video recycling','Video lobby screen','Video lobby fascia','Video gallery low ceiling','Video central low ceiling'])
for o in list(COL['11 Video central circulation'].objects):
 if o.name.startswith(('Video noticeboard','Video notice paper','Video notice printed line')) and o.location.x<0:bpy.data.objects.remove(o,do_unlink=True)
theta=math.radians(-30);U=Vector((math.cos(theta),math.sin(theta),0));D=Vector((-math.sin(theta),math.cos(theta),0));A=Vector(V(2.2,5.4,0))
def W(u,v,z):return A+U*u+D*v+Vector((0,0,z))
def box(name,uvz,dim,ma,bev=0):
 o=cube('Polish '+name,W(*uvz),dim,ma,bev);o.rotation_euler.z=theta;return o
box('lobby rear wall',(4.3,0,2.4),(10.3,.18,4.8),'Video wall',.005)
box('lobby wall skirting',(4.3,-.105,.065),(10.3,.03,.13),'Video skirting')
box('lobby ceiling',(2.3,1.5,4.88),(11,6,.18),'Polish ceiling')
box('lobby board',(1.5,-.115,2.3),(2.0,.06,1.8),'Video cork',.01)
# Reuse varied papers until source-rectified textures are installed.
rr=__import__('random').Random(53)
for i in range(35):
 u=1.25+rr.uniform(-.68,.68);z=1.87+rr.uniform(-.84,.84);w=rr.uniform(.17,.29);h=rr.uniform(.23,.37)
 box('lobby notice',(u,-.152-i*.0008,z),(w,.003,h),['Paper','Paper','Poster pink','Poster blue','Poster yellow'][i%5])
for u in [-2.95,-1.3,.35,2.0]:box('screen upright',(u,-.45,2.4),(.095,.12,4.8),'Video steel',.004)
for z in [2.1,3.2,4.15,4.8]:box('screen transom',(-.5,-.45,z),(5.1,.12,.09),'Video steel',.004)
box('recycling body',(4.65,-.48,.46),(1.28,.54,.92),'Metal',.025)
box('recycling purple cap',(4.65,-.48,.955),(1.32,.58,.10),'Slate purple',.022)
for i in range(3):
 box('bin top aperture',(4.22+i*.43,-.55,1.013),(.24,.21,.007),'Black',.045)
 box('bin front seam',(4.0+(i+1)*.426,-.754,.48),(.007,.006,.79),'Dark metal')
 box('bin label',(4.22+i*.43,-.761,.73),(.26,.008,.075),'Paper',.003)
box('bench seat',(6.7,-.4,.47),(2.1,.64,.09),'Wood',.018)
for u in [5.85,7.55]:box('bench support',(u,-.4,.24),(.07,.44,.48),'Metal',.007)
# Close the short gap beside the lowest stair without covering its opening.
o=bpy.data.objects['Video central east floor'];o.location.x-=.5;o.scale.x=9/8
# Satin lever and reader, with a small inset and softened edges.
for o in bpy.data.objects:
 if o.name.startswith(('Video card lever backplate','Video silver lever','Video lever neck')):o.data.materials.clear();o.data.materials.append(M['Polish chrome'])
 if o.name.startswith('Video curved glass core'):o.data.materials.clear();o.data.materials.append(M['Polish channel glass'])
for x in [9.35+1.1*.4,8.05+.94*.4]:
 cyl('Polish reader status disc',V(x,7.582,1.205),.009,.008,'Polish chrome',24,(0,1,0))
 for z in [.978,1.223]:cyl('Polish reader screw',V(x,7.58,z),.0025,.009,'Dark metal',12,(0,1,0))
text('Polish room plaque2139','2139',V(8.62,7.55,1.63),.048,'Black')
# Soft ambient illumination removes the unobserved sharp sun bands.
for n in bpy.context.scene.world.node_tree.nodes:
 if n.type=='TEX_SKY':n.sun_disc=False
for o in bpy.data.objects:
 if o.type=='LIGHT' and o.name.startswith('Warm gallery light'):o.data.color=(1,.95,.85)
area('Polish lobby broad bounce',V(-.5,-1.8,3.5),280,4.5,(.89,.95,1),V(1.5,2.5,.6))
area('Polish rear wall light',W(3,-2,3.5),150,3,(1,.98,.94),W(3,0,1.4))
area('Polish corridor softbox',V(9,4.4,3.1),150,3,(1,1,.97),V(10,7.7,1.3))
for o in bpy.data.objects:
 if o.type=='LIGHT':o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False
collection('10 Lighting and cameras')
camera('audit_lobby_offset',V(-.1,-1.9,1.6),V(4.7,4.3,1.35),28)
camera('video_1452_offset',V(9.25,3.4,1.6),V(10.42,7.7,1.32),38)
# Photographic details are rectified surfaces from the supplied MP4.
def photo_material(name,filename,emission=0):
 m=mat(name,'#ffffff',.72);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(P/'textures'/filename),check_existing=True);t.image.pack();l.new(t.outputs['Color'],p.inputs['Base Color'])
 if emission:l.new(t.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=emission
 m['source_texture']=True;return name
def photo_plane(name,points,ma):
 o=mesh(name,points,[(0,1,2,3)],ma);uv=o.data.uv_layers.new(name='UVMap')
 for i,co in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[i].uv=co
 o['preserve_uv']=True;return o
photo_material('Source monitor','source-monitor.jpg',.75)
photo_material('Source notices','source-notices.jpg')
remove(['Video monitor heading','Video monitor second line','Video monitor text line','Video monitor violet screen'])
for o in list(COL['11 Video central circulation'].objects):
 if o.name.startswith(('Video notice paper','Video notice printed line')):bpy.data.objects.remove(o,do_unlink=True)
photo_plane('Polish actual monitor content',[V(x,7.288,z) for x,z in [(11.43,1.805),(12.35,1.805),(12.35,2.395),(11.43,2.395)]],'Source monitor')
# Raise and slightly turn the projecting display to match the top-cropped892view.
from mathutils import Matrix
pivot=Vector(V(11.89,7.35,2.1));rot=Matrix.Rotation(.12,4,'Z')@Matrix.Rotation(.045,4,'Y')
for o in bpy.data.objects:
 if o.name.startswith(('Video monitor','Polish actual monitor')):
  bpy.context.view_layer.update();o.matrix_world=Matrix.Translation(Vector((-.12,0,.18)))@Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)@o.matrix_world
photo_plane('Polish actual corridor notices',[V(x,7.502,z) for x,z in [(12.525,.33),(13.455,.33),(13.455,2.41),(12.525,2.41)]],'Source notices')
# A proper rectilinear weather envelope around the interior curved rooms.
collection('07 Roofs and skylights')
for name,loc,dim,ma in [('south atrium glass',(-10,-14.7,20.95),(21,.028,25.7),'Glass'),('east atrium return',(.5,-9.6,20.95),(.028,10.2,25.7),'Glass'),('extended atrium skylight',(-10,-9.65,33.75),(21,10.1,.04),'Glass')]:
 o=cube('Polish '+name,loc,dim,ma);o['cutaway_shell']=True
for x in [-20.5,-18.75,-17,-15.25,-13.5,-11.75,-10,-8.25,-6.5,-4.75,-3,-1.25,.5]:
 cube('Polish envelope vertical',(x,-14.74,20.95),(.07,.15,25.7),'Metal')
 beam('Polish skylight rafter',(x,-14.7,33.65),(x,-4.6,33.65),.10,'Metal',.18)
for z in [8.1,12.6,16.8,21,25.2,29.4,33.8]:
 cube('Polish envelope transom',(-10,-14.74,z),(21,.15,.10),'Metal')
 cube('Polish return transom',(.54,-9.65,z),(.15,10.1,.10),'Metal')
for y in [-14.7,-13,-11.3,-9.6,-7.9,-6.2,-4.5]:
 cube('Polish return mullion',(.54,y,23.35),(.15,.07,20.9),'Metal')
 cube('Polish skylight crossbar',(-10,y,33.72),(21,.07,.10),'Metal')
# Channel-glass ribs on the internal curved room wall, distinct from weather glass.
collection('11 Video central circulation')
for level in range(8):
 z=level*4.2-4.2
 for k in range(76):
  a=-math.pi*.52+k*math.pi*1.25/75;x=-6.8+3.83*math.cos(a);y=1+3.83*math.sin(a)
  beam('Polish channel glass seam',V(x,y,z+.05),V(x,y,z+4.15),.014,'Polish channel glass',.035,0)
# Dense real printed surfaces in the near stair lobby.
collection('11 Video central circulation')
remove(['Polish lobby notice'])
photo_material('Source lobby notices','source-lobby-notices.jpg')
photo_plane('Polish source lobby noticeboard',[W(u,-.154,z) for u,z in [(.5,1.4),(2.5,1.4),(2.5,3.2),(.5,3.2)]],'Source lobby notices')
photo_material('Source recycling labels','source-recycling-front.jpg')
# Source bin remains squat; increase width and height together, grounded at z0.
for o in list(COL['11 Video central circulation'].objects):
 if o.name.startswith(('Polish recycling','Polish bin')):
  pivot=W(4.65,-.48,0);o.location=pivot+(o.location-pivot)*1.28;o.scale*=1.28
photo_plane('Polish real recycling labels',[W(u,-.836,z) for u,z in [(3.83,.04),(5.47,.04),(5.47,1.08),(3.83,1.08)]],'Source recycling labels')
box('wall directory',(2.5,-.115,1.8),(.32,.028,.48),'Metal',.01)
for z in [1.94,1.87,1.8,1.73]:box('directory inset',(2.5,-.133,z),(.26,.003,.037),'Paper')
# The frame sits proud of plaster, avoiding coplanar speckling in oblique views.
for o in bpy.data.objects:
 if o.name.startswith(('Video narrow door frame','Video door frame head')):o.location.y-=.017
# A real dark rebated jamb keeps the narrow reveal continuous in oblique views.
for center,width in [(9.35,1.1),(8.05,.94)]:
 for side in [-1,1]:
  x=center+side*width/2
  cube('Polish dark door rebate',V(x+side*.004,7.711,1.38),(.018,.016,2.77),'Black')
  for o in list(COL['11 Video central circulation'].objects):
   if o.name.startswith('Video narrow door frame') and abs(o.location.x-(-8+x+side*.026))<.001:o.location.x+=side*.005
# The display emits its own pixels without receiving a diffuse white wash.
m=M['Source monitor'];p=m.node_tree.nodes.get('Principled BSDF')
for l in list(p.inputs['Base Color'].links):m.node_tree.links.remove(l)
p.inputs['Base Color'].default_value=(0,0,0,1);p.inputs['Emission Strength'].default_value=1.65;p.inputs['Specular IOR Level'].default_value=0
# Source rectangular pendant near the rear wall.
box('lobby pendant housing',(5.4,-1.0,4.15),(.9,.52,.18),'Metal',.025)
box('lobby pendant diffuser',(5.4,-1.0,4.053),(.78,.44,.012),'Video white light',.008)
area('Polish lobby practical',W(5.4,-1,4.04),85,1,(1,.96,.89),W(5.4,-1,0))
# Recessed bin and flanking table stay attached to their shared floor/wall.
for o in list(COL['11 Video central circulation'].objects):
 if o.name.startswith(('Polish recycling','Polish bin','Polish real recycling','Polish bench')):o.location+=U*.8
# Restrained polished stone and timber reflect the inset step luminaires.
recolor('Video timber','#58412e',.24)
m=M['Video tread'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
tc=n.new('ShaderNodeTexCoord');nt=n.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=180;nt.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],nt.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements.remove(r.color_ramp.elements[1]);r.color_ramp.elements[0].position=.28;r.color_ramp.elements[0].color=(*linear('#46514e'),1)
for pos,col in [(.43,'#56615b'),(.54,'#626d65'),(.62,'#7c867b'),(.72,'#91998c')]:r.color_ramp.elements.new(pos).color=(*linear(col),1)
l.new(nt.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
p.inputs['Roughness'].default_value=.16;p.inputs['Coat Weight'].default_value=.24;p.inputs['Coat Roughness'].default_value=.13
M['Video white light'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=10
# Contemporary lecture room: warm acoustic lining and erased-board patina.
collection('13 Video lecture theatre')
mat('Polish theatre lining','#55453d',.66,0,.0002,True)
mat('Polish theatre carpet','#665d56',.95,0,.0003)
recolor('Theatre desk','#443027',.3)
for o in COL['13 Video lecture theatre'].objects:
 if o.name.startswith(('Theatre side wall','Theatre back wall')):o.data.materials.clear();o.data.materials.append(M['Polish theatre lining'])
 if o.name.startswith(('Theatre raked platform','Theatre aisle half step')):o.data.materials.clear();o.data.materials.append(M['Polish theatre carpet'])
 if o.name.startswith(('Theatre chalkboard','Theatre chalk tray')):o.location.z+=.7
for y in [11+i*.9 for i in range(17)]:
 for x in [9.69,30.31]:cube('Polish acoustic wall joint',(x,y,3.6),(.015,.012,7.1),'Dark metal')
for x in [10+i*1.05 for i in range(20)]:cube('Polish rear acoustic joint',(x,26.39,4.1),(.012,.012,8),'Dark metal')
m=M['Theatre chalkboard'];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(2,2,8);l.new(tc.outputs['Generated'],mapping.inputs[0]);nt=n.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=3.3;nt.inputs['Detail'].default_value=2;l.new(mapping.outputs[0],nt.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*linear('#3d3c44'),1);r.color_ramp.elements[1].color=(*linear('#48464e'),1);l.new(nt.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color'])
# Broad luminous roof recess over the board wall, visible in07:30.
remove(['Theatre skylight glass'])
cube('Polish theatre daylight diffuser',(20,10.7,7.12),(11,2.1,.045),'Video white light')
for y in [9.65,11.75]:cube('Polish theatre recess reveal',(20,y,6.88),(11,.12,.48),'Theatre wall')
for x in [14.45,25.55]:cube('Polish theatre recess end',(x,10.7,6.88),(.12,2.1,.48),'Theatre wall')
for o in bpy.data.objects:
 if o.type=='LIGHT' and o.name.startswith('Theatre light'):o.data.color=(1,.87,.75);o.data.energy=170
# Camera framing revised against the actual six-board corners and aisle position.
def aim(name,loc,target,lens):
 o=bpy.data.objects[name];o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens
aim('video_0730',(14.776,15.969,2.416),(19.661,8.57,3.689),24)
aim('video_0630',(15,12.7,2.1),(20,23,.9),38)
# Replace the segmented entrance-mat edge with a continuous eased curve.
collection('12 Video street and entry');remove(['Video curved entry mat'])
pts=[(31.8,-4.7,.024),(22,-4.7,.024),(22,3.15,.024),(26.5,3.15,.024)]
for i in range(1,49):
 t=i/48;u=1-t;x=u*u*u*26.5+3*u*u*t*28+3*u*t*t*28.5+t*t*t*31.8;y=u*u*u*3.15+3*u*u*t*3.15+3*u*t*t*.65+t*t*t*1.3;pts.append((x,y,.024))
mesh('Polish curved entry mat',pts,[tuple(range(len(pts)))],'Video plum mat')
for o in bpy.data.objects:
 if o.type=='LIGHT':o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False
bpy.context.scene['revision']=os.getenv('BAHEN_REV','r15')
if __name__=='__main__':bpy.ops.wm.save_as_mainfile(filepath=str(P/'bahen-centre.blend'),compress=True)
