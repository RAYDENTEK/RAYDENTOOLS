import bpy
from bpy.types import (
    Operator,
)

class set_manipulation_mode_global(Operator):
    bl_idname = 'view3d.rt_set_manipulation_mode_global'
    bl_label = 'Global Mode'
    #bl_description = 'Calls Pie Operator 2'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
            bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class set_manipulation_mode_cursor(Operator):
    bl_idname = 'view3d.rt_set_manipulation_mode_cursor'
    bl_label = 'Cursor Mode'
    #bl_description = 'Calls Pie Operator 3'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
            bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class set_manipulation_mode_active(Operator):
    bl_idname = 'view3d.rt_set_manipulation_mode_active'
    bl_label = 'Active Element Mode'
    #bl_description = 'Calls Pie Operator 4'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
            bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class set_manipulation_mode_local(Operator):
    bl_idname = 'view3d.rt_set_manipulation_mode_local'
    bl_label = 'Local Mode'
    #bl_description = 'Calls Pie Operator 8'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
            bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class set_manipulation_mode_normal(Operator):
    bl_idname = 'view3d.rt_set_manipulation_mode_normal'
    bl_label = 'Normal Mode'
    #bl_description = 'Calls Pie Operator 8'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
            bpy.context.scene.transform_orientation_slots[0].type = 'NORMAL'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class set_manipulation_mode_custom(Operator):
    bl_idname = 'view3d.rt_set_manipulation_mode_custom'
    bl_label = 'Custom Mode'
    #bl_description = 'Calls Pie Operator 8'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            bpy.ops.transform.create_orientation(name="CustomOrient", use_view=False, use=True, overwrite=True)
            bpy.context.scene.transform_orientation_slots[0].type ='CustomOrient'
            bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

classes = (
    set_manipulation_mode_global,
    set_manipulation_mode_cursor,
    set_manipulation_mode_active,
    set_manipulation_mode_local,
    set_manipulation_mode_normal,
    set_manipulation_mode_custom,
)

def register():
   for c in classes:
       bpy.utils.register_class(c)

def unregister():
    for c in classes:
       bpy.utils.unregister_class(c)