from __future__ import print_function

import fbx, fbxsip

class Node(object):
    # TODO: Make 'scene' optional with 'manager'
    # Right now only 'scene' can be provided.
    def __init__(self, scene, name='', children=None):
        self._me = fbx.FbxNode.Create(scene._me, name)
        self.scene = scene
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def attach_to_root(self):
        # Must be better way to do this than calling native API
        self.scene._me.GetRootNode().AddChild(self._me)

    def add_child(self, node):
        assert isinstance(node, Node)
        self.children.append(node)

    def add_attribute(self, attr):
        self.attribute = attr
        self.attribute._me = attr._me
        # FIXME: This might be wrong (SetNodeAttribute)
        return self._me.AddNodeAttribute(attr._me)

    def set_local_translation(self, coordinate):
        x, y, z = coordinate
        self._me.LclTranslation.Set(fbx.FbxDouble3(x, z, y))

    def set_rotation_pivot(self, vertex):
        self._me.SetRotationActive(True)
        self._me.SetRotationPivot(fbx.FbxNode.eSourcePivot, vertex._me)

    def set_post_rotation(self, vertex):
        self._me.SetPostRotation(fbx.FbxNode.eSourcePivot, vertex._me)

class Exporter(object):
    def __init__(self, scene):
        self.scene = scene
        self.manager = self.scene.manager
        self._me = fbx.FbxExporter.Create(self.manager._me, '')
        # TODO: Make this belongs to `._me` attribute, not at this class's level
        self.ios = fbx.FbxIOSettings.Create(self.manager._me, fbx.IOSROOT)

    def set_ios(self, material=True, texture=True, embedded=True, shape=True,
                gobo=True, animation=True, global_settings=True):
        if not self.manager._me.GetIOSettings():
            self.manager._me.SetIOSettings(self.ios)

            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_MATERIAL, True)
            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_TEXTURE, True)
            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_EMBEDDED, True)
            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_SHAPE, True)
            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_GOBO, True)
            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_ANIMATION, True)
            self.manager._me.GetIOSettings().SetBoolProp(fbx.EXP_FBX_GLOBAL_SETTINGS, True)

    def export(self, path='default.fbx', binary=False):
        if binary:
            mode = 0
        else:
            mode = 1
        exportstat = self._me.Initialize(path, mode, self.manager._me.GetIOSettings())

        if not exportstat:
            try:
                raise IOError("Problem exporting file!")
            except IOError as e:
                print(e.message)

        exportstat = self._me.Export(self.scene._me)
        self.__destroy()
        
        return exportstat

    def __destroy(self):
        self._me.Destroy()

class Manager(object):
    nodes = []

    def __init__(self):
        self._me = fbx.FbxManager.Create()

    def create_scene(self, name=""):
        self.scene = Scene(self, name)

    def create_node(self, name=""):
        node = Node(self, name)
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def destroy(self):
        self._me.Destroy()

class Scene(object):
    def __init__(self, manager, name=""):
        self._me = fbx.FbxScene.Create(manager._me, name)
        self.manager = manager
        self.name = name
        self.root_node = Node(self, name + "_root_node")
        self.root_node._me = self._me.GetRootNode()
        self.exporter = Exporter(self)

    def create_node(self, name=""):
        node = Node(self, name)

class Mesh(object):
    def __init__(self, parent, name=""):
        self.parent = parent
        self.name = name
        self._me = fbx.FbxMesh.Create(parent._me, name)

    def add_to(self, node):
        node.add_attribute(self)

    def init_controlpoints(self, num_point):
        self._me.InitControlPoints(num_point)

    def set_controlpoints_at(self, vertex, index):
        self._me.SetControlPointAt(vertex._me, index)

    def begin_polygon(self):
        self._me.BeginPolygon()

    def add_polygon(self, index):
        self._me.AddPolygon(index)

    def end_polygon(self):
        self._me.EndPolygon()

class Vertex(object):
    def __init__(self, x, y, z, i=0):
        self._me = fbx.FbxVector4(x, y, z, i)
        self.coordinates = tuple(self._me)

    def get(self):
        return self.coordinates

    def set(self, x, y, z, i=0):
        self.coordinates = (x, y, z, i)
        return self.coordinates
        
class Pyramid(Mesh):
    def __init__(self, parent):
        super(Pyramid, self).__init__(parent)

    def create(self, base_width, height):
        self.base_width = base_width
        self.height = height

        # Calculate the vertices of the pyramid lying down
        base_width_half = base_width / 2
        controlpoints = [
            Vertex(0, height, 0),
            Vertex(base_width_half, 0, -base_width_half),
            Vertex(-base_width_half, 0, -base_width_half),
            Vertex(-base_width_half, 0, base_width_half)
        ]

        # Initialize and set the control points of the mesh
        controlpoint_count = len(controlpoints)
        self.init_controlpoints(controlpoint_count)
        for i, v in enumerate(controlpoints):
            self.set_controlpoints_at(v, i)

        # Set the controlpoint indices of the bottom plane of the pyramid
        self.begin_polygon()
        self.add_polygon(1)
        self.add_polygon(4)
        self.add_polygon(3)
        self.add_polygon(2)
        self.end_polygon()

        # Set the controlpoint indices of the front plane
        self.begin_polygon()
        self.add_polygon(0)
        self.add_polygon(1)
        self.add_polygon(2)
        self.end_polygon()

        # Set the controlpoint indices of the left plane
        self.begin_polygon()
        self.add_polygon(0)
        self.add_polygon(2)
        self.add_polygon(3)
        self.end_polygon()

        # Set the controlpoint indices of the back plane
        self.begin_polygon()
        self.add_polygon(0)
        self.add_polygon(3)
        self.add_polygon(4)
        self.end_polygon()

        # Set the controlpoint indices of the right plane
        self.begin_polygon()
        self.add_polygon(0)
        self.add_polygon(4)
        self.add_polygon(1)
        self.end_polygon()
        
    


