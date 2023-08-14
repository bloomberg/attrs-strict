from __future__ import annotations

import re
import sys
from typing import List, Union
from unittest.mock import MagicMock

import pytest

from attrs_strict import type_validator


@pytest.mark.parametrize(
    ("element", "type_", "error_message"),
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
                "Value of foo p is not of type {} in [1, 2, 'p']".format(
                    "typing.Optional[int]"
                    if sys.version_info >= (3, 9)
                    else "typing.Union[NoneType, int]"
                )
            ),
        ),
        (
            10,
            str | None if sys.version_info >= (3, 10) else Union[str, None],
            "Value of foo 10 is not of type {}".format(
                "str | None"
                if sys.version_info >= (3, 10)
                else "typing.Optional[str]"
                if sys.version_info >= (3, 9)
                else "typing.Union[str, NoneType]"
            ),
        ),
    ],
)
def test_union_when_type_is_not_specified_raises(element, type_, error_message):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    with pytest.raises(ValueError, match=re.escape(error_message)):
        validator(None, attr, element)


@pytest.mark.parametrize(
    ("element", "type_"),
    [
        (2.0, Union[int, float]),
        ([1, 2, None, 4, 5], List[Union[None, int]]),
        (None, Union[int, None]),
        (10, int | None)
        if sys.version_info >= (3, 10)
        else (10, Union[int, None]),
    ],
)
def test_union_not_raise_for_correct_values(element, type_):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    validator(None, attr, element)
