import bpy
from bpy.types import (
    Menu,
    Operator,
)

class VIEW3D_MT_PIE_utility_actions(Menu):
    bl_label = 'Utility Actions'
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("view3d.rt_set_normals")
        pie.operator("view3d.rt_merge_hierarchy")
        pie.operator("view3d.rt_parent")
        pie.operator("view3d.rt_unparent")
        pie.box()
        pie.box()
        pie.box()
        pie.box()
        
       

class VIEW3D_OT_PIE_utility_actions_call(Operator):
    bl_idname = 'view3d.rt_utility_actions'
    bl_label = 'RaydenTools Utility Actions'
    bl_description = 'Opens pie menu'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_utility_actions")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_utility_actions)
    bpy.utils.register_class(VIEW3D_OT_PIE_utility_actions_call)
    


def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_utility_actions)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_utility_actions_call)

