import textwrap

from setuptools import setup

with open("README.md") as fp:
    readme = fp.read()

long_description = "".join(
    [
        section.split("<!-- end -->")[0]
        for section in readme.split("<!-- begin -->")
        if "<!-- end -->" in section
    ]
)

setup(
    name="attrs-strict",
    description="Runtime validators for attrs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Erik-Cristian Seulean",
    author_email="eseulean@bloomberg.net",
    license="Apache 2.0",
    packages=["attrs_strict"],
    install_requires=["attrs", "typing; python_version<'3.5'"],
    tests_require=["mock", "pytest"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
    url="https://github.com/bloomberg/attrs-strict",
    project_urls={
        "Source": "https://github.com/bloomberg/attrs-strict",
        "Tracker": "https://github.com/bloomberg/attrs-strict/issues",
        "Documentation": "https://github.com/bloomberg/attrs-strict/blob/"
        "master/README.md#attrs-runtime-validation",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    use_scm_version={
        "write_to": "attrs_strict/_version.py",
        "write_to_template": textwrap.dedent(
            """
        __version__ = {version!r}
    # --------------------------------------------------------------------------
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
    # ----------------------------- END-OF-FILE --------------------------------
    """
        ).lstrip(),
    },
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
