# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_dering


import bmesh
import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Dering",
    "description": "Removes edges by checker deselecting, starting from single selected edge",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Dering",
    "doc_url": "https://github.com/Korchy/1d_dering",
    "tracker_url": "https://github.com/Korchy/1d_dering",
    "category": "All"
}


# MAIN CLASS

class Dering:

    @classmethod
    def dering_by_selection(cls, context):
        # make dering for each selected edge
        # save selected edges
        bm = bmesh.from_edit_mesh(context.object.data)
        selected_edges = [edge for edge in bm.edges if edge.select]
        # loop_multi_select()
        bpy.ops.mesh.loop_multi_select(ring=True)
        # select_nth()
        # it works starting by active edge, so - for each saved selected edge, make it active and call operator
        for edge in selected_edges:
            # make edge active
            bm.select_history.clear()
            edge.select = True
            bm.select_history.add(edge)
            bmesh.update_edit_mesh(context.object.data)
            # call operator
            bpy.ops.mesh.select_nth()
        # loop_multi_select
        bpy.ops.mesh.loop_multi_select(ring=False)
        # dissolve_mode
        bpy.ops.mesh.dissolve_mode(use_verts=True)

    @staticmethod
    def ui(layout, context, area):
        # ui panels
        # dering
        box = layout.box().column()
        box.label(text='Dering')
        op = box.operator(
            operator='dering.dering',
            icon='UV_EDGESEL'
        )


# OPERATORS

class Dering_OT_dering(Operator):
    bl_idname = 'dering.dering'
    bl_label = 'Dering'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        Dering.dering_by_selection(
            context=context
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object.mode == 'EDIT'


# PANELS

class Dering_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Dering'
    bl_category = '1D'

    def draw(self, context):
        Dering.ui(
            layout=self.layout,
            context=context,
            area='VIEWPORT'
        )


# REGISTER

def register(ui=True):
    register_class(Dering_OT_dering)
    if ui:
        register_class(Dering_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(Dering_PT_panel)
    # butch clean
    unregister_class(Dering_OT_dering)


if __name__ == '__main__':
    register()
