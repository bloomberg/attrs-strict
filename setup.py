from setuptools import setup

try:
    from attrs_strict._version import __version__
except ImportError:
    _version_globals = {}
    with open("attrs_strict/_version.py") as fp:
        exec(fp.read(), _version_globals)
    __version__ = _version_globals["__version__"]

setup(
    name="attrs-strict",
    version=__version__,
    description="Runtime validators for attrs",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    author="Erik-Cristian Seulean",
    author_email="eseulean@bloomberg.net",
    license="Apache 2.0",
    packages=["attrs_strict"],
    install_requires=["attrs"],
    tests_require=["mock", "pytest"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
)

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
