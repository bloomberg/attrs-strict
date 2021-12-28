from __future__ import annotations

import re
import sys
from enum import Enum
from typing import Any, List
from unittest.mock import MagicMock

import pytest

from attrs_strict import type_validator

if sys.version_info >= (3, 8):  # pragma: >=3.8 cover
    from typing import Literal
else:  # pragma: <3.8 cover
    from typing_extensions import Literal


class Numbers(Enum):
    one = 1
    two = 2


@pytest.mark.parametrize(
    ("element", "type_", "error_message"),
    [
        pytest.param(
            "c",
            Literal["a", "b"],
            "Value of foo c is not any of the literals specified ['a', 'b']",
            id="Value not present in literal",
        ),
        pytest.param(
            2.0,
            Literal[1, 2],
            "Value of foo 2.0 is not any of the literals specified [1, 2]",
            id="2.0 == 2 but their types are not same",
        ),
        pytest.param(
            0,
            Literal[True, False],
            "Value of foo 0 is not any of the literals specified [True, False]",
            id="0 == False evalutes to True but their types are not same",
        ),
    ],
)
def test_literal_when_type_is_not_specified_raises(
    element, type_, error_message
):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    with pytest.raises(ValueError, match=re.escape(error_message)):
        validator(None, attr, element)


@pytest.mark.parametrize(
    ("element", "type_"),
    [
        pytest.param("enum-a", Literal["enum-a", "enum-b"], id="Literal match"),
        pytest.param(
            "enum-a",
            Literal[("enum-a", "enum-b")],
            id="Literal accepts immutable tuple of enums to match",
        ),
        pytest.param(
            20, Literal[0x14], id="20 and 0x14 are equivalent in value and type"
        ),
        pytest.param(
            [1, 2, 3, 4, None],
            List[Literal[1, 2, 3, 4, None]],
            id="Literal part of another type",
        ),
        pytest.param(
            2,
            Literal[Literal[4], Literal[3, Literal[2]]],
            id="Combination of literals",
        ),
        pytest.param(
            Numbers.one, Literal[Numbers.one, Numbers.two], id="Enums"
        ),
    ],
)
def test_literal_not_raise_for_correct_values(element, type_):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    validator(None, attr, element)


@pytest.mark.parametrize(
    ("element", "type_", "error_message"),
    [
        pytest.param(
            "type",
            Literal[Any],
            "Type checking not supported for literals specified in"
            " [typing.Any]",
            id="Any inside Literal",
        ),
        pytest.param(
            3.14,
            Literal[3.14],
            "Type checking not supported for literals specified in [3.14]",
            id="Float inside Literal",
        ),
        pytest.param(
            ["enum-a", "enum-b"],
            Literal[["enum-a", "enum-b"]],
            "Type checking not supported for literals specified in "
            "[['enum-a', 'enum-b']]",
            id="Mutable list of enum inside Literal",
        ),
        pytest.param(
            "enum-a",
            Literal[List[str]],
            "Type checking not supported for literals specified in "
            "[typing.List[str]]",
            id="List type inside Literal",
        ),
    ],
)
def test_literal_raises_for_invalid_type_arguments_to_literal(
    element, type_, error_message
):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "foo"
    attr.type = type_

    with pytest.raises(ValueError, match=re.escape(error_message)):
        validator(None, attr, element)
