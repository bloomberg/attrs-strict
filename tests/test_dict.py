import collections
from typing import Any, DefaultDict, Dict, List, Mapping, MutableMapping

import pytest

from attrs_strict import type_validator

try:
    from collections.abc import Mapping as CollectionsMapping
    from collections.abc import MutableMapping as CollectionsMutableMapping
except ImportError:
    from collections import Mapping as CollectionsMapping
    from collections import MutableMapping as CollectionsMutableMapping


try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


def test_defaultdict_raise_error():
    elem = collections.defaultdict(int)
    elem[5] = [1, 2, 3]

    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = DefaultDict[int, List[str]]

    with pytest.raises(ValueError) as error:
        validator(None, attr, elem)

    assert (
        "<foo must be typing.DefaultDict[int, typing.List[str]] "
        "(got 1 that is a {}) in [1, 2, 3] in "
        "defaultdict({}, {{5: [1, 2, 3]}})>"
    ).format(int, int) == repr(error.value)


def test_defaultdict_with_correct_type_no_raise():
    elem = collections.defaultdict(int)
    elem[5] = [1, 2, 3]
    elem[6] = [4, 5, 6]

    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = DefaultDict[int, List[int]]

    validator(None, attr, elem)


def test_dict_with_any_does_not_raise():
    elem = {"foo": 123, "b": "abc"}

    validator = type_validator()

    attr = MagicMock()
    attr.name = "zoo"
    attr.type = Dict[str, Any]

    validator(None, attr, elem)


@pytest.mark.parametrize(
    "data, type, validator_type, error_message",
    [
        (
            {"foo": 123},
            CollectionsMapping,
            Mapping,
            (
                "<zoo must be typing.Mapping[str, str] "
                "(got 123 that is a {})"
            ).format(int),
        ),
        (
            {1: "boo", 2: "zoo"},
            CollectionsMutableMapping,
            MutableMapping,
            (
                "<zoo must be typing.MutableMapping[str, str] "
                "(got 1 that is a {})"
            ).format(int),
        ),
    ],
)
def test_abc_mapping_types_throw_when_type_is_wrong(
    data, type, validator_type, error_message
):
    class TestMapping(type):
        def __init__(self, items):
            self._data = items

        def __getitem__(self, item):
            return self._data[item]

        def __len__(self):
            return len(self._data)

        def __iter__(self):
            return iter(self._data)

        def __delitem__(self, item):
            pass

        def __setitem__(self, item, value):
            pass

    validator = type_validator()

    attr = MagicMock()
    attr.name = "zoo"
    attr.type = validator_type[str, str]

    with pytest.raises(ValueError) as error:
        validator(None, attr, TestMapping(data))

    assert error_message in repr(error.value)
