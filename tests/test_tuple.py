from typing import Tuple

import pytest

from attrs_strict import type_validator

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


def test_tuple_with_incorrect_number_of_arguments_raises():
    element = (1, 2, 3, 4)

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[int, int, int]

    validator = type_validator()

    with pytest.raises(ValueError) as error:
        validator(None, attr, element)

    assert (
        "<Element (1, 2, 3, 4) has more elements than types specified "
        "in typing.Tuple[int, int, int]. Expected 3 received 4>"
    ) == repr(error.value)


def test_tuple_of_tuple_raises():
    element = ((1, 2), (3, 4, 5))

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[Tuple[int, int], Tuple[int, int]]

    validator = type_validator()

    with pytest.raises(ValueError) as error:
        validator(None, attr, element)

    assert (
        "<Element (3, 4, 5) has more elements than types specified "
        "in typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]. "
        "Expected 2 received 3 in ((1, 2), (3, 4, 5))>"
    ) == repr(error.value)
