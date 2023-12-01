import bpy
from ...sollumz_properties import FlagPropertyGroup


class RoomFlags(FlagPropertyGroup, bpy.types.PropertyGroup):
    size = 10

    flag1: bpy.props.BoolProperty(
        name="1 - Freeze vehicles",
        description="Old name: Unknown 1",
        update=FlagPropertyGroup.update_flag)
    flag2: bpy.props.BoolProperty(
        name="2 - Freeze peds",
        description="Old name: Disables wanted level",
        update=FlagPropertyGroup.update_flag)
    flag3: bpy.props.BoolProperty(
        name="4 - No directional light",
        description="Old name: Disable exterior shadows",
        update=FlagPropertyGroup.update_flag)
    flag4: bpy.props.BoolProperty(
        name="8 - No exterior lights",
        description="Old name: Unknown 4",
        update=FlagPropertyGroup.update_flag)
    flag5: bpy.props.BoolProperty(
        name="16 - Force freeze",
        description="Old name: Unknown 5",
        update=FlagPropertyGroup.update_flag)
    flag6: bpy.props.BoolProperty(
        name="32 - Reduce cars",
        description="Old name: Reduces vehicle population",
        update=FlagPropertyGroup.update_flag)
    flag7: bpy.props.BoolProperty(
        name="64 - Reduce peds",
        description="Old name: Reduces ped population",
        update=FlagPropertyGroup.update_flag)
    flag8: bpy.props.BoolProperty(
        name="128 - Force directional light ON",
        description="Old name: Unknown 8",
        update=FlagPropertyGroup.update_flag)
    flag9: bpy.props.BoolProperty(
        name="256 - Don't render exterior",
        description="Old name: Disable limbo portals",
        update=FlagPropertyGroup.update_flag)
    flag10: bpy.props.BoolProperty(
        name="512 - Mirror potentially visible",
        description="Old name: Unknown 10",
        update=FlagPropertyGroup.update_flag)


class PortalFlags(FlagPropertyGroup, bpy.types.PropertyGroup):
    size = 14

    flag1: bpy.props.BoolProperty(
        name="1 - One way",
        description="Disable interior rendering when standing outside.\nOld name: Disables exterior rendering",
        update=FlagPropertyGroup.update_flag)
    flag2: bpy.props.BoolProperty(
        name="2 - Link",
        description="Can be used to as invert compare to previous flag.\nOld name: Disables interior rendering",
        update=FlagPropertyGroup.update_flag)
    flag3: bpy.props.BoolProperty(
        name="4 - Mirror",
        description="",
        update=FlagPropertyGroup.update_flag)
    flag4: bpy.props.BoolProperty(
        name="8 - Ignore modifier",
        description="Old name: Extra bloom",
        update=FlagPropertyGroup.update_flag)
    flag5: bpy.props.BoolProperty(
        name="16 - Mirror using expensive shaders",
        description="",
        update=FlagPropertyGroup.update_flag)
    flag6: bpy.props.BoolProperty(
        name="32 - Low LOD only",
        description="Old name: Use exterior LOD",
        update=FlagPropertyGroup.update_flag)
    flag7: bpy.props.BoolProperty(
        name="64 - Allow closing",
        description="Portal will be disabled if an attached entity is closed.\nOld name: Hide when door closed",
        update=FlagPropertyGroup.update_flag)
    flag8: bpy.props.BoolProperty(
        name="128 - Mirror can see directional light",
        description="Old name: Unknown 8",
        update=FlagPropertyGroup.update_flag)
    flag9: bpy.props.BoolProperty(
        name="256 - Mirror using portal traversal",
        description="Old name: Mirror exterior portals",
        update=FlagPropertyGroup.update_flag)
    flag10: bpy.props.BoolProperty(
        name="512 - Mirror floor",
        description="Old name: Unknown 10",
        update=FlagPropertyGroup.update_flag)
    flag11: bpy.props.BoolProperty(
        name="1024 - Mirror can see exterior view",
        description="Old name: Mirror limbo entities",
        update=FlagPropertyGroup.update_flag)
    flag12: bpy.props.BoolProperty(
        name="2048 - Water surface",
        description="Old name: Unknown 12",
        update=FlagPropertyGroup.update_flag)
    flag13: bpy.props.BoolProperty(
        name="4096 - Water surface extend to horizon",
        description="Old name: Unknown 13",
        update=FlagPropertyGroup.update_flag)
    flag14: bpy.props.BoolProperty(
        name="8192 - Use light bleed",
        description="Old name: Disable farclipping",
        update=FlagPropertyGroup.update_flag)


class EntityFlags(FlagPropertyGroup, bpy.types.PropertyGroup):
    flag1: bpy.props.BoolProperty(
        name="Allow full rotation", update=FlagPropertyGroup.update_flag)
    flag2: bpy.props.BoolProperty(
        name="Unknown 2", update=FlagPropertyGroup.update_flag)
    flag3: bpy.props.BoolProperty(
        name="Disable embedded collisions", update=FlagPropertyGroup.update_flag)
    flag4: bpy.props.BoolProperty(
        name="Unknown 4", update=FlagPropertyGroup.update_flag)
    flag5: bpy.props.BoolProperty(
        name="Unknown 5", update=FlagPropertyGroup.update_flag)
    flag6: bpy.props.BoolProperty(
        name="Static entity", update=FlagPropertyGroup.update_flag)
    flag7: bpy.props.BoolProperty(
        name="Object isn't dark at night", update=FlagPropertyGroup.update_flag)
    flag8: bpy.props.BoolProperty(
        name="Unknown 8", update=FlagPropertyGroup.update_flag)
    flag9: bpy.props.BoolProperty(
        name="Unknown 9", update=FlagPropertyGroup.update_flag)
    flag10: bpy.props.BoolProperty(
        name="Disable embedded light sources", update=FlagPropertyGroup.update_flag)
    flag11: bpy.props.BoolProperty(
        name="Unknown 11", update=FlagPropertyGroup.update_flag)
    flag12: bpy.props.BoolProperty(
        name="Unknown 12", update=FlagPropertyGroup.update_flag)
    flag13: bpy.props.BoolProperty(
        name="Unknown 13", update=FlagPropertyGroup.update_flag)
    flag14: bpy.props.BoolProperty(
        name="Unknown 14", update=FlagPropertyGroup.update_flag)
    flag15: bpy.props.BoolProperty(
        name="Unknown 15", update=FlagPropertyGroup.update_flag)
    flag16: bpy.props.BoolProperty(
        name="Unknown 16", update=FlagPropertyGroup.update_flag)
    flag17: bpy.props.BoolProperty(
        name="Unknown 17", update=FlagPropertyGroup.update_flag)
    flag18: bpy.props.BoolProperty(
        name="Unknown 18", update=FlagPropertyGroup.update_flag)
    flag19: bpy.props.BoolProperty(name="Disable archetype extensions",
                                   update=FlagPropertyGroup.update_flag)
    flag20: bpy.props.BoolProperty(
        name="Unknown 20", update=FlagPropertyGroup.update_flag)
    flag21: bpy.props.BoolProperty(
        name="Unknown 21", update=FlagPropertyGroup.update_flag)
    flag22: bpy.props.BoolProperty(
        name="Unknown 22", update=FlagPropertyGroup.update_flag)
    flag23: bpy.props.BoolProperty(
        name="Disable shadow for entity", update=FlagPropertyGroup.update_flag)
    flag24: bpy.props.BoolProperty(
        name="Disable entity, shadow casted", update=FlagPropertyGroup.update_flag)
    flag25: bpy.props.BoolProperty(
        name="Object will not cast reflections", update=FlagPropertyGroup.update_flag)
    flag26: bpy.props.BoolProperty(
        name="Interior proxy", update=FlagPropertyGroup.update_flag)
    flag27: bpy.props.BoolProperty(
        name="Unknown 27", update=FlagPropertyGroup.update_flag)
    flag28: bpy.props.BoolProperty(
        name="Reflection proxy", update=FlagPropertyGroup.update_flag)
    flag29: bpy.props.BoolProperty(
        name="Unknown 29", update=FlagPropertyGroup.update_flag)
    flag30: bpy.props.BoolProperty(
        name="Mirror proxy", update=FlagPropertyGroup.update_flag)
    flag31: bpy.props.BoolProperty(
        name="Unknown 31", update=FlagPropertyGroup.update_flag)
    flag32: bpy.props.BoolProperty(
        name="Unknown 32", update=FlagPropertyGroup.update_flag)


class ArchetypeFlags(FlagPropertyGroup, bpy.types.PropertyGroup):
    flag1: bpy.props.BoolProperty(
        name="1 - Wet Road Reflection",
        description="Old name: Unknown 1",
        update=FlagPropertyGroup.update_flag)
    flag2: bpy.props.BoolProperty(
        name="2 - Dont Fade",
        description="Old name: Unknown 2",
        update=FlagPropertyGroup.update_flag)
    flag3: bpy.props.BoolProperty(
        name="4 - Draw Last",
        description="Old name: Unknown 3",
        update=FlagPropertyGroup.update_flag)
    flag4: bpy.props.BoolProperty(
        name="8 - Climbable By AI",
        description="Old name: Unknown 4",
        update=FlagPropertyGroup.update_flag)
    flag5: bpy.props.BoolProperty(
        name="16 - Suppress HD TXDs",
        description="Old name: Unknown 5",
        update=FlagPropertyGroup.update_flag)
    flag6: bpy.props.BoolProperty(
        name="32 - Static",
        description="Old name: Static",
        update=FlagPropertyGroup.update_flag)
    flag7: bpy.props.BoolProperty(
        name="64 - Disable alpha sorting",
        description="Old name: Unknown 7",
        update=FlagPropertyGroup.update_flag)
    flag8: bpy.props.BoolProperty(
        name="128 - Tough For Bullets",
        description="Old name: Instance",
        update=FlagPropertyGroup.update_flag)
    flag9: bpy.props.BoolProperty(
        name="256 - Is Generic",
        description="Old name: Unknown 9",
        update=FlagPropertyGroup.update_flag)
    flag10: bpy.props.BoolProperty(
        name="512 - Has Anim (YCD)",
        description="Old name: Bone anims (YCD)",
        update=FlagPropertyGroup.update_flag)
    flag11: bpy.props.BoolProperty(
        name="1024 - UV anims (YCD)",
        description="Old name: UV anims (YCD)",
        update=FlagPropertyGroup.update_flag)
    flag12: bpy.props.BoolProperty(
        name="2048 - Shadow Only",
        description="Old name: Invisible but blocks lights/shadows",
        update=FlagPropertyGroup.update_flag)
    flag13: bpy.props.BoolProperty(
        name="4096 - Damage Model",
        description="Old name: Unknown 13",
        update=FlagPropertyGroup.update_flag)
    flag14: bpy.props.BoolProperty(
        name="8192 - Dont Cast Shadows",
        description="Old name: Object won't cast shadow",
        update=FlagPropertyGroup.update_flag)
    flag15: bpy.props.BoolProperty(
        name="16384 - Cast Texture Shadows",
        description="Old name: Unknown 15",
        update=FlagPropertyGroup.update_flag)
    flag16: bpy.props.BoolProperty(
        name="32768 - Dont Collide With Flyer",
        description="Old name: Unknown 16",
        update=FlagPropertyGroup.update_flag)
    flag17: bpy.props.BoolProperty(
        name="65536 - Double-sided rendering",
        description="Old name: Double-sided rendering",
        update=FlagPropertyGroup.update_flag)
    flag18: bpy.props.BoolProperty(
        name="131072 - Dynamic",
        description="Old name: Dynamic",
        update=FlagPropertyGroup.update_flag)
    flag19: bpy.props.BoolProperty(
        name="262144 - Override Physics Bounds",
        description="Old name: Unknown 19",
        update=FlagPropertyGroup.update_flag)
    flag20: bpy.props.BoolProperty(
        name="524288 - Auto Start Anim",
        description="Old name: Unknown 20",
        update=FlagPropertyGroup.update_flag)
    flag21: bpy.props.BoolProperty(
        name="1048576 - Has Pre Reflected Water Proxy",
        description="Old name: Unknown 21",
        update=FlagPropertyGroup.update_flag)
    flag22: bpy.props.BoolProperty(
        name="2097152 - Has Drawable Proxy For Water Reflections",
        description="Old name: Unknown 22",
        update=FlagPropertyGroup.update_flag)
    flag23: bpy.props.BoolProperty(
        name="4194304 - Does Not Provide AI Cover",
        description="Old name: Unknown 23",
        update=FlagPropertyGroup.update_flag)
    flag24: bpy.props.BoolProperty(
        name="8388608 - Does Not Provide Player Cover",
        description="Old name: Unknown 24",
        update=FlagPropertyGroup.update_flag)
    flag25: bpy.props.BoolProperty(
        name="16777216 - Is Ladder Deprecated",
        description="Old name: Unknown 25",
        update=FlagPropertyGroup.update_flag)
    flag26: bpy.props.BoolProperty(
        name="33554432 - Has Cloth",
        description="Old name: Unknown 26",
        update=FlagPropertyGroup.update_flag)
    flag27: bpy.props.BoolProperty(
        name="67108864 - Enable Door Physics",
        description="Old name: Enables special attribute",
        update=FlagPropertyGroup.update_flag)
    flag28: bpy.props.BoolProperty(
        name="134217728 - Is Fixed For Navigation",
        description="Old name: Unknown 28",
        update=FlagPropertyGroup.update_flag)
    flag29: bpy.props.BoolProperty(
        name="268435456 -  Dont Avoid By Peds",
        description="Old name: Disable red vertex channel",
        update=FlagPropertyGroup.update_flag)
    flag30: bpy.props.BoolProperty(
        name="536870912 - Use Ambient Scale",
        description="Old name: Disable green vertex channel",
        update=FlagPropertyGroup.update_flag)
    flag31: bpy.props.BoolProperty(
        name="1073741824 - Is Debug",
        description="Old name: Disable blue vertex channel",
        update=FlagPropertyGroup.update_flag)
    flag32: bpy.props.BoolProperty(
        name="2147483648 - Has Alpha Shadow",
        description="Old name: Disable alpha vertex channel",
        update=FlagPropertyGroup.update_flag)


class MloInstanceFlags(FlagPropertyGroup, bpy.types.PropertyGroup):
    flag1: bpy.props.BoolProperty(
        name="1 - Gps on",
        description="No description yet",
        update=FlagPropertyGroup.update_flag)
    flag2: bpy.props.BoolProperty(
        name="2 - Cap contents alpha",
        description="No description yet",
        update=FlagPropertyGroup.update_flag)
    flag3: bpy.props.BoolProperty(
        name="4 - Short fade",
        description="No description yet",
        update=FlagPropertyGroup.update_flag)
    flag4: bpy.props.BoolProperty(
        name="8 - Special behaviour 1",
        description="No description yet",
        update=FlagPropertyGroup.update_flag)
    flag5: bpy.props.BoolProperty(
        name="16 - Special behaviour 2",
        description="No description yet",
        update=FlagPropertyGroup.update_flag)
    flag6: bpy.props.BoolProperty(
        name="32 - Special behaviour 3",
        description="No description yet",
        update=FlagPropertyGroup.update_flag)
