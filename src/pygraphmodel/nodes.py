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

from typing import get_type_hints, Any, Callable


class FrozenInstanceError(AttributeError):
	pass


def node_property(*, index: bool, primary_key: bool):
	pass


class Field:
	def __init__(self, name: str, constructor: Callable) -> None:
		if not callable(constructor) or constructor is type(None):
			raise TypeError(f"{name!r} type hint must be callable")
		self.name = name
		self.constructor = constructor

	def __set__(self, instance: Any, value: Any) -> None:
		if value is ...:
			value = self.constructor()
		else:
			try:
				value = self.constructor(value)
			except (TypeError, ValueError) as e:
				type_name = self.constructor.__name__
				msg = f"{value!r} is not compatible with {self.name}: {type_name}"
				raise TypeError(msg) from e
		instance.__dict__[self.name] = value


def _fields(cls: type) -> dict[str, type]:
	return get_type_hints(cls)


def __init__(self: Any, **kwargs: Any) -> None:
	for name in self._fields():
		value = kwargs.pop(name, ...)
		setattr(self, name, value)
	if kwargs:
		self.__flag_unknown_attrs(*kwargs)


def __setattr__(self: Any, name: str, value: Any) -> None:
	if name in self._fields():
		cls = self.__class__
		descriptor = getattr(cls, name)
		descriptor.__set__(self, value)
	else:
		self.__flag_unknown_attrs(name)


def __flag_unknown_attrs(self: Any, *names: str) -> None:
	plural = "s" if len(names) > 1 else ""
	extra = ", ".join(f"{name!r}" for name in names)
	cls_name = repr(self.__class__.__name__)
	raise AttributeError(f"{cls_name} has no attribute{plural} {extra}")


def asdict(self: Any) -> dict[str, Any]:
	return {
		name: getattr(self, name)
		for name, attr in self.__class__.__dict__.items()
		if isinstance(attr, Field)
	}


def __repr__(self: Any) -> str:
	kwargs = ", ".join(f"{key}={value!r}" for key, value in asdict(self).items())
	return f"{self.__class__.__name__}({kwargs})"


def node(cls: type | None = None) -> type:
	def wrap(cls):
		for name, constructor in _fields(cls).items():
			setattr(cls, name, Field(name, constructor))
		cls._fields = classmethod(_fields)  # type: ignore
		instance_methods = (
			__init__,
			__repr__,
			__setattr__,
			__flag_unknown_attrs,
		)
		for method in instance_methods:
			setattr(cls, method.__name__, method)
		return cls

	# called without parens
	if cls is None:
		return wrap

	# called with parens
	return wrap(cls)
