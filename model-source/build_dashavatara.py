import bpy, math, os
from mathutils import Vector,Matrix
from math import pi,sin,cos
ROOT='/workspace/scratch/e9ff7d14d887/madhava';OUT=ROOT+'/app/src/main/assets/forms';os.makedirs(OUT,exist_ok=True)
def mat(n,c,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.36;return m
blue=mat('Vishnu blue',(.16,.43,.61));gold=mat('Sacred gold',(.74,.43,.08),.7);yellow=mat('Golden silk',(.93,.58,.06));red=mat('Crimson',(.55,.025,.04));white=mat('Ivory',(.88,.84,.69));black=mat('Hair and eyes',(.026,.018,.012));orange=mat('Saffron',(.85,.23,.025));green=mat('Lotus green',(.05,.28,.14));brown=mat('Boar brown',(.25,.13,.055));tan=mat('Human skin',(.61,.36,.19));shell=mat('Tortoise shell',(.19,.23,.13),.15);tawny=mat('Lion tawny skin',(.61,.30,.065));ember=mat('Fierce amber eyes',(.95,.19,.015));stone=mat('Teal pedestal',(.035,.12,.12),.4)
def world(o):return world(o.parent)@o.matrix_parent_inverse@o.matrix_basis if o.parent else o.matrix_basis.copy()
def parent(o,p):
 if p:
  w=world(o);o.parent=p;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=world(p).inverted()@w
 return o
def finish(o,n,m,p=None):
 o.name=n;o.data.materials.clear();o.data.materials.append(m)
 if o.type=='MESH':
  for f in o.data.polygons:f.use_smooth=True
 return parent(o,p)
def empty(n,pos=(0,0,0),p=None):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=pos;return parent(o,p)
def uv(n,pos,size,m,p=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=pos);o=bpy.context.object;o.scale=size;return finish(o,n,m,p)
def rod(n,a,b,r,m,p=None,r2=None):
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cone_add(vertices=20,radius1=r,radius2=r if r2 is None else r2,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return finish(o,n,m,p)
def line(n,pts,r,m,p=None):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for b,q in zip(sp.points,pts):b.co=(*q,1)
 o=bpy.data.objects.new(n,c);bpy.context.collection.objects.link(o);return finish(o,n,m,p)
def ring(n,pos,r,m,p=None,rot=(pi/2,0,0),minor=.018):
 bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=8,major_radius=r,minor_radius=minor,location=pos,rotation=rot);return finish(bpy.context.object,n,m,p)
def base():
 rod('Lotus foundation',(0,0,.04),(0,0,.15),.67,stone)
 for j in range(12):
  t=j*pi/6;o=uv('Lotus petal',(.48*cos(t),.48*sin(t),.18),(.23,.10,.075),gold);o.rotation_euler.z=t

def crown(h,z=3.05):
 ring('Crown rim',(0,0,z),.265,gold,h,(0,0,0),.025)
 rod('Golden crown',(0,0,z),(0,0,z+.39),.265,gold,h,.055)
 for j in range(9):
  t=2*pi*j/9;uv('Crown jewel',(.247*cos(t),.247*sin(t),z+.035),(.033,.033,.033),red,h)
 uv('Crown finial',(0,0,z+.43),(.057,.057,.065),gold,h)
def face(h,m=blue,kind='human',z=2.83):
 uv('Face',(0,-.02,z),(.25,.22,.30),m,h);uv('Hair',(0,.05,z+.08),(.255,.23,.28),black,h)
 for side in [-1,1]:
  uv('Ear',(side*.25,0,z),(.05,.04,.08),m,h)
  uv('Eye ivory',(side*.09,-.216,z+.04),(.056,.018,.029),white,h);uv('Iris',(side*.09,-.234,z+.04),(.02,.011,.021),black,h)
  line('Brow',[(side*.045,-.236,z+.10),(side*.09,-.238,z+.116),(side*.14,-.22,z+.10)],.011,black,h)
 uv('Nose',(0,-.239,z-.024),(.04,.035,.064),m,h)
 uv('Rig_MouthOpen',(0,-.227,z-.13),(.055,.012,.027),black,h)
 line('Lower lip',[(-.052,-.235,z-.15),(0,-.242,z-.16),(.052,-.235,z-.15)],.009,red,h)
 if kind!='buddha':
  line('Tilak',[(-.025,-.216,z+.22),(-.018,-.234,z+.14),(0,-.24,z+.13),(.018,-.234,z+.14),(.025,-.216,z+.22)],.009,white,h)
  for side in [-1,1]:ring('Earring',(side*.255,-.01,z-.10),.06,gold,h)
 if kind=='boar':
  uv('Boar muzzle',(0,-.30,z-.035),(.14,.19,.10),m,h)
  for side in [-1,1]:
   uv('Nostril',(side*.045,-.48,z-.02),(.026,.018,.018),black,h)
   line('Ivory tusk',[(side*.105,-.36,z-.12),(side*.16,-.39,z-.07),(side*.19,-.37,z+.035)],.022,white,h)
 if kind=='lion':
  for j in range(20):
   t=2*pi*j/20;uv('Lion mane',(.31*cos(t),.035,z+.37*sin(t)),(.095,.095,.12),brown,h)
  uv('Lion muzzle',(0,-.30,z-.03),(.12,.085,.075),white,h)
  uv('Lion nose',(0,-.36,z+.015),(.045,.027,.032),black,h)
  for side in [-1,1]:rod('Fang',(side*.065,-.36,z-.09),(side*.065,-.36,z-.17),.015,white,h,.004)
def arm(side,shoulder,elbow,wrist,palm,m=blue):
 n='Rig_Left' if side==-1 else 'Rig_Right';u=empty(n+'_Upper',shoulder);f=empty(n+'_Fore',elbow,u);h=empty(n+'_Hand',wrist,f)
 rod('Upper arm',shoulder,elbow,.081,m,u);uv('Elbow',elbow,(.087,.087,.087),m,f);rod('Forearm',elbow,wrist,.063,m,f);uv('Palm',palm,(.057,.035,.079),m,h)
 for j in range(4):
  x=palm[0]+(j-1.5)*.026;rod('Finger',(x,palm[1],palm[2]+.03),(x,palm[1]-.012,palm[2]+.13-(abs(j-1.5)*.015)),.010,m,h)
 rod('Thumb',(palm[0]-.055,palm[1],palm[2]),(palm[0]-.085,palm[1]-.02,palm[2]+.056),.016,m,h)
 ring('Wrist bracelet',wrist,.071,gold,h,(0,0,0),.01)
 return h

def humanoid(kind,m=blue,robe=yellow,scale=1):
 base();uv('Torso',(0,0,2.0),(.34,.19,.48),m)
 for side in [-1,1]:
  uv('Dhoti leg',(side*.135,.02,.97),(.17,.18,.72),robe)
  uv('Foot',(side*.16,-.13,.30),(.095,.19,.085),m)
 rod('Waist silk',(0,0,1.49),(0,0,1.66),.34,robe,None,.32)
 rod('Neck',(0,0,2.32),(0,0,2.59),.092,m)
 h=empty('Rig_Head',(0,0,2.57));face(h,m,kind)
 if kind not in ['buddha','sage','vamana']:crown(h)
 if kind in ['sage','vamana']:
  uv('Topknot',(0,.04,3.18),(.10,.10,.13),black,h)
  for j in range(7 if kind=='sage' else 0):uv('Sage beard',((j-3)*.045,-.18,2.60),(.035,.037,.12),white,h)
 if kind=='buddha':
  uv('Ushnisha',(0,.04,3.16),(.10,.09,.10),black,h)
  uv('Monastic robe',(-.08,-.01,1.98),(.31,.21,.47),orange)
 else:
  for z in [2.33,2.16]:
   line('Necklace',[(-.24,-.15,z+.05),(0,-.225,z-.09),(.24,-.15,z+.05)],.015,gold)
   uv('Pendant',(0,-.235,z-.10),(.037,.017,.046),red)
 ring('Halo',(0,.32,2.91),.53,gold,h,minor=.013)
 l=arm(-1,(-.28,0,2.3),(-.48,-.08,1.96),(-.47,-.24,2.19),(-.47,-.25,2.28),m)
 r=arm(1,(.28,0,2.3),(.49,-.06,1.94),(.47,-.24,2.18),(.47,-.25,2.27),m)
 return h,l,r

def bow(hand,x=.58):
 line('Royal bow',[(x,-.30,1.60),(x+.20,-.29,2.15),(x,-.30,2.86)],.025,gold,hand)
 rod('Bow string',(x,-.30,1.60),(x,-.30,2.86),.003,white,hand)
 rod('Arrow',(-.68,-.33,2.36),(.69,-.33,2.36),.01,brown)
 rod('Arrowhead',(.66,-.33,2.36),(.79,-.33,2.36),.033,white,None,.001)

def build(name):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 if name in ['matsya','kurma']:
  base()
  if name=='matsya':
   uv('Sacred fish body',(0,0,1.67),(.66,.30,1.12),blue)
   h=empty('Rig_Head',(0,0,2.45));face(h,blue,z=2.66);crown(h,2.89)
   for side in [-1,1]:
    o=uv('Fish tail',(side*.25,0,.57),(.32,.065,.24),gold);o.rotation_euler.y=side*.43
    uv('Fish fin',(side*.62,.005,1.75),(.30,.05,.17),gold)
   for k in range(8):line('Fish scale band',[(-.40,-.27,.91+k*.17),(0,-.30,.87+k*.17),(.40,-.27,.91+k*.17)],.008,gold)
  else:
   uv('Tortoise shell',(0,.05,1.19),(.75,.55,.43),shell)
   for k in range(3):ring('Shell patterned band',(0,.05,1.40+k*.04),.50-k*.10,gold,None,(0,0,0),.012)
   h=empty('Rig_Head',(0,-.39,1.0));uv('Tortoise head',(0,-.55,1.04),(.24,.27,.20),blue,h)
   for side in [-1,1]:
    uv('Eye ivory',(side*.13,-.74,1.12),(.04,.018,.034),white,h);uv('Iris',(side*.13,-.756,1.12),(.018,.01,.021),black,h)
    for y in [-.24,.38]:uv('Tortoise flipper',(side*.63,y,.97),(.30,.14,.075),blue)
   uv('Rig_MouthOpen',(0,-.802,1.0),(.06,.012,.021),black,h)
   rod('Mandara mountain',(0,.08,1.46),(0,.08,2.68),.35,brown,None,.025)
   ring('Mountain cloud',(0,.08,2.16),.38,white,None,(0,0,0),.037)
   line('Ocean serpent',[(.39*cos(i*pi/12),.08+.39*sin(i*pi/12),1.57+i*.011) for i in range(73)],.027,gold)
 elif name=='varaha':
  h,l,r=humanoid('boar',brown)
  uv('Earth globe',(-.47,-.29,2.56),(.18,.18,.18),blue,l)
  for q in [(-.52,-.44,2.61),(-.40,-.42,2.52),(-.53,-.40,2.48)]:uv('Earth land',q,(.064,.033,.055),green,l)
 elif name=='narasimha':
  h,l,r=humanoid('lion',tawny)
  bpy.data.objects['Torso'].scale=(.46,.25,.48)
  for o in list(bpy.context.scene.objects):
   if o.name.startswith(('Eye ivory','Iris','Brow','Rig_MouthOpen','Lower lip','Lion mane','Fang')):bpy.data.objects.remove(o,do_unlink=True)
   elif o.name.startswith('Upper arm'):o.scale.x*=1.65;o.scale.y*=1.65
   elif o.name.startswith('Forearm'):o.scale.x*=1.45;o.scale.y*=1.45
   elif o.name.startswith('Dhoti leg'):o.scale.x*=1.3
  for side in [-1,1]:
   uv('Pectoral muscle',(side*.205,-.19,2.20),(.23,.14,.16),tawny)
   uv('Deltoid muscle',(side*.36,-.015,2.31),(.16,.15,.17),tawny)
   uv('Biceps muscle',(side*.41,-.07,2.12),(.13,.11,.19),tawny)
   for z in [1.99,1.84,1.70]:uv('Abdominal muscle',(side*.105,-.226,z),(.105,.052,.08),tawny)
   eye=uv('Eye ivory',(side*.10,-.224,2.89),(.071,.018,.023),white,h);eye.rotation_euler.y=side*.26
   uv('Iris',(side*.10,-.242,2.89),(.025,.012,.022),ember,h)
   uv('Vertical lion pupil',(side*.10,-.254,2.89),(.007,.006,.016),black,h)
   line('Fierce brow',[(side*.028,-.247,2.92),(side*.10,-.24,2.967),(side*.18,-.20,2.975)],.022,brown,h)
  for j in range(26):
   t=2*pi*j/26;o=uv('Lion mane',(.36*cos(t),.035,2.83+.43*sin(t)),(.115,.10,.15),brown,h);o.rotation_euler.y=-t
  uv('Rig_MouthOpen',(0,-.337,2.69),(.092,.016,.088),black,h)
  for side in [-1,1]:
   rod('Upper fierce fang',(side*.058,-.365,2.765),(side*.060,-.365,2.661),.022,white,h,.003)
   rod('Lower fierce fang',(side*.058,-.362,2.621),(side*.058,-.362,2.66),.014,white,h,.003)
   for j in range(4):
    x=side*.47+(j-1.5)*.026
    line('Lion claw',[(x,-.26,2.38),(x,-.28,2.44),(x,-.31,2.48),(x,-.35,2.46)],.011,white,l if side==-1 else r)
 elif name=='vamana':
  h,l,r=humanoid('vamana',tan,white)
  rod('Umbrella pole',(-.47,-.25,1.7),(-.47,-.25,3.72),.018,brown,l)
  rod('Umbrella canopy',(-.47,-.25,3.50),(-.47,-.25,3.76),.55,gold,l,.045)
  ring('Umbrella border',(-.47,-.25,3.50),.54,red,l,(0,0,0),.016)
  uv('Water pot',(.47,-.25,2.50),(.10,.10,.14),gold,r);ring('Pot neck',(.47,-.25,2.64),.06,gold,r,(0,0,0))
 elif name=='parashurama':
  h,l,r=humanoid('sage',tan,orange)
  rod('Axe shaft',(.47,-.25,1.7),(.47,-.25,3.0),.023,brown,r)
  uv('Axe blade',(.61,-.25,2.89),(.20,.045,.14),white,r)
  line('Sacred thread',[(-.25,-.17,2.39),(0,-.23,2.05),(.25,-.18,1.70)],.009,white)
 elif name=='rama':
  h,l,r=humanoid('human',blue);bow(r)
  rod('Quiver',(-.21,.22,1.83),(-.26,.24,2.50),.10,brown)
  for x in [-.29,-.23,-.17]:rod('Quiver arrow',(x,.25,2.28),(x,.25,2.83),.008,gold)
 elif name=='buddha':
  h,l,r=humanoid('buddha',tan,orange)
  # Meditative standing depiction with open palms and a monastic robe.
 elif name=='kalki':
  h,l,r=humanoid('human',blue,white)
  # Raise the torso to the saddle and replace standing legs with a seated riding pose.
  for o in list(bpy.context.scene.objects):
   if o.name.startswith(('Dhoti leg','Foot')):bpy.data.objects.remove(o,do_unlink=True)
   elif not o.parent and not o.name.startswith(('Lotus foundation','Lotus petal')):o.location.z+=.23
  for o in list(bpy.context.scene.objects):
   if o.name.startswith('Lotus foundation'):o.scale.x*=1.8;o.scale.y*=1.5
   elif o.name.startswith('Lotus petal'):o.location.x*=1.8;o.location.y*=1.5;o.scale.x*=1.3
  for side in [-1,1]:
   # Thighs descend outside each flank; boots hang below the knees.
   rod('Rider thigh',(-.03,side*.13,1.84),(-.16,side*.38,1.43),.14,white)
   uv('Rider knee',(-.16,side*.38,1.43),(.13,.12,.12),white)
   rod('Rider lower leg',(-.16,side*.38,1.43),(-.13,side*.42,.87),.075,white)
   uv('Rider boot',(-.06,side*.43,.86),(.15,.085,.073),gold)
   ring('Stirrup',(-.12,side*.45,.93),.10,gold,None,(pi/2,0,0),.013)
   line('Stirrup strap',[(-.12,side*.25,1.68),(-.12,side*.45,.93)],.014,brown)
  horse=empty('Horse_mount')
  uv('White horse body',(.10,0,1.34),(.76,.26,.34),white,horse)
  uv('Horse chest',(.62,0,1.44),(.29,.27,.33),white,horse)
  for x in [-.47,.65]:
   for y in [-.19,.19]:
    uv('Horse haunch',(x,y,1.30),(.13,.115,.24),white,horse)
    rod('Horse upper leg',(x,y,1.24),(x+.035,y,.75),.085,white,horse)
    uv('Horse knee',(x+.035,y,.75),(.080,.075,.08),white,horse)
    rod('Horse lower leg',(x+.035,y,.75),(x+.08,y,.30),.048,white,horse)
    uv('Horse hoof',(x+.10,y,.27),(.091,.069,.075),black,horse)
  rod('Horse neck',(.61,0,1.45),(.86,0,2.14),.19,white,horse,.125)
  uv('Horse head',(.97,-.02,2.17),(.24,.135,.15),white,horse)
  uv('Horse muzzle',(1.12,-.02,2.10),(.18,.115,.09),white,horse)
  for side in [-1,1]:
   uv('Horse ear',(.86,side*.083,2.34),(.051,.04,.115),white,horse)
   uv('Horse eye',(1.00,side*.135,2.21),(.023,.012,.025),black,horse)
   line('Horse bridle',[(1.16,side*.116,2.17),(.88,side*.14,2.26),(.79,side*.12,2.13)],.012,gold,horse)
   line('Rein',[(1.07,side*.125,2.13),(.70,side*.16,2.03),(.47,-.25,2.50)],.009,brown,r)
  line('Horse mane',[(.78,.025,2.25),(.68,.03,2.08),(.57,.03,1.86),(.51,.025,1.66)],.059,black,horse)
  line('Horse tail',[(-.60,.03,1.51),(-.82,.04,1.30),(-.92,.02,.86),(-.90,0,.62)],.042,black,horse)
  uv('Royal saddle',(-.07,0,1.68),(.34,.29,.067),red)
  ring('Saddle belt',(.03,0,1.35),.29,gold,None,(0,pi/2,0),.019)
  rod('Sword grip',(-.47,-.26,2.50),(-.47,-.26,2.79),.021,gold,l)
  rod('Sword guard',(-.58,-.26,2.78),(-.36,-.26,2.78),.014,gold,l)
  rod('Sword blade',(-.47,-.26,2.79),(-.47,-.26,3.60),.035,white,l,.004)
 if name=='kurma':
  for o in list(bpy.context.scene.objects):
   if not o.parent and not o.name.startswith(('Lotus foundation','Lotus petal')):o.location.z-=.72
 if name=='vamana':
  short=empty('Vamana proportions');
  for o in list(bpy.context.scene.objects):
   if o!=short and not o.parent and not o.name.startswith(('Lotus foundation','Lotus petal')):parent(o,short)
  short.scale.z=.80
 # Every form has its own geometry and a head pivot for conversational motion.
 bpy.ops.object.select_all(action='DESELECT')
 for o in bpy.context.scene.objects:
  if o.type in ['MESH','CURVE']:o.select_set(True)
 bpy.context.view_layer.objects.active=next(o for o in bpy.context.scene.objects if o.type=='MESH')
 bpy.ops.object.convert(target='MESH')
 # Apply transforms to mesh data once; preserve rig node transforms.
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.ops.object.select_all(action='SELECT');bpy.ops.export_scene.gltf(filepath=OUT+'/'+name+'.glb',export_format='GLB',use_selection=True)
 bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/model-source/'+name+'.blend',compress=True)
 # Render a front view for checking distinctive silhouettes and props.
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=12;sc.render.resolution_x=440;sc.render.resolution_y=560;sc.render.resolution_percentage=100
 sc.world.color=(.13,.13,.13)
 bpy.ops.object.camera_add(location=(0,-8,3.0));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.9))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.7;sc.camera=cam
 for pos,power,size in [((-3,-4,6),700,5),((3,-1,5),500,4)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.8))-o.location).to_track_quat('-Z','Y').to_euler()
 sc.render.image_settings.file_format='PNG';sc.render.filepath=ROOT+'/build/'+name+'-preview.png';bpy.ops.render.render(write_still=True)
 print('FORM_COMPLETE',name,flush=True)
import sys
for name in (sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['matsya','kurma','varaha','narasimha','vamana','parashurama','rama','buddha','kalki']):build(name)
print('DASHAVATARA_COMPLETE',flush=True)
