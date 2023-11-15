import bpy

from bpy.props import (FloatProperty, PointerProperty, StringProperty, IntProperty, FloatVectorProperty)


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


def update_flag(self, context):
    obj = context.active_object
    if obj:
        obj.ymap_properties.script_loaded = self.script_loaded


class MapFlags(bpy.types.PropertyGroup):
    script_loaded: bpy.props.BoolProperty(
        name="Script Loaded", update=update_flag)


def update_ymap_name(self, context):
    if hasattr(self, "id_data") and self.id_data:
        self.id_data.name = self.name


class YmapBlockProperties(bpy.types.PropertyGroup):
    version: StringProperty(
        name="Version", default='0', update=lambda self, context: update_uint_prop(self, context, 'version'))
    flags: StringProperty(
        name="Flags", default='0', update=lambda self, context: update_uint_prop(self, context, 'flags'))
    name: StringProperty(
        name="Name")
    exported_by: StringProperty(
        name="Exported By", default="Sollumz")
    owner: StringProperty(
        name="Owner")
    time: StringProperty(
        name="Time")


class YmapProperties(bpy.types.PropertyGroup):
    parent: StringProperty(
        name="Parent", default="")
    flags: IntProperty(
        name="Flags", default=0, min=0, max=3, update=update_flag)

    streaming_extents_min: FloatVectorProperty()
    streaming_extents_max: FloatVectorProperty()
    entities_extents_min: FloatVectorProperty()
    entities_extents_max: FloatVectorProperty()

    flags_toggle: PointerProperty(type=MapFlags)
    script_loaded: bpy.props.BoolProperty()

    block: PointerProperty(
        type=YmapBlockProperties)


class YmapModelOccluderProperties(bpy.types.PropertyGroup):
    model_occl_flags: IntProperty(
        name="Flags", default=0)


class YmapCarGeneratorProperties(bpy.types.PropertyGroup):
    car_model: StringProperty(
        name="CarModel", default="panto")
    cargen_flags: IntProperty(
        name="Flags", default=0)
    pop_group: StringProperty(
        name="PopGroup", default="")
    perpendicular_length: FloatProperty(

        name="PerpendicularLength", default=2.3)
    body_color_remap_1: IntProperty(
        name="BodyColorRemap1", default=-1)
    body_color_remap_2: IntProperty(
        name="BodyColorRemap2", default=-1)
    body_color_remap_3: IntProperty(
        name="BodyColorRemap3", default=-1)
    body_color_remap_4: IntProperty(
        name="BodyColorRemap4", default=-1)
    livery: IntProperty(
        name="Livery", default=-1)


def register():
    bpy.types.Object.ymap_properties = PointerProperty(type=YmapProperties)
    bpy.types.Object.ymap_model_occl_properties = PointerProperty(type=YmapModelOccluderProperties)
    bpy.types.Object.ymap_cargen_properties = PointerProperty(type=YmapCarGeneratorProperties)


def unregister():
    del bpy.types.Object.ymap_properties
    del bpy.types.Object.ymap_model_occl_properties
    del bpy.types.Object.ymap_cargen_properties
