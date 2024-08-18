#!/usr/bin/python3
import os
import bpy
from mathutils import Euler


bl_info = {
    "name": "Collection to GLTF",
    "blender": (4, 1, 0),
    "category": "Import-Export",
}


class ExportOperator(bpy.types.Operator):
    bl_idname = "export.collection_to_gltf"
    bl_label = "Collection to GLTF"

    def execute(self, context: bpy.context):
        basedir = os.path.dirname(bpy.data.filepath)

        if not basedir:
            raise Exception("Blend file is not saved")

        collection = context.view_layer.active_layer_collection.collection
        children = collection.objects

        export_filepath = os.path.join(basedir, collection.name + ".gltf")
        print(f'Exporting collection "{collection.name}" to {export_filepath}')
        
        origin_matrix = None
        for child in children:
            if child.name == "Origin":
                origin_matrix = child.matrix_world.copy()
                print("Shifting to world origin.")
                break

        if origin_matrix is not None:
            for child in children:
                child.matrix_world = child.matrix_world @ origin_matrix.inverted()

        try:
            bpy.ops.export_scene.gltf(
                filepath=export_filepath,
                use_active_collection=True,
                export_apply=True
            )
        except Exception as exc:
            print(exc)
            print("Failed to save gltf!")

        if origin_matrix is not None:
            for child in children:           
                child.matrix_world = child.matrix_world @ origin_matrix

        return { "FINISHED" }


def register():
    print("Registered")
    bpy.utils.register_class(ExportOperator)


def unregister():
    print("Unregistrered")
    bpy.utils.unregister_class(ExportOperator)


if __name__ == "__main__":
    register()