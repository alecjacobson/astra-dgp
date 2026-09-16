"""Corrections from second render review, folded into reproducible build."""
from pathlib import Path
p=Path(__file__).with_name('build_model.py');s=p.read_text()
s=s.replace("for i in range(4):\n z=i*4.2", "for i in range(3):\n z=i*4.2")
s=s.replace("for z in [5.2,9.4,13.6]:", "for z in [4.9,9.1]:")
s=s.replace("for k in range(15):cube('Acoustic wood louvre'", "for k in range(18):cube('Acoustic wood louvre'")
s=s.replace("z+.92),(.11,.2,2.12)","z+1.1),(.11,.2,2.5)")
s=s.replace("(18,16.3,29)","(18,12.9,29)")
s=s.replace("6,16.3,33.8", "6,12.9,33.8")
s=s.replace("0,15.8,3.5,3.95", "0,12.8,3.5,3.2")
s=s.replace("0,15.2,3.2,3.8", "0,12.8,3.2,3.2")
s=s.replace("0,15.2,1.2,2.15", "0,12.8,1.2,3.2")
s=s.replace("('atrium_east',(17,-.8,1.7),(32.6,.15,6.6),23)","('atrium_east',(12,-.8,1.75),(32.6,.1,4.9),25)")
s=s.replace("('atrium_west',(16,-.7,1.8),(-12,0,6.4),24)","('atrium_west',(16,-.7,1.8),(-12,0,5.3),26)")
s=s.replace("('landing',(18.6,1.7,5.85),(14,6,5.7),24)","('landing',(19,1,5.85),(18,6.05,5.85),24)")
# Add gallery landing slab to make stair endpoint connected across narrow interstitial gap.
s=s.replace("# Frosted guard along south gallery", """cube('Landing connection to north gallery',(18.8,3.1,4.08),(2.4,3.2,.24),'Floor')
# Frosted guard along south gallery""")
# Heritage facade proportion correction applied only to its collection.
s=s.replace("collection('05 Circulation')", """for o in COL['04 Heritage Koffler wall'].objects:
 if not o.name.startswith(('Koffler context','Koffler exterior')):
  o.location.z*=.83;o.scale.z*=.83
collection('05 Circulation')""")
s=s.replace("# Hidden light emitters still", """# Controlled mineral surface contrast; initial generated noise was too coarse.
for name in ['Concrete','Limestone']:
 m=M[name];n=m.node_tree.nodes
 for nn in n:
  if nn.type=='VALTORGB':
   c=m.diffuse_color
   nn.color_ramp.elements[0].color=(*(v*.94 for v in c[:3]),1)
   nn.color_ramp.elements[1].color=(*(v*1.04 for v in c[:3]),1)
  if nn.type=='BUMP':nn.inputs['Distance'].default_value=.0004;nn.inputs['Strength'].default_value=.12
# Hidden light emitters still""")
# Both a view matched to reference and usable complete connected stair landing.
s=s.replace("cube('Upper research roof',(-19,17,32.45)","cube('Upper research roof',(-19,17,33.8)")
s=s.replace("(-19,y,32.75)","(-19,y,34.1)").replace("(x,17,32.75)","(x,17,34.1)").replace("(x,19,33.1)","(x,19,34.5)")
p.write_text(s)
