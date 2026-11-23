import bpy,sys
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/tmp/rig/vill.glb')
me=[o for o in bpy.data.objects if o.type=='MESH'][0]
bpy.context.view_layer.objects.active=me;me.select_set(True)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=0.0005);bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.armature_add(location=(0,0,0));arm=bpy.context.object;arm.name='Armature'
bpy.ops.object.mode_set(mode='EDIT');eb=arm.data.edit_bones;eb.remove(eb[0])
def B(n,h,t,p=None,c=True):
    b=eb.new(n);b.head=h;b.tail=t
    if p:b.parent=eb[p];b.use_connect=c
    return b
X=0.03
B('Hips',(X,0,-0.29),(X,0,-0.15))
B('Spine',(X,0,-0.15),(X,0,-0.02),'Hips')
B('Head',(X,0,-0.02),(X,0,0.5),'Spine')
for s,n in((1,'Left'),(-1,'Right')):
    B(n+'Arm',(X,s*0.14,-0.06),(X,s*0.185,-0.165),'Spine',False)
    B(n+'ForeArm',(X,s*0.185,-0.165),(X+0.01,s*0.195,-0.255),n+'Arm')
    B(n+'Hand',(X+0.01,s*0.195,-0.255),(X+0.01,s*0.2,-0.30),n+'ForeArm')
    B(n+'UpLeg',(X,s*0.08,-0.29),(X,s*0.085,-0.395),'Hips',False)
    B(n+'Leg',(X,s*0.085,-0.395),(X,s*0.085,-0.475),n+'UpLeg')
    B(n+'Foot',(X,s*0.085,-0.475),(X+0.09,s*0.085,-0.5),n+'Leg')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT');me.select_set(True);arm.select_set(True);bpy.context.view_layer.objects.active=arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
empty=[vg.name for vg in me.vertex_groups if not any(g.group==vg.index for v in me.data.vertices for g in v.groups)]
nw=sum(1 for v in me.data.vertices if not v.groups or sum(g.weight for g in v.groups)<0.01)
print('RESULT groups',len(me.vertex_groups),'empty',empty,'unweighted',nw,'of',len(me.data.vertices))
bpy.ops.export_scene.gltf(filepath='/tmp/rig/vill_rig2.glb',export_format='GLB',export_animations=False,export_yup=True)
