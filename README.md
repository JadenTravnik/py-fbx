pyfbx
======

A simple-to-use wrapper for Autodesk Python FBX SDK.

FBX
---
> FBX(Filmbox) is a proprietary file format (.fbx) developed by 
> Kaydara and owned by [Autodesk](https://en.wikipedia.org/wiki/Autodesk) 
> since 2006. It is used to provide interoperability between digital
> content creation applications. 
>
> from [Wikipedia](https://en.wikipedia.org/wiki/FBX)

Why another wrapper?
--------------------
I have had a chance to work on a project which needed Python to generate
FBX file for Maya. Autodesk did a rather poor job at its Python FBX SDK such as:

+ Lack of documentation
+ C-style APIs instead of Pythonic
+ Tedious wrapper classes i.e. `FbxDouble3` to wrap around C++ array.

How it works
------------
Classes in *pyfbx* does not inherit the original classes from the SDK. Each instance
of the class have a private property `_me` which interact with the original class's 
instance while pyfbx "floats" above i.e.

```python

from pyfbx import *

manager = Manager()
scene = Scene(manager)
assert isinstance(scene, pyfbx.Scene)       # True
assert isinstance(scene._me, fbx.FbxScene)  # True

```

Install
-------

```bash

git clone https://github.com/jochasinga/pyfbx
cd pyfbx && python setup.py install

```

Examples
--------

```python

from pyfbx import * 

manager = Manager()
scene = Scene(manager)
node = Node(manager)
mesh = Mesh(manager)

# Set mesh attributes 

node.add_attribute(mesh)
scene.root_node.add_child(node)

```

However, since `Manager` and `Scene` is a singleton in charge of all the  nodes, it makes 
sense for them to be atomic.

```python

manager = Manager()
manager.create_scene()    # equivalent to `Scene(manager)`
manager.create_node()     # equivalent to `Node(manager)`
scene = manager.scene
scene.create_node()       # equivalent to `Node(scene)

```

Node Tree
---------

FBX depends on node hierachy, with the scene's root node acting as the descendent of all. While
you can always use the underlying API to traverse through nodes in the scene, `Node` also keeps
track of its children using simple list.

```python

from pyfbx import *

manager = Manager()
p_node = Node(manager, "parent_node")
node.add_child(Node(manager, "child_node_1"))
node.add_child(Node(manager, "child_node_2"))

assert p_node.children[0].name == "child_node_1"

c_node_1 = node.children[0]
c_node_1.add_child(Node(manager, "grandchild_node"))

assert p_node.children[0].children[0].name == "grandchild_node"

```







