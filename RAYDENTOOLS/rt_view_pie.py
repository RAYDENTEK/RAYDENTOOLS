import bpy
from bpy.types import (
    Menu,
    Operator,
)

class VIEW3D_MT_PIE_view_options(Menu):
    bl_label = 'View Options'
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("view3d.rt_view_toggle_edge_length")
        pie.operator("view3d.draw_center_axes")
        pie.operator("view3d.rt_view_toggle_overlays")
        pie.operator("view3d.rt_view_toggle_view_modes")
        pie.operator("view3d.rt_view_toggle_face_orientation")
        pie.operator("view3d.draw_forward_vector")
        label = wm = context.window_manager
        label = "Bounding Box ON" if wm.my_operator_toggle else "Bounding Box OFF"
        pie.prop(wm, 'my_operator_toggle', text=label, toggle=True)
        pie.operator("view3d.rt_view_hide_hierarchy")

class VIEW3D_OT_PIE_view_options_call(Operator):
    bl_idname = 'view3d.rt_view_options'
    bl_label = 'RaydenTools View Options'
    bl_description = 'Opens pie menu'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_view_options")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_view_options)
    bpy.utils.register_class(VIEW3D_OT_PIE_view_options_call)
    
def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_view_options)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_view_options_call)

