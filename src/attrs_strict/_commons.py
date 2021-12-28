from __future__ import annotations

import typing


def is_newtype(type_: type[typing.Any]) -> bool:
    return hasattr(type_, "__name__") and hasattr(type_, "__supertype__")


def format_type(type_: type[typing.Any]) -> str:
    if is_newtype(type_):
        return f"NewType({type_.__name__}, {type_.__supertype__})"

    return str(type_)
