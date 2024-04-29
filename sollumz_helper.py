import bpy
import bmesh
import traceback
import os
import time
from abc import abstractmethod
from .tools.blenderhelper import get_children_recursive, get_object_with_children
from .sollumz_properties import BOUND_TYPES
from .ydr.ydrexport import get_used_materials


class SOLLUMZ_OT_base:
    bl_options = {"UNDO"}
    bl_action = "do"
    bl_showtime = False
    bl_update_view = False

    def __init__(self):
        self.messages = []

    @abstractmethod
    def run(self, context):
        pass

    def execute(self, context):
        start = time.time()
        try:
            result = self.run(context)
            if self.bl_update_view:
                reset_sollumz_view(context.scene)
        except:
            result = False
            self.error(
                f"Error occured running operator : {self.bl_idname} \n {traceback.format_exc()}")
        end = time.time()

        if self.bl_showtime and result == True:
            self.message(
                f"{self.bl_label} took {round(end - start, 3)} seconds to {self.bl_action}.")

        if len(self.messages) > 0:
            self.message("\n".join(self.messages))

        if result:
            return {"FINISHED"}
        else:
            return {"CANCELLED"}

    def message(self, msg):
        self.report({"INFO"}, msg)

    def warning(self, msg):
        self.report({"WARNING"}, msg)

    def error(self, msg):
        self.report({"ERROR"}, msg)


def set_object_collection(obj):
    target = bpy.context.view_layer.active_layer_collection.collection
    objs = get_object_with_children(obj)
    for obj in objs:
        if len(obj.users_collection) > 0:
            collection = obj.users_collection[0]
            collection.objects.unlink(obj)
        target.objects.link(obj)


def reset_sollumz_view(scene):
    scene.hide_collision = not scene.hide_collision
    scene.hide_high_lods = not scene.hide_high_lods
    scene.hide_medium_lods = not scene.hide_medium_lods
    scene.hide_low_lods = not scene.hide_low_lods
    scene.hide_very_low_lods = not scene.hide_very_low_lods

    scene.hide_collision = not scene.hide_collision
    scene.hide_high_lods = not scene.hide_high_lods
    scene.hide_medium_lods = not scene.hide_medium_lods
    scene.hide_low_lods = not scene.hide_low_lods
    scene.hide_very_low_lods = not scene.hide_very_low_lods


def get_sollumz_objects_from_objects(objs, sollum_type):
    robjs = []
    for obj in objs:
        if obj.sollum_type in sollum_type:
            robjs.append(obj)
        for child in obj.children:
            if child.sollum_type in sollum_type:
                robjs.append(child)
    return robjs


def find_fragment_file(filepath):
    directory = os.path.dirname(filepath)
    for file in os.listdir(directory):
        if file.endswith(".yft.xml"):
            return os.path.join(directory, file)
    return None


def has_embedded_textures(obj):
    for mat in get_used_materials(obj):
        nodes = mat.node_tree.nodes
        for node in nodes:
            if isinstance(node, bpy.types.ShaderNodeTexImage):
                if node.texture_properties.embedded == True:
                    return True
    return False


def has_collision(obj):
    for child in get_children_recursive(obj):
        if child.sollum_type in BOUND_TYPES:
            return True
    return False


def duplicate_object_with_children(obj):
    objs = get_object_with_children(obj)
    new_objs = []
    for o in objs:
        new_obj = o.copy()
        new_obj.animation_data_clear()
        new_objs.append(new_obj)
    for i in range(len(objs)):
        if objs[i].parent:
            new_objs[i].parent = new_objs[objs.index(objs[i].parent)]
    for new_obj in new_objs:
        bpy.context.scene.collection.objects.link(new_obj)
    return new_objs[0]

def bmesh_join(list_of_bmeshes, normal_update=False):

  """
  https://blender.stackexchange.com/questions/50160/scripting-low-level-join-meshes-elements-hopefully-with-bmesh
  
  takes as input a list of bm references and outputs a single merged bmesh 
  alows an additional 'normal_update=True' to force _normal_ calculations.
  """

  bm = bmesh.new()
  add_vert = bm.verts.new
  add_face = bm.faces.new
  add_edge = bm.edges.new

  for bm_to_add in list_of_bmeshes:
    offset = len(bm.verts)

    for v in bm_to_add.verts:
      add_vert(v.co)

    bm.verts.index_update()
    bm.verts.ensure_lookup_table()

    if bm_to_add.faces:
      for face in bm_to_add.faces:
        add_face(tuple(bm.verts[i.index+offset] for i in face.verts))
        bm.faces.index_update()

    if bm_to_add.edges:
      for edge in bm_to_add.edges:
        edge_seq = tuple(bm.verts[i.index+offset] for i in edge.verts)
        try:
          add_edge(edge_seq)
        except ValueError:
          # edge exists!
          pass
      bm.edges.index_update()

  if normal_update:
    bm.normal_update()

  return bm

def mesh_join(list_of_objs:list, name = 'merged'):
    
    new_mesh = bpy.data.meshes.new(name + '_mesh')

    for obj in list_of_objs:
        for mat in obj.data.materials:
            found = False
            for mat2 in new_mesh.materials:
                if mat == mat2:
                    found = True
                    break
            if not found:
                new_mesh.materials.append(mat)

    new_obj = bpy.data.objects.new(name, new_mesh)

    selected = [new_obj] + list_of_objs

    with bpy.context.temp_override(active_object=new_obj, selected_editable_objects=selected):
        bpy.ops.object.join()

    return new_obj

def hide_set_obj_and_children(obj, toggle: bool):
    for x in obj.children:
        hide_set_obj_and_children(x, toggle)
    obj.hide_set(toggle)

def get_all_hierarchy(obj):
    data = []
    for x in obj.children:
        if len(x.children) != 0:
            data.extend(get_all_hierarchy(x))
        else:
            data.append(x)
    return data

def delete_obj_and_children(obj, do_unlink = True):
    data = get_all_hierarchy(obj)
    for x in data:
        bpy.data.objects.remove(x, do_unlink=do_unlink)
    bpy.data.objects.remove(obj, do_unlink=do_unlink)

def link_modifiers(active_object, selected_objects, clear_existing_modifiers=True):
    if len(selected_objects) <= 1:
        return

    for o in bpy.context.selected_objects:
        if o is active_object:
            continue

        if clear_existing_modifiers:
            o.modifiers.clear()

        for m in active_object.modifiers:
            o.modifiers.new(m.name, m.type)
