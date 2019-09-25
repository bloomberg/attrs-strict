import collections
import typing

from ._error import AttributeTypeError, BadTypeError, TupleError, UnionError


def type_validator(empty_ok=True):
    """
    Validates the attributes using the type argument specified. If the
    type argument is not present, the attribute is considered valid.

    :param empty_ok: Boolean flag that indicates if the field can be empty
                     in case of a collection or None for builtin types.

    """

    def _validator(instance, attribute, field):
        if not empty_ok and not field:
            raise ValueError("Expected a non-empty attribute")

        _validate_elements(attribute, field, attribute.type)

    return _validator


def _validate_elements(attribute, value, expected_type):
    base_type = (
        expected_type.__origin__
        if hasattr(expected_type, "__origin__")
        and expected_type.__origin__ is not None
        else expected_type
    )

    if base_type is None:
        return

    if base_type != typing.Union and not isinstance(value, base_type):
        raise AttributeTypeError(value, attribute)

    if base_type in {set, list, typing.List, typing.Set}:
        _handle_set_or_list(attribute, value, expected_type)
    elif base_type in {
        dict,
        collections.OrderedDict,
        collections.defaultdict,
        typing.Dict,
        typing.DefaultDict,
    }:
        _handle_dict(attribute, value, expected_type)
    elif base_type in {tuple, typing.Tuple}:
        _handle_tuple(attribute, value, expected_type)
    elif base_type == typing.Union:
        _handle_union(attribute, value, expected_type)


def _handle_set_or_list(attribute, container, expected_type):
    element_type, = expected_type.__args__

    for element in container:
        try:
            _validate_elements(attribute, element, element_type)
        except BadTypeError as error:
            error.add_container(container)
            raise error


def _handle_dict(attribute, container, expected_type):
    key_type, value_type = expected_type.__args__

    for key in container:
        try:
            _validate_elements(attribute, key, key_type)
            _validate_elements(attribute, container[key], value_type)
        except BadTypeError as error:
            error.add_container(container)
            raise error


def _handle_tuple(attribute, container, expected_type):
    tuple_types = expected_type.__args__

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
