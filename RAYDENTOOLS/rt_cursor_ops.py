import bpy
import mathutils
from bpy.types import (
    Operator,
)
class cursor_reset_rotation(Operator):
    bl_idname = 'view3d.rt_cursor_reset_rotation'
    bl_label = 'Reset Cursor Rotation'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            #bpy.context.scene.tool_settings.use_transform_data_origin = True
            bpy.context.scene.cursor.rotation_euler = mathutils.Vector((0,0,0))
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
            

class cursor_set_to_active(Operator):
    bl_idname = 'view3d.rt_cursor_set_to_active'
    bl_label = 'Set Cursor to Active'
    #bl_description = 'Calls Pie Operator 5'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            active_obj = bpy.context.active_object
            if active_obj is None:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            bpy.ops.view3d.snap_cursor_to_active()
            bpy.context.scene.cursor.rotation_euler = active_obj.matrix_world.to_euler()
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
        

class cursor_set_rotation_to_active(Operator):
    bl_idname = 'view3d.rt_cursor_set_rotation_to_active'
    bl_label = 'Set Cursor Rotation to Active'
    #bl_description = 'Calls Pie Operator 6'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            active_obj = bpy.context.active_object
            if active_obj is None:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            #bpy.ops.view3d.snap_cursor_to_active()
            bpy.context.scene.cursor.rotation_euler = active_obj.matrix_world.to_euler()
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class cursor_set_rotation_from_view(Operator):
    bl_idname = 'view3d.rt_cursor_set_rotation_from_view'
    bl_label = 'Set Cursor Rotation From View'
    #bl_description = 'Calls Pie Operator 7'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            cursor = context.scene.cursor
            rotation_mode = cursor.rotation_mode
            cursor.rotation_mode = 'QUATERNION'
            cursor.rotation_quaternion =  context.region_data.view_rotation
            cursor.rotation_mode = rotation_mode
            
            #bpy.ops.view3d.snap_cursor_to_active()
            #bpy.context.scene.cursor.rotation_euler = active_obj.matrix_world.to_euler()
            
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class cursor_set_rotation_from_parent(Operator):
    bl_idname = 'view3d.rt_cursor_set_rotation_from_parent'
    bl_label = 'Cursor Rotation from Parent'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            active_obj = bpy.context.active_object
            if active_obj is None or (len(context.selected_objects) == 0):
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            
            if active_obj.parent is None:
                self.report({'ERROR'}, "No Parent")
                return {'CANCELLED'}     
            
            parent_obj = bpy.context.active_object.parent
            bpy.context.scene.cursor.rotation_euler = parent_obj.matrix_world.to_euler()
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

classes = (
    cursor_reset_rotation,
    cursor_set_to_active,
    cursor_set_rotation_to_active,
    cursor_set_rotation_from_view,
    cursor_set_rotation_from_parent,
)

def register():
   for c in classes:
       bpy.utils.register_class(c)

def unregister():
    for c in classes:
       bpy.utils.unregister_class(c)