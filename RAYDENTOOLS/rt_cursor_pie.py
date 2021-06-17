import bpy
from bpy.types import (
    Menu,
    Operator,
)

class VIEW3D_MT_PIE_cursor_actions(Menu):
    bl_label = 'Cursor Actions'
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("view3d.rt_cursor_set_rotation_to_active")
        pie.operator("view3d.rt_cursor_reset_rotation")
        pie.operator("view3d.rt_cursor_set_to_active")
        pie.operator("view3d.rt_cursor_set_rotation_from_parent")
        pie.box()
        pie.operator("view3d.rt_cursor_set_rotation_from_view")
        pie.box()
        pie.box()
        
       

class VIEW3D_OT_PIE_cursor_actions_call(Operator):
    bl_idname = 'view3d.rt_cursor_actions'
    bl_label = 'RaydenTools Cursor Actions'
    bl_description = 'Opens pie menu'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_cursor_actions")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_cursor_actions)
    bpy.utils.register_class(VIEW3D_OT_PIE_cursor_actions_call)
    


def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_cursor_actions)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_cursor_actions_call)

