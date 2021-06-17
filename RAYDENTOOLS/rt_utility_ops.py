import bpy
from bpy.types import (
    Operator,
)  

class ParentOperator(Operator):
    """Parent and fix location to reflect local location"""
    bl_idname = "view3d.rt_parent"
    bl_label = "Parent"
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode != 'EDIT_MESH'

    def execute(self, context):
        try:
            active_obj = context.active_object
            selected_objs = context.selected_objects
            
            if active_obj is None:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            
            if (len(selected_objs) < 2):
                self.report({'ERROR'}, "Select more objects")
                return {'CANCELLED'}
            
            parent_location = active_obj.matrix_world.copy()
            location_active = active_obj.location.copy()
                
            matrices = dict()
            for obj in selected_objs:
                matrices[obj] = obj.matrix_world.copy()
            
            bpy.ops.object.parent_no_inverse_set()
            
            for obj in selected_objs:
                bpy.context.view_layer.objects.active = obj
                
                if (obj is not active_obj):
                    inv = parent_location
                    inv.invert()
                    obj.matrix_local = inv @ matrices[obj]
                    
            bpy.context.view_layer.objects.active = active_obj
            active_obj.location = location_active
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class UnparentOperator(Operator):
    """Unparent and keep world location"""
    bl_idname = "view3d.rt_unparent"
    bl_label = "Unparent"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode != 'EDIT_MESH'

    def execute(self, context):
        try:
            active_obj = context.active_object
            if active_obj is None or (len(context.selected_objects) == 0):
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            
            if active_obj.parent is None:
                self.report({'ERROR'}, "No Parent")
                return {'CANCELLED'}     
            
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class SetNormalsOperator(Operator):
    """Sets smoothing, auto-creasing by sharp edges (strangely called auto smooth in blender) & adds a weighted normals modifier"""
    bl_idname = "view3d.rt_set_normals"
    bl_label = "Set Normals"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.mode != 'EDIT_MESH'

    def execute(self, context):
        try:
            selected_objs = context.selected_objects
            active_obj = bpy.context.active_object
            
            if active_obj is None or (len(context.selected_objects) == 0):
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}            
            
            for obj in selected_objs:
                if obj.type != 'MESH':
                    self.report({'ERROR'}, "Not a mesh")
                    return {'CANCELLED'}    
                #bpy.context.view_layer.objects.active = obj
                #bpy.ops.object.shade_smooth()
                mesh = obj.data
                #for face in mesh.polygons:
                #    face.use_smooth = True
                values = [True] * len(mesh.polygons)
                mesh.polygons.foreach_set("use_smooth", values)

                obj.data.use_auto_smooth = True
                obj.data.auto_smooth_angle = 3.14159
            
                mod = obj.modifiers.get("WeightedNormal")
                if mod is None:
                    mod = obj.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
                mod.weight = 100
                mod.keep_sharp = True
                
                #bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                #obj.modifiers["WeightedNormal"].weight = 100
                #obj.modifiers["WeightedNormal"].keep_sharp = True
            
            bpy.context.view_layer.objects.active = active_obj
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class MergeHierarchyOperator(Operator):
    bl_idname = 'view3d.rt_merge_hierarchy'
    bl_label = 'Merge Hierarchy'
    #bl_description = 'Calls Pie Operator 6'
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
            selected_objs = context.selected_objects
            for obj in selected_objs:
                if obj.type != 'MESH':
                    obj.select_set(False)
        
            selected_objs = context.selected_objects
            if len(selected_objs):
                bpy.ops.object.join()
                
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

classes = (
    ParentOperator,
    UnparentOperator,
    SetNormalsOperator,
    MergeHierarchyOperator,
)

def register():
   for c in classes:
       bpy.utils.register_class(c)

def unregister():
    for c in classes:
       bpy.utils.unregister_class(c)