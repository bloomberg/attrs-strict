from __future__ import annotations

import typing

import attr
import pytest

from attrs_strict import AttributeTypeError, CallableError, type_validator


class _TestResources:
    NewInt = typing.NewType("NewType", int)

    def plain_unannotated_callable(a, b):  # noqa: U100,N805
        ...

    def int_int_returns_str(a, b):  # noqa: U100,N805
        ...

    int_int_returns_str.__annotations__ = {"a": int, "b": int, "return": str}

    def no_args_returns_str():
        ...

    no_args_returns_str.__annotations__ = {"return": str}

    def int_int_returns_none(a, b):  # noqa: U100,N805
        ...

    int_int_returns_none.__annotations__ = {"a": int, "b": int, "return": None}

    def int_default_int_returns_str(a, b=1):  # noqa: U100,N805
        ...

    int_default_int_returns_str.__annotations__ = {
        "a": int,
        "b": int,
        "return": str,
    }

    def int_default_kwonly_int_returns_str(a, *, b=1):  # noqa: U100,N805
        ...

    int_default_kwonly_int_returns_str.__annotations__ = {
        "a": int,
        "b": int,
        "return": str,
    }

    def int_kwonly_int_returns_str(a, *, b):  # noqa: U100,N805
        ...

    int_kwonly_int_returns_str.__annotations__ = {
        "a": int,
        "b": int,
        "return": str,
    }

    def newint_int_returns_str(a, b):  # noqa: U100,N805
        ...

    newint_int_returns_str.__annotations__ = {
        "a": NewInt,
        "b": int,
        "return": str,
    }

    def int_int_returns_int(a, b):  # noqa: U100,N805
        ...

    int_int_returns_int.__annotations__ = {"a": int, "b": int, "return": int}

    def dict_str_int_returns_int(a):  # noqa: U100,N805
        ...

    dict_str_int_returns_int.__annotations__ = {
        "a": typing.Dict[str, int],
        "return": int,
    }

    def int_returns_int(a):  # noqa: U100,N805
        ...

    int_returns_int.__annotations__ = {"a": int, "return": int}

    def dict_int_str_returns_int(a):  # noqa: U100,N805
        ...

    dict_int_str_returns_int.__annotations__ = {
        "a": typing.Dict[int, str],
        "return": int,
    }

    def dict_str_str_returns_int(a):  # noqa: U100,N805
        ...

    dict_str_str_returns_int.__annotations__ = {
        "a": typing.Dict[str, str],
        "return": int,
    }

    def int_default_returns_int(a=123):  # noqa: U100,N805
        ...

    int_default_returns_int.__annotations__ = {"a": int, "return": int}


@pytest.mark.parametrize(
    ("name", "callable_", "attribute_type"),
    [
        (
            "no-types-defined-matches-typed-callable",
            _TestResources.int_int_returns_str,
            typing.Callable,
        ),
        (
            "no-types-defined-matches-untyped-callable",
            _TestResources.plain_unannotated_callable,
            typing.Callable,
        ),
        (
            "list_of_untyped_callables",
            [_TestResources.plain_unannotated_callable] * 3,
            typing.List[typing.Callable],
        ),
        (
            "typed_callable_expected_has_newtype",
            _TestResources.int_int_returns_str,
            typing.Callable[[_TestResources.NewInt, int], str],
        ),
        (
            "typed_callable_value_has_newtype",
            _TestResources.newint_int_returns_str,
            typing.Callable[[int, int], str],
        ),
        (
            "typed_callable_",
            _TestResources.int_int_returns_str,
            typing.Callable[[int, int], str],
        ),
        (
            "typed_callable_no_args",
            _TestResources.no_args_returns_str,
            typing.Callable[[], str],
        ),
        (
            "typed_callable_none",
            _TestResources.int_int_returns_none,
            typing.Callable[[int, int], None],
        ),
        (
            "typed_callable_default_missing",
            _TestResources.int_default_int_returns_str,
            typing.Callable[[int], str],
        ),
        (
            "typed_callable_default_present",
            _TestResources.int_default_int_returns_str,
            typing.Callable[[int, int], str],
        ),
        (
            "typed_callable_kwonly_default_missing",
            _TestResources.int_default_kwonly_int_returns_str,
            typing.Callable[[int], str],
        ),
        (
            "list_of_typed_callables",
            [_TestResources.int_int_returns_str] * 3,
            typing.List[typing.Callable[[int, int], str]],
        ),
        (
            "union_type_arg2_provided",
            _TestResources.int_int_returns_str,
            typing.Callable[[int, int], typing.Union[int, str]],
        ),
        (
            "union_type_arg1_provided",
            _TestResources.int_int_returns_int,
            typing.Callable[[int, int], typing.Union[int, str]],
        ),
        (
            "dict_type",
            _TestResources.dict_str_int_returns_int,
            typing.Callable[[typing.Dict[str, int]], int],
        ),
        (
            "union_of_int_dict_arg1_provided",
            _TestResources.int_returns_int,
            typing.Callable[[typing.Union[int, typing.Dict[int, str]]], int],
        ),
        (
            "union_of_int_dict_arg2_provided",
            _TestResources.dict_int_str_returns_int,
            typing.Callable[[typing.Union[int, typing.Dict[int, str]]], int],
        ),
        (
            "nested_unions_arg1_provided",
            _TestResources.int_returns_int,
            typing.Callable[
                [typing.Union[int, typing.Dict[typing.Union[str, int], str]]],
                int,
            ],
        ),
        (
            "nested_unions_arg2_provided",
            _TestResources.dict_str_str_returns_int,
            typing.Callable[
                [typing.Union[int, typing.Dict[typing.Union[str, int], str]]],
                int,
            ],
        ),
        (
            "any_type_int_provided",
            _TestResources.int_int_returns_int,
            typing.Callable[[int, int], typing.Any],
        ),
        (
            "any_type_str_provided",
            _TestResources.int_int_returns_str,
            typing.Callable[[int, int], typing.Any],
        ),
        (
            "any_type_none_provided",
            _TestResources.int_int_returns_none,
            typing.Callable[[int, int], typing.Any],
        ),
        (
            "callable_with_default_arg",
            _TestResources.int_default_returns_int,
            typing.Callable[[int], int],
        ),
    ],
)
def test_callable_not_raises_with_valid_annotations(
    name,  # noqa: U100
    callable_,
    attribute_type,
):
    @attr.s
    class Something:
        call_me = attr.ib(validator=type_validator(), type=attribute_type)

    Something(call_me=callable_)


@pytest.mark.parametrize(
    ("name", "callable_", "attribute_type", "raised_error_type"),
    [
        (
            "not_a_callable",
            "clearly-not-a-callable",
            typing.Callable,
            AttributeTypeError,
        ),
        (
            "callable_with_not_enough_types",
            _TestResources.int_int_returns_int,
            typing.Callable[[int, int, int], str],
            CallableError,
        ),
        (
            "callable_with_too_many_types",
            _TestResources.int_int_returns_int,
            typing.Callable[[int], str],
            CallableError,
        ),
        (
            "callable_with_incorrect_types",
            _TestResources.int_int_returns_int,
            typing.Callable[[int, int], str],
            CallableError,
        ),
        (
            "callable_with_incorrect_default_types",
            _TestResources.int_default_int_returns_str,
            typing.Callable[[int, str], str],
            CallableError,
        ),
        (
            "callable_with_provided_default_kwonly_types",
            _TestResources.int_default_kwonly_int_returns_str,
            typing.Callable[[int, int], str],
            CallableError,
        ),
        (
            "callable_with_missing_kwonly_types",
            _TestResources.int_kwonly_int_returns_str,
            typing.Callable[[int], str],
            CallableError,
        ),
        (
            "callable_with_provided_kwonly_types",
            _TestResources.int_kwonly_int_returns_str,
            typing.Callable[[int, int], str],
            CallableError,
        ),
        (
            "list_of_callables_different_types",
            [
                _TestResources.int_int_returns_int,
                _TestResources.int_int_returns_str,
            ],
            typing.List[typing.Callable[[int, int], str]],
            CallableError,
        ),
    ],
)
def test_callable_raises_with_invalid_types(
    name,  # noqa: U100
    callable_,
    attribute_type,
    raised_error_type,
):
    @attr.s
    class Something:
        call_me = attr.ib(validator=type_validator(), type=attribute_type)

    with pytest.raises(raised_error_type):
        Something(call_me=callable_)
