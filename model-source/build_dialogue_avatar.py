import bpy,math,random,os
from math import sin,cos,pi
from mathutils import Vector,Matrix
ROOT='/workspace/scratch/e9ff7d14d887'
OUT=ROOT+'/madhava/app/src/main/assets'
bpy.ops.wm.open_mainfile(filepath=ROOT+'/krishna/Krishna.blend')
source=open(ROOT+'/krishna/create_krishna.py').read()
exec(source[source.index('def finish'):source.index('# Lotus pedestal')])
skin=bpy.data.materials['Blue jade porcelain'];gold=bpy.data.materials['Antique gold'];white=bpy.data.materials['Ivory'];black=bpy.data.materials['Deep brown eyes'];red=bpy.data.materials['Crimson silk']
def empty(n,p,parent=None):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=p
 if parent:attach(o,parent)
 return o
def attach(o,p):
 bpy.context.view_layer.update();w=o.matrix_world.copy();o.parent=p;o.matrix_world=w;bpy.context.view_layer.update()
# Replace the fixed arms with an articulated flute-holding pose.
for o in list(bpy.data.objects):
 if o.name.startswith(('Left arm','Right arm','Left palm','Right palm','Left finger','Right finger','Left thumb','Right thumb','Gold bangle','Bansuri','Flute band','Flute hole','Gold cloth folds')):bpy.data.objects.remove(o,do_unlink=True)
head=empty('Rig_Head',(-.015,0,2.78));bpy.context.view_layer.update()
head_prefix=('Hair mass','Face','Chin','Ear','Side curl','Eye','Iris','Nose','Smile','Vaishnava','Tilak','Gold crown','Crown','Gem pearl','Feather','Peacock','Halo')
for o in list(bpy.data.objects):
 if o.type in {'MESH','CURVE'} and o.name.startswith(head_prefix):attach(o,head)
mouth=uv('Rig_MouthOpen',(-.015,-.299,2.931),(.063,.012,.032),black);attach(mouth,head)
# Fully local transform hierarchy for upper arm, forearm and hand gestures.
def limb(n,a,b,r,parent):
 o=uv(n,(Vector(a)+Vector(b))/2,(r,r,(Vector(b)-Vector(a)).length/2+.035),skin);o.rotation_euler=(Vector(b)-Vector(a)).to_track_quat('Z','Y').to_euler();bpy.context.view_layer.update();attach(o,parent);return o

def arm(n,shoulder,elbow,wrist,palm,up=1,parent=None):
 upper=empty(n+'_Upper',shoulder,parent);bpy.context.view_layer.update()
 fore=empty(n+'_Fore',elbow,upper);bpy.context.view_layer.update()
 hand=empty(n+'_Hand',wrist,fore);bpy.context.view_layer.update()
 limb(n+'_upper_mesh',shoulder,elbow,.102,upper);limb(n+'_fore_mesh',elbow,wrist,.076,fore)
 o=uv(n+'_elbow',elbow,(.082,.080,.09),skin);attach(o,fore)
 o=uv(n+'_palm',palm,(.066,.04,.088),skin);attach(o,hand)
 x,y,z=palm
 for f in range(4):
  fx=x+(f-1.5)*.029;dz=[.14,.18,.165,.12][f]
  o=line(n+'_finger',[(fx,y,z+up*.042),(fx+(f-1.5)*.005,y-.005,z+up*dz*.7),(fx+(f-1.5)*.006,y-.025,z+up*dz)],.0115,skin);attach(o,hand)
 o=line(n+'_thumb',[(x-.053,y,z),(x-.097,y-.025,z+up*.045),(x-.10,y-.045,z+up*.087)],.018,skin);attach(o,hand)
 for dz in [0,-.04*up]:
  o=tor(n+'_bangle',(wrist[0],wrist[1],wrist[2]+dz),.075,.013,gold);attach(o,hand)
 return upper,fore,hand
left=arm('Rig_Left',(-.34,-.02,2.56),(-.65,-.27,2.20),(-.52,-.45,2.42),(-.51,-.46,2.51),1)
right=arm('Rig_Right',(.32,0,2.56),(.57,-.18,2.20),(.36,-.46,2.44),(.36,-.47,2.53),1)
flute=empty('Rig_Flute',(-.51,-.51,2.57),left[2]);bpy.context.view_layer.update()
o=rod('Golden flute',(-.86,-.51,2.57),(.74,-.51,2.57),.025,gold);attach(o,flute)
for x in [-.8,-.61,-.29,.02,.30,.64]:
 o=tor('Flute ornament',(x,-.51,2.57),.028,.007,gold,(0,pi/2,0));attach(o,flute)
for x in [-.23,-.1,.03,.16,.29,.42]:
 o=uv('Flute finger hole',(x,-.535,2.58),(.012,.004,.009),black);attach(o,flute)
# Fingers curl around the flute rather than remaining extended.
for hand in [left[2],right[2]]:
 for o in list(hand.children):
  if '_finger' in o.name:bpy.data.objects.remove(o,do_unlink=True)
 x=-.51 if hand==left[2] else .36
 for j in range(4):
  fx=x+(j-1.5)*.028
  o=line('Holding finger',[(fx,-.46,2.53),(fx,-.49,2.59),(fx,-.54,2.59),(fx,-.54,2.55)],.0115,skin);attach(o,hand)

# Universal-form interpretation following the supplied devotional reference.
cosmic=empty('Cosmic_Form',(0,0,0));bpy.context.view_layer.update()
def tint(n,color):
 m=skin.copy();m.name=n;m.diffuse_color=(*color,1)
 m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*color,1)
 return m
colors=[tint('Universal azure',(.20,.47,.63)),tint('Universal ivory',(.74,.62,.46)),tint('Universal green',(.17,.42,.28)),tint('Universal rose',(.64,.34,.29)),tint('Universal golden',(.68,.47,.20))]
head_parts=[o for o in list(bpy.data.objects) if o.parent==head and not o.name.startswith(('Halo','Feather','Peacock','Rig_Mouth','Chin'))]
for side in [-1,1]:
 for k in range(5):
  center=Vector((side*(.50+.37*k),.24+.10*k,3.12-.08*k));scale=.70-.055*k
  group=empty(f'Cosmic_Head_{side}_{k}',center,cosmic);bpy.context.view_layer.update()
  for orig in head_parts:
   new=orig.copy();new.data=orig.data.copy();bpy.context.collection.objects.link(new);new.name='UniversalFace_'+orig.name
   new.parent=None;new.matrix_world=Matrix.Translation(center)@Matrix.Scale(scale,4)@Matrix.Translation(Vector((.015,0,-3.08)))@orig.matrix_world
   if new.data.materials and new.data.materials[0]==skin:new.data.materials[0]=colors[(k+(side>0))%5]
   attach(new,group)
  # Varied silhouettes: elephant, bearded sage and leonine faces.
  cx,cy,cz=center
  if k==1 and side==-1:
   o=line('Elephant trunk',[(cx,cy-.19,cz+.03),(cx,cy-.23,cz-.16),(cx+.08,cy-.24,cz-.27),(cx+.14,cy-.25,cz-.20)],.065,colors[1]);attach(o,group)
   for sign in [-1,1]:
    o=uv('Elephant ear',(cx+sign*.17,cy-.04,cz+.01),(.09,.033,.13),colors[1]);attach(o,group)
  if k==2:
   for j in range(9):
    t=pi*j/8;o=uv('Sage beard',(cx+.11*cos(t),cy-.17,cz-.08-.09*sin(t)),(.038,.022,.075),white);attach(o,group)
  if k==3 and side==1:
   for j in range(14):
    t=2*pi*j/14;o=uv('Lion mane',(cx+.17*cos(t),cy-.06,cz+.18*sin(t)),(.065,.034,.07),colors[4]);attach(o,group)
   o=uv('Lion muzzle',(cx,cy-.20,cz-.04),(.087,.04,.053),colors[1]);attach(o,group)
 # Eight arms each side, with a spread of identifiable held objects.
 for k in range(8):
  wz=3.12-k*.225;wx=1.14+.57*sin(pi*k/7)
  u,f,h=arm(f'Cosmic_Arm_{side}_{k}',(side*.31,.21,2.53),(side*(.69+.19*sin(pi*k/7)),.12,2.91-k*.15),(side*wx,.02,wz),(side*(wx+.025),-.02,wz+.075),1,cosmic)
  x=side*(wx+.025);y=-.065;z=wz+.25
  def held(o):attach(o,h)
  if k==0:
   held(tor('Cosmic chakra',(x,y,z),.13,.018,gold,(pi/2,0,0)))
   for j in range(12):
    t=2*pi*j/12;held(rod('Chakra spoke',(x,y,z),(x+.13*cos(t),y,z+.13*sin(t)),.005,gold))
  elif k==1:
   held(uv('Cosmic conch',(x,y,z),(.075,.07,.15),white))
   for j in range(4):held(tor('Conch spiral',(x,y,z-.04+j*.027),.063-j*.008,.009,gold))
  elif k==2:
   held(rod('Trident shaft',(x,y,wz),(x,y,z+.35),.013,gold))
   for sign in [-1,0,1]:held(line('Trident prong',[(x,y,z+.15),(x+sign*.09,y,z+.23),(x+sign*.10,y,z+.38)],.014,gold))
  elif k==3:
   held(rod('Sword grip',(x,y,wz),(x,y,z),.017,gold));held(rod('Sword guard',(x-.08,y,z),(x+.08,y,z),.013,gold))
   held(rod('Sword blade',(x,y,z),(x,y,z+.34),.026,white,.004))
  elif k==4:
   held(rod('Mace shaft',(x,y,wz),(x,y,z+.10),.019,gold));held(uv('Mace head',(x,y,z+.16),(.09,.075,.11),gold))
  elif k==5:
   held(line('Bow',[(x-side*.10,y,wz-.12),(x+side*.12,y,wz+.11),(x-side*.10,y,wz+.36)],.019,gold));held(rod('Bow string',(x-side*.10,y,wz-.12),(x-side*.10,y,wz+.36),.003,white))
  elif k==6:
   held(rod('Lotus stem',(x,y,wz),(x,y,z),.009,gold))
   for j in range(7):
    t=2*pi*j/7;held(uv('Pink lotus petal',(x+.055*cos(t),y+.045*sin(t),z),(.035,.027,.08),red))
  else:held(tor('Rosary',(x,y,z),.085,.015,gold,(pi/2,0,0)))
# Serpent canopy and a richly ornamented universal body.
for j in range(7):
 x=(j-3)*.19;z=3.66+.13*(1-abs(j-3)/3)
 o=line('Serpent canopy',[(x,.43,3.25),(x*1.14,.45,z-.10),(x,.39,z)],.038,colors[2]);attach(o,cosmic)
 o=uv('Serpent hood',(x,.37,z),(.079,.038,.12),colors[2]);attach(o,cosmic)
 for sign in [-1,1]:
  o=uv('Serpent eye',(x+sign*.028,.329,z+.025),(.009,.006,.012),gold);attach(o,cosmic)
for zz in [2.43,2.31,2.15,1.96,1.78]:
 o=line('Universal jeweled necklace',[(-.29,-.22,zz+.10),(0,-.30,zz-.09),(.29,-.22,zz+.10)],.016,gold);attach(o,cosmic)
 o=uv('Universal pendant',(0,-.32,zz-.10),(.042,.02,.058),colors[2]);attach(o,cosmic)
for radius in [1.91,1.97,2.02]:
 o=tor('Cosmic aureole',(0,.61,2.28),radius,.01,gold,(pi/2,0,0));attach(o,cosmic)
for j in range(90):
 t=2*pi*j/90;r=2.06;o=rod('Cosmic radiance',(r*cos(t),.63,2.28+r*sin(t)),((r+.11)*cos(t),.63,2.28+(r+.11)*sin(t)),.004,gold);attach(o,cosmic)
# Sun and moon anchor the cosmic field.
o=uv('Cosmic sun',(-1.67,.63,3.94),(.13,.045,.13),gold);attach(o,cosmic)
o=line('Cosmic moon',[(1.64+.14*cos(t),.62,3.94+.14*sin(t)) for t in [pi*.35+i*pi*1.3/20 for i in range(21)]],.025,white);attach(o,cosmic)
# Optimize per material and parent. Keep animatable facial parts independent.
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type in {'MESH','CURVE'} and o.name!='Stage':o.select_set(True)
bpy.ops.object.convert(target='MESH');objects=list(bpy.context.selected_objects)
for o in objects:
 bpy.context.view_layer.objects.active=o
 if len(o.data.polygons)>200:
  mod=o.modifiers.new('Mobile surface','DECIMATE');mod.ratio=.35;bpy.ops.object.modifier_apply(modifier=mod.name)
keep=('Eye','Iris','Smile','Rig_Mouth','Chin')
groups={}
for o in objects:
 if o.name.startswith(keep):continue
 groups.setdefault((o.parent.name if o.parent else '',o.data.materials[0].name),[]).append(o)
for (parent,material),obs in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();obs[0].name=(parent or 'Body')+'_'+material
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if (o.type=='MESH' and o.name!='Stage') or o.type=='EMPTY':o.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT+'/Krishna-dialogue.glb',use_selection=True,export_format='GLB')
# Save editable master and render ordinary + cosmic previews.
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/madhava/model-source/Krishna-dialogue.blend',compress=True)
sc=bpy.context.scene;sc.cycles.samples=20;sc.render.resolution_x=650;sc.render.resolution_y=850;sc.render.resolution_percentage=100
mouth.scale.z*=.06
for o in cosmic.children_recursive:o.hide_render=True
sc.render.filepath=ROOT+'/madhava/build/Krishna-dialogue-preview.png';bpy.ops.render.render(write_still=True)
for o in cosmic.children_recursive:o.hide_render=False
sc.camera.data.ortho_scale=6.25;sc.render.filepath=ROOT+'/madhava/build/Vishwaroopa-preview.png';bpy.ops.render.render(write_still=True)
print('DIALOGUE_AND_COSMIC_EXPORT_COMPLETE')
