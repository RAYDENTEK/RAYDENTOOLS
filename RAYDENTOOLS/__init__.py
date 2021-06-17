bl_info = {
    "name" : "RAYDENTOOLS",
    "author" : "RAYDEN",
    "description" : "Custom Productivity Tools for Blender",
    "blender" : (2, 93, 1),
    "version" : (1, 0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}
import bpy
from . rt_panel import RT_Panel
from . import (
    rt_utility_pie,
    rt_utility_ops,
    rt_cursor_pie,
    rt_cursor_ops,
    rt_manipulation_modes_pie,
    rt_manipulation_modes_ops,
    rt_origin_pie,
    rt_origin_ops,
    rt_view_pie,
    rt_view_ops,
    rt_selections_pie,
    rt_selections_ops,
    rt_gizmo_ops,
)

def register():
    rt_manipulation_modes_pie.register()
    rt_manipulation_modes_ops.register()
    rt_cursor_pie.register()
    rt_cursor_ops.register()
    rt_utility_pie.register()
    rt_utility_ops.register()
    rt_origin_pie.register()
    rt_origin_ops.register()
    rt_view_pie.register()
    rt_view_ops.register()
    rt_selections_pie.register()
    rt_selections_ops.register()
    rt_gizmo_ops.register()
    #for c in classes:
    #    bpy.utils.register_class(c)
    bpy.utils.register_class(RT_Panel)

def unregister():
    rt_manipulation_modes_pie.unregister()
    rt_manipulation_modes_ops.unregister()
    rt_cursor_pie.unregister()
    rt_cursor_ops.unregister()
    rt_utility_pie.unregister()
    rt_utility_ops.unregister()
    rt_origin_pie.unregister()
    rt_origin_ops.unregister()
    rt_view_pie.unregister()
    rt_view_ops.unregister()
    rt_selections_pie.unregister()
    rt_selections_ops.unregister()
    rt_gizmo_ops.unregister()
    #for c in classes:
    #    bpy.utils.unregister_class(c)
    bpy.utils.unregister_class(RT_Panel)


#register, unregister = bpy.utils.register_classes_factory(classes)