import pytest
from pygraphmodel import node


@node
class DummyNode:
	name: str


@pytest.fixture()
def node_obj():
	return DummyNode(name="dummy_node")
