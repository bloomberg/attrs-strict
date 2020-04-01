from typing import Any, Dict, List, Set, Tuple

import pytest

from attrs_strict import type_validator

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


@pytest.mark.parametrize(
    "values, type_, error_message",
    [
        (
            [1, 2, "a"],
            List[int],
            (
                (
                    "numbers must be typing.List[int] "
                    "(got a that is a {}) in [1, 2, 'a']"
                ).format(str)
            ),
        ),
        (
            [[1, "a"]],
            List[List[int]],
            (
                (
                    "numbers must be "
                    "typing.List[typing.List[int]] (got a that is a {}) "
                    "in [1, 'a'] in [[1, 'a']]"
                ).format(str)
            ),
        ),
        (
            [[1, 2, 3], ["a"]],
            List[List[int]],
            (
                (
                    "numbers must be "
                    "typing.List[typing.List[int]] (got a that is a {}) "
                    "in ['a'] in [[1, 2, 3], ['a']]"
                ).format(str)
            ),
        ),
        (
            [(1, 2, "foo")],
            List[Tuple[int, int, int]],
            (
                "numbers must be "
                "typing.List[typing.Tuple[int, int, int]] (got foo "
                "that is a {}) in (1, 2, 'foo') in "
                "[(1, 2, 'foo')]"
            ).format(str),
        ),
    ],
)
def test_list_of_values_raise_value_error(values, type_, error_message):

    validator = type_validator()

    attrib = MagicMock()
    attrib.name = "numbers"
    attrib.type = type_

    with pytest.raises(ValueError) as error:
        validator(None, attrib, values)

    # THEN
    msg = "<{}>".format(error_message)
    assert msg == repr(error.value)


@pytest.mark.parametrize(
    "values, type_",
    [
        ([1, 2, 3], List[int]),
        ([[1], [2], [3]], List[List[int]]),
        ({1, 2, 3}, Set[int]),
        ([{1: [1, 2, 3], 2: [3, 4, 5]}], List[Dict[int, List[int]]]),
        ([1, 2, 3, 4], List[Any]),
        ([1, 2, {"foo": "bar"}], List[Any]),
    ],
)
def test_list_of_valid_values_no_raise(values, type_):
    validator = type_validator()

    attrib = MagicMock()
    attrib.name = "numbers"
    attrib.type = type_

    validator(None, attrib, values)
