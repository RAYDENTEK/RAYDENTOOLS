import bpy

class RT_Panel(bpy.types.Panel):
    bl_idname= "RT_Panel"
    bl_label = "Rayden Tools"
    bl_category = "RAYDENTOOLS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        layout.label(text="Utility Actions")
        row = layout.row()
        row.operator('view3d.rt_set_normals',text="Set Normals")
        row = layout.row()
        row.operator('view3d.rt_parent',text="Parent")
        row = layout.row()
        row.operator('view3d.rt_unparent',text="Unparent")
        row = layout.row()
        row.operator('view3d.rt_merge_hierarchy',text="Merge Hierarchy")
        