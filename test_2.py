from pygraphmodel import node


@node
class DummyNode:
	name: str


node_obj = DummyNode(name="dummy_node")

print(node_obj)

print(vars(node_obj))
