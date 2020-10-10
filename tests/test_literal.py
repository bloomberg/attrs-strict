import typing

import pytest

from attrs_strict import AttributeTypeError, BadTypeError, LiteralError, type_validator

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


@pytest.mark.parametrize("correct", ['a', 'b'])
def test_typing_literal_success(correct):
    literal_type = typing.Literal['a', 'b', 'c']

    validator = type_validator()
    attr = MagicMock()
    attr.type = literal_type

    validator(None, attr, correct)


@pytest.mark.parametrize("wrong", ['d', 'e'])
def test_typing_literal_failure(wrong):
    literals = ('a', 'b', 'c')
    literal_type = typing.Literal[literals]

    validator = type_validator()
    attr = MagicMock()
    attr.type = literal_type

    with pytest.raises(LiteralError) as error:
        validator(None, attr, wrong)

    assert "Value of {}, {} is not any of the literals specified {}".format(attr, wrong, literals) in str(
        error.value
    )


@pytest.mark.parametrize(
    "container, literals, correct",
    [
        (typing.List, ('a', 'b', 'c'), ['a']),
        (typing.Tuple, ('a', 'b', 'c'), ('b',)),
        (typing.Optional, ('a', 'b', 'c'), 'c'),
    ],
)
def test_typing_literal_within_container_success(
    container, literals, correct
):
    literal_type = typing.Literal[literals]

    validator = type_validator()
    attr = MagicMock()
    attr.type = container[literal_type]

    validator(None, attr, correct)


@pytest.mark.parametrize(
    "container, literals, wrong",
    [
        (typing.List, ('a', 'b', 'c'), ['d']),
        (typing.Tuple, ('a', 'b', 'c'), ('e',)),
        (typing.Optional, ('a', 'b', 'c'), 'd'),
    ],
)
def test_typing_literal_within_container_failure(
    container, literals, wrong
):
    literal_type = typing.Literal[literals]

    validator = type_validator()
    attr = MagicMock()
    attr.type = container[literal_type]

    with pytest.raises(BadTypeError) as error:
        validator(None, attr, wrong)

    assert "is not of type {}".format(str(attr.type)) in str(
        error.value
    ) or "is not any of the literals specified {}".format(str(literals)) in str(error.value)
