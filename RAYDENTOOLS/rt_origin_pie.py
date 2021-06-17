import bpy
from bpy.types import (
    Menu,
    Operator,
)

class VIEW3D_MT_PIE_origin_actions(Menu):
    bl_label = 'Origin Actions'
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie = layout.menu_pie()
        pie.operator("view3d.rt_origin_set_to_cursor")
        pie.box()
        pie.operator("view3d.rt_origin_edit")
        pie.box()
        pie.box()
        pie.box()
        pie.operator("view3d.rt_origin_set_to_selected")
        pie.box()

class VIEW3D_OT_PIE_origin_actions_call(Operator):
    bl_idname = 'view3d.rt_origin_actions'
    bl_label = 'RaydenTools Origin Actions'
    bl_description = 'Opens pie menu'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_origin_actions")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_origin_actions)
    bpy.utils.register_class(VIEW3D_OT_PIE_origin_actions_call)
    
def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_origin_actions)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_origin_actions_call)

