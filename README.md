<!-- begin -->

[![Latest version on
PyPi](https://badge.fury.io/py/attrs-strict.svg)](https://badge.fury.io/py/attrs-strict)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/attrs-strict.svg)](https://pypi.org/project/attrs-strict/)
[![Build Status](https://github.com/bloomberg/attrs-strict/workflows/check/badge.svg)](https://github.com/bloomberg/attrs-strict/actions)
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# attrs runtime validation

`attrs-strict` is a Python package which contains runtime validation for [`attrs`](https://github.com/python-attrs/attrs) data classes based on the types existing in the typing module.

<!-- end -->

## Menu

- [Rationale](#rationale)
- [Quick start](#quick-start)
- [Building](#building)
- [Installation](#installation)
- [Contributions](#contributions)
- [License](#license)
- [Code of Conduct](#code-of-conduct)
- [Security Vulnerability Reporting](#security-vulnerability-reporting)

<!-- begin -->

## Rationale

The purpose of the library is to provide runtime validation for attributes specified in
[`attrs`](https://www.attrs.org/en/stable/) data classes. The types supported are all the builtin
types and most of the ones defined in the typing library. For Python 2, the typing module is
available through the backport found [`here`](https://pypi.org/project/typing/).

## Quick Start

Type enforcement is based on the `type` attribute set on any field specified in an `attrs` dataclass. If the type argument is not specified, no validation takes place.

`pip install attrs-strict`

```python
from typing import List
import attr
from attrs_strict import type_validator


@attr.s
class SomeClass(object):
    list_of_numbers = attr.ib(validator=type_validator(), type=List[int])


sc = SomeClass([1, 2, 3, 4])
print(sc)
SomeClass(list_of_numbers=[1, 2, 3, 4])

try:
    SomeClass([1, 2, 3, "four"])
except ValueError as exception:
    print(repr(exception))
```

```console
SomeClass(list_of_numbers=[1, 2, 3, 4])
<list_of_numbers must be typing.List[int] (got four that is a <class 'str'>) in [1, 2, 3, 'four']>
```

Nested type exceptions are validated accordingly, and a backtrace to the initial container is maintained to ease with debugging. This means that if an exception occurs because a nested element doesn't have the correct type, the representation of the exception will contain the path to the specific element that caused the exception.

```python
from typing import List, Tuple
import attr
from attrs_strict import type_validator


@attr.s
class SomeClass(object):
    names = attr.ib(validator=type_validator(), type=List[Tuple[str, str]])


try:
    SomeClass(names=[("Moo", "Moo"), ("Zoo", 123)])
except ValueError as exception:
    print(exception)
```

```console
names must be typing.List[typing.Tuple[str, str]] (got 123 that is a <class 'int'>) in ('Zoo', 123) in [('Moo', 'Moo'), ('Zoo', 123)]
```

### What is currently supported ?

Currently, there's support for simple types and types specified in the `typing` module: `List`, `Dict`, `DefaultDict`, `Set`, `Union`, `Tuple`, `NewType`, `Callable` and any combination of them. This means that you can specify nested types like `List[List[Dict[int, str]]]` and the validation would check if attribute has the specific type.

`Callable` will validate if the callable function's annotation matches the type definition. If type does not specify any annotations then all callables will pass the validation against it. Support for `Callable` is not available for `python2`.

```python
def fully_annotated_function(self, a: int, b: int) -> str:
    ...


def un_annonated_function(a, b):
    ...


@attr.s
class Something(object):
    a = attr.ib(
        validator=type_validator(), type=typing.Callable
    )  # Will work for any callable
    b = attr.ib(validator=type_validator(), type=typing.Callable[[int, int], str])


Something(a=un_annonated_function, b=fully_annotated_function)
```

`TypeVars` or `Generics` are not supported yet but there are plans to support this in the future.

## Building

For development, the project uses [`tox`](http://tox.readthedocs.org/) in order to install dependencies, run tests and generate documentation. In order to be able to do this, you need tox `pip install tox` and after that invoke `tox` in the root of the project.

## Installation

Run `pip install attrs-strict` to install the latest stable version from [PyPi](https://pypi.org/project/attrs-strict/). Documentation is hosted on [readthedocs](https://attrs-strict.readthedocs.io/en/latest/).

For the latest version, on github `pip install git+https://github.com/bloomberg/attrs-strict`.

<!-- end -->

## Contributions

We :heart: contributions.

Have you had a good experience with this project? Why not share some love and contribute code, or just let us know about any issues you had with it?

We welcome issue reports [here](../../issues); be sure to choose the proper issue template for your issue, so that we can be sure you're providing the necessary information.

Before sending a [Pull Request](../../pulls), please make sure you read our
[Contribution Guidelines](https://github.com/bloomberg/.github/blob/master/CONTRIBUTING.md).

## License

Please read the [LICENSE](LICENSE) file.

## Code of Conduct

This project has adopted a [Code of Conduct](https://github.com/bloomberg/.github/blob/master/CODE_OF_CONDUCT.md).
If you have any concerns about the Code, or behavior which you have experienced in the project, please
contact us at opensource@bloomberg.net.

## Security Vulnerability Reporting

If you believe you have identified a security vulnerability in this project, please send email to the project
team at opensource@bloomberg.net, detailing the suspected issue and any methods you've found to reproduce it.

Please do NOT open an issue in the GitHub repository, as we'd prefer to keep vulnerability reports private until
we've had an opportunity to review and address them.
