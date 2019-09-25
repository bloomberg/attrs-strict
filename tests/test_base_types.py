import attr
import pytest

from attrs_strict import type_validator


@pytest.mark.parametrize(
    "value, expected, actual",
    [
        (3, str, int),
        ("five", int, str),
        (None, str, type(None)),
        (2.3, int, float),
    ],
)
def test_primitive_types(value, expected, actual):
    @attr.s
    class Something(object):
        number = attr.ib(validator=type_validator(), type=expected)

    with pytest.raises(ValueError) as error:
        Something(number=value)

    assert repr(
        error.value
    ) == "<number must be {} (got {} that is a {})>".format(
        expected, value, actual
    )


def test_reassign_evaluate():
    @attr.s
    class Something(object):
        number = attr.ib(validator=type_validator(), type=str)

    x = Something(number="foo")
    with pytest.raises(ValueError) as error:
        x.number = 5
        attr.validate(x)

    assert repr(
        error.value
    ) == "<number must be {} (got 5 that is a {})>".format(str, int)
