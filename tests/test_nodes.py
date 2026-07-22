from pygraphmodel import asdict


class TestNodes:
	def test_node_decorator(self, node_obj):
		assert asdict(node_obj) == {"name": "dummy_node"}
