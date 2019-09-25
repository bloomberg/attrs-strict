import collections
from typing import DefaultDict, List

import pytest

from attrs_strict import type_validator

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
