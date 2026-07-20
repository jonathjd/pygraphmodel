"""
Defines the node decorator along with associated helpers.

Interface examples:

@node
class Gene:
    name: str
    ensembl_id: str = node_property(index = True, primary_key = True)
    length: int

gene = Gene(name="Hexokinase", enesembl_id="ENSG00000159399", )

assert node_asdict(gene) == {"name": "Hexokinase, "ensembl_id": "ENSG00000159399}
assert node.index ==
"""


class FrozenInstanceError(AttributeError):
    pass


def node_property(*, index: bool, primary_key: bool):
    pass
