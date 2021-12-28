import re
import sys
from typing import Optional

import attr
import pytest

from attrs_strict import type_validator


@pytest.mark.parametrize(
    ("type_", "good_value", "bad_value", "error_msg"),
    [
        (
            str,
            "str",
            0xBAD,
            f"value must be {str} (got 2989 that is a {int})",
        ),
        (
            int,
            7,
            "bad",
            f"value must be {int} (got bad that is a {str})",
        ),
        (
            Optional[str],
            None,
            0xBAD,
            "Value of value 2989 is not of type {}".format(
                "typing.Optional[str]"
                if sys.version_info == (2, 7) or sys.version_info > (3, 9)
                else "typing.Union[str, NoneType]"
            ),
        ),
    ],
)
def test_real_types(type_, good_value, bad_value, error_msg):
    @attr.s(auto_attribs=True)
    class Something:
        value: type_ = attr.ib(validator=type_validator())

    with pytest.raises(ValueError, match=re.escape(error_msg)):
        Something(bad_value)

    x = Something(good_value)
    x.value = bad_value
    with pytest.raises(ValueError, match=re.escape(error_msg)):
        attr.validate(x)


@attr.s(auto_attribs=True)
class Child:
    parent: "Parent" = attr.ib(validator=type_validator())


@attr.s(auto_attribs=True)
class Parent:
    pass


def test_forward_ref():
    Child(Parent())
    msg = f"parent must be {Parent} (got 15 that is a {int})"
    with pytest.raises(ValueError, match=re.escape(msg)):
        Child(15)


@attr.s(auto_attribs=True)
class Self:
    parent: Optional["Self"] = attr.ib(None, validator=type_validator())


def test_recursive():
    Self(Self())
    Self(Self(None))
    type_repr = (
        "typing.Optional[test_auto_attribs__py3.Self]"
        if sys.version_info == (2, 7) or sys.version_info > (3, 9)
        else "typing.Union[test_auto_attribs__py3.Self, NoneType]"
    )
    msg = f"Value of parent 17 is not of type {type_repr}"
    with pytest.raises(ValueError, match=re.escape(msg)):
        Self(Self(17))
