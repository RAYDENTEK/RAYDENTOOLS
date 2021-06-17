import bpy, bmesh
from bpy.types import (
    Operator,
)

class selections_separate(Operator):
    bl_idname = 'view3d.rt_selections_separate'
    bl_label = 'Separate'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        try:
            if (len(context.selected_objects) == 0):
                self.report({'ERROR'}, "No Selection")
                return {'CANCELLED'}

            org_obj_list = {obj.name for obj in context.selected_objects}
            
            ob = bpy.context.edit_object
            if (ob is not None):
                bpy.ops.mesh.separate(type = 'SELECTED')
                #if context.active_object.mode == 'EDIT':
                bpy.ops.object.editmode_toggle()
                for obj in context.selected_objects:
                    if obj and obj.name in org_obj_list:
                        obj.select_set(False)
                    else:
                        context.view_layer.objects.active = obj
            else:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
    

class selections_linked(Operator):
    bl_idname = 'view3d.rt_selections_linked'
    bl_label = 'Select Linked'
    #bl_description = 'Calls Pie Operator 6'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'

    def execute(self, context):
        try:
            bpy.ops.mesh.select_linked(delimit={'SEAM'})
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class selections_join(Operator):
    bl_idname = 'view3d.rt_selections_join'
    bl_label = 'Join'
    #bl_description = 'Calls Pie Operator 3'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode != 'EDIT_MESH'

    def execute(self, context):
        try:
            bpy.ops.object.join()
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class selections_split(Operator):
    bl_idname = 'view3d.rt_selections_split'
    bl_label = 'Split'
    #bl_description = 'Calls Pie Operator 4'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'

    def execute(self, context):
        try:
            bpy.ops.mesh.split()
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class selections_merge(Operator):
    bl_idname = 'view3d.rt_selections_merge'
    bl_label = 'Merge'
    #bl_description = 'Calls Pie Operator 4'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'

    def execute(self, context):
        try:
            bpy.ops.mesh.remove_doubles(threshold=0.0001)
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class selections_material(Operator):
    bl_idname = 'view3d.rt_selections_material'
    bl_label = 'Select Material'
    #bl_description = 'Calls Pie Operator 4'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode == 'EDIT_MESH'

    def execute(self, context):
        try:
            bpy.ops.mesh.select_similar(type='MATERIAL', threshold=0.01)
            return {'FINISHED'} 
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class selections_hierarchy(Operator):
    bl_idname = 'view3d.rt_selections_hierarchy'
    bl_label = 'Select Hierarchy'
    #bl_description = 'Calls Pie Operator 4'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode != 'EDIT_MESH'

    def execute(self, context):
        try:
            active_obj = context.active_object
            
            if active_obj is None:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}

            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
            active_obj.select_set(True)
            
            return {'FINISHED'} 
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

classes = (
    selections_separate,
    selections_linked,
    selections_join,
    selections_split,
    selections_merge,
    selections_material,
    selections_hierarchy,
)

def register():
   for c in classes:
       bpy.utils.register_class(c)

def unregister():
    for c in classes:
       bpy.utils.unregister_class(c)