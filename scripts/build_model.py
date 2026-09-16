"""Bahen Centre photo-guided architectural model. Coordinates metres, Z up.
Build: blender -b --python scripts/build_model.py
Inferred dimensions; visual sources and limitations: review/sources.json.
"""
import bpy,sys,math,random,json,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
from model_lib import *
P=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
 if c.name!='Collection':bpy.data.collections.remove(c)
rng=random.Random(31)
# Physically based material palette, in sRGB.
for args in [('Concrete','#c0beb3',.7,0,.001),('Limestone','#bfb8a3',.73,0,.0006),('Plaster','#eeeade',.8),('Metal','#697777',.32,.65),('Dark metal','#313b3e',.35,.6),('Wood','#503426',.42,0,.001,True),('Door wood','#755139',.45,0,.001,True),('Glass','#dceaea',.1,0,0,False,True),('Frosted glass','#b9dadd',.3,0,0,False,True),('Roof','#929d9c',.78),('Brick','#d0c7a6',.8),('Heritage brick','#b3a475',.86),('Red brick','#9e6448',.82),('Copper','#488079',.4,.65),('Floor','#b8bcb8',.26,0,.0006),('Floor dark','#79838a',.4),('Slate purple','#716c83',.7),('Asphalt','#565c5d',.95,0,.012),('Paving','#c3c2b7',.85,0,.005),('Grass','#7a8759',.95),('Soil','#5a4e38',1),('Bark','#736956',.95),('Leaf','#667f44',.9),('Leaf light','#8d9b58',.9),('Water','#3d7979',.15,.4),('Red seat','#ad3a24',.4),('Paper','#e5e3d6',.8),('Sign blue','#1e3b54',.55),('Black','#252827',.6),('Warm light','#fff2c3',.3),('Exit green','#1f7953',.5)]:mat(*args)
M['Frosted glass'].node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.45
M['Warm light'].node_tree.nodes.get('Principled BSDF').inputs['Emission Color'].default_value=(1,.83,.52,1)
M['Warm light'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=3
for name in ['Concrete','Limestone','Paving','Asphalt']:
 n=M[name].node_tree.nodes;l=M[name].node_tree.links
 tc=next((v for v in n if v.type=='TEX_COORD'),None);vm=next((v for v in n if v.type=='VECT_MATH'),None)
 if tc and vm:l.new(tc.outputs['Object'],vm.inputs[0])
# World-metric masonry texture on two orientations; portable export retains palette.
def masonry(base,axis='XZ'):
 m=M[base].copy();m.name=base+' '+axis;M[m.name]=m;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 tex=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tex.outputs['Object'],sep.inputs[0]);comb=n.new('ShaderNodeCombineXYZ');l.new(sep.outputs['X' if axis=='XZ' else 'Y'],comb.inputs[0]);l.new(sep.outputs['Z'],comb.inputs[1])
 # Triplanar metric coordinates keep end faces from becoming horizontal stripes.
 gx=n.new('ShaderNodeNewGeometry');sn=n.new('ShaderNodeSeparateXYZ');l.new(gx.outputs['Normal'],sn.inputs[0]);ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(sn.outputs['X'],ab.inputs[0]);cmp=n.new('ShaderNodeMath');cmp.operation='GREATER_THAN';cmp.inputs[1].default_value=.5;l.new(ab.outputs[0],cmp.inputs[0])
 yz=n.new('ShaderNodeCombineXYZ');l.new(sep.outputs['Y'],yz.inputs[0]);l.new(sep.outputs['Z'],yz.inputs[1]);xz=n.new('ShaderNodeCombineXYZ');l.new(sep.outputs['X'],xz.inputs[0]);l.new(sep.outputs['Z'],xz.inputs[1]);mix=n.new('ShaderNodeMixRGB');l.new(cmp.outputs[0],mix.inputs[0]);l.new(xz.outputs[0],mix.inputs[1]);l.new(yz.outputs[0],mix.inputs[2])
 b=n.new('ShaderNodeTexBrick');l.new(mix.outputs[0],b.inputs['Vector']);b.inputs['Scale'].default_value=1;b.inputs['Brick Width'].default_value=.26;b.inputs['Row Height'].default_value=.085;b.inputs['Mortar Size'].default_value=.004;b.inputs['Mortar Smooth'].default_value=.003
 rgb=m.diffuse_color;b.inputs['Color1'].default_value=rgb;b.inputs['Color2'].default_value=(*(v*.75 for v in rgb[:3]),1);b.inputs['Mortar'].default_value=(.32,.31,.26,1);l.new(b.outputs['Color'],p.inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.35;bump.inputs['Distance'].default_value=.009;l.new(b.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal']);return m.name
for b in ['Brick','Heritage brick','Red brick']:
 masonry(b,'XZ');masonry(b,'YZ')
# Terrazzo: finely varied aggregate at world metric scale.
n=M['Floor'].node_tree.nodes;l=M['Floor'].node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=95;noise.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],noise.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.27;r.color_ramp.elements[0].color=(.17,.2,.2,1);r.color_ramp.elements[1].position=.7;r.color_ramp.elements[1].color=(.65,.66,.62,1);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs['Color'],p.inputs['Base Color'])

def grid_glass(name,axis,plane,a0,a1,z0,z1,dx=1.5,dz=2.1,glass='Glass',frame='Metal'):
 # Surface vertical plane; frames are deliberately dimensional.
 def box2(n,a,z,w,h,depth,ma):
  return cube(name+' '+n,(a,plane,z) if axis=='X' else (plane,a,z),(w,depth,h) if axis=='X' else (depth,w,h),ma)
 box2('glazing',(a0+a1)/2,(z0+z1)/2,a1-a0,z1-z0,.038,glass)
 for i in range(round((a1-a0)/dx)+1):
  a=a0+(a1-a0)*i/round((a1-a0)/dx);box2('vertical mullion',a,(z0+z1)/2,.07,z1-z0,.13,frame)
 for i in range(round((z1-z0)/dz)+1):
  z=z0+(z1-z0)*i/round((z1-z0)/dz);box2('transom',(a0+a1)/2,z,a1-a0,.075,.13,frame)

def rail(a,b,z,name='Glass guard',frost=True):
 a=Vector((a[0],a[1],z));b=Vector((b[0],b[1],z));d=b-a;N=max(1,math.ceil(d.length/1.45))
 for i in range(N):
  aa=a+d*i/N;bb=a+d*(i+1)/N;mid=(aa+bb)/2;o=cube(name+' panel',mid+Vector((0,0,.6)),((bb-aa).length-.06,.026,.94),'Frosted glass' if frost else 'Glass');o.rotation_euler.z=math.atan2(d.y,d.x)
 for i in range(N+1):
  pt=a+d*i/N;beam(name+' post',pt,pt+Vector((0,0,1.15)),.045,'Metal')
 beam(name+' wood handrail',a+Vector((0,0,1.15)),b+Vector((0,0,1.15)),.065,'Wood',bev=.012)
 beam(name+' bottom channel',a+Vector((0,0,.12)),b+Vector((0,0,.12)),.05,'Metal')

def stairs(x,y,z,run,rise,width,n,name):
 for i in range(n):
  h=rise*(i+1)/n;cube(name+' tread',(x+run*(i+.5)/n,y,z+h-.09),(abs(run)/n+.012,width,.18),'Concrete',.008)
 for side in [-1,1]:
  yy=y+side*(width/2+.035);a=Vector((x,yy,z));b=Vector((x+run,yy,z+rise));beam(name+' stringer',a,b,.18,'Metal',.3)
  points=[]
  for i in range(5):
   pt=a+(b-a)*i/4;beam(name+' guard post',pt,pt+Vector((0,0,1.08)),.045,'Metal');points.append(pt+Vector((0,0,1.1)))
  beam(name+' handrail',points[0],points[-1],.065,'Wood',bev=.015)
  for i in range(4):
   aa=a+(b-a)*i/4;bb=a+(b-a)*(i+1)/4;mesh(name+' frosted panel',[aa+Vector((0,0,.18)),bb+Vector((0,0,.18)),bb+Vector((0,0,.96)),aa+Vector((0,0,.96))],[(0,1,2,3)],'Frosted glass')

def arcmesh(name,cx,cy,r0,r1,z0,z1,t0=0,t1=math.tau,steps=96,ma='Concrete'):
 vs=[]
 for z in [z0,z1]:
  for r in [r0,r1]:
   vs += [(cx+r*math.cos(t0+(t1-t0)*i/steps),cy+r*math.sin(t0+(t1-t0)*i/steps),z) for i in range(steps+1)]
 N=steps+1;fs=[]
 for i in range(steps):
  fs.extend([(i,i+1,N+i+1,N+i),(2*N+i,3*N+i,3*N+i+1,2*N+i+1),(i,2*N+i,2*N+i+1,i+1),(N+i,N+i+1,3*N+i+1,3*N+i)])
 fs.extend([(0,N,3*N,2*N),(steps,2*N+steps,3*N+steps,N+steps)])
 return mesh(name,vs,fs,ma)

collection('01 Site')
cube('Presentation site base',(0,0,-.55),(91,76,.8),'Limestone',.25)
cube('St George Street',(41,0,-.07),(9,76,.13),'Asphalt')
cube('Russell Street',(0,33,-.07),(91,8,.13),'Asphalt')
cube('East sidewalk',(34.5,0,-.02),(5,65,.16),'Paving')
cube('North sidewalk',(0,27.8,-.02),(70,3,.16),'Paving')
cube('South quadrangle',(0,-19,-.07),(70,29,.16),'Paving')
for x in range(-34,36,3):cube('Paving expansion joint',(x,-22,.02),(.012,24,.01),'Roof')
for y in range(-33,-5,3):cube('Paving expansion joint',(0,y,.02),(70,.012,.01),'Roof')
for y in range(-30,34,5):cube('Street broken centre line',(42,y,.01),(.12,2.4,.012),'Paper')
# Rainwater garden is an architectural feature, approximate plan.
cube('Pool stone coping',(-13,-24,.27),(19,5,.55),'Limestone',.08)
cube('Rainwater reflecting pool',(-13,-24,.56),(18.3,4.3,.025),'Water')
cube('Raised water rill',(-3.5,-30,.65),(1,12,1.3),'Limestone',.04)
cube('Rill water',(-3.5,-30,1.31),(.65,12,.03),'Water')

collection('02 Envelope')
# Set-back blocks; facade panels assembled around true glazed openings.
# Hollow shell with real window openings rather than solid glazing backers.
for z in [0,4.2,8.4,12.6,16.8,21]:cube('North wing floor',(-1,17,z-.16),(68,22,.32),'Concrete')
for z in [0.5,4.2,8.4,12.6,16.8,20.5]:cube('North wall spandrel',(-1,28,z),(68,.35,1.4),'Brick XZ')
for x in range(-32,33,3):cube('North wall pier',(x+1.5,28,10.5),(1.25,.35,21),'Brick XZ')
cube('East north wall backing',(32.7,18,10.5),(.3,25,21),'Brick YZ')
cube('West north wall',(-35,17,10.5),(.3,22,21),'Brick YZ')
# Keep atrium side open: wing starts behind circulation gallery at y=6.
for z in [2.1,6.3,10.5,14.7,18.9]:
 for x in range(-32,33,3):
  grid_glass('North window','X',28.06,x-.82,x+.82,z-.9,z+.9,1.7,1.8)
# Enclose upper storeys above the low atrium roof.
for z in [13.1,16.8,20.5]:cube('North wing south spandrel',(14,6,z),(38,.35,1.35),'Brick XZ')
for z in [14.7,18.9]:grid_glass('South research ribbon','X',5.98,-5,33,z-1.05,z+1.05,1.45,2.1)
for x in [-5,4.5,14,23.5,33]:cube('South research pier',(x,6,16.8),(.55,.35,8.4),'Brick XZ')
# Eastern facade with inserted historic house between two cream masonry masses.
# Existing mass is recessed at x33; front articulation goes out to x34.
for y0,y1 in [(5,13),(23,28)]:
 cube('Street facing masonry',(33.4,(y0+y1)/2,8.3),(.8,y1-y0,16.6),'Brick YZ')
 for z in [2.1,6.4,10.6,14.5]:
  grid_glass('East recessed window','Y',33.83,y0+.65,y1-.65,z-1.0,z+1,1.4,2)
# Large projecting glass entry bay.
grid_glass('Street glazed bay','Y',33.9,-4.5,5,0,12.8,3.2,3.2)
grid_glass('East bay return','X',5,31.5,33.9,0,12.8,1.2,3.2)
cube('Entry canopy',(35.1,.2,3.5),(4.2,10,.18),'Glass')
for yy in [-3,0,3]:beam('Canopy bracket',(32.8,yy,4),(36.8,yy,3.5),.09,'Metal')
# North upper block and western research wing.
for z in [21,25.2,29.4,33.6]:cube('Upper research floor',(-19,17,z-.15),(30,22,.3),'Concrete')
for y in [6,28]:
 for z in [21.4,25.2,29.4,33.2]:cube('Upper research spandrel',(-19,y,z),(30,.3,1.35),'Brick XZ')
 for x in range(-33,-3,3):cube('Upper research pier',(x,y,27.4),(.65,.35,12),'Brick XZ')
 grid_glass('Upper research facade','X',y,-34,-4,21.6,32.9,1.5,2.1)
for z in [21.4,25.2,29.4,33.2]:cube('Upper east spandrel',(-4,17,z),(.3,22,1.35),'Brick YZ')
for z in [23.2,27.4,31]:
 grid_glass('Upper north glazing','X',28.1,-33.5,-4.5,z-1.15,z+1.15,1.5,2.3)
 grid_glass('Upper east glazing','Y',-3.93,6,28,z-1.15,z+1.15,1.5,2.3)
for z in [0,4.2,8.4,12.6,16.8,21,25.2,29.4]:
 cube('West wing floor',(-28,-13,z-.15),(15,18,.3),'Concrete')
 cube('West wing spandrel',(-28,-22,z+.5),(15,.35,1.1),'Brick XZ')
for x in [-35.4,-20.6]:cube('West wing end pier',(x,-13,14.7),(.3,18,29.4),'Brick YZ')
grid_glass('West wing atrium wall','X',-4,-35.5,-20.5,.3,29.2,1.5,2.1)
# Vertical glazed closure at the step between low and high atrium roofs.
grid_glass('High atrium east clerestory','Y',.5,-4.5,6,12.9,33.8,1.5,2.5)
grid_glass('High atrium south closure','X',-4.5,-3.1,.5,8.4,33.8,1.2,2.5)
for z in [2.3,6.5,10.7,14.9,19.1,23.3,27.5]:
 grid_glass('South solar facade','X',-22.15,-35.5,-20.5,z-1.25,z+1.25,1.5,2.5)
 for zz in [z-.9,z-.45,z,z+.45,z+.9]:cube('South external sunshade',(-28,-22.6,zz),(15.2,.7,.065),'Metal')
grid_glass('West curtain glazing','Y',-35.65,-22,28,1,29,1.6,2.1)
# Cafe with curtain wall facing court.
for z in [.15,4.2,8.4]:cube('Cafe floor',(-7,-16,z),(25,9,.3),'Concrete')
grid_glass('Cafe south glass','X',-20.5,-19.5,5.5,.3,8.25,1.45,2.1)
grid_glass('Cafe east glass','Y',5.5,-20.5,-10.5,.3,8.25,1.45,2.1)

collection('03 Atrium structure')
cube('Atrium terrazzo floor',(0,0,-.14),(65,11,.28),'Floor')
# Level changes to a basement are localized to south-west edge.
cube('Level one south gallery',(-17,-5,4.08),(35,3,.24),'Concrete')
for i in range(3):
 z=i*4.2
 if i>0:
  cube('North gallery floor '+str(i),(0,5.3,z-.17),(65,3.2,.34),'Concrete')
  cube('Gallery fascia '+str(i),(0,3.67,z-.22),(65,.08,.42),'Slate purple')
  if i==1:
   rail((-32,3.66),(17.5,3.66),z,frost=False);rail((20.1,3.66),(32,3.66),z,frost=False)
  else:
   rail((-32,3.66),(9.4,3.66),z,frost=False);rail((11.8,3.66),(32,3.66),z,frost=False)
 for x in [-28,-20,-12,-4,4,12,20,28]:
  cyl('Concrete column north', (x,3.3,z+2.1),.38,4.2,'Concrete',40)
  cyl('Column cast joint',(x,3.3,z+2.25),.385,.027,'Roof',40)
  if x<8:
   cyl('Concrete column south',(x,-3.45,z+2.1),.38,4.2,'Concrete',40)
   cyl('Column cast joint',(x,-3.45,z+2.25),.385,.027,'Roof',40)
  if i>0:cube('Column capital',(x,3.3,z-.33),(1.05,.94,.52),'Concrete',.06)
# North classroom frontage: white wall piers and recessed wood doors.
for x in range(-28,33,8):
 cube('Classroom wall panel',(x,6.02,1.65),(5.9,.22,3.3),'Plaster')
 cube('Classroom skirting',(x,5.87,.13),(5.9,.1,.26),'Dark metal')
 cube('Recessed timber door',(x-3.4,6.1,1.4),(1.08,.12,2.8),'Door wood',.015)
 cube('Door side frame',(x-4,6,1.43),(.09,.2,2.88),'Metal')
 cube('Door header',(x-3.4,6,2.84),(1.3,.2,.09),'Metal')
 beam('Door pull',(x-3.04,5.99,1.05),(x-3.04,5.99,1.6),.026,'Metal')
 text('Room number','BA '+str(1100+x+28),(x-3.4,5.97,3.08),.14,'Dark metal')
# Horizontal wood screens visibly separated and mounted outside upper galleries.
for z in [4.9,9.1]:
 for x in range(-28,29,8):
  if x==20 and z<6:continue
  for k in range(18):cube('Acoustic wood louvre',(x,3.03,z+k*.13),(6.6,.15,.075),'Wood',.008)
  for xx in [x-3.3,x+3.3]:cube('Wood screen upright',(xx,3.03,z+1.1),(.11,.2,2.5),'Wood')
# Transverse bridges at measured-looking but inferred stations.
for x,z in [(7,4.2),(7,8.4),(-19,4.2),(-19,8.4),(-19,12.6)]:
 cube('Atrium crossing bridge',(x,0,z-.17),(2.4,8.8,.34),'Concrete')
 rail((x-1.2,-4.4),(x-1.2,4.4),z)
 rail((x+1.2,-4.4),(x+1.2,4.4),z)
cube('South gallery purple fascia',(-24,-4.65,5.1),(21,.2,1.8),'Slate purple')
grid_glass('South gallery fluted glazing','X',-4.65,-34.5,-13.5,6,8.1,.32,2.1,'Frosted glass','Metal')
# Main entrance curtain wall and glazed doors.
grid_glass('East atrium portal','Y',32.4,-4.5,6,0,12.8,3.5,3.2)
for yy in [-2.7,-1.5,-.3,.9]:
 cube('Entrance glass door',(32.53,yy,1.25),(.05,1.13,2.5),'Glass')
 for y in [yy-.6,yy+.6]:cube('Entrance door stile',(32.6,y,1.3),(.11,.05,2.6),'Metal')
 beam('Entrance door handle',(32.67,yy+.35,1),(32.67,yy+.35,1.5),.025,'Metal')
cube('Portal door lintel',(32.6,-.9,2.65),(.22,5.2,.16),'Limestone')
# West glazed termination.
grid_glass('West atrium light','Y',-35.2,-4.5,5,0,16,1.5,2.3)

collection('04 Heritage Koffler wall')
# Actual openings; yellow brick historic exterior is now indoors.
cube('Heritage base plinth',(21,-5.45,.6),(24,1.1,1.2),'Limestone',.03)
cube('Heritage copper ledge',(21,-4.82,1.27),(24,.5,.1),'Copper')
for z0,z1 in [(1.3,2.0),(5.5,6.6),(10.1,11.2),(14.2,15.0)]:cube('Heritage masonry spandrel',(21,-5.45,(z0+z1)/2),(24,1.1,z1-z0),'Heritage brick XZ')
for x in [10,14,18,22,26,30,32.5]:cube('Heritage brick pier',(x,-5.45,8),(1.2,1.1,13.4),'Heritage brick XZ')
for x in [12,16,20,24,28,31.2]:
 for z0,z1 in [(2,5.5),(6.6,10.1),(11.2,14.2)]:
  w=2.5 if x<30 else 1.1
  grid_glass('Heritage sash','X',-5.45,x-w/2,x+w/2,z0,z1,w/2,(z1-z0)/2,'Glass','Wood')
  cube('Heritage stone sill',(x,-4.84,z0-.08),(w+.3,.38,.12),'Limestone',.02)
  cube('Heritage stone lintel',(x,-4.9,z1+.12),(w+.3,.18,.18),'Heritage brick XZ',.02)
  for xx in [x-w/2,x+w/2]:cube('Heritage brick reveal',(xx,-5.2,(z0+z1)/2),(.18,.65,z1-z0),'Heritage brick XZ')
for x in [12,16,20,24,28]:
 for dx in [-.85,-.43,0,.43,.85]:beam('Heritage window iron grille',(x+dx,-5.06,2),(x+dx,-5.06,5.4),.018,'Dark metal')
 for zz in [2.2,3.4,4.6,5.3]:cube('Heritage grille rail',(x,-5.06,zz),(2.35,.025,.024),'Dark metal')
# Preserved exterior context on south/east.
cube('Koffler context roof',(21,-16.9,12.3),(24,21.8,.5),'Roof')
cube('Koffler context floor',(21,-16.9,0),(24,21.8,.3),'Concrete')
cube('Koffler south facade',(21,-27.75,6.1),(24,.3,12.2),'Heritage brick XZ')
cube('Koffler west facade',(9,-16.9,6.1),(.3,21.8,12.2),'Heritage brick YZ')
for z in [1.1,5.2,8.9,11.7]:cube('Koffler east stone course',(33.05,-16.9,z),(.35,21.8,.4 if z>2 else 2.2),'Limestone')
for y in [-6,-10.8,-16,-21.2,-27.8]:cube('Koffler east brick pilaster',(33,-abs(y),6.7),(.4,1.5,10.9),'Heritage brick YZ')
for y in [-8.4,-13.4,-18.6,-24.3]:
 for z0,z1 in [(2.2,5),(5.5,8.7),(9.1,11.5)]:
  grid_glass('Koffler street window','Y',32.9,y-1.5,y+1.5,z0,z1,1,1.3,'Glass','Wood')
  cube('Koffler street sill',(33.15,y,z0),(.45,3.2,.16),'Limestone')
cube('Koffler east cornice',(33.18,-16.9,12.08),(.7,22.2,.3),'Limestone')
for x in [12,16,20,24,28]:grid_glass('Koffler exterior sash','X',-27.86,x-1.2,x+1.2,3,8,1.2,2.5,'Glass','Wood')

for o in COL['04 Heritage Koffler wall'].objects:
 if not o.name.startswith('Koffler'):
  o.location.z*=.83;o.scale.z*=.83
collection('05 Circulation')
stairs(27,4.8,0,-7,4.2,1.85,25,'East main stair')
cube('First landing',(18.8,4.8,4.08),(2.4,1.9,.24),'Floor')
stairs(17.6,4.8,4.2,-7,4.2,1.85,25,'Second main stair')
cube('Upper stair landing',(10.6,4.8,8.28),(2.4,5,.24),'Floor')


cube('Upper landing wall header',(18.7,6.05,7.65),(8,.25,1),'Plaster')
# Upper landing frontage and doors observed in the video thumbnail.
for x,w in [(14.8,3.2),(18,1.3),(21.7,2.2)]:
 cube('Landing cream wall pier',(x,6.05,5.85),(w,.25,3.3),'Plaster')
 cube('Landing dark skirting',(x,5.9,4.32),(w,.1,.24),'Dark metal')
for x in [16.8,19.6,20.6]:
 cube('Upper landing wood door',(x,6.05,5.55),(.9,.15,2.7),'Door wood',.01)
 for xx in [x-.48,x+.48]:cube('Upper door metal frame',(xx,5.98,5.57),(.055,.2,2.78),'Metal')
 cube('Upper door head',(x,5.98,6.95),(1.05,.2,.07),'Metal')
 beam('Upper door handle',(x+.3,5.93,5.2),(x+.3,5.93,5.65),.025,'Metal')
 text('Upper room sign','BA 21'+str(int(x)),(x,5.94,7.15),.11,'Dark metal')
 cube('Upper door downlight',(x,5.2,7.63),(.6,.6,.06),'Warm light')
# Frosted guard along south gallery, dark bench behind it from video stills.
rail((-32,-3.4),(3,-3.4),4.2)
for x in [-27,-23,-4,0]:
 cube('Built in wood bench',(x,-3.28,.46),(3.5,.64,.16),'Wood',.03)
 for xx in [x-1.4,x+1.4]:cube('Bench plinth',(xx,-3.28,.23),(.15,.48,.45),'Dark metal')
# Multi-level circular glass stair lantern.
cx,cy=-10,-10
for level in range(8):
 z=level*4.2
 arcmesh('Circular floor ring',cx,cy,4.3,6.8,z-.24,z,steps=96)
 # Semi cylindrical meeting room core, visible through circulation glazing.
 arcmesh('Meeting room core glass',cx,cy,4.18,4.22,z+.2,z+3.95,steps=72,ma='Glass')
 for k in range(16):
  t=k*math.tau/16;cyl('Core mullion',(cx+4.23*math.cos(t),cy+4.23*math.sin(t),z+2.05),.032,4.1,'Metal',12)
 # Faceted glazed outer shell with transoms and thin steel ribs.
 for k in range(40):
  a=k*math.tau/40;b=(k+1)*math.tau/40
  mesh('Lantern curved glazing',[(cx+6.85*math.cos(t),cy+6.85*math.sin(t),zz) for zz in [z+.12,z+4.08] for t in [a,b]],[(0,1,3,2)],'Glass')
  beam('Lantern vertical mullion',(cx+6.9*math.cos(a),cy+6.9*math.sin(a),z),(cx+6.9*math.cos(a),cy+6.9*math.sin(a),z+4.2),.055,'Metal')
 arcmesh('Lantern floor transom',cx,cy,6.8,6.99,z-.12,z+.12,ma='Metal')
 arcmesh('Lantern intermediate transom',cx,cy,6.81,6.92,z+2.15,z+2.2,ma='Metal')
 # curved stair climbing 280 degrees per storey, remaining angle is landing
 for k in range(28):
  a=.3+k*4.8/28;b=.3+(k+1)*4.8/28;zz=z+(k+1)*4.2/28
  arcmesh('Circular stair tread',cx,cy,4.65,6.5,zz-.14,zz,a,b,3,'Concrete')
  if k%2==0:
   aa=(cx+6.42*math.cos(a),cy+6.42*math.sin(a),zz);beam('Circular stair baluster',aa,(aa[0],aa[1],aa[2]+1.05),.035,'Metal')
 curve('Circular stair wood rail',[(cx+6.42*math.cos(.3+k*4.8/100),cy+6.42*math.sin(.3+k*4.8/100),z+k*4.2/100+1.1) for k in range(101)],.035,'Wood')
# Circular atrium floor cap roof kept as a separate collection below.

collection('06 Retained house')
# 44 St George: yellow brick, contrasting red bands, steep gable.
cube('Retained house',(34,18,4.75),(6,7,9.5),'Heritage brick YZ')
mesh('Retained house gable',[(37.03,14.5,9.5),(37.03,21.5,9.5),(37.03,18,13.5)],[(0,1,2)],'Heritage brick YZ')
for zz in [1.1,4.6,7.8,9.1]:cube('House red brick stringcourse',(37.08,18,zz),(.06,7,.16),'Red brick YZ')
for yy in [15.9,19.9]:
 for z in [2.7,6.3,9]:
  grid_glass('House tall sash','Y',37.1,yy-.65,yy+.65,z-1.1,z+1.1,1.3,1.1,'Glass','Paper')
  cube('House limestone sill',(37.2,yy,z-1.15),(.25,1.5,.15),'Limestone')
grid_glass('House door','Y',37.14,17.8,18.8,.4,3.3,1,2.9,'Glass','Paper')
text('House address','44',(37.22,18.3,3.52),.22,'Paper',(math.pi/2,0,math.pi/2))
for i in range(4):cube('House entrance step',(38.5-i*.25,18.3,.1+i*.1),(.9,2.2,.2+i*.2),'Concrete')
for sign in [-1,1]:
 o=cube('Steep heritage roof',(34,18+sign*1.75,11.5),(6.5,5.32,.16),'Roof');o.rotation_euler.x=-sign*math.atan2(4,3.5)
beam('House gable bargeboard',(37.35,14.3,9.45),(37.35,18,13.7),.2,'Paper')
beam('House gable bargeboard',(37.35,18,13.7),(37.35,21.7,9.45),.2,'Paper')

collection('07 Roofs')
for x,z,w in [(16.5,12.9,32),(-17,33.8,35)]:
 cube('Atrium skylight',(x,.5,z),(w,11,.04),'Glass')
 for xx in range(int(x-w/2)+1,int(x+w/2),3):cube('Skylight structural rafter',(xx,.5,z-.3),(.16,11,.6),'Paper')
 for yy in [-4.5,-2,.5,3,5.5]:cube('Skylight purlin',(x,yy,z+.08),(w,.075,.14),'Metal')
cube('North roof',(14,17,21.2),(38,22,.4),'Roof')
cube('Upper research roof',(-19,17,33.8),(30,22,.45),'Roof')
cube('Western wing roof',(-28,-13,29.05),(15,18,.45),'Roof')
cyl('Lantern glazed roof',(-10,-10,33.75),6.95,.08,'Glass',96)
for y in [6.1,27.8]:cube('Upper roof parapet',(-19,y,34.1),(30,.25,.85),'Brick XZ')
for x in [-34,-4]:cube('Upper roof parapet',(x,17,34.1),(.25,22,.85),'Brick YZ')
for x in [-26,-18,-10]:cube('Rooftop mechanical equipment',(x,19,34.5),(4,4,1.15),'Metal',.08)

collection('08 Interior details')
# Ground floor patterned terrazzo joints and circulation mats.
for x in range(-32,33,4):cube('Terrazzo brass joint',(x,0,.012),(.004,10,.006),'Roof')
for y in [-3,0,3]:cube('Terrazzo longitudinal joint',(0,y,.013),(64,.004,.006),'Roof')
cube('Entrance walk off mat',(29,-1,.018),(5,5,.025),'Floor dark')
# Floor rail with horizontal dark metal bars visible in sampled video frame.
for x in [-27,-19]:
 for i in range(6):cube('Video landing horizontal guard',(x,-2.9,.24+i*.14),(6.8,.045,.045),'Dark metal')
 for xx in [x-3.4,x,x+3.4]:cube('Video landing guard post',(xx,-2.9,.6),(.06,.06,1.2),'Metal')
 cube('Video bench back',(x,-3.2,.35),(6.8,.24,.7),'Wood')
# Doors and wall/seat bench from preview frame 1.
cube('West room plaster panel',(-30,-4.8,1.7),(3,.15,3.4),'Plaster')
# Seating and cafe tables, wood slat benches in quad.
for x in [-29,-25,10]:
 for i in range(3):
  xx=x+i*.62;cube('Linked red study seat',(xx,5.15,.48),(.48,.45,.075),'Red seat',.05);cube('Linked seat back',(xx,5.38,.78),(.48,.06,.49),'Red seat',.04);beam('Seat support',(xx,5.15,.05),(xx,5.15,.45),.075,'Metal')
for x in [-16,-10,-4,2]:
 cyl('Cafe table',(x,-17,.76),.65,.075,'Paper',32);cyl('Cafe pedestal',(x,-17,.38),.065,.72,'Metal',16);cyl('Cafe table foot',(x,-17,.04),.32,.06,'Metal',24)
 for yy in [-18.1,-15.9]:
  cube('Cafe chair seat',(x,yy,.45),(.46,.44,.07),'Red seat',.04);cube('Cafe chair back',(x,yy+.18,.72),(.46,.05,.5),'Red seat',.03)
  for dx in [-.17,.17]:
   for dy in [-.16,.16]:beam('Cafe chair leg',(x+dx,yy+dy,.03),(x+dx,yy+dy,.43),.025,'Metal')
# Warm practical luminaires, door signs and pinboards.
for x in range(-28,33,8):
 for z in [3.92,8.12,12.32]:cube('Gallery linear luminaire',(x,4.8,z),(2,.28,.06),'Warm light')
 cube('Notice board',(x+1,5.82,1.65),(1,.08,1.05),'Sign blue')
 for k in range(5):cube('Notice paper',(x+.65+(k%3)*.25,5.766,1.4+(k//3)*.32),(.18,.014,.26),'Paper')
for x in [31,-34]:
 cube('EXIT sign',(x,0,2.85),(.15,.64,.24),'Exit green')
 text('Wayfinding exit','EXIT',(x-.09,0,2.85),.15,'Paper',(math.pi/2,0,-math.pi/2))
text('Entry identification','BAHEN CENTRE',(34.03,0,4.8),.37,'Paper',(math.pi/2,0,math.pi/2))
text('University name','UNIVERSITY OF TORONTO',(34.04,0,4.23),.19,'Paper',(math.pi/2,0,math.pi/2))
# Slotted floor grilles.
for x in [-28,-20,-12,-4,4,12,20,28]:
 for k in range(9):cube('Floor displacement vent',(x-.35+k*.085,2.5,.022),(.026,.55,.02),'Dark metal')

collection('09 Landscape')
for x,y in [(36,-20),(36,10),(36,25),(-30,-29),(-23,-29),(-16,-29),(-9,-29),(8,-22)]:
 cube('Tree pit',(x,y,.03),(2.4,2.4,.07),'Soil',.06);cyl('Tree trunk',(x,y,2.4),.13,4.8,'Bark',12)
 for i in range(7):
  a=rng.random()*math.tau;dx=math.cos(a)*rng.uniform(.6,1.65);dy=math.sin(a)*rng.uniform(.6,1.65);zz=rng.uniform(3.7,5.7);beam('Tree branch',(x,y,2.7),(x+dx,y+dy,zz),.055,'Bark');sphere('Tree foliage',(x+dx,y+dy,zz),(1.3,1.2,1.6),'Leaf' if i%2 else 'Leaf light',12,8)
for x in [-28,-19,-10]:
 for k in range(5):cube('Court wood bench slat',(x,-26.5+k*.1,.5),(3.6,.08,.075),'Wood',.01)
 for xx in [x-1.3,x+1.3]:cube('Court bench leg',(xx,-26.3,.25),(.14,.55,.5),'Metal')
# Cycle parking along St George.
for yy in [6.8,8.5,10.2,25,26.7]:
 pts=[(35.7,yy-.5,0),(35.7,yy-.5,.8),(35.7,yy-.4,.92),(35.7,yy+.4,.92),(35.7,yy+.5,.8),(35.7,yy+.5,0)];curve('Bicycle rack',pts,.035,'Metal')

exec(compile((P/'scripts/video_geometry.py').read_text(),str(P/'scripts/video_geometry.py'),'exec'))

exec(compile((P/'scripts/video_spaces.py').read_text(),str(P/'scripts/video_spaces.py'),'exec'))

collection('10 Lighting and cameras')
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='METERS';scene.unit_settings.scale_length=1;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 scene.cycles.device='GPU' if any(d.type=='OPTIX' for d in prefs.devices) else 'CPU'
except Exception:scene.cycles.device='CPU'
world=bpy.data.worlds.new('Toronto daylight');scene.world=world;world.use_nodes=True;nd=world.node_tree.nodes;lk=world.node_tree.links;sky=nd.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_elevation=math.radians(42);sky.sun_rotation=math.radians(145);sky.altitude=.1;nd.get('Background').inputs['Strength'].default_value=.18;lk.new(sky.outputs[0],nd.get('Background').inputs[0])
# Broad interior bounced illumination, preserving visible directional skylight.
for x in [-25,-10,5,20]:area('Atrium skylight fill',(x,0,13.5),1200,7,(.82,.9,1),(x,0,0))
for x in [-28,-12,4,20]:
 for z in [3.7,7.9,12.1]:area('Warm gallery light',(x,5,z),130,2,(1,.78,.48),(x,0,z-2))
area('Entry daylight',(35,-1,9),1500,8,(.88,.95,1),(10,0,3))
area('Court daylight',(-5,-24,16),1700,12,(1,.95,.84),(-10,-4,10))
for name,loc,target,lens in [('atrium_east',(12,-.8,1.75),(32.6,.1,4.9),25),('atrium_west',(16,-.7,1.8),(-12,0,5.3),26),('landing',(18.8,-2.1,5.85),(18.6,6.05,5.7),23),('lantern',(-1,-1,2.0),(-12,-7,16),20),('exterior',(84,-87,62),(-1,1,12),47),('street',(58,-39,20),(30,8,8),38),('overview',(70,-85,78),(-2,0,8),46)]:camera(name,loc,target,lens)
scene.camera=bpy.data.objects['atrium_east'];scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX';scene.view_settings.exposure=.35
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
# Controlled mineral surface contrast; initial generated noise was too coarse.
for name in ['Concrete','Limestone']:
 m=M[name];n=m.node_tree.nodes
 for nn in n:
  if nn.type=='VALTORGB':
   c=m.diffuse_color
   nn.color_ramp.elements[0].color=(*(v*.94 for v in c[:3]),1)
   nn.color_ramp.elements[1].color=(*(v*1.04 for v in c[:3]),1)
  if nn.type=='BUMP':nn.inputs['Distance'].default_value=.0004;nn.inputs['Strength'].default_value=.12
# Hidden light emitters still illuminate but do not draw giant discs in glazing.
for o in bpy.data.objects:
 if o.type=='LIGHT':
  o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False
# Neutral photographic backdrop for exterior presentation, sky kept for lighting.
n=world.node_tree.nodes;l=world.node_tree.links;bg=n.get('Background');out=n.get('World Output');lp=n.new('ShaderNodeLightPath');neutral=n.new('ShaderNodeBackground');neutral.inputs[0].default_value=(.68,.72,.72,1);neutral.inputs[1].default_value=.65;mx=n.new('ShaderNodeMixShader');l.new(lp.outputs['Is Camera Ray'],mx.inputs[0]);l.new(bg.outputs[0],mx.inputs[1]);l.new(neutral.outputs[0],mx.inputs[2]);l.new(mx.outputs[0],out.inputs[0])
exec(compile((P/'scripts/polish_model.py').read_text(),str(P/'scripts/polish_model.py'),'exec'))
# Friendly initial Blender view.
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  a.spaces.active.region_3d.view_distance=100;a.spaces.active.region_3d.view_location=(0,0,12)
scene['evidence']='Full video GGaJsGu_5zA downloaded and decoded. Video circulation assembly grounded in 14:30,14:52,16:30 frames. Global registration and hidden geometry inferred.'
scene['scale_note']='Metres. Dimensions and concealed geometry inferred, not survey measured.'
scene['revision']=os.getenv('BAHEN_REV','r01')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'bahen-centre.blend'),compress=True)
(P/'review/scene-stats.json').write_text(json.dumps({'objects':len(bpy.data.objects),'mesh_objects':len([o for o in bpy.data.objects if o.type=='MESH']),'vertices':sum(len(o.data.vertices) for o in bpy.data.objects if o.type=='MESH'),'revision':scene['revision']},indent=2))
print('BAHEN_BUILD_DONE')
