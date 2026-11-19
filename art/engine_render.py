import bpy, math, os
from mathutils import Vector

ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=os.environ.get('ENGINE_OUT',os.path.join(ROOT,'frames'))
os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def mat(name, color, metal=0, rough=.4):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    return m
cast=mat('Brushed cast aluminum',(.31,.34,.36),.82,.31)
cast_light=mat('Machined aluminum',(.59,.62,.63),.9,.25)
dark=mat('Graphite engine block',(.055,.067,.073),.72,.29)
black=mat('Ceramic black',(.015,.021,.026),.38,.34)
red=mat('Deep race red',(.26,.006,.012),.62,.27)
red_bright=mat('Signal red',(.9,.018,.027),.42,.25)
rubber=mat('Belts and hoses',(.013,.016,.018),.05,.58)
brass=mat('Brass fittings',(.5,.34,.12),.85,.24)
glass=mat('Sensor lens',(.1,.26,.29),.5,.16)

rig=bpy.data.objects.new('ENGINE / ROTATION',None);bpy.context.collection.objects.link(rig)
def register(obj,material):
    obj.data.materials.append(material);obj.parent=rig;return obj
def bevel(obj,amount=.06,segments=3):
    mod=obj.modifiers.new('Machined radii','BEVEL');mod.width=amount;mod.segments=segments
    mod.affect='EDGES';obj.modifiers.new('Weighted edges','WEIGHTED_NORMAL');return obj
def box(name,loc,scale,material,b=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name
    o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if b:bevel(o,b)
    return register(o,material)
def cyl(name,loc,r,depth,material,axis='Z',verts=32,b=.015):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name
    if axis=='X':o.rotation_euler[1]=math.pi/2
    if axis=='Y':o.rotation_euler[0]=math.pi/2
    if b:bevel(o,b,2)
    return register(o,material)
def torus(name,loc,major,minor,material,axis='Z'):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=48,minor_segments=10,location=loc)
    o=bpy.context.object;o.name=name
    if axis=='X':o.rotation_euler[1]=math.pi/2
    if axis=='Y':o.rotation_euler[0]=math.pi/2
    return register(o,material)
def tube(name,points,r,material):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=20;c.bevel_depth=r;c.bevel_resolution=3
    s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
    for p,xyz in zip(s.bezier_points,points):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);return register(o,material)
def text(name,loc,size,material,rot=(0,0,0),align='LEFT'):
    c=bpy.data.curves.new(name,'FONT');c.body=name;c.size=size;c.extrude=.002;c.bevel_depth=.001;c.align_x=align
    o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=rot;return register(o,material)

# Cast inline-four long block and the pressed oil pan. The long x-axis makes
# four combustion positions legible from a three-quarter hero angle.
box('Sump / lower crankcase',(0,0,.35),(4.4,1.72,.56),dark,.15)
box('Sump outer lip',(0,0,.65),(4.5,1.82,.13),cast_light,.035)
box('Cylinder block',(0,0,1.24),(4.35,1.86,1.27),cast,.15)
box('Head gasket',(0,0,1.93),(4.39,1.9,.08),black,.02)
box('Cylinder head',(0,0,2.19),(4.22,1.81,.47),cast_light,.085)
box('Valve cover rim',(0,0,2.46),(4.35,1.87,.12),black,.045)
box('Valve cover / red accent',(0,0,2.61),(4.1,1.62,.25),red,.14)
box('Valve cover upper panel',(0,0,2.745),(3.85,1.3,.06),dark,.04)
box('Red engine spine',(0,-.55,2.786),(3.43,.14,.035),red_bright,.012)
box('Cast front timing plate',(2.27,0,1.68),(.24,1.84,1.81),dark,.095)
box('Timing plate silver edge',(2.407,0,1.68),(.035,1.63,1.55),cast_light,.04)

for i,x in enumerate([-1.55,-.53,.49,1.51]):
    # Cylinder-side webs, ribs, plug wells and four distinct coils.
    box(f'Block side web {i+1}',(x,-.957,1.26),(.71,.13,.94),dark,.055)
    for z in [.88,1.06,1.27,1.49]:
        box(f'Cooling rib {i+1}/{z}',(x,-1.04,z),(.64,.14,.045),cast_light,.012)
    cyl(f'Ignition plug seat {i+1}',(x,0,2.79),.17,.06,cast_light)
    cyl(f'Ignition coil {i+1}',(x,0,2.87),.125,.18,black)
    box(f'Coil red key {i+1}',(x,-.04,2.967),(.19,.13,.026),red_bright,.008)
    cyl(f'Block plug {i+1}',(x,-1.11,1.75),.075,.09,brass,'Y',16)

for x in [-1.94,-.97,0,.97,1.94]:
    for y in [-.71,.71]:cyl('Valve cover bolt',(x,y,2.754),.04,.035,cast_light,verts=12,b=.006)
    box('Sump fastener',(x,-.9,.64),(.075,.035,.075),cast_light,.008)

# Cam bearing bridges remain visible on the head once the cover lifts.
for x in [-1.56,-.52,.52,1.56]:
    box('Head cam bridge',(x,0,2.445),(.52,1.25,.065),dark,.025)
    for y in [-.41,.41]:
        cyl('Cam bearing', (x,y,2.49),.15,.045,cast_light,verts=32,b=.008)
        cyl('Cam insert', (x,y,2.519),.085,.012,dark,verts=32,b=.004)
        cyl('Bridge bolt', (x,y,2.531),.025,.025,brass,verts=12,b=.003)
for x in [-1.8,-1.2,-.6,0,.6,1.2,1.8]:
    box('Oil pan reinforcing fin',(x,-.5,.12),(.06,.7,.095),cast,.017)

# Intake runners on the far bank, a plenum, fuel rail and hard lines.
box('Intake plenum',(0,1.42,1.94),(3.5,.52,.46),cast_light,.18)
for i,x in enumerate([-1.52,-.51,.5,1.51]):
    tube(f'Intake runner {i+1}',[(x,.82,2.14),(x,1.03,2.03),(x,1.16,1.77),(x,1.33,1.77)],.103,cast)
    cyl(f'Injector rail boss {i+1}',(x,1.72,2.04),.095,.13,black,'Y',20)
tube('Fuel rail',[(-1.98,1.75,2.16),(-.9,1.75,2.16),(.9,1.75,2.16),(1.98,1.75,2.16)],.042,red_bright)
cyl('Throttle body',(1.97,1.45,1.95),.31,.29,dark,'X')
torus('Throttle machined lip',(2.14,1.45,1.95),.285,.035,cast_light,'X')

# Swept polished exhaust headers on the near side converge toward a turbine.
for i,x in enumerate([-1.48,-.49,.5,1.49]):
    cyl(f'Exhaust flange {i+1}',(x,-.997,2.19),.16,.09,dark,'Y')
    path=[(x,-1.03,2.16),(x,-1.31,2.15),(x+.05,-1.52,1.8),(x+.27,-1.59,1.41),(.58+(x+1.48)*.23,-1.57,1.13)]
    tube(f'Mandrel-bent exhaust runner {i+1}',path,.105,cast_light)
tube('Collector',[(-.15,-1.57,1.11),(.58,-1.58,1.05),(1.43,-1.54,1.05),(1.86,-1.48,1.1)],.16,cast)
for i,x in enumerate([-1.48,-.49,.5,1.49]):
    for dx in [-.14,.14]:cyl('Header stud',(x+dx,-1.057,2.2),.028,.095,brass,'Y',12,.003)

# Turbocharger: machined hot scroll, compressor face and oil line.
cyl('Turbine core',(2.1,-1.5,1.11),.41,.53,cast,'X')
torus('Scroll housing',(2.36,-1.5,1.11),.41,.17,cast_light,'X')
cyl('Compressor face',(2.58,-1.5,1.11),.28,.04,dark,'X')
torus('Compressor rim',(2.62,-1.5,1.11),.245,.026,red,'X')
for a in range(8):
    th=2*math.pi*a/8
    cyl('Turbine vane',(2.614,-1.5+math.cos(th)*.14,1.11+math.sin(th)*.14),.027,.026,cast_light,'X',12,.004)
cyl('Turbine shaft',(2.64,-1.5,1.11),.056,.08,cast_light,'X')
tube('Turbo oil feed',[(1.2,-.95,2.33),(1.83,-1.09,2.38),(2.23,-1.35,1.66),(2.14,-1.48,1.42)],.035,brass)
tube('Turbo outlet',[(2.08,-1.68,.72),(2.25,-1.85,.58),(2.48,-1.76,.47)],.145,cast)

# Timing / accessory drive. These circular components face the camera at x+.
for name,y,z,r in [('Crank',0,.78,.34),('Cam A',-.45,2.07,.27),('Cam B',.47,2.07,.27),('Idler',.72,1.12,.20)]:
    cyl(name+' pulley',(2.54,y,z),r,.22,dark,'X',48,.025)
    torus(name+' outer machined ring',(2.68,y,z),r*.82,.026,cast_light,'X')
    cyl(name+' hub',(2.69,y,z),r*.36,.035,cast_light,'X',24,.01)
    for a in range(6):
        th=2*math.pi*a/6
        cyl(name+' fastening',(2.715,y+math.cos(th)*r*.55,z+math.sin(th)*r*.55),.018,.026,black,'X',10,.003)
tube('Serpentine belt / left',[(2.72,-.75,2.1),(2.72,-.67,1.64),(2.72,-.3,.61),(2.72,.18,.46),(2.72,.66,1.02)],.053,rubber)
tube('Serpentine belt / right',[(2.72,.66,1.02),(2.72,.75,1.32),(2.72,.73,2.07),(2.72,.46,2.36),(2.72,-.44,2.37),(2.72,-.75,2.1)],.053,rubber)

# Filter, wiring loom, fluid line and serviceable cues.
cyl('Oil filter',(1.52,-.68,.46),.2,.43,black,verts=32)
torus('Oil filter rolled edge',(1.52,-.68,.66),.175,.025,cast_light)
box('Engine data plate',(-1.45,-.98,1.49),(.62,.025,.27),black,.012)
box('Data plate red marker',(-1.69,-1.002,1.49),(.095,.012,.17),red_bright,.003)
tube('Main wiring loom',[(-2.08,.34,2.51),(-2.31,.16,2.23),(-2.35,-.49,1.76),(-2.03,-1.01,1.5)],.066,rubber)
for x in [-1.55,-.53,.49,1.51]:
    tube('Coil wiring',[(x,.05,2.91),(x,.3,2.98),(x+.2,.54,2.78)],.024,rubber)
for x in [-1.55,-.53,.49,1.51]:
    cyl('Machined service port',(x,.91,1.68),.09,.06,cast_light,'Y',20)
    cyl('Service port insert',(x,.95,1.68),.052,.015,black,'Y',20)

# Grounded mounting lugs and recessed detail make the silhouette less toy-like.
for x in [-1.7,1.7]:
    box('Mounting bracket',(x,.76,.68),(.34,.54,.14),cast_light,.045)
    cyl('Mounting hole',(x,1.03,.69),.073,.025,dark,verts=24)

# A serviceable four-cylinder deck sits under the removable head. When the
# engine opens, piston crowns, bore rings and their fasteners are revealed.
for i,x in enumerate([-1.53,-.51,.51,1.53]):
    cyl(f'Cylinder bore liner {i+1}',(x,0,1.885),.355,.025,dark,verts=48,b=.006)
    torus(f'Machined bore ring {i+1}',(x,0,1.905),.315,.032,cast_light)
    cyl(f'Piston crown {i+1}',(x,0,1.91),.255,.036,cast_light,verts=48,b=.015)
    cyl(f'Piston dish {i+1}',(x,0,1.932),.135,.006,cast,verts=48,b=.003)
    for a in range(4):
        th=2*math.pi*a/4
        cyl(f'Head stud {i+1}/{a}',(x+math.cos(th)*.43,math.sin(th)*.43,1.91),.027,.085,brass,verts=12,b=.003)

# Component groups keep the animation mechanically meaningful: the cover
# lifts, the complete head separates, external systems move sideways, and the
# oil pan lowers. Every frame is rendered from the actual 3D assembly.
parts={}
for name in ['cover','head','exhaust','front','block','sump']:
    e=bpy.data.objects.new(name.upper()+' / ASSEMBLY',None);bpy.context.collection.objects.link(e);e.parent=rig;parts[name]=e
def part_for(name):
    if name.startswith(('Valve cover','Red engine spine','Ignition','Coil red','Coil wiring')) or name=='Valve cover bolt':return 'cover'
    if name.startswith(('Cylinder head','Head gasket','Intake','Fuel rail','Injector rail','Throttle','Service port','Head cam','Cam bearing','Cam insert','Bridge bolt')):return 'head'
    if name.startswith(('Exhaust','Mandrel','Collector','Turbine','Scroll','Compressor','Turbo')):return 'exhaust'
    if name.startswith(('Cast front','Timing plate','Serpentine')) or ' pulley' in name or ' fastening' in name or ' outer machined ring' in name or ' hub' in name:return 'front'
    if name.startswith(('Sump','Oil filter','Oil pan reinforcing fin')):return 'sump'
    return 'block'
for o in list(bpy.context.scene.objects):
    if o.parent==rig and o not in parts.values():
        o.parent=parts[part_for(o.name)]
offsets={'cover':Vector((-.12,.03,1.10)),'head':Vector((-.12,.05,.43)),
         'exhaust':Vector((-.78,-.40,.04)),'front':Vector((.76,0,.04)),
         'block':Vector((0,0,0)),'sump':Vector((0,0,-.60))}

scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.resolution_x=720;scene.render.resolution_y=720
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True
scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
scene.render.resolution_percentage=100
scene.render.engine='BLENDER_EEVEE_NEXT';scene.eevee.taa_render_samples=32
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.view_settings.view_transform='AgX'
world=bpy.data.worlds.new('Studio atmosphere');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.15,.17,.19,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35

def light(name,loc,power,color,size,target=(0,0,1.5)):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color;data.shape='DISK';data.size=size
    o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
light('Key / cold studio',(0,-5,8),900,(.83,.9,1),7)
light('Red automotive rim',(-2.5,3,5),530,(1,.04,.06),5)
light('Machined edge',(4,2,3.5),600,(.78,.85,1),4)
light('Front fill',(5,-3,2.8),390,(1,.92,.85),4)

bpy.ops.object.camera_add(location=(7.6,-8.8,6.0));cam=bpy.context.object
target=Vector((0,0,1.48));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=6.8;scene.camera=cam

# A restrained angular turntable keeps the model's most legible side toward
# the viewer while still making every frame a genuinely rendered 3D view.
mode=os.environ.get('ENGINE_MODE','turntable')
if mode=='turntable':
    frames=[(a,0) for a in [-24,-20,-16,-12,-8,-4,0,4,8,12,16,20,24]]
elif mode=='open_preview':frames=[(0,1)]
elif mode=='assembled_preview':frames=[(0,0)]
else:
    # 25 steps allow the user to run the assembly either way without snaps.
    frames=[(0,i/24) for i in range(25)]
if mode.endswith('preview'):OUT=os.environ.get('ENGINE_OUT',os.path.join(ROOT,'preview'))
elif mode=='sequence':OUT=os.environ.get('ENGINE_OUT',os.path.join(ROOT,'assembly'))
os.makedirs(OUT,exist_ok=True)
for i,(angle,amount) in enumerate(frames):
    rig.rotation_euler[2]=math.radians(angle)
    # smoothstep creates a measured, heavy mechanical lift.
    t=amount*amount*(3-2*amount)
    for key,e in parts.items():e.location=offsets[key]*t
    scene.render.filepath=os.path.join(OUT,f'{i:02d}.png')
    bpy.ops.render.render(write_still=True)
    print(f'RENDERED {i:02d} angle={angle} assembly={amount:.2f}',flush=True)
