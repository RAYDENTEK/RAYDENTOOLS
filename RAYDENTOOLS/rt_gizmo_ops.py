import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

def draw_line(start, end, color):
    shader_line = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch = batch_for_shader(shader_line, 'LINES', {"pos": [start, end]})
    try:
        if start is not None and end is not None:
            shader_line.bind()
            shader_line.uniform_float("color", color)
            #shader_line.uniform_float("lineWidth", imm_line_width)
            #shader_line.uniform_float("viewportSize", imm_viewport)
            batch.draw(shader_line)
    except:
        pass
def get_camera_view_distance(self, context, point = (0,0,0)):
    distance = 1
    try:
        areas = [a for a in context.screen.areas if a.type == 'VIEW_3D']
        if not len(areas):
            return 1
            
        #rv = context.space_data.region_3d
        rv = areas[0].spaces[0].region_3d
    
        #if rv is None:
        #    rv = context.space_data.region_quadview
        if rv is None:
            return 1
        
        view_matrix = rv.view_matrix
        if rv.is_perspective:
            distance = (view_matrix @ point).length
        else:
            distance = rv.view_distance
    except:
        pass
    return distance

def draw_forward_callback(self, context):
    active_obj = bpy.context.active_object
    if active_obj is None:
        return
    direction = Vector((0,-1.0,0))
    color = (0.0, 0.0, 0.0, 0.5)
    draw_axis(self, context, active_obj, direction, color)
    
def draw_center_axes_callback(self, context):
    active_obj = bpy.context.active_object
    if active_obj is None:
        return
    direction = Vector((0,0,1.0))
    color = (0.0, 0.0, 1.0, 0.5)
    draw_axis(self, context, active_obj, direction, color)
    direction = Vector((1.0,0,0))
    color = (1.0, 0.0, 0.0, 0.5)
    draw_axis(self, context, active_obj, direction, color)
    direction = Vector((0,1.0,0))
    color = (0.0, 1.0, 0.0, 0.5)
    draw_axis(self, context, active_obj, direction, color)

def draw_axis(self, context, active_obj, direction, color):
    try:
        rotation_matrix = active_obj.matrix_local.copy()
        rotation = rotation_matrix.to_quaternion()
        rotation_matrix = rotation.to_matrix().to_4x4()
        
        if active_obj.parent is not None:
            parent_matrix = active_obj.parent.matrix_world.copy()
            location_active = parent_matrix @ active_obj.location.copy()
            
        else:
            location_active = active_obj.location.copy()
            
        start = location_active
        
        distance  = get_camera_view_distance(self, context, start)
        base_size = 0.5
        base_distance = 10
        size = distance / base_distance * base_size
        
        if active_obj.parent is not None:
            vec = rotation_matrix @ (direction * size)
            end_location = vec +  active_obj.location.copy()
            end_location = parent_matrix @ end_location
        else:
            vec = rotation_matrix @ (direction * size)
            end_location = vec + active_obj.location.copy()
        end = end_location
        
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        #bgl.glEnable(bgl.GL_DEPTH_TEST)
        bgl.glLineWidth(3)
        draw_line(start, end, color)
        
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
        #bgl.glEnable(bgl.GL_DEPTH_TEST)
    except:
        pass
    
class VIEW3D_OT_draw_forward_vector(bpy.types.Operator):
    bl_idname = "view3d.draw_forward_vector"
    bl_label = "Forward Vector"
    
    _handle = None
    
    def modal(self, context, event):
        context.tag.area_redraw()
        if not context.window_manager.draw_forward_vector:
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
    
    @staticmethod
    def handle_add(self, context):
        VIEW3D_OT_draw_forward_vector._handle = bpy.types.SpaceView3D.draw_handler_add(
            draw_forward_callback, 
            (self, context),
            'WINDOW', 'POST_VIEW')
            
    @staticmethod
    def handle_remove(context):
        _handle = VIEW3D_OT_draw_forward_vector._handle
        if _handle != None:
            bpy.types.SpaceView3D.draw_handler_remove(_handle, 'WINDOW')
        VIEW3D_OT_draw_forward_vector._handle = None
    
    def invoke(self, context, event):
        if not context.window_manager.draw_forward_vector:
            context.window_manager.draw_forward_vector = True
            VIEW3D_OT_draw_forward_vector.handle_add(self,context)
            return {'RUNNING_MODAL'}
        else:
            context.window_manager.draw_forward_vector = False
            VIEW3D_OT_draw_forward_vector.handle_remove(context)
            return {'CANCELLED'}
        
class VIEW3D_OT_draw_center_axes(bpy.types.Operator):
    bl_idname = "view3d.draw_center_axes"
    bl_label = "Center Axes"
    _handle2 = None
    def modal(self, context, event):
        context.tag.area_redraw()
        if not context.window_manager.draw_center_axes:
            return {'CANCELLED'}
        return {'PASS_THROUGH'}
    
    @staticmethod
    def handle_add(self, context):
        VIEW3D_OT_draw_center_axes._handle2 = bpy.types.SpaceView3D.draw_handler_add(
            draw_center_axes_callback, 
            (self, context),
            'WINDOW', 'POST_VIEW')
            
    @staticmethod
    def handle_remove(context):
        _handle2 = VIEW3D_OT_draw_center_axes._handle2
        if _handle2 != None:
            bpy.types.SpaceView3D.draw_handler_remove(_handle2, 'WINDOW')
        VIEW3D_OT_draw_center_axes._handle2 = None
    
    def invoke(self, context, event):
        if not context.window_manager.draw_center_axes:
            context.window_manager.draw_center_axes = True
            VIEW3D_OT_draw_center_axes.handle_add(self,context)
            return {'RUNNING_MODAL'}
        else:
            context.window_manager.draw_center_axes = False
            VIEW3D_OT_draw_center_axes.handle_remove(context)
            return {'CANCELLED'}
def SetDrawCenterAxes(is_active, self, context):
    if (is_active):
        if not context.window_manager.draw_center_axes:
            bpy.ops.view3d.draw_center_axes('INVOKE_DEFAULT')
        
    else:
        if context.window_manager.draw_center_axes:
            bpy.ops.view3d.draw_center_axes('INVOKE_DEFAULT')
    
def SetForwardVector(is_active, self, context):
    if (is_active):
        if not context.window_manager.draw_forward_vector:
            bpy.ops.view3d.draw_forward_vector('INVOKE_DEFAULT')
    else:
        if context.window_manager.draw_forward_vector:
            bpy.ops.view3d.draw_forward_vector('INVOKE_DEFAULT')
    
def register():
    bpy.types.WindowManager.show_origin_axes = bpy.props.BoolProperty(
        name = "Is Show Origin Axes",
        default = False
    )
    bpy.types.WindowManager.draw_forward_vector = bpy.props.BoolProperty(
        name = "Is Draw Forward Vector",
        default = False
    )
    bpy.types.WindowManager.draw_center_axes = bpy.props.BoolProperty(
        name = "Is Draw Center Axes",
        default = False
    )
    bpy.utils.register_class(VIEW3D_OT_draw_center_axes)
    bpy.utils.register_class(VIEW3D_OT_draw_forward_vector)
    

def unregister():
    VIEW3D_OT_draw_forward_vector.handle_remove(bpy.context)
    VIEW3D_OT_draw_center_axes.handle_remove(bpy.context)
    bpy.utils.unregister_class(VIEW3D_OT_draw_center_axes)
    bpy.utils.unregister_class(VIEW3D_OT_draw_forward_vector)
    bpy.context.window_manager.draw_center_axes = False
