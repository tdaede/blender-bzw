import bpy
from math import pi

def write_transform(f, object):
    f.write('scale ')
    for s in object.scale:
        f.write(str(s) + ' ')
    f.write('\n')
    r = object.rotation_euler
    f.write('spin '+str(r[0]*180/pi)+' 1 0 0\n')
    f.write('spin '+str(r[1]*180/pi)+' 0 1 0\n')
    f.write('spin '+str(r[2]*180/pi)+' 0 0 1\n')
    f.write('shift ')
    for s in object.location:
        f.write(str(s) + ' ')
    f.write('\n')

def write_map(context, filepath, export_as_group):
    print("Exporting BZW map...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("# BZW Exporter by Thomas Daede\n")
    for object in bpy.data.objects:
        if object.type != 'MESH':
            continue
        mesh = object.data
        f.write('mesh\n')
        f.write('name '+object.name+'\n')
        write_transform(f,object)
        for v in mesh.vertices:
            f.write('vertex ')
            for c in v.co:
                f.write(str(c) + ' ')
            f.write('\n')
            f.write('normal ')
            for n in v.normal:
                f.write(str(n) + ' ')
            f.write('\n')
        for p in mesh.polygons:
            f.write('face\n')
            f.write('vertices ')
            for v in p.vertices:
                f.write(str(v) + ' ')
            f.write('\n')
            f.write('normals ')
            for v in p.vertices:
                f.write(str(v) + ' ')
            f.write('\n')
            f.write('endface\n')
        f.write('end\n')
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportBZWMap(Operator, ExportHelper):
    """Export BZW Map tool documentation goes here"""
    bl_idname = "export_bzw.export_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export BZW Map"

    # ExportHelper mixin class uses this
    filename_ext = ".bzw"

    filter_glob = StringProperty(
            default="*.bzw",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    export_as_group = BoolProperty(
            name="Export as Group",
            description="Wraps map in a define. Useful for including in a hand-edited map",
            default=False,
            options={'HIDDEN'},
            )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.export_as_group)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportBZWMap.bl_idname, text="BZW Export")


def register():
    bpy.utils.register_class(ExportBZWMap)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportBZWMap)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    #register()

    # test call
    #bpy.ops.export_test.some_data('INVOKE_DEFAULT')
    #unregister()
    write_map(bpy.context,'/home/thomas/wheel.txt',False)