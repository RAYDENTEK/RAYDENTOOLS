import bpy

from bpy.types import (
    Menu,
    Operator,
)

class VIEW3D_MT_PIE_manipulation_modes(Menu):
    bl_label = 'Manipulation Modes'
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("view3d.rt_set_manipulation_mode_local")
        pie.operator("view3d.rt_set_manipulation_mode_global")
        pie.operator("view3d.rt_set_manipulation_mode_active")
        pie.operator("view3d.rt_set_manipulation_mode_cursor")
        pie.operator("view3d.rt_set_manipulation_mode_normal")
        pie.operator("view3d.rt_set_manipulation_mode_custom")
        pie.box()
        pie.box()

class VIEW3D_OT_PIE_manipulation_modes_call(Operator):
    bl_idname = 'view3d.rt_manipulation_modes'
    bl_label = 'RaydenTools Manipulation Modes'
    bl_description = 'Opens pie menu'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_manipulation_modes")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_manipulation_modes)
    bpy.utils.register_class(VIEW3D_OT_PIE_manipulation_modes_call)


def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_manipulation_modes)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_manipulation_modes_call)

