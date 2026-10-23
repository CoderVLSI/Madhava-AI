import bpy,bmesh,math,os,sys
from mathutils import Vector
from math import pi,sin,cos
ROOT='/workspace/scratch/e9ff7d14d887/madhava'
# Reuse the small primitive helpers, without executing the avatar-building loop.
source=open(ROOT+'/model-source/build_dashavatara.py').read();exec(source[:source.index('def build(name):')])
def render(name,scale=4.55):
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=520;s.render.resolution_y=680;s.render.resolution_percentage=100
 for o in list(bpy.context.scene.objects):
  if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
 bpy.ops.object.camera_add(location=(0,-8,3));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.35 if name=='vamana' else 1.9))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale;s.camera=cam
 for pos,power,size in [((-3,-4,6),700,5),((3,-1,5),500,4)]:
  bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.8))-o.location).to_track_quat('-Z','Y').to_euler()
 s.render.image_settings.file_format='PNG';s.render.filepath=ROOT+'/build/'+name+'-preview.png';bpy.ops.render.render(write_still=True)
def export(name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in bpy.context.scene.objects:
  if o.type in ['CURVE','MESH']:o.select_set(True)
 bpy.context.view_layer.objects.active=next(o for o in bpy.context.scene.objects if o.type=='MESH')
 bpy.ops.object.convert(target='MESH')
 bpy.ops.object.select_all(action='DESELECT')
 for o in bpy.context.scene.objects:
  if o.type in ['MESH','EMPTY']:o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=ROOT+'/app/src/main/assets/forms/'+name+'.glb',export_format='GLB',use_selection=True)
 bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/model-source/'+name+'.blend',compress=True)

def rama():
 bpy.ops.wm.open_mainfile(filepath=ROOT+'/model-source/Krishna-dialogue.blend')
 for n in ['Cosmic_Form','Rig_Flute']:
  o=bpy.data.objects.get(n)
  if o:
   for q in list(o.children_recursive):bpy.data.objects.remove(q,do_unlink=True)
   bpy.data.objects.remove(o,do_unlink=True)
 for o in list(bpy.context.scene.objects):
  if o.type in ['LIGHT','CAMERA'] or o.name=='Stage':bpy.data.objects.remove(o,do_unlink=True)
 # Remove the peacock plume from merged head meshes, retaining the full jeweled crown.
 head=bpy.data.objects['Rig_Head']
 for o in list(head.children):
  if o.type!='MESH':continue
  bm=bmesh.new();bm.from_mesh(o.data)
  remaining=set(bm.verts);verts=[]
  while remaining:
   first=remaining.pop();component={first};stack=[first]
   while stack:
    v=stack.pop()
    for e in v.link_edges:
     q=e.other_vert(v)
     if q in remaining:remaining.remove(q);component.add(q);stack.append(q)
   zs=[(o.matrix_world@v.co).z for v in component]
   if max(zs)>3.83 and sum(zs)/len(zs)>3.75:verts.extend(component)
  if verts:bmesh.ops.delete(bm,geom=verts,context='VERTS');bm.to_mesh(o.data);o.data.update()
  bm.free()
 # Keep the sculpted silk, jewelry, floral garland and detailed crown from Krishna.
 left=bpy.data.objects['Rig_Left_Hand'];right=bpy.data.objects['Rig_Right_Hand']
 g=bpy.data.materials['Antique gold'];w=bpy.data.materials['Ivory'];dark=bpy.data.materials['Deep brown eyes']
 bowpts=[(-.56,-.51,1.57),(-.75,-.51,1.75),(-.85,-.51,2.12),(-.52,-.51,2.56),(-.84,-.51,2.93),(-.74,-.51,3.19),(-.56,-.51,3.33)]
 c=bpy.data.curves.new('Royal bow curve','CURVE');c.dimensions='3D';c.bevel_depth=.027;c.bevel_resolution=3;sp=c.splines.new('BEZIER');sp.bezier_points.add(len(bowpts)-1)
 for v,q in zip(sp.bezier_points,bowpts):v.co=q;v.handle_left_type='AUTO';v.handle_right_type='AUTO'
 bow=bpy.data.objects.new('Royal bow',c);bpy.context.collection.objects.link(bow);finish(bow,'Royal bow',g,left)
 line('Bow string',[bowpts[0],bowpts[-1]],.004,w,left)
 for z in [2.51,2.56,2.61]:ring('Bow jeweled grip',(-.52,-.51,z),.034,g,left,(0,0,0),.006)
 rod('Royal arrow shaft',(.36,-.51,2.12),(.36,-.51,3.21),.010,g,right)
 rod('Royal arrowhead',(.36,-.51,3.18),(.36,-.51,3.32),.037,w,right,.001)
 for side in [-1,1]:uv('Arrow feather',(.36+side*.028,-.51,2.18),(.026,.012,.085),w,right)
 rod('Royal quiver',(.24,.20,1.90),(.30,.20,2.73),.10,dark)
 for z in [1.96,2.61,2.73]:ring('Quiver gold band',(.28,.20,z),.10,g,None,(0,0,0),.012)
 for j in range(4):
  x=.24+j*.036;rod('Quiver arrow',(x,.20,2.44),(x,.20,3.00+j*.025),.008,g)
  uv('Quiver feather',(x,.20,2.95+j*.025),(.024,.015,.07),w)
 # Saffron shoulder silk distinguishes Rama without reducing detail.
 cloth=bpy.data.materials.get('Crimson silk')
 if cloth:
  cloth.diffuse_color=(.80,.25,.04,1);cloth.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.80,.25,.04,1)
 export('rama')
 bpy.data.objects['Rig_MouthOpen'].scale.z*=.055
 render('rama',4.65)
 print('REFINED_RAMA_COMPLETE',flush=True)

def vamana():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 # Refresh materials after opening another blend.
 global blue,gold,yellow,red,white,black,orange,green,brown,tan,stone
 gold=mat('Vamana gold',(.74,.43,.08),.7);white=mat('Vamana white silk',(.93,.89,.77));black=mat('Vamana hair',(.022,.014,.01));red=mat('Vamana rose',(.57,.08,.10));tan=mat('Vamana warm skin',(.73,.45,.27));brown=mat('Umbrella wood',(.23,.12,.035));stone=mat('Teal foundation',(.035,.12,.12),.4)
 base()
 # Large youthful head on a short, round body: total height ~2.25 including umbrella.
 uv('Child torso',(0,0,1.13),(.24,.17,.29),tan)
 for side in [-1,1]:
  uv('Short dhoti leg',(side*.105,0,.61),(.125,.13,.27),white)
  uv('Small foot',(side*.12,-.085,.32),(.072,.125,.057),tan)
 rod('Tiny waist wrap',(0,0,.82),(0,0,.93),.25,white,None,.24)
 rod('Child neck',(0,0,1.31),(0,0,1.47),.068,tan)
 h=empty('Rig_Head',(0,0,1.43));face(h,tan,'vamana',1.73)
 # Round cheeks, rounded nose, big eyes and a soft smiling mouth.
 for o in list(h.children):
  if o.name.startswith(('Face','Hair')):o.scale.x*=1.08;o.scale.z*=.94
  if o.name.startswith('Nose'):o.scale=(.029,.024,.036)
  if o.name.startswith('Eye ivory'):o.scale.x*=1.18;o.scale.z*=1.20
  if o.name.startswith('Iris'):o.scale.x*=1.16;o.scale.z*=1.18
  if o.name.startswith(('Brow','Lower lip')):bpy.data.objects.remove(o,do_unlink=True)
 for side in [-1,1]:
  uv('Round child cheek',(side*.137,-.17,1.65),(.066,.028,.055),tan,h)
  uv('Eye glint',(side*.09-.007,-.248,1.78),(.007,.005,.008),white,h)
  line('Soft child brow',[(side*.046,-.223,1.86),(side*.09,-.232,1.88),(side*.143,-.21,1.86)],.008,black,h)
 line('Gentle smile',[(-.058,-.234,1.60),(0,-.244,1.58),(.058,-.234,1.60)],.009,red,h)
 uv('Child topknot',(0,.04,2.06),(.079,.079,.086),black,h)
 ring('Small halo',(0,.27,1.77),.38,gold,h,minor=.012)
 l=arm(-1,(-.19,0,1.30),(-.32,-.06,1.05),(-.30,-.18,1.18),(-.30,-.19,1.27),tan)
 r=arm(1,(.19,0,1.30),(.32,-.06,1.05),(.30,-.18,1.18),(.30,-.19,1.27),tan)
 # Downscale hands and fingers about their wrist pivots, preserving the rig.
 l.scale=(.75,.75,.75);r.scale=(.75,.75,.75)
 line('Sacred thread',[(-.16,-.14,1.35),(0,-.18,1.16),(.18,-.14,.94)],.006,white)
 rod('Umbrella pole',(-.32,-.20,.65),(-.32,-.20,2.33),.013,brown,l)
 rod('Umbrella canopy',(-.32,-.20,2.17),(-.32,-.20,2.36),.42,gold,l,.028)
 ring('Umbrella border',(-.32,-.20,2.17),.415,red,l,(0,0,0),.012)
 uv('Little water pot',(.30,-.20,1.43),(.075,.075,.098),gold,r)
 ring('Pot neck',(.30,-.20,1.53),.040,gold,r,(0,0,0),.010)
 export('vamana')
 bpy.data.objects['Rig_MouthOpen'].scale.z*=.055
 render('vamana',3.2)
 print('REFINED_VAMANA_COMPLETE',flush=True)
if '--' in sys.argv:
 for name in sys.argv[sys.argv.index('--')+1:]:globals()[name]()
else:rama();vamana()
