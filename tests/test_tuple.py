from __future__ import annotations

import re
from typing import Tuple
from unittest.mock import MagicMock

import pytest

from attrs_strict import type_validator


def test_tuple_with_incorrect_number_of_arguments_raises():
    element = (1, 2, 3, 4)

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[int, int, int]

    validator = type_validator()

    msg = (
        "Element (1, 2, 3, 4) has more elements than types specified "
        "in typing.Tuple[int, int, int]. Expected 3 received 4"
    )
    with pytest.raises(ValueError, match=re.escape(msg)):
        validator(None, attr, element)


def test_tuple_of_tuple_raises():
    element = ((1, 2), (3, 4, 5))

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[Tuple[int, int], Tuple[int, int]]

    validator = type_validator()

    msg = (
        "Element (3, 4, 5) has more elements than types specified "
        "in typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]. "
        "Expected 2 received 3 in ((1, 2), (3, 4, 5))"
    )
    with pytest.raises(ValueError, match=re.escape(msg)):
        validator(None, attr, element)


def test_variable_length_tuple():
    element = (1, 2, 3, 4)

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[int, ...]

    validator = type_validator()

    validator(None, attr, element)


def test_variable_length_tuple_empty():
    element = ()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[int, ...]

    validator = type_validator()

    validator(None, attr, element)


def test_variable_length_tuple_raises():
    element = (1, 2, 3, "4")

    attr = MagicMock()
    attr.name = "foo"
    attr.type = Tuple[int, ...]

    validator = type_validator()

    msg = (
        "foo must be typing.Tuple[int, ...] (got 4 that is a {}) "
        "in (1, 2, 3, '4')"
    ).format(str)
    with pytest.raises(ValueError, match=re.escape(msg)):
        validator(None, attr, element)
