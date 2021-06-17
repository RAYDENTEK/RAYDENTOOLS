import bpy
from bpy.types import (
    Operator,
)
from collections import namedtuple
from .rt_gizmo_ops import (
    SetDrawCenterAxes,
    SetForwardVector,
)
render_options = dict()
RenderOptions = namedtuple("RenderOptions", "show_overlays show_gizmos show_face_orientation show_edge_lengths use_bloom use_gtao use_ssr show_forward show_center_axes")

def save_render_options(self, context):
    wm = context.window_manager
    self._options = RenderOptions(
        bpy.context.space_data.overlay.show_overlays, 
        bpy.context.space_data.show_gizmo, 
        bpy.context.space_data.overlay.show_face_orientation, 
        bpy.context.space_data.overlay.show_extra_edge_length, 
        bpy.context.scene.eevee.use_bloom,
        bpy.context.scene.eevee.use_gtao,
        bpy.context.scene.eevee.use_ssr,
        bpy.context.window_manager.draw_forward_vector,
        bpy.context.window_manager.draw_center_axes,
    )
    render_options[wm.view_mode] = self._options
  

def set_render_options(self, context):
    wm = context.window_manager
    bpy.context.space_data.overlay.show_overlays = render_options[wm.view_mode].show_overlays
    bpy.context.space_data.show_gizmo = render_options[wm.view_mode].show_gizmos
    bpy.context.space_data.overlay.show_face_orientation = render_options[wm.view_mode].show_face_orientation
    bpy.context.space_data.overlay.show_extra_edge_length = render_options[wm.view_mode].show_edge_lengths
    bpy.context.scene.eevee.use_bloom = render_options[wm.view_mode].use_bloom
    bpy.context.scene.eevee.use_gtao = render_options[wm.view_mode].use_gtao
    bpy.context.scene.eevee.use_ssr = render_options[wm.view_mode].use_ssr
    SetForwardVector(render_options[wm.view_mode].show_forward, self, context)
    SetDrawCenterAxes(render_options[wm.view_mode].show_center_axes, self, context)
    
    
class view_toggle_view_modes(bpy.types.Operator):
    bl_idname = 'view3d.rt_view_toggle_view_modes'
    bl_label = 'Toggle View Mode'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #try:
            wm = context.window_manager
            scene = bpy.context.scene
            save_render_options(self, context)
            
            if (wm.view_mode == 'MODELING'):
                wm.view_mode = 'RENDERING'
                if wm.view_mode not in render_options:
                    #create default options
                    new_options = RenderOptions(
                        False, 
                        False,
                        False, 
                        False,  
                        True,
                        True,
                        True,
                        False,
                        False,
                    )
                    render_options[wm.view_mode] = new_options
                
                bpy.context.space_data.shading.type = 'RENDERED'
                set_render_options(self, context)
                
                if "World_Render" in bpy.data.worlds:
                    world = bpy.data.worlds["World_Render"]
                    scene.world = world
                else:
                    self.report({'ERROR'}, "Create World_Render scene world first")
                    return {'CANCELLED'}
                    #new_world = bpy.data.worlds.new("New World")
                    #new_world.use_sky_paper = True
                    #scene.world = new_world
                    
            else:
                wm.view_mode = 'MODELING'
                
                if wm.view_mode not in render_options:
                    #create default options
                    new_options = RenderOptions(
                        True, 
                        True, 
                        True, 
                        True, 
                        False,
                        False,
                        False,
                        True,
                        True,
                    )
                    render_options[wm.view_mode] = new_options
                
                bpy.context.space_data.shading.type = 'MATERIAL'
                set_render_options(self, context)
                
                if "World" in bpy.data.worlds:
                    world = bpy.data.worlds["World"]
                    scene.world = world
                else:
                    self.report({'ERROR'}, "Create World_Render scene world first")
                    return {'CANCELLED'}
                
        
            return {'FINISHED'}
        #except:
        #    self.report({'ERROR'}, "Error occured: " + self.bl_idname)
        #    return {'CANCELLED'}


class view_toggle_edge_length(Operator):
    bl_idname = 'view3d.rt_view_toggle_edge_length'
    bl_label = 'Toggle Edge Length'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.space_data.overlay.show_extra_edge_length ^= 1
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class view_toggle_face_orientation(Operator):
    bl_idname = 'view3d.rt_view_toggle_face_orientation'
    bl_label = 'Toggle Face Orientation'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.space_data.overlay.show_face_orientation ^= 1
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class view_toggle_overlays(Operator):
    bl_idname = 'view3d.rt_view_toggle_overlays'
    bl_label = 'Toggle All Overlays'
    #bl_description = 'Calls Pie Operator 1'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.context.space_data.overlay.show_overlays ^= 1
            bpy.context.space_data.show_gizmo = bpy.context.space_data.overlay.show_overlays
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

def hide_recursively(obj):
        for child in obj.children:
            #if (child.hide_viewport is False):
            hidden_objects.append(child)
            child.hide_set(True)
            hide_recursively(child)

hidden_objects = []

class HideHierarchy(Operator):
    bl_idname = 'view3d.rt_view_hide_hierarchy'
    bl_label = 'Hide Hierarchy'
    #bl_description = 'Calls Pie Operator 6'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            #active_obj = context.active_object
            selected_objs = context.selected_objects

            #if active_obj is None or (len(context.selected_objects) == 0):
            #    self.report({'ERROR'}, "No Object")
            #    return {'CANCELLED'}

            org_obj_list = {obj.name for obj in context.selected_objects}
            
            if (len(selected_objs) < 1):
                #Unhide all
                for o in hidden_objects:
                    o.hide_set(False)
                hidden_objects.clear()
            else:
                for obj in selected_objs:
                    hide_recursively(obj)
                    #for child in obj.children:
                        #child.hide_set(True)
                        #bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        
            selected_objs = context.selected_objects
            for obj in selected_objs:
                hidden_objects.append(obj)
                obj.hide_set(True)
            
            for obj in selected_objs:
                if obj and obj.name in org_obj_list:
                    obj.select_set(False)
            
            bpy.context.view_layer.objects.active = None
        
            return {'FINISHED'}
        except:
            self.report({'ERROR'}, "Error occured: " + self.bl_idname)
            return {'CANCELLED'}

class ToggleBBox(bpy.types.Operator):
    bl_idname = "view3d.view_toggle_bbox"
    bl_label = 'Toggle Bounding Box'
    #bl_description = 'Calls Pie Operator 3'
    #bl_options = {'REGISTER', 'UNDO'}
    
    def modal(self, context, event):
        try:
            active_obj = context.active_object
            
            if active_obj is None:
                self._obj = None
            
            if self._obj is not active_obj:
                obj_new = active_obj
                bpy.context.view_layer.objects.active = self._obj
                if bpy.context.object is not None:
                    bpy.context.object.show_bounds = False
                bpy.context.view_layer.objects.active = obj_new
                self._obj = obj_new
                bpy.context.object.show_bounds = True
                #print(self._obj.dimensions)
            
            if not context.window_manager.my_operator_toggle:
                context.window_manager.event_timer_remove(self._timer)
                obj_new = active_obj
                if self._obj is not None:
                    bpy.context.view_layer.objects.active = self._obj
                    bpy.context.object.show_bounds = False
                bpy.context.view_layer.objects.active = obj_new
                return {'FINISHED'}
            
            return {'PASS_THROUGH'}
        except:
            self.report({'ERROR'}, "Error occured 1: " + self.bl_idname)
            return {'CANCELLED'}
        

    def invoke(self, context, event):
        try:
            self._timer = context.window_manager.event_timer_add(0.01, window=context.window)
            context.window_manager.modal_handler_add(self)
            active_obj = context.active_object
            if active_obj is not None:
                self._obj = active_obj
                bpy.context.object.show_bounds = True
            else:
                self._obj = None
            
            #print(self._obj.dimensions)
            return {'RUNNING_MODAL'}
        except:
            self.report({'ERROR'}, "Error occured 2: " + self.bl_idname)
            return {'CANCELLED'}

classes = (
    view_toggle_view_modes,
    view_toggle_edge_length,
    view_toggle_face_orientation,
    view_toggle_overlays,
    HideHierarchy,
    ToggleBBox,
)

def update_function(self, context):
    if self.my_operator_toggle:       
        bpy.ops.view3d.view_toggle_bbox('INVOKE_DEFAULT')
    return

def register():
    
    bpy.types.WindowManager.view_mode = bpy.props.EnumProperty(
        items = {
            ('MODELING', 'Modeling View', "-"),
            ('RENDERING', 'Rendering View', "-"),
        },
        name = "View Mode",
        #description = "Choose a method to separate mesh",
        default = 'MODELING'
    )
    
    bpy.types.WindowManager.my_operator_toggle = bpy.props.BoolProperty(default = False,update = update_function)
    

    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
       bpy.utils.unregister_class(c)