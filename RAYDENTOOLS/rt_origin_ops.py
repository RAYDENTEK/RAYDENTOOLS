import bpy
from bpy.types import (
    Operator,
)

def has_children(obj, self, context):
    has_children_bool = False
    selected_objs = context.selected_objects
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    obj.select_set(False)
    children = context.selected_objects
    if (len(children) > 0):
        for c in children:
            c.select_set(False)
        for s in selected_objs:
            s.select_set(True)
        has_children_bool = True
    obj.select_set(True)
    return has_children_bool

class origin_set_to_cursor(Operator):
    bl_idname = 'view3d.rt_origin_set_to_cursor'
    bl_label = 'Origin to Cursor (Location Only)'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            active_obj = context.active_object
            if active_obj is not None:
                if has_children(active_obj, self, context):
                    self.report({'ERROR'}, "Don't use on parents, children will have messed up transforms")
                    return {'CANCELLED'}
                
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
    
class origin_set_to_selected(Operator):
    bl_idname = 'view3d.rt_origin_set_to_selected'
    bl_label = 'Origin to Selected (Location Only)'
    #bl_description = 'Calls Pie Operator 3'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        try:
            cursor_start_location = bpy.context.scene.cursor.location.copy()
            active_obj = context.active_object
            if active_obj is None:
                self.report({'ERROR'}, "No Object")
                return {'CANCELLED'}
            
            if has_children(active_obj, self, context):
                self.report({'ERROR'}, "Don't use on parents, children will have messed up transforms")
                return {'CANCELLED'}
            
            if active_obj.mode == 'EDIT':
                if active_obj.type == 'MESH':
                    if  context.object.data.total_vert_sel == 0:
                        bpy.ops.view3d.snap_cursor_to_center()
                    else:
                        bpy.ops.view3d.snap_cursor_to_selected()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR', center='BOUNDS')
                    bpy.ops.object.mode_set(mode='EDIT')
                else:
                    bpy.ops.view3d.snap_cursor_to_selected()
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            else:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            bpy.context.scene.cursor.location = (cursor_start_location[0],cursor_start_location[1],cursor_start_location[2])
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}
        
class origin_edit(Operator):
    bl_idname = 'view3d.rt_origin_edit'
    bl_label = 'Toggle Origin Editing'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            #context.tool_settings.use_proportional_edit ^= 1
            #context.tool_settings.use_proportional_edit_objects ^= 1
            bpy.context.scene.tool_settings.use_transform_data_origin ^= 1
            bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
            bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

classes = (
    origin_set_to_cursor,
    origin_edit,
    origin_set_to_selected,
)

def register():
   for c in classes:
       bpy.utils.register_class(c)

def unregister():
    for c in classes:
       bpy.utils.unregister_class(c)
