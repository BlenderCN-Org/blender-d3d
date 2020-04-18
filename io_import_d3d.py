bl_info = {
    "name": "Import D3D",
    "description": "Importer for GameMaker's legacy D3D model format",
    "author": "Bart Teunis",
    "version": (0, 0, 6),
    "blender": (2, 79, 0),
    "location": "File > Import",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/bartteunis/blender-d3d/wiki",
    "category": "Import-Export"}

import bpy, bmesh
from mathutils import *

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportD3D(Operator, ImportHelper):
    """Import legacy D3D model format of GameMaker"""
    bl_idname = "import_mesh.d3d"  # important since its how bpy.ops.import_mesh.d3d is constructed
    bl_label = "Import D3D"

    # ImportHelper mixin class uses this
    filename_ext = ".d3d"

    filter_glob = StringProperty(
            default="*.txt;*.d3d;*.gmmod",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    import_as_separate_objects = BoolProperty(
            name="One Object Per Primitive",
            description="Import each primitive in the file as a separate Blender object",
            default=False,
            )

    def execute(self, context):
        # https://blender.stackexchange.com/a/416
        file = open(self.filepath, 'r')
        version = int(file.readline())
        no_lines = int(file.readline())
        if version != 100:
            self.report({'ERROR'}, "Unsupported version number")
            return {'FINISHED'}
        
        mat_identity = Matrix()
        if self.import_as_separate_objects:
            # Add a new object of type 'MESH' for each primitive in the file
            pass
        else:
            # Add all primitives to a single new mesh (default)
            bpy.ops.object.add(type='MESH')
            obj = bpy.context.object
            mesh = obj.data
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(mesh)
            
            for i in range(no_lines):
                # Parse each line
                line = file.readline()
                print(line)
                type, *params = [float(item) for item in line.split()]
                
                # https://docs.blender.org/api/current/bmesh.ops.html
                if   type ==  0:
                    # d3d_model_primitive_begin
                    # TODO only support pr_trianglelist for now
                    pass
                elif type ==  1:
                    # d3d_model_primitive_end
                    # see bmesh.ops.contextual_create for this
                    pass
                elif type ==  2:
                    pass
                elif type ==  3:
                    pass
                elif type ==  4:
                    pass
                elif type ==  5:
                    pass
                elif type ==  6:
                    pass
                elif type ==  7:
                    pass
                elif type ==  8:
                    pass
                elif type ==  9:
                    pass
                elif type == 10:
                    # Box, d3d_model_block
                    bmesh.ops.create_cube(bm, size=1, matrix=mat_identity, calc_uvs=True)
                elif type == 11:
                    # Cylinder, d3d_model_cylinder
                    x1,y1,z1,x2,y2,z2,hrepeat,vrepeat,closed,steps = params
                    pos1, pos2 = Vector([x1, y1, z1]), Vector([x2, y2, z2])
                    dia = (pos2-pos1)[0]
                    height = pos2.z-pos1.z
                    print(params)
                    bmesh.ops.create_cone(bm, cap_ends=closed, cap_tris=False, segments=steps, diameter1=dia, diameter2=dia, depth=height, matrix=mat_identity, calc_uvs=True)
                elif type == 12:
                    # Cone, d3d_model_cone
                    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, diameter1=1, diameter2=2, depth=2, matrix=mat_identity, calc_uvs=True)
                elif type == 13:
                    # UV Sphere, d3d_model_ellipsoid
                    bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=12, diameter=2, matrix=mat_identity, calc_uvs=True)
                elif type == 14:
                    # Grid, d3d_model_wall
                    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size = 1, matrix=mat_identity, calc_uvs=True)
                elif type == 15:
                    # Grid, d3d_model_floor
                    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size = 1, matrix=mat_identity, calc_uvs=True)
            
            bmesh.update_edit_mesh(obj.data)
            
            bpy.ops.object.mode_set(mode='OBJECT')
        
        file.close()
        
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportD3D.bl_idname, text="Import D3D (.d3d/.gmmod)")


def register():
    bpy.utils.register_class(ImportD3D)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportD3D)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_mesh.d3d('INVOKE_DEFAULT')