import typing

import pytest

from attrs_strict import AttributeTypeError, BadTypeError, type_validator

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


@pytest.mark.parametrize("test_type, correct", [(str, "foo"), (int, 42)])
def test_typing_newtype_single_validation_success(test_type, correct):
    SomeNew = typing.NewType("SomeNew", test_type)

    validator = type_validator()
    attr = MagicMock()
    attr.type = SomeNew

    validator(None, attr, correct)
    validator(None, attr, SomeNew(correct))


@pytest.mark.parametrize(
    "test_type, wrongs", [(str, [42, True]), (int, ["foo", ()])]
)
def test_typing_newtype_single_validation_failure(test_type, wrongs):
    SomeNew = typing.NewType("SomeNew", test_type)

    validator = type_validator()
    attr = MagicMock()
    attr.type = SomeNew

    for wrong in wrongs:
        with pytest.raises(AttributeTypeError) as error:
            validator(None, attr, wrong)

    assert "must be NewType(SomeNew, {})".format(str(test_type)) in str(
        error.value
    )


@pytest.mark.parametrize(
    "container, test_type, correct",
    [
        (typing.List, str, ["foo", "bar"]),
        (typing.Tuple, int, (0,)),
        (typing.Optional, str, None),
    ],
)
def test_typing_newtype_within_container_validation_success(
    container, test_type, correct
):
    SomeNew = typing.NewType("SomeNew", test_type)

    validator = type_validator()
    attr = MagicMock()
    attr.type = container[SomeNew]

    validator(None, attr, correct)


@pytest.mark.parametrize(
    "container, test_type, wrongs",
    [
        (typing.List, str, [42, True, "foo", ("foo", "bar")]),
        (typing.Tuple, int, ["foo", 42, [0, 1, "2"]]),
        (typing.Optional, str, [42, (1, 2)]),
    ],
)
def test_typing_newtype_within_container_validation_failure(
    container, test_type, wrongs
):
    SomeNew = typing.NewType("SomeNew", test_type)

    validator = type_validator()
    attr = MagicMock()
    attr.type = container[SomeNew]

    for wrong in wrongs:
        with pytest.raises(BadTypeError) as error:
            validator(None, attr, wrong)

    assert "must be {}".format(str(attr.type)) in str(
        error.value
    ) or "is not of type {}".format(str(attr.type)) in str(error.value)


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
