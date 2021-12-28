from __future__ import annotations

import inspect
import typing

import attr

from ._commons import format_type


class TypeValidationError(Exception):
    def __repr__(self) -> str:
        return f"<{str(self)}>"


class BadTypeError(TypeValidationError, ValueError):
    def __init__(self) -> None:
        self.containers: list[typing.Iterable[typing.Any]] = []

    def add_container(self, container: typing.Any) -> None:
        self.containers.append(container)

    def _render(self, error: str) -> str:
        if self.containers:
            backtrack = " in ".join(
                [str(container) for container in self.containers]
            )
            return f"{error} in {backtrack}"

        return error


class AttributeTypeError(BadTypeError):
    def __init__(
        self, value: typing.Any, attribute: attr.Attribute[typing.Any]
    ) -> None:
        super().__init__()
        self.value = value
        self.attribute = attribute

    def __str__(self) -> str:
        if self.attribute.type is None:
            error = (
                "attrs-strict error: AttributeTypeError was raised on an"
                " attribute ({}) with no defined type".format(
                    self.attribute.name
                )
            )
        else:
            error = "{} must be {} (got {} that is a {})".format(
                self.attribute.name,
                format_type(self.attribute.type),
                self.value,
                type(self.value),
            )

        return self._render(error)


class CallableError(BadTypeError):
    def __init__(
        self,
        attribute: attr.Attribute[typing.Any],
        callable_signature: inspect.Signature,
        expected_signature: type[typing.Callable[..., typing.Any]],
        mismatch_callable_arg: type[typing.Any],
        expected_callable_arg: type[typing.Any],
    ) -> None:
        super().__init__()
        self.attribute = attribute
        self.callable_signature = callable_signature
        self.expected_signature = expected_signature
        self.mismatch_callable_arg = mismatch_callable_arg
        self.expected_callable_arg = expected_callable_arg

    def __str__(self) -> str:
        error_msg = (
            "Error with: {} . Expected Callable signature: {} "
            "got: {}. {} should be {}".format(
                self.attribute.name,
                self.expected_signature,
                self.callable_signature,
                self.mismatch_callable_arg,
                self.expected_callable_arg,
            )
        )
        return self._render(error_msg)


class EmptyError(BadTypeError):
    def __init__(
        self, container: typing.Any, attribute: attr.Attribute[typing.Any]
    ) -> None:
        super().__init__()
        self.container = container
        self.attribute = attribute

    def __str__(self) -> str:
        if self.attribute.type is None:
            error = (
                "attrs-strict error: AttributeTypeError was raised on an"
                " attribute ({}) with no defined type".format(
                    self.attribute.name
                )
            )
        else:
            error = "{} can not be empty and must be {} (got {})".format(
                self.attribute.name,
                format_type(self.attribute.type),
                self.container,
            )

        return self._render(error)


class TupleError(BadTypeError):
    def __init__(
        self,
        container: typing.Any,
        attribute: type[typing.Any] | None,
        tuple_types: tuple[type[typing.Any]],
    ) -> None:
        super().__init__()
        self.attribute = attribute
        self.container = container
        self.tuple_types = tuple_types

    def __str__(self) -> str:
        error = (
            "Element {} has {} elements than types specified in {}. "
            "Expected {} received {}".format(
                self.container,
                self._more_or_less(),
                self.attribute,
                len(self.tuple_types),
                len(self.container),
            )
        )

        return self._render(error)

    def _more_or_less(self) -> str:
        return "more" if len(self.container) > len(self.tuple_types) else "less"


class UnionError(BadTypeError):
    def __init__(
        self,
        container: typing.Any,
        attribute: str,
        expected_type: type[typing.Any],
    ) -> None:
        super().__init__()
        self.attribute = attribute
        self.container = container
        self.expected_type = expected_type

    def __str__(self) -> str:
        msg = "Value of {} {} is not of type {}"
        error = msg.format(self.attribute, self.container, self.expected_type)

        return self._render(error)


class LiteralError(BadTypeError):
    def __init__(
        self, attribute: str, value: typing.Any, literals: list[str]
    ) -> None:
        super().__init__()
        self.attribute = attribute
        self.value = value
        self.literals = literals

    def __str__(self) -> str:
        msg = "Value of {} {} is not any of the literals specified {}"
        error = msg.format(self.attribute, self.value, self.literals)
        return self._render(error)


class UnsupportedLiteralError(BadTypeError):
    def __init__(self, unsupported_literals: list[typing.Any]) -> None:
        super().__init__()
        self.unsupported_literals = unsupported_literals

    def __str__(self) -> str:
        msg = "Type checking not supported for literals specified in {}"
        error = msg.format(self.unsupported_literals)
        return self._render(error)
