import pytest
import fbx
import pyfbx

def test_node():
    manager = pyfbx.Manager()
    node = pyfbx.Node(manager, "my_node")

    assert isinstance(node._me, fbx.FbxNode)
    assert len(node.children) == 0

    node.add_child( pyfbx.Node(manager, "child_node"))
    assert len(node.children) == 1
    assert node.children[0].name == "child_node"

    node.children[0].add_child(pyfbx.Node(manager, "grandchild_susan"))
    node.children[0].add_child(pyfbx.Node(manager, "grandchild_eleanor"))
    
    assert len(node.children[0].children) == 2
    assert node.children[0].children[0].name == "grandchild_susan"
    assert node.children[0].children[1].name == "grandchild_eleanor"

    node.add_attribute(pyfbx.Mesh(manager, ''))
    assert isinstance(node.attribute, pyfbx.Mesh)
    assert isinstance(node.attribute._me, fbx.FbxMesh)

def test_manager():

    manager = pyfbx.Manager()
    manager.create_scene()
    manager.create_node()

    assert isinstance(manager._me, fbx.FbxManager)
    assert isinstance(manager.scene._me, fbx.FbxScene)
    assert isinstance(manager.nodes[0]._me, fbx.FbxNode)

def test_scene():

    manager = pyfbx.Manager()
    scene = pyfbx.Scene(manager, name="ma_scene")
    
    assert isinstance(scene._me, fbx.FbxScene)
    assert scene.name == "ma_scene"
    assert isinstance(scene.manager, pyfbx.Manager)
    assert isinstance(scene.root_node, pyfbx.Node)
    assert isinstance(scene.root_node._me, fbx.FbxNode)

