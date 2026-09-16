"""Additional actual-video corrections: street00:30, entry03:30, theatre06:30/07:30.
Location and measured dimensions are inferred; visible typologies from source frames.
"""
collection('12 Video street and entry')
# Replace generic ribbon frontage with observed broad masonry plane and double-height louvre bay.
for o in list(bpy.data.objects):
 if o.name.startswith(('Street facing masonry','East recessed window','East north wall backing')):bpy.data.objects.remove(o,do_unlink=True)
# Front block y5..22, raised over recessed glazed ground floor.
for yy0,yy1,zz0,zz1 in [(5,22,3.5,4.8),(5,22,12.1,16.6),(5,9.6,4.8,12.1),(17.4,22,4.8,12.1)]:
 cube('Video east broad masonry',(33.4,(yy0+yy1)/2,(zz0+zz1)/2),(.6,yy1-yy0,zz1-zz0),'Brick YZ')
grid_glass('Video ground recessed curtain wall','Y',32.78,5,22,.3,3.5,1.4,3.2)
for yy in [5.3,8.1,10.9,13.7,16.5,19.3,21.7]:cyl('Video slender street columns',(33.25,yy,1.8),.10,3.5,'Limestone',20)
cube('Video black plinth',(33.45,13.5,.29),(.4,17,.58),'Dark metal')
grid_glass('Video large upper glass bay','Y',33.77,9.6,17.4,4.8,12.1,2.6,3.65)
mat('Video louvre glass','#8faaa0',.25,.22)
for z in [5.02+i*.43 for i in range(17)]:
 o=cube('Video street horizontal glass louvre',(34.13,13.5,z),(.62,7.75,.07),'Video louvre glass');o.rotation_euler.y=math.radians(-12)
for yy in [9.6,12.2,14.8,17.4]:cube('Video louvre fin support',(34.15,yy,8.45),(.12,.065,7.5),'Metal')
# Inset small punched windows through backing (boolean differences on masonry panels).
def punch(y,z,w,h):
 cutter=cube('Window opening temporary',(33.4,y,z),(2,w,h),'Black')
 bpy.context.view_layer.update()
 for o in list(COL['12 Video street and entry'].objects):
  if not o.name.startswith('Video east broad masonry'):continue
  mod=o.modifiers.new('Punched opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter
  bpy.context.view_layer.objects.active=o
  bpy.ops.object.modifier_apply(modifier=mod.name)
 bpy.data.objects.remove(cutter,do_unlink=True)
 grid_glass('Video punched street window','Y',33.68,y-w/2,y+w/2,z-h/2,z+h/2,w,h)
punch(7.0,6.75,2.0,2.0);punch(20.0,6.75,2.0,2.0);punch(18.9,11.75,.75,2.2)
cube('Video engineering banner',(34.0,8.8,6.8),(.06,1.7,2.05),'Slate purple')
text('Video engineering sign','Engineering\nScience',(34.045,8.8,6.65),.24,'Paper',(math.pi/2,0,math.pi/2))
# House is farther along street than the first-draft repetitive facade implied.
for o in COL['06 Retained house'].objects:o.location.y+=8
# Broad plum entrance mat wraps around the north stair/column as seen03:30.
mat('Video plum mat','#66606a',.97)
for o in list(bpy.data.objects):
 if o.name.startswith('Entrance walk off mat'):bpy.data.objects.remove(o,do_unlink=True)
pts=[(31.8,-4.7,.024),(22,-4.7,.024),(22,3.15,.024),(26.5,3.15,.024),(27.5,2.7,.024),(28.4,2,.024),(29.2,1.35,.024),(30,1.2,.024),(31.8,1.3,.024)]
mesh('Video curved entry mat',pts,[tuple(range(len(pts)))],'Video plum mat')
# Metal collars catch light at the bases of the pale cylindrical entry columns.
for x in [12,20,28]:cyl('Video column metal foot',(x,3.3,.11),.389,.22,'Metal',40)
# Street trees were leafless in source. Preserve trunks and branches; no summer crowns.
for o in list(COL['09 Landscape'].objects):
 if o.name.startswith('Tree foliage') and o.location.x>34:bpy.data.objects.remove(o,do_unlink=True)
camera('video_0030',(60,10,1.75),(33.4,10,2.5),31)
camera('video_0330',(31,2.0,1.7),(12,0,.7),24)

collection('13 Video lecture theatre')
# Room fitted into the north wing. Carve the double-height interior out of intermediate slab.
cut=cube('Theatre void cutter',(20,18,4.3),(22,18,7.9),'Black')
bpy.context.view_layer.update()
for o in list(bpy.data.objects):
 if o.name.startswith('North wing floor') and 1<o.location.z<8:
  mod=o.modifiers.new('Double height theatre void','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cut,do_unlink=True)
mat('Video bright aluminum','#c5cacb',.25,.6)
mat('Theatre desk','#302322',.34,0,.0005,True);mat('Theatre seat','#dad9df',.38);mat('Theatre chalkboard','#34383f',.8);mat('Theatre wall','#bfc0bb',.85)
# Local x transverse, y front-to-back, z at ground. Front teaching wall y9.4.
TX,TY=20,10
def th(n,l,d,m,b=0):return cube('Theatre '+n,(TX+l[0],TY+l[1],l[2]),d,m,b)
th('front wall',(0,-.8,3.6),(21,.25,7.2),'Theatre wall')
th('back wall',(0,16.5,4.1),(21,.2,8.2),'Theatre wall')
for x in [-10.4,10.4]:th('side wall',(x,7.9,3.6),(.2,17,7.2),'Theatre wall')
# Eight raked rows, narrow steps in the side aisle; white individual seat backs.
for row in range(9):
 y=3+row*1.25;z=row*.32
 for a,b in [(-10,-5.725),(-4.075,10)]:th('raked platform',((a+b)/2,y+.4,z/2-.16),(b-a,1.25,.32+z),'Floor dark')
 for side,(a,b) in enumerate([(-8.8,-5.8),(-4.0,9.0)]):
  mid=(a+b)/2
  th('continuous desk top',(mid,y,z+.77),(b-a,.39,.06),'Theatre desk',.016)
  th('desk modesty panel',(mid,y+.14,z+.43),(b-a,.055,.58),'Theatre desk',.009)
  for x in [a+.3,b-.3]:th('desk support',(x,y,z+.38),(.035,.08,.72),'Dark metal')
  for k in range(int((b-a)/.68)):
   x=a+.37+k*.68
   th('white seat back',(x,y+.76,z+.67),(.52,.065,.37),'Theatre seat',.10)
   th('white seat',(x,y+.58,z+.43),(.5,.43,.065),'Theatre seat',.06)
   th('seat pedestal',(x,y+.58,z+.21),(.045,.08,.42),'Metal')
 for j in range(2):
  th('aisle half step',(-4.9,y-.225+j*.625,z-.16+j*.16),(1.65,.625,.32),'Floor dark')
  th('aisle nosing',(-4.9,y-.526+j*.625,z+.006+j*.16),(1.65,.025,.015),'Metal')
# Three banks of vertically sliding dark chalkboards, silver frames and chalk trays.
for x in [-3.1,0,3.1]:
 for z in [1.2,3.18]:
  th('chalkboard',(x,-.61,z),(2.96,.07,1.86),'Theatre chalkboard')
  for xx in [x-1.5,x+1.5]:th('chalkboard vertical track',(xx,-.55,z),(.046,.13,1.98),'Video bright aluminum')
  for zz in [z-.95,z+.95]:th('chalkboard horizontal frame',(x,-.55,zz),(3.02,.09,.038),'Video bright aluminum')
  th('chalkboard pull',(x,-.46,z-.9),(.22,.04,.032),'Paper',.008)
 th('chalk tray',(x,-.39,.22),(3.02,.32,.065),'Metal')
th('wood lectern',(-6.8,.6,.57),(1.5,.72,1.14),'Door wood',.015)
th('lectern sloped top',(-6.8,.6,1.19),(1.58,.85,.07),'Theatre desk',.012)
# High clerestory over board wall; broad daylight slit not solid low slab.
th('upper front wall',(0,-.8,6.45),(21,.2,1.5),'Theatre wall')
th('skylight glass',(0,.7,7.1),(11,2.1,.04),'Glass')
for x in range(-5,6):th('skylight rib',(x,.7,7.07),(.08,2.1,.12),'Paper')
th('ceiling',(0,9.4,7.1),(21,15,.18),'Theatre wall')
for y in [4,8,12]:
 for x in [-7,0,7]:
  th('ceiling diffuser',(x,y,6.99),(1.3,.35,.06),'Video white light')
  area('Theatre light',(TX+x,TY+y,6.8),130,2,(1,.93,.85),(TX+x,TY+y,0))
area('Theatre board daylight',(TX,TY+.5,6.9),1000,7,(.86,.91,1),(TX,TY,2))
camera('video_0630',(TX-6.1,TY+3,2.6),(TX-.8,TY+8,1.1),28)
camera('video_0730',(TX-5.6,TY+3.6,1.7),(TX,TY-.5,2.85),22)

collection('12 Video street and entry')
# Glazed street doors sit at the outer face of the entry bay, under its canopy.
for yy in [-2.7,-1.5,-.3,.9]:
 cube('Video outer entrance door',(34.02,yy,1.35),(.055,1.16,2.7),'Glass')
 for y in [yy-.58,yy+.58]:cube('Video outer door silver stile',(34.09,y,1.35),(.10,.065,2.7),'Metal')
 for z in [.1,.48,2.65]:cube('Video outer door silver rail',(34.09,yy,z),(.10,1.16,.075),'Metal')
 beam('Video outer door pull',(34.17,yy+.38,1.05),(34.17,yy+.38,1.6),.026,'Metal')
 cube('Video outer door kick plate',(34.09,yy,.27),(.085,1.08,.33),'Metal')
for yy in [-3.6,3.6]:cyl('Video entry polished dark column',(34.45,yy,1.75),.33,3.5,'Dark metal',36)
cube('Video canopy dark front edge',(37.15,.2,3.5),(.10,10,.22),'Dark metal')

# Flat low ceiling over the wall side of the stair lobby, open above the stair itself.
collection('11 Video central circulation')
vc('central low ceiling',(6.6,3.8,3.4),(14.2,11.6,.18),'Plaster')
# Source theatre chairs have rounded top corners; construct their actual profile.
for o in list(COL['13 Video lecture theatre'].objects):
 if not o.name.startswith('Theatre white seat back'):continue
 loc=o.location.copy();bpy.data.objects.remove(o,do_unlink=True)
 w,h,r=.52,.37,.14;outline=[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2-r)]
 for i in range(9):
  t=i*math.pi/16;outline.append((w/2-r+r*math.cos(t),h/2-r+r*math.sin(t)))
 outline.append((-w/2+r,h/2))
 for i in range(9):
  t=math.pi/2+i*math.pi/16;outline.append((-w/2+r+r*math.cos(t),h/2-r+r*math.sin(t)))
 n=len(outline);vs=[(x,y,z) for y in [-.032,.032] for x,z in outline];fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 collection('13 Video lecture theatre');o=mesh('Theatre rounded white seat back',vs,fs,'Theatre seat');o.location=loc;bevel(o,.009)

# True openings for the entry-side flights shifted behind the foreground columns.
collection('12 Video street and entry')
for x,z in [(23.5,4.2),(14.1,8.4)]:
 cut=cube('Entry gallery stairwell cutter',(x,4.8,z),(7.2,2.0,1),'Black')
 bpy.context.view_layer.update()
 for o in list(bpy.data.objects):
  if o.name.startswith('North gallery floor') and abs(o.location.z-(z-.17))<.1:
   mod=o.modifiers.new('Entry stairwell opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 bpy.data.objects.remove(cut,do_unlink=True)
