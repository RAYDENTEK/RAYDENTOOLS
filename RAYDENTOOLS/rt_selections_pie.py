import bpy
from bpy.types import Menu

class VIEW3D_MT_PIE_selections(Menu):
    bl_label = 'Selections'
    def draw(self, context):
        layout = self.layout
        
        pie = layout.menu_pie()
        
        pie.operator("view3d.rt_selections_split")
        pie.operator("view3d.rt_selections_merge")
        if context.active_object.mode == 'EDIT':
            pie.operator("view3d.rt_selections_separate")
        else:
            pie.operator("view3d.rt_selections_join")
        pie.operator("view3d.rt_selections_hierarchy")
        pie.operator("view3d.rt_selections_material")
        pie.operator("view3d.rt_selections_linked")
        
        if context.active_object.mode == 'EDIT':
            pie.operator("mesh.select_all", text="Select/Deselect All").action = 'TOGGLE'
            pie.operator("mesh.select_all", text="Inverse").action = 'INVERT'
        else:
            pie.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
            pie.operator("object.select_all", text="Inverse").action = 'INVERT'
     

class VIEW3D_OT_PIE_selections_call(bpy.types.Operator):
    bl_idname = 'view3d.rt_selections'
    bl_label = 'RaydenTools Selections'
    bl_description = 'Opens pie menu'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_selections")
        return {'FINISHED'}



def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_selections)
    bpy.utils.register_class(VIEW3D_OT_PIE_selections_call)

def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_selections)
    bpy.utils.unregister_class(VIEW3D_OT_PIE_selections_call)