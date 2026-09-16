import bpy, math, random
from mathutils import Vector
from pathlib import Path
P=Path(__file__).parent
M={};COL={};ACTIVE='Architecture';rng=random.Random(47)
def collection(name):
 global ACTIVE
 ACTIVE=name
 if name not in COL:
  c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c);COL[name]=c
 return COL[name]
def put(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 COL[ACTIVE].objects.link(o);return o
def linear(h):
 if isinstance(h,str):vals=[int(h[i:i+2],16)/255 for i in (1,3,5)]
 else:vals=h[:3]
 return tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in vals)
def mat(name,color,rough=.65,metal=0,noise=0,wood=False,glass=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*linear(color),1);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=m.diffuse_color;p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if glass:p.inputs['Transmission Weight'].default_value=.95;p.inputs['IOR'].default_value=1.48
 if noise or wood:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=38 if not wood else 3;tex.inputs['Detail'].default_value=3;tex.inputs['Roughness'].default_value=.72
  coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1,24,12) if wood else (1,1,1);l.new(coord.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs['Vector'])
  ramp=n.new('ShaderNodeValToRGB');rgb=linear(color);ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*(c*.56 for c in rgb),1);ramp.color_ramp.elements[1].position=.83;ramp.color_ramp.elements[1].color=(*(min(1,c*1.28) for c in rgb),1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
  bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.0018 if wood else noise;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 M[name]=m;return m
def materials():
 for args in [('Plaster','#f1eee6',.78,0,.001),('Mortar','#a69883',.98,0,.003),('Charcoal','#343d3e',.43),('Trim ivory','#e7e3d7',.42),('Zinc','#646d70',.3,.7),('Black metal','#202a2c',.29,.65),('Roof membrane','#484a48',.93,0,.005),('Concrete','#b8b6a8',.92,0,.006),('Stone cap','#c7c4af',.84,0,.006),('Glass','#f0f6f4',.08,0,0,False,True),('Mirror','#eef0ed',.05,1),('Oak','#c8a775',.58,0,0,True),('Cedar','#a68050',.68,0,0,True),('Porch cedar','#a9a18b',.82,0,0,True),('Warm cedar','#bd8e50',.66,0,0,True),('Cabinet','#e7e5dc',.42),('Quartz','#f2f1e9',.28,0,.0004),('Fabric ivory','#dfdacf',.95,0,.002),('Fabric sage','#a5afa0',.95,0,.002),('Fabric gray','#8e9291',.95,0,.002),('Rug','#b4aaa0',.98,0,.003),('Stainless','#abb1ad',.24,.85),('Soil','#332e23',1,0,.02),('Asphalt','#6d6e68',.94,0,.008),('Leaf','#42723a',.8),('Leaf light','#668740',.8),('Bark','#6b5943',.96,0,.009),('Fireplace','#858c8a',.75,0,.002),('Black stone','#292b29',.32),('Terracotta','#af6749',.85,0,.002),('Ceramic','#e9e6dc',.18)]:mat(*args)
 for i in range(14):
  v=rng.uniform(.80,1.13);rgb=[min(.95,c*v+rng.uniform(-.025,.025)) for c in (.59,.29,.20)];mat(f'Brick{i}',rgb,.91,0,.004)
 for i in range(9):
  v=rng.uniform(.65,1.14);mat(f'Sidebrick{i}',tuple(c*v for c in (.42,.39,.31)),.94,0,.004)
 for i in range(8):
  v=rng.uniform(.94,1.06);mat(f'Shingle{i}',tuple(c*v for c in (.23,.26,.27)),.93,0,.004)
 for i in range(6):
  v=rng.uniform(.94,1.06);mat(f'Gableshingle{i}',tuple(c*v for c in (.35,.37,.37)),.83,0,.002)
def mesh(name,vs,fs,matname='Plaster',mi=None,mats=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);COL[ACTIVE].objects.link(o)
 for m in (mats or [matname]):me.materials.append(M[m])
 if mi:
  for p,i in zip(me.polygons,mi):p.material_index=i
 return o
def bevel(o,w=.008,seg=2):
 if w:
  mod=o.modifiers.new('Edge highlights','BEVEL');mod.width=w;mod.segments=max(seg,6 if w>.04 else seg)
  mod=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL');mod.keep_sharp=True
 return o
def cube(name,loc,dim,ma='Plaster',bev=0):
 x,y,z=(v/2 for v in dim);vs=[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)];fs=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
 fs=[tuple(reversed(f)) for f in fs]
 o=mesh(name,vs,fs,ma);o.location=loc;return bevel(o,bev)
def beam(name,a,b,w=.04,ma='Charcoal',depth=None,bev=.003):
 a,b=Vector(a),Vector(b);o=cube(name,(a+b)/2,(w,depth or w,(b-a).length),ma,bev);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def cyl(name,loc,r,depth,ma='Charcoal',verts=16,direction=None):
 vs=[]
 for z in [-depth/2,depth/2]:vs += [(r*math.cos(i*math.tau/verts),r*math.sin(i*math.tau/verts),z) for i in range(verts)]
 fs=[tuple(reversed(range(verts))),tuple(range(verts,verts*2))]+[(i,(i+1)%verts,(i+1)%verts+verts,i+verts) for i in range(verts)]
 o=mesh(name,vs,fs,ma);o.location=loc
 if direction:o.rotation_euler=Vector(direction).to_track_quat('Z','Y').to_euler()
 for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
 return o
def sphere(name,loc,scale,ma='Fabric ivory',segments=24,rings=12):
 vs=[(0,0,1)];fs=[]
 for j in range(1,rings):
  theta=math.pi*j/rings
  vs.extend([(math.sin(theta)*math.cos(i*math.tau/segments),math.sin(theta)*math.sin(i*math.tau/segments),math.cos(theta)) for i in range(segments)])
 bottom=len(vs);vs.append((0,0,-1))
 for i in range(segments):
  ni=(i+1)%segments;fs.append((0,1+i,1+ni))
  for j in range(rings-2):
   a=1+j*segments+i;b=1+j*segments+ni;fs.append((a,a+segments,b+segments,b))
  a=1+(rings-2)*segments+i;b=1+(rings-2)*segments+ni;fs.append((a,bottom,b))
 o=mesh(name,vs,fs,ma);o.location=loc;o.scale=scale
 for f in o.data.polygons:f.use_smooth=True
 return o
def curve(name,points,r=.014,ma='Black metal'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=12;cu.bevel_depth=r;cu.bevel_resolution=3;s=cu.splines.new('POLY');s.points.add(len(points)-1)
 for p,co in zip(s.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,cu);COL[ACTIVE].objects.link(o);cu.materials.append(M[ma]);return o
def text(name,body,loc,size=.15,ma='Trim ivory',rotation=(math.pi/2,0,0)):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.extrude=.001;cu.bevel_depth=.0003;o=bpy.data.objects.new(name,cu);COL[ACTIVE].objects.link(o);o.location=loc;o.rotation_euler=rotation;cu.materials.append(M[ma]);return o
class Batch:
 def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def box(self,loc,dim,mi=0):
  x,y,z=(v/2 for v in dim);n=len(self.v);self.v.extend([(loc[0]+a,loc[1]+b,loc[2]+c) for a,b,c in [(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]]);self.f.extend([tuple(n+i for i in reversed(f)) for f in [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]]);self.mi.extend([mi]*6)
 def finish(self,bev=0):return bevel(mesh(self.name,self.v,self.f,mats=self.mats,mi=self.mi),bev,1)
def camera(name,loc,target,lens=40):
 ca=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,ca);COL[ACTIVE].objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();ca.lens=lens;ca.clip_end=300;return o
def area(name,loc,power,size,color=(1,.93,.83),target=None):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);COL[ACTIVE].objects.link(o);o.location=loc
 if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 return o
