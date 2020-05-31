import collections
import typing

from ._commons import is_newtype
from ._error import (
    AttributeTypeError,
    BadTypeError,
    CallableError,
    EmptyError,
    TupleError,
    UnionError,
)

try:
    from collections.abc import Mapping, MutableMapping, Callable
except ImportError:
    from collections import Mapping, MutableMapping, Callable

try:
    from inspect import signature
except ImportError:
    # silencing type error so mypy doesn't complain about duplicate import
    from funcsigs import signature  # type: ignore

try:
    from itertools import zip_longest
except ImportError:
    # silencing type error so mypy doesn't complain about duplicate import
    from itertools import izip_longest as zip_longest  # type: ignore


class SimilarTypes:
    Dict = {
        dict,
        collections.OrderedDict,
        collections.defaultdict,
        Mapping,
        MutableMapping,
        typing.Dict,
        typing.DefaultDict,
        typing.Mapping,
        typing.MutableMapping,
    }
    List = {set, list, typing.List, typing.Set}
    Tuple = {tuple, typing.Tuple}
    Callable = {typing.Callable, Callable}


def type_validator(empty_ok=True):
    """
    Validates the attributes using the type argument specified. If the
    type argument is not present, the attribute is considered valid.

    :param empty_ok: Boolean flag that indicates if the field can be empty
                     in case of a collection or None for builtin types.

    """

    def _validator(instance, attribute, field):
        if not empty_ok and not field:
            raise EmptyError(field, attribute)

        _validate_elements(attribute, field, attribute.type)

    return _validator


def _validate_elements(attribute, value, expected_type):
    if expected_type is None:
        return

    base_type = _get_base_type(expected_type)

    if base_type == typing.Any:
        return

    if base_type != typing.Union and not isinstance(  # type: ignore
        value, base_type
    ):
        raise AttributeTypeError(value, attribute)

    if base_type == typing.Union:  # type: ignore
        _handle_union(attribute, value, expected_type)
    elif base_type in SimilarTypes.List:
        _handle_set_or_list(attribute, value, expected_type)
    elif base_type in SimilarTypes.Dict:
        _handle_dict(attribute, value, expected_type)
    elif base_type in SimilarTypes.Tuple:
        _handle_tuple(attribute, value, expected_type)
    elif base_type in SimilarTypes.Callable:  # type: ignore
        _handle_callable(attribute, value, expected_type)


def _get_base_type(type_):
    if hasattr(type_, "__origin__") and type_.__origin__ is not None:
        base_type = type_.__origin__  # type: typing.Type[typing.Any]
    elif is_newtype(type_):
        base_type = type_.__supertype__
    else:
        base_type = type_

    return base_type


def _type_matching(actual, expected):
    actual = actual.__supertype__ if is_newtype(actual) else actual
    expected = expected.__supertype__ if is_newtype(expected) else expected

    if expected == actual or expected == typing.Any:
        return True

    base_type = _get_base_type(expected)

    if base_type == typing.Union:  # type: ignore
        return any(
            _type_matching(actual, expected_candidate)
            for expected_candidate in expected.__args__
        )

    elif base_type in (
        SimilarTypes.Dict
        | SimilarTypes.List
        | SimilarTypes.Tuple
        | SimilarTypes.Callable
    ):
        return all(
            _type_matching(actual, expected)
            for actual, expected in zip_longest(
                actual.__args__, expected.__args__
            )
        )

    return False


def _handle_callable(attribute, callable_, expected_type):
    _signature = signature(callable_)
    callable_args = [
        param.annotation for param in _signature.parameters.values()
    ]
    callable_args.append(_signature.return_annotation)
    if not expected_type.__args__:  # type: ignore
        return  # No annotations specified on type, matches all Callables

    for callable_arg, expected_arg in zip_longest(
        callable_args, expected_type.__args__  # type: ignore
    ):
        if not _type_matching(callable_arg, expected_arg):
            raise CallableError(
                attribute, _signature, expected_type, callable_arg, expected_arg
            )


def _handle_set_or_list(attribute, container, expected_type):
    (element_type,) = expected_type.__args__  # type: ignore

    for element in container:
        try:
            _validate_elements(attribute, element, element_type)
        except BadTypeError as error:
            error.add_container(container)
            raise error


def _handle_dict(attribute, container, expected_type):
    key_type, value_type = expected_type.__args__  # type: ignore

    for key in container:
        try:
            _validate_elements(attribute, key, key_type)
            _validate_elements(attribute, container[key], value_type)
        except BadTypeError as error:
            error.add_container(container)
            raise error


def _handle_tuple(attribute, container, expected_type):
    tuple_types = expected_type.__args__  # type: ignore
    if len(tuple_types) == 2 and tuple_types[1] == Ellipsis:
        element_type = tuple_types[0]
        tuple_types = (element_type,) * len(container)

    if len(container) != len(tuple_types):
        raise TupleError(container, attribute.type, tuple_types)

    for element, expected_type in zip(container, tuple_types):
        try:
            _validate_elements(attribute, element, expected_type)
        except BadTypeError as error:
            error.add_container(container)
            raise error


def _handle_union(attribute, value, expected_type):
    union_has_none_type = any(
        elem is None.__class__ for elem in expected_type.__args__
    )

    if value is None and union_has_none_type:
        return

    for arg in expected_type.__args__:
        try:
            _validate_elements(attribute, value, arg)
            return
        except ValueError:
            pass
    raise UnionError(value, attribute.name, expected_type)


# -----------------------------------------------------------------------------
# Copyright 2019 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------- END-OF-FILE -----------------------------------
