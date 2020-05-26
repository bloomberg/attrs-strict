import typing
import attr
import inspect

class TypeValidationError(Exception):
    def __repr__(self) -> str: ...

class BadTypeError(TypeValidationError, ValueError):
    def __init__(self) -> None:
        self.containers: typing.List[typing.Iterable[typing.Any]]
    def add_container(self, container: typing.Any) -> None: ...
    def _render(self, error: str) -> str: ...

class AttributeTypeError(BadTypeError):
    def __init__(
        self, value: typing.Any, attribute: attr.Attribute[typing.Any]
    ) -> None: ...
    def __str__(self) -> str: ...

class CallableError(BadTypeError):
    def __init__(
        self,
        attribute: attr.Attribute[typing.Any],
        callable_signature: inspect.Signature,
        expected_signature: typing.Type[typing.Callable[..., typing.Any]],
        mismatch_callable_arg: inspect.Parameter,
        expected_callable_arg: inspect.Parameter,
    ) -> None: ...
    def __str__(self) -> str: ...

class EmptyError(BadTypeError):
    def __init__(
        self, container: typing.Any, attribute: attr.Attribute[typing.Any]
    ) -> None: ...
    def __str__(self) -> str: ...

class TupleError(BadTypeError):
    def __init__(
        self,
        container: typing.Any,
        attribute: typing.Optional[typing.Type[typing.Any]],
        tuple_types: typing.Tuple[typing.Type[typing.Any]],
    ) -> None: ...
    def __str__(self) -> str: ...
    def _more_or_less(self) -> str: ...

class UnionError(BadTypeError):
    def __init__(
        self,
        container: typing.Any,
        attribute: str,
        expected_type: typing.Type[typing.Any],
    ) -> None: ...
    def __str__(self) -> str: ...
