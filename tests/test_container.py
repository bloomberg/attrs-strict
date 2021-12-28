from __future__ import annotations

import re
import typing
from unittest.mock import MagicMock

import attr
import pytest

from attrs_strict import type_validator


@pytest.mark.parametrize(
    ("items", "types", "message"),
    [
        (
            [1, 2, 3],
            typing.Set,
            "Smth must be {} (got [1, 2, 3] that is a {})".format(
                typing.Set, list
            ),
        ),
        (
            [1, 2, 3],
            typing.Dict,
            "Smth must be {} (got [1, 2, 3] that is a {})".format(
                typing.Dict, list
            ),
        ),
        (
            [1, 2, 3],
            typing.Tuple,
            "Smth must be {} (got [1, 2, 3] that is a {})".format(
                typing.Tuple, list
            ),
        ),
    ],
)
def test_container_is_not_of_expected_type_raises_type_error(
    items, types, message
):
    validator = type_validator()

    attr = MagicMock()
    attr.name = "Smth"
    attr.type = types

    with pytest.raises(ValueError, match=re.escape(message)):
        validator(None, attr, items)


def test_does_not_raise_when_container_is_empty_and_allowed():
    items = []

    validator = type_validator(True)
    attr = MagicMock()
    attr.type = typing.List[int]

    validator(None, attr, items)


def test_raises_when_container_is_empty_and_empty_ok_is_false():
    # GIVEN
    items = []
    validator = type_validator(empty_ok=False)
    attr = MagicMock()
    attr.name = "Smth"
    attr.type = str

    msg = f"Smth can not be empty and must be {str} (got [])"
    with pytest.raises(ValueError, match=re.escape(msg)):
        validator(None, attr, items)


def test_no_type_specified_is_fine():
    @attr.s
    class Something:
        numbers = attr.ib(validator=type_validator())

    Something([1, 2, 3, 4])


# -----------------------------------------------------------------------------
# Copyright 2019 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------- END-OF-FILE -----------------------------------
