from typing import List, Union

import pytest

from attrs_strict import type_validator

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


@pytest.mark.parametrize(
    "element, type_, error_message",
    [
        (
            2.0,
            Union[int, str],
            "Value of foo 2.0 is not of type typing.Union[int, str]",
        ),
        (
            [1, 2, "p"],
            List[Union[None, int]],
            (
                "Value of foo p is not of type typing.Union[NoneType, int] "
                "in [1, 2, 'p']"
            ),
        ),
    ],
)
def test_union_when_type_is_not_specified_raises(element, type_, error_message):

    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    with pytest.raises(ValueError) as error:
        validator(None, attr, element)

    repr_msg = "<{}>".format(error_message)
    assert repr_msg == repr(error.value)


@pytest.mark.parametrize(
    "element, type_,",
    [
        (2.0, Union[int, float]),
        ([1, 2, None, 4, 5], List[Union[None, int]]),
        (None, Union[int, None]),
    ],
)
def test_union_not_raise_for_correct_values(element, type_):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    validator(None, attr, element)
