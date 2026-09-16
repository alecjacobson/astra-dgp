"""Geometry revisions grounded in decoded video; dimensions/overall registration inferred.
Executed by build_model.py with its helper namespace.
Local source-backed assemblies: 14:30 stair, 14:52 room2133, 16:30 curved glass.
"""
collection('11 Video central circulation')
# Remove the earlier speculative continuous spiral and the invented landing doors.
for o in list(bpy.data.objects):
 if o.name.startswith(('Circular ','Core mullion','Meeting room core','Lantern ','Upper landing wall','Landing cream wall','Landing dark skirting','Upper landing wood','Upper door','Upper room')):
  bpy.data.objects.remove(o,do_unlink=True)
bpy.context.view_layer.update()
# Clear obsolete first-draft geometry from the reconstructed circulation zone.
# Context outside this box remains approximate; do not let old columns/rails pierce new walls.
for o in list(bpy.data.objects):
 if o.type not in {'MESH','CURVE','FONT'}:continue
 if any(c.name.startswith(('02','07','09','11')) for c in o.users_collection):continue
 center=o.matrix_world @ (sum((Vector(v) for v in o.bound_box),Vector())/8)
 if -20 < center.x < 7 and -18 < center.y < .6 and 3.65 < center.z < 34:
  bpy.data.objects.remove(o,do_unlink=True)
# Source palette: dark closed risers, speckled treads, blue lower guard and round wood rails.
for args in [('Video door ebony','#191913',.5),('Video cream','#d0cfba',.66),('Video wall','#d5d4c5',.8),('Video riser','#44484b',.36,.4),('Video steel','#52606b',.3,.65),('Video timber','#382c25',.38,0,.0004,True),('Video white light','#fffde8',.2),('Video screen','#5336a2',.35),('Video cork','#393633',.9),('Poster pink','#ba729e',.9),('Poster yellow','#c4bb5b',.9),('Poster blue','#628094',.9),('Video skirting','#252923',.65),('Video tread','#41494a',.28,0,.0003)]:mat(*args)
for name,power in [('Video white light',6),('Video screen',.65)]:
 p=M[name].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=M[name].diffuse_color;p.inputs['Emission Strength'].default_value=power
mat('Video frosted glass','#719db5',.3,.08,0,False,True)
M['Video frosted glass'].node_tree.nodes.get('Principled BSDF').inputs['Transmission Weight'].default_value=.18
# Dense, small aggregate in the illuminated stair treads.
n=M['Video tread'].node_tree.nodes;l=M['Video tread'].node_tree.links;p=n.get('Principled BSDF');tc=n.new('ShaderNodeTexCoord');nt=n.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=175;nt.inputs['Detail'].default_value=2;l.new(tc.outputs['Object'],nt.inputs[0]);ra=n.new('ShaderNodeValToRGB');ra.color_ramp.elements[0].position=.32;ra.color_ramp.elements[0].color=(.012,.02,.025,1);ra.color_ramp.elements[1].position=.7;ra.color_ramp.elements[1].color=(.16,.18,.17,1);l.new(nt.outputs['Fac'],ra.inputs[0]);l.new(ra.outputs[0],p.inputs['Base Color'])
# Register the observed central circulation west of the heritage entrance axis.
OX,OY=-8,-10
OZ=4.2
def V(x,y,z):return (OX+x,OY+y,OZ+z)
def vc(name,loc,dim,ma,bev=0):return cube('Video '+name,V(*loc),dim,ma,bev)
def vb(name,a,b,width,ma,depth=None):return beam('Video '+name,V(*a),V(*b),width,ma,depth)
def tube(name,a,b,r=.032,ma='Video timber'):
 a,b=Vector(V(*a)),Vector(V(*b));return cyl('Video '+name,(a+b)/2,r,(b-a).length,ma,24,b-a)
def vt(name,body,loc,size,ma='Dark metal'):return text('Video '+name,body,V(*loc),size,ma)
def postergroup(x,y,z,w,h,count=27):
 vc('noticeboard',(x,y,z),(w,.065,h),'Video cork')
 rr=random.Random(round(x*731)+53)
 for i in range(count):
  px=x+rr.uniform(-w*.43,w*.43);pz=z+rr.uniform(-h*.43,h*.43);pw=rr.uniform(.14,.28);ph=rr.uniform(.19,.36);ma=['Paper','Paper','Paper','Poster pink','Poster yellow','Poster blue'][i%6]
  o=vc('notice paper',(px,y-.039-i*.0008,pz),(pw,.004,ph),ma);o.rotation_euler.y=rr.uniform(-.12,.12)
  for j in range(rr.randint(3,7)):
   vc('notice printed line',(px,y-.045-i*.0008,pz+ph*.25-j*.025),(pw*.75,.002,.005),'Dark metal')
# A real rectangular stair opening: separate floor strips, no filled slab under guard.
vc('central east floor',(4,-.75,-.14),(8,6.5,.28),'Floor')
vc('central approach floor',(-2,-1.9,-.14),(4,3.8,.28),'Floor')
vc('gallery floor',(6,6.4,-.14),(16,2.8,.28),'Floor')
vc('level below floor',(0,2,-4.34),(17,15,.28),'Floor')
# Short upper gallery from stair to room2133; adjacency observed14:45–16:10.
vc('2133 corridor floor',(10,5,-.14),(10,5.6,.28),'Floor')
# Room frontage at y7.7. Near end visible behind14:30 stair, room2133 farther along gallery.
vc('lobby rear wall',(3.9,5.35,1.7),(4.3,.2,3.4),'Video wall')
postergroup(2.65,5.22,1.65,1.7,2.15,34)
vc('lobby bin',(5.15,4.8,.46),(1.25,.48,.92),'Metal',.025)
vc('recycling purple top',(5.15,4.8,.94),(1.3,.53,.1),'Slate purple',.02)
for xx in [4.8,5.15,5.5]:vc('recycling aperture',(xx,4.69,1.0),(.2,.18,.015),'Black')
# Doors are true infill leaves in separately built wall jambs.
D=9.35;DY=7.7
for a,b in [(6.0,7.55),(8.55,8.77),(9.93,13.8)]:
 vc('room2133 plaster',( (a+b)/2,DY,1.7),(b-a,.2,3.4),'Video wall')
 vc('room2133 black base',((a+b)/2,DY-.12,.058),(b-a,.045,.116),'Video skirting')
vc('room2133 header',(10.0,DY,3.08),(7.8,.2,.64),'Video wall')
for center,width,material,name in [(D,1.1,'Video cream','2133 cream door'),(8.05,.94,'Video door ebony','adjacent timber door')]:
 vc(name,(center,DY-.025,1.38),(width,.065,2.76),material,.006)
 for x in [center-width/2-.026,center+width/2+.026]:vc('narrow door frame',(x,DY-.079,1.4),(.046,.04,2.8),'Video cream')
 vc('door frame head',(center,DY-.079,2.79),(width+.10,.04,.045),'Video cream')
 x=center+width*.40
 vc('card lever backplate',(x,DY-.085,1.10),(.071,.026,.28),'Metal',.005)
 vc('black card inset',(x,DY-.101,1.135),(.041,.009,.16),'Black',.003)
 tube('silver lever',(x,DY-.157,1.015),(x-.14,DY-.157,1.015),.015,'Metal')
 tube('lever neck',(x,DY-.09,1.015),(x,DY-.157,1.015),.022,'Metal')
vt('room number2133','2133',(D+.18,DY-.065,1.60),.065,'Black')
vc('door wall plaque',(8.62,DY-.13,1.58),(.16,.017,.25),'Metal')

# Projecting monitor: actual purple content is abstracted, architecture is modeled.
vc('monitor mount',(11.89,DY-.17,2.10),(.28,.3,.2),'Black')
vc('monitor black housing',(11.89,DY-.35,2.1),(.98,.11,.66),'Black',.018)
vc('monitor violet screen',(11.89,DY-.412,2.10),(.92,.009,.59),'Video screen')
vt('monitor heading','DEPARTMENT OF COMPUTER SCIENCE',(11.89,DY-.423,2.29),.034,'Paper')
vt('monitor second line','NEWS AND EVENTS',(11.89,DY-.423,2.22),.031,'Paper')
for k in range(5):vc('monitor text line',(11.85,DY-.423,2.15-k*.04),(.75-k*.035,.002,.008),'Paper')
postergroup(12.99,DY-.15,1.37,.93,2.08,36)
vc('low wall outlet',(12.03,DY-.125,.30),(.053,.016,.095),'Metal',.004)
for z in [.28,.32]:vc('outlet socket',(12.03,DY-.136,z),(.022,.006,.024),'Black')
# Illuminated stair rises away to a turning landing; closed risers and round projecting rails.
def litflight(x,y,z,run=3.92,rise=2.1,n=14,width=1.82):
 before_flight=set(bpy.data.objects)
 for i in range(n):
  h=rise*(i+1)/n;yy=y+run*i/n
  vc('central stair closed riser',(x,yy+.025,z+h-rise/n/2),(width,.075,rise/n),'Video riser')
  vc('central terrazzo tread',(x,yy+run/n/2,z+h-.025),(width+.025,run/n+.035,.05),'Video tread',.007)
  # Lamp sits on riser, slightly right of centre as observed in14:30.
  vc('riser lamp bezel',(x+.35,yy-.018,z+h-rise/n*.56),(.28,.013,.092),'Metal',.004)
  vc('riser luminaire',(x+.35,yy-.027,z+h-rise/n*.56),(.23,.008,.06),'Video white light' if i%5!=0 else 'Concrete',.003)
  if i%5==0:
   for j in range(4):vc('riser vent slit',(x+.35,yy-.033,z+h-rise/n*.56-.022+j*.014),(.21,.002,.003),'Dark metal')
 for side in [-1,1]:
  xx=x+side*(width/2+.045)
  vb('inclined steel stringer',(xx,y,z-.09),(xx,y+run,z+rise-.09),.11,'Video steel',.20)
  for i in range(5):
   yy=y+run*i/4;zz=z+rise*i/4;vb('stair guard newel',(xx,yy,zz-.02),(xx,yy,zz+1.02),.055,'Video steel',.075)
   if i<4:
    dy=run/4;dz=rise/4
    mesh('Video clear stair guard',[V(xx,yy+.025,zz+.16),V(xx,yy+dy-.025,zz+dz+.16),V(xx,yy+dy-.025,zz+dz+.94),V(xx,yy+.025,zz+.94)],[(0,1,2,3)],'Glass')
  tube('round projecting stair handrail',(xx,y-.24,z+1.05),(xx,y+run+.19,z+rise+1.15),.036)
 for o in set(bpy.data.objects)-before_flight:o['source_flight_base']=z
 return z+rise
litflight(-2,0,0)
vc('central intermediate landing',(-2,4.62,1.96),(2.1,1.4,.28),'Floor')
# Second straight flight turns around the curved frontage; local90deg turn remains inferred.
before=set(bpy.data.objects)
litflight(-2,5.35,2.1)
bpy.context.view_layer.update()
from mathutils import Matrix
pivot=Vector(V(-2,5.35,0));rot=Matrix.Rotation(math.pi/2,4,'Z')
for o in set(bpy.data.objects)-before:o.matrix_world=Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)@o.matrix_world
vc('upper level landing',(-6.65,5.35,4.06),(1.6,2.1,.28),'Floor')
# Adjacent descending flight visible through the horizontal guard.
litflight(.4,0,-2.1)
def sourceguard(a,b,z):
 a,b=Vector(a),Vector(b);d=b-a;count=max(1,round(d.length/1.35))
 for i in range(count):
  aa=a+d*i/count;bb=a+d*(i+1)/count
  for lo,hi,ma in [(.13,.85,'Video frosted glass'),(.85,1.28,'Glass')]:
   mesh('Video level guard '+ma,[V(aa.x,aa.y,z+lo),V(bb.x,bb.y,z+lo),V(bb.x,bb.y,z+hi),V(aa.x,aa.y,z+hi)],[(0,1,2,3)],ma)
 for i in range(count+1):
  pt=a+d*i/count;vb('level guard post',(pt.x,pt.y,z),(pt.x,pt.y,z+.94),.045,'Video steel')
 tube('level round rail',(a.x,a.y,z+.97),(b.x,b.y,z+.97),.033)
sourceguard((-.9,2.5),(3.9,2.5),0)
vc('side path beside void',(5.9,4.1,-.14),(4,3.2,.28),'Floor')
vc('descending stair arrival',(.4,4.8,-.14),(2.1,1.7,.28),'Floor')
# Curved glazed enclosure seen16:20–16:45; straight flights are outside it.
for level in range(8):
 z=level*4.2-4.2
 for k in range(25):
  a=-math.pi*.52+k*math.pi*1.25/25;b=-math.pi*.52+(k+1)*math.pi*1.25/25
  cx,cy=-6.8,1.0;r=3.83
  mesh('Video curved glass core',[V(cx+r*math.cos(t),cy+r*math.sin(t),zz) for zz in [z,z+4.2] for t in [a,b]],[(0,1,3,2)],'Glass')
  aa=(cx+r*math.cos(a),cy+r*math.sin(a))
  vb('core narrow mullion',(aa[0],aa[1],z),(aa[0],aa[1],z+4.2),.045,'Video steel')
  for zz in [z+.12,z+2.05,z+4.07]:
   vb('core transom',(aa[0],aa[1],zz),(cx+r*math.cos(b),cy+r*math.sin(b),zz),.055,'Video steel')
# Dark framed screen behind the foot of the stair, with clear transoms above.
for xx in [-3.3,-1.65,0,1.65]:
 vc('lobby screen upright',(xx,5.9,1.75),(.09,.13,3.5),'Video steel')
for zz in [2.38,2.9,3.35]:vc('lobby screen transom',(-.8,5.9,zz),(5.1,.13,.085),'Video steel')
# Ground/upper light around central circulation. Local ceiling only over wall/gallery.
vc('gallery low ceiling',(5,6.5,3.42),(18,3.5,.17),'Plaster')
vc('lobby fascia',(.0,5.1,3.65),(8,.22,.55),'Video steel')
for x in [2,5,8,11,13]:
 vc('rectangular pendant housing',(x,6.5,3.20),(.72,.35,.13),'Metal')
 vc('rectangular pendant diffuser',(x,6.5,3.124),(.63,.3,.012),'Video white light')
 area('Video gallery light',V(x,6.25,3.15),65,1.0,(.95,1,.88),V(x,6.3,0))
area('Video central soft light',V(0,-2,7),300,5,(.78,.9,1),V(-1,3,1))
area('Video camera fill',V(4,-2,2.8),55,3,(.93,1,.9),V(4,6,1))
# 892 camera crops the top of door; anchor layout follows full source frame.
camera('video_1452',V(9.0,3.15,1.60),V(10.42,7.7,1.32),38)
camera('video_1430',V(-3.5,-2.8,1.60),V(3.5,6.5,.8),24)
camera('video_central',V(8,-6,6.1),V(-1,3,3),28)

# Repeated upper circulation follows the floor4–8 tour; exact registration is inferred.
bpy.context.view_layer.update()
flight_parts=[o for o in COL['11 Video central circulation'].objects if o.get('source_flight_base',-9)>=0 or o.name.startswith(('Video central intermediate','Video upper level landing'))]
for level in [-1,1,2,3,4,5]:
 dz=level*4.2
 for src in flight_parts:
  o=src.copy();o.data=src.data.copy();COL['11 Video central circulation'].objects.link(o);o.location.z+=dz;o.name=src.name+' inferred repeated storey'+str(level+2)
for level in range(1,7):
 z=level*4.2
 vc('upper circulation gallery',(2,6.5,z-.14),(17,2.8,.28),'Floor')
 sourceguard((-6.5,5.15),(1,5.15),z)
 vc('upper corridor rear wall',(7.5,7.85,z+1.6),(6,.2,3.2),'Video wall')
 vc('upper corridor ceiling',(7.5,6.5,z+3.4),(6,3,.2),'Plaster')
 for x in [5.4,7.4,9.4]:
  vc('upper office door',(x,7.72,z+1.18),(.85,.07,2.36),'Video timber')
  vt('upper office number',str((level+2)*1000+133+round(x)),(x,7.672,z+1.65),.07,'Paper')
 vc('upper lamp',(7,6.5,z+3.25),(1.2,.4,.1),'Video white light')

# Real pane thickness prevents half-space refraction artifacts from open single faces.
for o in COL['11 Video central circulation'].objects:
 if o.type=='MESH' and o.name.startswith(('Video clear stair guard','Video level guard','Video curved glass core')):
  mod=o.modifiers.new('Glass pane thickness','SOLIDIFY');mod.thickness=.012

# Source sloped guards are clear, with little blur.
M['Glass'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.012
