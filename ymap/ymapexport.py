import bpy
import re
import math

from mathutils import Vector
from struct import pack

from ..cwxml.ymap import *
from binascii import hexlify
from ..tools.blenderhelper import remove_number_suffix
from ..tools.meshhelper import get_bound_center_from_bounds, get_combined_bound_box, get_extents
from ..sollumz_properties import SOLLUMZ_UI_NAMES, EntityLodLevel, SollumType
from ..sollumz_preferences import get_export_settings
from ..tools.utils import get_max_vector, get_min_vector
from .. import logger


def box_from_obj(obj):
    box = BoxOccluder()

    bbmin, bbmax = get_extents(obj)
    center = get_bound_center_from_bounds(bbmin, bbmax)
    dimensions = obj.dimensions

    box.center_x = round(center.x * 4)
    box.center_y = round(center.y * 4)
    box.center_z = round(center.z * 4)

    box.length = round(dimensions.x * 4)
    box.width = round(dimensions.y * 4)
    box.height = round(dimensions.z * 4)

    dir = Vector((1, 0, 0))
    dir.rotate(obj.rotation_euler)
    dir *= 0.5
    box.sin_z = round(dir.x * 32767)
    box.cos_z = round(dir.y * 32767)

    return box


def triangulate_obj(obj):
    """Convert mesh from n-polygons to triangles"""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode="OBJECT")


def get_verts_from_obj(obj):
    """
    For each vertex get its coordinates in global space (this way we don't need to apply transfroms)
    then get their bytes hex representation and append. After that for each face get its indices,
    get their bytes hex representation and append.

    :return verts: String if vertex coordinates and face indices in hex representation
    :rtype str:
    """
    verts = ''
    for v in obj.data.vertices:
        for c in obj.matrix_world @ v.co:
            verts += str(hexlify(pack('f', c)))[2:-1].upper()
    for p in obj.data.polygons:
        for i in p.vertices:
            verts += str(hexlify(pack('B', i)))[2:-1].upper()
    return verts


def model_from_obj(obj):
    triangulate_obj(obj)

    model = OccludeModel()
    model.bmin, model.bmax = get_extents(obj)
    model.verts = get_verts_from_obj(obj)
    model.num_verts_in_bytes = len(obj.data.vertices) * 12
    face_count = len(obj.data.polygons)
    model.num_tris = face_count + 32768
    model.data_size = model.num_verts_in_bytes + (face_count * 3)
    model.flags = obj.ymap_properties.flags

    return model


def entity_from_obj(obj):
    # Removing " (not found)" suffix, created when importing ymaps while entity was not found in the view layer
    obj.name = re.sub(" \(not found\)", "", obj.name.lower())

    entity = Entity()
    entity.archetype_name = remove_number_suffix(obj.name)
    entity.flags = int(obj.entity_properties.flags)
    entity.guid = int(obj.entity_properties.guid)
    entity.position = obj.location
    entity.rotation = obj.rotation_euler.to_quaternion()
    if entity.type != "CMloInstanceDef":
        entity.rotation.invert()
    entity.scale_xy = obj.scale.x
    entity.scale_z = obj.scale.z
    entity.parent_index = int(obj.entity_properties.parent_index)
    entity.lod_dist = obj.entity_properties.lod_dist
    entity.child_lod_dist = obj.entity_properties.child_lod_dist
    entity.lod_level = obj.entity_properties.lod_level.upper().replace("SOLLUMZ_", "")
    entity.num_children = int(obj.entity_properties.num_children)
    entity.priority_level = obj.entity_properties.priority_level.upper().replace("SOLLUMZ_", "")
    entity.ambient_occlusion_multiplier = int(
        obj.entity_properties.ambient_occlusion_multiplier)
    entity.artificial_ambient_occlusion = int(
        obj.entity_properties.artificial_ambient_occlusion)
    entity.tint_value = int(obj.entity_properties.tint_value)

    return entity


def calculate_extents(ymap, obj):
    bbmin = Vector((0, 0, 0))
    bbmax = Vector((0, 0, 0))
    smin = Vector((0, 0, 0))
    smax = Vector((0, 0, 0))
    found = False

    if obj.sollum_type == SollumType.DRAWABLE:
        bbmin, bbmax = get_combined_bound_box(obj)
        lod_dist = obj.entity_properties.lod_dist or 0
        smin = bbmin - Vector((lod_dist, lod_dist, lod_dist))
        smax = bbmax + Vector((lod_dist, lod_dist, lod_dist))
        found = True

    elif obj.sollum_type == SollumType.YMAP_CAR_GENERATOR:
        len = obj.ymap_cargen_properties.perpendicular_length
        bbmin = obj.location - Vector((len, len, len))
        bbmax = obj.location + Vector((len, len, len))
        smin = obj.location - Vector((len * 2.0, len * 2.0, len * 2.0))
        smax = obj.location + Vector((len * 2.0, len * 2.0, len * 2.0))
        found = True

    elif obj.sollum_type == SollumType.YMAP_BOX_OCCLUDER:
        size = round(obj.dimensions.x * 4) * 0.5
        bbmin = obj.location - Vector((size, size, size))
        bbmax = obj.location + Vector((size, size, size))
        smin = bbmin
        smax = bbmax
        found = True

    elif obj.sollum_type == SollumType.YMAP_MODEL_OCCLUDER:
        bbmin, bbmax = get_combined_bound_box(obj)
        smin = bbmin
        smax = bbmax
        found = True

    if found:
        ymap.entities_extents_min = get_min_vector(ymap.entities_extents_min, bbmin)
        ymap.entities_extents_max = get_max_vector(ymap.entities_extents_max, bbmax)
        ymap.streaming_extents_min = get_min_vector(ymap.streaming_extents_min, smin)
        ymap.streaming_extents_max = get_max_vector(ymap.streaming_extents_max, smax)


def cargen_from_obj(obj):
    cargen = CarGenerator()
    cargen.position = obj.location

    cargen.orient_x, cargen.orient_y = calculate_cargen_orient(obj)

    cargen.perpendicular_length = obj.ymap_cargen_properties.perpendicular_length
    cargen.car_model = obj.ymap_cargen_properties.car_model
    cargen.flags = obj.ymap_cargen_properties.cargen_flags
    cargen.body_color_remap_1 = obj.ymap_cargen_properties.body_color_remap_1
    cargen.body_color_remap_2 = obj.ymap_cargen_properties.body_color_remap_2
    cargen.body_color_remap_3 = obj.ymap_cargen_properties.body_color_remap_3
    cargen.body_color_remap_4 = obj.ymap_cargen_properties.body_color_remap_4
    cargen.pop_group = obj.ymap_cargen_properties.pop_group
    cargen.livery = obj.ymap_cargen_properties.livery

    return cargen


def calculate_cargen_orient(obj):
    # *-1 because GTA likes to invert values
    angle = obj.rotation_euler[2] * -1

    return 5 * math.sin(angle), 5 * math.cos(angle)


def calculate_flags(ymap: CMapData, script_loaded: bool = True):
    flags = 0
    content_flags = 0

    if script_loaded:
        flags |= 1

    if len(ymap.entities) > 0:
        for entity in ymap.entities:
            if entity.lod_level == "LODTYPES_DEPTH_HD" or entity.lod_level == "LODTYPES_DEPTH_ORPHANHD":
                content_flags |= 1

            if entity.lod_level == "LODTYPES_DEPTH_LOD":
                flags |= 2
                content_flags |= 2

            if entity.lod_level == "LODTYPES_DEPTH_SLOD1":
                flags |= 2
                content_flags |= 16

            if entity.lod_level == "LODTYPES_DEPTH_SLOD2" or entity.lod_level == "LODTYPES_DEPTH_SLOD3" or entity.lod_level == EntityLodLevel.LODTYPES_DEPTH_SLOD4:
                flags |= 2
                content_flags |= 4
                content_flags |= 16

    return flags, content_flags


def ymap_from_object(obj):
    ymap = CMapData()

    # Default extents
    max_int = (2**31) - 1
    ymap.entities_extents_min = Vector((max_int, max_int, max_int))
    ymap.entities_extents_max = Vector((-max_int, -max_int, -max_int))
    ymap.streaming_extents_min = Vector((max_int, max_int, max_int))
    ymap.streaming_extents_max = Vector((-max_int, -max_int, -max_int))

    export_settings = get_export_settings()
    exclude_entities = export_settings.ymap_exclude_entities
    exclude_box_occluders = export_settings.ymap_box_occluders
    exclude_model_occluders = export_settings.ymap_model_occluders
    exclude_cargens = export_settings.ymap_car_generators

    for child in obj.children:
        # Entities
        if child.sollum_type == SollumType.YMAP_ENTITY_GROUP and not exclude_entities:
            for entity_obj in child.children:
                if entity_obj.sollum_type == SollumType.DRAWABLE:
                    ymap.entities.append(entity_from_obj(entity_obj))
                    calculate_extents(ymap, entity_obj)
                else:
                    logger.warning(f"Object {entity_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.DRAWABLE]} type.")

        # Box occluders
        if child.sollum_type == SollumType.YMAP_BOX_OCCLUDER_GROUP and not exclude_box_occluders:
            for box_obj in child.children:
                if box_obj.sollum_type == SollumType.YMAP_BOX_OCCLUDER:
                    ymap.box_occluders.append(box_from_obj(box_obj))
                    calculate_extents(ymap, box_obj)
                else:
                    logger.warning(f"Object {box_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.YMAP_BOX_OCCLUDER]} type.")

        # Model occluders
        if child.sollum_type == SollumType.YMAP_MODEL_OCCLUDER_GROUP and not exclude_model_occluders:
            for model_obj in child.children:
                if model_obj.sollum_type == SollumType.YMAP_MODEL_OCCLUDER:
                    if len(model_obj.data.vertices) > 256:
                        logger.warning(f"Object {model_obj.name} has too many vertices and will be skipped. It can not have more than 256 vertices.")
                        continue

                    ymap.occlude_models.append(model_from_obj(model_obj))
                    calculate_extents(ymap, model_obj)
                else:
                    logger.warning(f"Object {model_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.YMAP_MODEL_OCCLUDER]} type.")

        # Car generators
        if child.sollum_type == SollumType.YMAP_CAR_GENERATOR_GROUP and not exclude_cargens:
            for cargen_obj in child.children:
                if cargen_obj.sollum_type == SollumType.YMAP_CAR_GENERATOR:
                    ymap.car_generators.append(cargen_from_obj(cargen_obj))
                    calculate_extents(ymap, cargen_obj)
                else:
                    logger.warning(f"Object {cargen_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.YMAP_CAR_GENERATOR]} type.")

        # TODO: physics_dictionaries
        # TODO: time cycle
        # TODO: lod ligths
        # TODO: distant lod lights

    print("Scripted?", obj.ymap_properties.script_loaded)
    ymap.name = remove_number_suffix(obj.name)
    ymap.parent = obj.ymap_properties.parent
    flags, content_flags = calculate_flags(ymap, obj.ymap_properties.script_loaded)

    ymap.flags = flags
    ymap.content_flags = content_flags

    ymap.block.version = obj.ymap_properties.block.version
    ymap.block.versiflagson = obj.ymap_properties.block.flags
    ymap.block.name = obj.ymap_properties.block.name
    ymap.block.exported_by = obj.ymap_properties.block.exported_by
    ymap.block.owner = obj.ymap_properties.block.owner
    ymap.block.time = obj.ymap_properties.block.time

    return ymap


def export_ymap(obj: bpy.types.Object, filepath: str) -> bool:

    print("Scripted?", obj.ymap_properties.script_loaded)
    ymap = ymap_from_object(obj)
    ymap.write_xml(filepath)
    return True
