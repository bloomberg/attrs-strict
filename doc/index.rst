attrs_strict documentation
============================

Background
----------

The purpose of the library is to provide runtime validation for attributes specified in
`attrs <https://www.attrs.org/en/stable/>`_ data classes. The types supported are all the builtin
types and most of the ones defined in the typing library. For Python 2, the typing module is
available through the backport found `here <https://pypi.org/project/typing/>`_.

Getting started
---------------

Run :code:`pip install attrs-strict` to install the latest stable version from PyPi.
The source code is hosted on github at `<https://github.com/bloomberg/attrs-strict>`_.
The library currently supports :code:`Python2.7`, :code:`Python3.6` and :code:`Python3.7`.

Usage and examples
------------------
Type enforcement is based on the :code:`type` attribute set on any field specified in an :code:`attrs` dataclass.
If the type argument is not specified no validation takes place.

.. code-block:: python

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

.. code-block:: console

   SomeClass(list_of_numbers=[1, 2, 3, 4])
   <list_of_numbers must be typing.List[int] (got four that is a <class 'str'>) in [1, 2, 3, 'four']>

Nested type exceptions are validated accordingly, and a backtrace to the initial
container is maintained to ease with debugging. This means that if an exception
occurs because a nested element doesn't have the correct type, the representation
of the exception will contain the path to the specific element that caused the exception.

.. code-block:: python

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

.. code-block:: console

   names must be typing.List[typing.Tuple[str, str]] (got 123 that is a <class 'int'>) in ('Zoo', 123) in [('Moo', 'Moo'), ('Zoo', 123)]

What is currently supported ?
-----------------------------

Currently, there's support for builtin types and types specified in the :code:`typing`
module: :code:`List`, :code:`Dict`, :code:`DefaultDict`, :code:`Set`, :code:`Union`,
:code:`Tuple`, :code:`NewType` and any combination of them. This means that you can
specify nested types like :code:`List[List[Dict[int, str]]]` and the validation would
check if attribute has the specific type.

:code:`Callables`, :code:`TypeVars` or :code:`Generics` are not supported yet but
there are plans to support this in the future.

.. toctree::
   :maxdepth: 1

   api
