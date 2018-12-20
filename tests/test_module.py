import attr_strict


def test_version():
    assert hasattr(attr_strict, "__version__")
    assert hasattr(attr_strict, "type_validator")
    assert hasattr(attr_strict, "AttributeTypeError")
    assert hasattr(attr_strict, "BadTypeError")
    assert hasattr(attr_strict, "UnionError")
    assert hasattr(attr_strict, "TupleError")
    assert hasattr(attr_strict, "TypeValidationError")


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
