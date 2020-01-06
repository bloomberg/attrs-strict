import typing
import attr


class TypeValidationError(Exception):
    def __repr__(self) -> str:
        return "<{}>".format(str(self))


class BadTypeError(TypeValidationError, ValueError):
    def __init__(self) -> None:
        self.containers: typing.List[typing.Any] = []

    def add_container(self, container: typing.Any) -> None:
        self.containers.append(container)

    def _render(self, error: str) -> str:
        if self.containers:
            backtrack = " in ".join(
                [str(container) for container in self.containers]
            )
            return "{} in {}".format(error, backtrack)

        return error


class AttributeTypeError(BadTypeError):
    def __init__(
        self, container: typing.Any, attribute: attr.Attribute
    ) -> None:
        super(AttributeTypeError, self).__init__()
        self.container = container
        self.attribute = attribute

    def __str__(self) -> str:
        error = "{} must be {} (got {} that is a {})".format(
            self.attribute.name,
            self.attribute.type,
            self.container,
            type(self.container),
        )

        return self._render(error)


class EmptyError(BadTypeError):
    def __init__(self, container: typing.Any, attribute: attr.Attribute):
        super(EmptyError, self).__init__()
        self.container = container
        self.attribute = attribute

    def __str__(self) -> str:
        error = "{} can not be empty and must be {} (got {})".format(
            self.attribute.name, self.attribute.type, self.container
        )

        return self._render(error)


class TupleError(BadTypeError):
    def __init__(
        self,
        container: typing.Any,
        attribute: typing.Optional[typing.Type],
        tuple_types: typing.Tuple[typing.Type],
    ):
        super(TupleError, self).__init__()
        self.attribute = attribute
        self.container = container
        self.tuple_types = tuple_types

    def __str__(self) -> str:
        error = (
            "Element {} has {} elements than types "
            "specified in {}. Expected {} received {}"
        ).format(
            self.container,
            self._more_or_less(),
            self.attribute,
            len(self.tuple_types),
            len(self.container),
        )

        return self._render(error)

    def _more_or_less(self) -> str:
        return "more" if len(self.container) > len(self.tuple_types) else "less"


class UnionError(BadTypeError):
    def __init__(
        self,
        container: typing.Any,
        attribute: str,
        expected_type: typing.Optional[typing.Type],
    ) -> None:
        super(UnionError, self).__init__()
        self.attribute = attribute
        self.container = container
        self.expected_type = expected_type

    def __str__(self) -> str:
        error = "Value of {} {} is not of type {}".format(
            self.attribute, self.container, self.expected_type
        )

        return self._render(error)
