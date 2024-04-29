import bpy

from ..sollumz_properties import SOLLUMZ_UI_NAMES, SollumType
from ..sollumz_helper import mesh_join, hide_set_obj_and_children, delete_obj_and_children
from ..cwxml.drawable import YDR
from ..ydr.ydrimport import drawable_to_obj


ADDON_NAME = 'Sollumz-Grass'
ADDONS_PATH = bpy.utils.user_resource('SCRIPTS') + '/addons'
ADDON_PATH = ADDONS_PATH + '/' + ADDON_NAME
DATA_PATH  = ADDON_PATH + '/data'
PROC_PATH = DATA_PATH + '/proc_drawables'
TEXTURE_PATH = PROC_PATH + '/textures'

class CustomImportSettings():
    batch_mode                 = "SELECTED_FILE"
    import_as_asset            = True
    join_geometries            = False
    split_by_bone              = False
    import_ext_skeleton        = False
    selected_armature          = -1
    ymap_skip_missing_entities = True
    ymap_exclude_entities      = False
    ymap_box_occluders         = False
    ymap_model_occluders       = False
    ymap_car_generators        = False
    ymap_instanced_data        = False

def ensure_grass_proc_model(archetype_name):
    
    GRASS_PROC_COLLECTION = bpy.data.collections.get('grass_proc_models')
    
    if GRASS_PROC_COLLECTION is None:
        GRASS_PROC_COLLECTION = bpy.data.collections.new('grass_proc_models')
        bpy.context.collection.children.link(GRASS_PROC_COLLECTION)

    for obj in GRASS_PROC_COLLECTION.objects:
        if obj.name.split('.')[0] == archetype_name:
            return obj
    
    print('loading procedural model: ' + archetype_name)
    
    filepath = PROC_PATH + '/' + archetype_name + '.ydr.xml'
    ydr_xml = YDR.from_xml_file(filepath)
    
    drawable_obj = drawable_to_obj(ydr_xml, filepath, archetype_name, bones_override=None, materials=None, import_settings=CustomImportSettings(), is_ydd=False)
    base_obj = mesh_join([x.children[0] for x in drawable_obj.children], archetype_name)
    
    GRASS_PROC_COLLECTION.objects.link(base_obj)
    
    delete_obj_and_children(drawable_obj)
    hide_set_obj_and_children(base_obj, True)
    
    tree = base_obj.data.materials[0].node_tree
    nodes = tree.nodes
    attr_node = nodes.new('ShaderNodeAttribute')
    attr_node.name = 'sollum_grass_color_attribute'
    attr_node.attribute_name = 'ymap_grass_instance_list_item_properties.color'
    attr_node.attribute_type = 'OBJECT'
    
    color_mix_node = nodes.new('ShaderNodeMix')
    color_mix_node.data_type = 'RGBA'
    color_mix_node.clamp_factor = True
    color_mix_node.factor_mode = 'UNIFORM'
    color_mix_node.blend_type = 'COLOR'

    diffuse_sampler_node = nodes['DiffuseSampler']

    tree.links.new(diffuse_sampler_node.outputs[0], color_mix_node.inputs[6])
    tree.links.new(attr_node.outputs[0], color_mix_node.inputs[7])
    
    tree.links.new(color_mix_node.outputs[2], nodes["Principled BSDF"].inputs[0])
    
    bpy.ops.file.find_missing_files(directory=TEXTURE_PATH)
        
    return base_obj

# TODO: This is not a real flag calculation, definitely need to do better
def calculate_ymap_content_flags(selected_ymap=None, sollum_type=None):
    content_flags = []
    if sollum_type == SollumType.YMAP_ENTITY_GROUP:
        selected_ymap.ymap_properties.content_flags_toggle.has_hd = True
        selected_ymap.ymap_properties.content_flags_toggle.has_physics = True
        selected_ymap.ymap_properties.content_flags_toggle.has_occl = False
    elif sollum_type == SollumType.YMAP_MODEL_OCCLUDER_GROUP or sollum_type == SollumType.YMAP_BOX_OCCLUDER_GROUP:
        selected_ymap.ymap_properties.content_flags_toggle.has_hd = False
        selected_ymap.ymap_properties.content_flags_toggle.has_physics = False
        selected_ymap.ymap_properties.content_flags_toggle.has_occl = True
        selected_ymap.ymap_properties.content_flags_toggle.has_grass = False
    elif sollum_type == SollumType.YMAP_GRASS_INSTANCED_DATA:
        selected_ymap.ymap_properties.content_flags_toggle.has_hd = False
        selected_ymap.ymap_properties.content_flags_toggle.has_physics = True
        selected_ymap.ymap_properties.content_flags_toggle.has_occl = False
        selected_ymap.ymap_properties.content_flags_toggle.has_grass = True
        
    return content_flags

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
    if sollum_type == SollumType.YMAP_ENTITY_GROUP:
        selected_ymap.ymap_properties.content_flags_toggle.has_hd = True
        selected_ymap.ymap_properties.content_flags_toggle.has_physics = True
    elif sollum_type == SollumType.YMAP_BOX_OCCLUDER_GROUP or sollum_type == SollumType.YMAP_MODEL_OCCLUDER_GROUP:
        selected_ymap.ymap_properties.content_flags_toggle.has_occl = True
    elif sollum_type == SollumType.YMAP_GRASS_INSTANCED_DATA:
        selected_ymap.ymap_properties.content_flags_toggle.has_physics = True
        selected_ymap.ymap_properties.content_flags_toggle.has_grass = True
    empty.parent = selected_ymap
    calculate_ymap_content_flags(selected_ymap, sollum_type)
    return empty

def add_occluder_material(sollum_type=None):
    """Get occluder material or create it if not exist."""
    mat_name = ""
    mat_color = []
    mat_transparency = 0.5
    
    if sollum_type == SollumType.YMAP_MODEL_OCCLUDER:
        mat_name = "model_occluder_material"
        mat_color = (1, 0, 0, mat_transparency)
        emission_color = (1, 0, 0, 1)
    elif sollum_type == SollumType.YMAP_BOX_OCCLUDER:
        mat_name = "box_occluder_material"
        mat_color = (0, 0, 1, mat_transparency)
        emission_color = (0, 0, 1, 1)

    material = bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name)
    material.blend_method = "BLEND"
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs['Alpha'].default_value = mat_transparency
    material.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = mat_color
    material.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 0
    material.node_tree.nodes["Principled BSDF"].inputs['Metallic'].default_value = 0
    material.node_tree.nodes["Principled BSDF"].inputs['Emission'].default_value = emission_color


    return material
        
