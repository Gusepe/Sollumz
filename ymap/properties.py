import bpy
from mathutils import Vector
from bpy.props import (EnumProperty, FloatProperty, PointerProperty, StringProperty, IntProperty, FloatVectorProperty, BoolProperty, IntVectorProperty, CollectionProperty)
from ..tools.utils import int_to_bool_list, flag_prop_to_list, flag_list_to_int
from ..tools.ymaphelper import ensure_grass_proc_model

def update_uint_prop(self, context, var_name):
    """Work around for storing uint values as a Blender property (credits: CFox)"""
    try:
        int(getattr(self, var_name))
    except ValueError:
        setattr(self, var_name, '0')

    value = int(getattr(self, var_name))
    max_val = (2**32) - 1

    if value < 0:
        setattr(self, var_name, '0')
    elif value > max_val:
        setattr(self, var_name, str(max_val))


class FlagPropertyGroup:
    """Credits: Sollumz"""

    def update_flags_total(self, context):
        flags = int_to_bool_list(int(self.flags), size=2)
        for index, flag_name in enumerate(MapFlags.__annotations__):
            self.flags_toggle[flag_name] = flags[index]

    def update_flag(self, context):
        flags = flag_prop_to_list(self.__class__, self)
        obj = context.active_object
        if obj:
            obj.ymap_properties.flags = flag_list_to_int(flags)


class ContentFlagPropertyGroup:
    """Credits: Sollumz"""

    def update_flags_total(self, context):
        flags = int_to_bool_list(int(self.content_flags), size=11)
        for index, flag_name in enumerate(ContentFlags.__annotations__):
            self.content_flags_toggle[flag_name] = flags[index]

    def update_flag(self, context):
        flags = flag_prop_to_list(self.__class__, self)
        obj = context.active_object
        if obj:
            obj.ymap_properties.content_flags = flag_list_to_int(flags)


class MapFlags(bpy.types.PropertyGroup):
    script_loaded: bpy.props.BoolProperty(
        name="Script Loaded", update=FlagPropertyGroup.update_flag)
    has_lod: bpy.props.BoolProperty(
        name="LOD", update=FlagPropertyGroup.update_flag)


class ContentFlags(bpy.types.PropertyGroup):
    has_hd: BoolProperty(
        name="HD", update=ContentFlagPropertyGroup.update_flag)
    has_lod: BoolProperty(
        name="LOD", update=ContentFlagPropertyGroup.update_flag)
    has_slod2: BoolProperty(
        name="SLOD2", update=ContentFlagPropertyGroup.update_flag)
    has_int: BoolProperty(
        name="Interior", update=ContentFlagPropertyGroup.update_flag)
    has_slod: BoolProperty(
        name="SLOD", update=ContentFlagPropertyGroup.update_flag)
    has_occl: BoolProperty(
        name="Occlusion", update=ContentFlagPropertyGroup.update_flag)
    has_physics: BoolProperty(
        name="Physics", update=ContentFlagPropertyGroup.update_flag)
    has_lod_lights: BoolProperty(
        name="Lod Lights", update=ContentFlagPropertyGroup.update_flag)
    has_dis_lod_lights: BoolProperty(
        name="Distant Lod Lights", update=ContentFlagPropertyGroup.update_flag)
    has_critical: BoolProperty(
        name="Critical", update=ContentFlagPropertyGroup.update_flag)
    has_grass: BoolProperty(
        name="Grass", update=ContentFlagPropertyGroup.update_flag)


class YmapBlockProperties(bpy.types.PropertyGroup):
    version: StringProperty(name="Version", default='0', update=lambda self,
                            context: update_uint_prop(self, context, 'version'))
    flags: StringProperty(name="Flags", default='0', update=lambda self,
                          context: update_uint_prop(self, context, 'flags'))
    # TODO: Sync the name input with the object name?
    name: StringProperty(name="Name")
    exported_by: StringProperty(name="Exported By", default="Sollumz")
    owner: StringProperty(name="Owner")
    time: StringProperty(name="Time")

class YmapPhysicsDictionariesList(bpy.types.PropertyGroup):
    name: StringProperty(name="name")

class YmapProperties(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="untitled_ymap")
    parent: StringProperty(name="Parent", default="")
    flags: IntProperty(name="Flags", default=0, min=0, max=3, update=FlagPropertyGroup.update_flags_total)
    content_flags: IntProperty(name="Content Flags", default=0, min=0, max=(2**11)-1, update=ContentFlagPropertyGroup.update_flags_total)

    streaming_extents_min: FloatVectorProperty()
    streaming_extents_max: FloatVectorProperty()
    entities_extents_min: FloatVectorProperty()
    entities_extents_max: FloatVectorProperty()

    flags_toggle: PointerProperty(type=MapFlags)
    content_flags_toggle: PointerProperty(type=ContentFlags)

    physicsDictionaries: CollectionProperty(type=YmapPhysicsDictionariesList)
    
    block: PointerProperty(type=YmapBlockProperties)


class YmapModelOccluderProperties(bpy.types.PropertyGroup):
    model_occl_flags: IntProperty(name="Flags", default=0)


class YmapGrassinstanceListProperties(bpy.types.PropertyGroup):
    
    IS_DOING_UPDATE = False
    
    def on_update_archetype_name(self, context):
        
        base_obj = ensure_grass_proc_model(context.active_object.ymap_grass_instance_list_properties.archetypeName)
        
        if not self.IS_DOING_UPDATE:
            self.IS_DOING_UPDATE = True
            for obj in context.selected_objects:
                for child in obj.children:
                    child.name = obj.ymap_grass_instance_list_properties.archetypeName
                    child.data = base_obj.data.copy()
            self.IS_DOING_UPDATE = False
    
    archetypeName: StringProperty(
        name="Archetype name",
        default="prop_grass_001_a",
        update=on_update_archetype_name
    )
    
    scaleRange: FloatVectorProperty(
        name="Scale Range",
        default=(1.0, 1.0, 1.0),
    )
    
    lodDist: FloatProperty(
        name="Grass LOD dist",
        default=120.0,
    )
    
    lodFadeStartDist: FloatProperty(
        name="Grass LOD fade start dist",
        default=15.0,
    )
    
    lodInstFadeRange: FloatProperty(
        name="Grass LOD inst fade range",
        default=0.75,
    )
    
    orientToTerrain: FloatProperty(
        name="Grass orient to terrain",
        default=1.0,
        min=0.0,
        max=1.0
    )
    
class YmapGrassinstanceListItemProperties(bpy.types.PropertyGroup):
    
    IS_DOING_UPDATE = False
    
    def on_update_color(self, context):
        if not self.IS_DOING_UPDATE:
            self.IS_DOING_UPDATE = True
            if context.active_object is not None:
                for obj in context.selected_objects:
                    _color = context.active_object.ymap_grass_instance_list_item_properties.color
                    if obj.ymap_grass_instance_list_item_properties.color != _color:
                        obj.ymap_grass_instance_list_item_properties.color = _color
            self.IS_DOING_UPDATE = False

    def on_update_scale(self, context):
        if not self.IS_DOING_UPDATE:
            self.IS_DOING_UPDATE = True
            if context.active_object is not None:
                for obj in context.selected_objects:
                    _scale = context.active_object.ymap_grass_instance_list_item_properties.scale
                    if obj.ymap_grass_instance_list_item_properties.scale != _scale:
                        obj.ymap_grass_instance_list_item_properties.scale = _scale
                    obj.scale = Vector([1,1,1]) * _scale
            self.IS_DOING_UPDATE = False

    color: FloatVectorProperty(
        name="Grass color",
        subtype='COLOR',
        default=(0.5, 0.5, 0.5),
        min=0.0,
        max=1.0,
        update=on_update_color
    )
  
    scale: FloatProperty(
        name="Grass scale",
        default=0.0,
        min=0.0,
        max=1.0,
        update=on_update_scale
    )
    
    ao: FloatProperty(
        name="Artificial occlusion",
        default=1.0,
        min=0.0,
        max=1.0
    )
    
    pad: IntVectorProperty(
        name="Pad",
        default=(0, 0, 0)
    )

class YmapCarGeneratorProperties(bpy.types.PropertyGroup):
    car_model: StringProperty(name="CarModel", default="panto")
    cargen_flags: IntProperty(name="Flags", default=0)
    pop_group: StringProperty(name="PopGroup", default="")
    perpendicular_length: FloatProperty(name="PerpendicularLength", default=2.3)
    body_color_remap_1: IntProperty(name="BodyColorRemap1", default=-1)
    body_color_remap_2: IntProperty(name="BodyColorRemap2", default=-1)
    body_color_remap_3: IntProperty(name="BodyColorRemap3", default=-1)
    body_color_remap_4: IntProperty(name="BodyColorRemap4", default=-1)
    livery: IntProperty(name="Livery", default=-1)


def register():
    bpy.types.Object.ymap_properties = PointerProperty(type=YmapProperties)
    bpy.types.Object.ymap_model_occl_properties = PointerProperty(type=YmapModelOccluderProperties)
    bpy.types.Object.ymap_grass_instance_list_properties = PointerProperty(type=YmapGrassinstanceListProperties)
    bpy.types.Object.ymap_grass_instance_list_item_properties = PointerProperty(type=YmapGrassinstanceListItemProperties)
    bpy.types.Object.ymap_cargen_properties = PointerProperty(type=YmapCarGeneratorProperties)


def unregister():
    del bpy.types.Object.ymap_properties
    del bpy.types.Object.ymap_model_occl_properties
    del bpy.types.Object.ymap_grass_instance_list_properties
    del bpy.types.Object.ymap_grass_instance_list_item_properties
    del bpy.types.Object.ymap_cargen_properties