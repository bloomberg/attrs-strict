from typing import Optional

import attr
import pytest

from attrs_strict import type_validator


@pytest.mark.parametrize(
    "type_, good_value, bad_value",
    [(str, "str", 0xBAD), (int, 7, "bad"), (Optional[str], None, 0xBAD)],
)
def test_real_types(type_, good_value, bad_value):
    @attr.s(auto_attribs=True)
    class Something:
        value: type_ = attr.ib(validator=type_validator())

    with pytest.raises(ValueError):
        Something(bad_value)

    x = Something(good_value)
    with pytest.raises(ValueError):
        x.value = bad_value
        attr.validate(x)


@attr.s(auto_attribs=True)
class Child:
    parent: "Parent" = attr.ib(validator=type_validator())


@attr.s(auto_attribs=True)
class Parent:
    pass


def test_forward_ref():
    Child(Parent())

    with pytest.raises(ValueError):
        Child(15)


@attr.s(auto_attribs=True)
class Self:
    parent: Optional["Self"] = attr.ib(None, validator=type_validator())


def test_recursive():
    Self(Self())
    Self(Self(None))

    with pytest.raises(ValueError):
        Self(Self(17))
