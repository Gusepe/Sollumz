import bpy

from ..sollumz_properties import SOLLUMZ_UI_NAMES, SollumType
from ..tools.blenderhelper import find_bsdf_and_material_output


def create_ymap(name="ymap", sollum_type=SollumType.YMAP):
    empty = bpy.data.objects.new(SOLLUMZ_UI_NAMES[sollum_type], None)
    empty.empty_display_size = 0
    empty.sollum_type = sollum_type
    empty.name = name
    empty.ymap_properties.name = name
    bpy.context.collection.objects.link(empty)
    return empty


def create_ymap_group(sollum_type=None, selected_ymap=None, empty_name=None):
    empty = bpy.data.objects.new(SOLLUMZ_UI_NAMES[sollum_type], None)
    empty.empty_display_size = 0
    empty.sollum_type = sollum_type
    empty.name = empty_name
    bpy.context.collection.objects.link(empty)
    empty.parent = selected_ymap
    return empty


def add_occluder_material(sollum_type=None):
    """Get occluder material or create it if not exist."""
    mat_name = ""
    mat_color = []
    mat_transparency = 0.5

    if sollum_type == SollumType.YMAP_MODEL_OCCLUDER:
        mat_name = "model_occluder_material"
        mat_color = (1, 0, 0, mat_transparency)
    elif sollum_type == SollumType.YMAP_BOX_OCCLUDER:
        mat_name = "box_occluder_material"
        mat_color = (0, 0, 1, mat_transparency)

    material = bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name)
    material.blend_method = "BLEND"
    material.use_nodes = True
    bsdf, _ = find_bsdf_and_material_output(material)
    bsdf.inputs["Alpha"].default_value = mat_transparency
    bsdf.inputs["Base Color"].default_value = mat_color
    bsdf.inputs["Specular"].default_value = 0
    bsdf.inputs["Roughness"].default_value = 0
    bsdf.inputs["Metallic"].default_value = 0

    return material
