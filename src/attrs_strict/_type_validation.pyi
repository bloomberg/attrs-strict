import typing
import attr

def resolve_types(
    cls: type,
    global_ns: typing.Optional[typing.Dict[str, typing.Any]] = None,
    local_ns: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> None: ...
def type_validator(
    empty_ok: bool = True,
) -> typing.Callable[
    [typing.Any, attr.Attribute[typing.Any], typing.Any], None
]:
    def _validator(
        instance: typing.Any,
        attribute: attr.Attribute[typing.Any],
        field: typing.Any,
    ) -> None: ...
    return _validator

def _validate_elements(
    attribute: attr.Attribute[typing.Any],
    value: typing.Any,
    expected_type: typing.Optional[typing.Type[typing.Any]],
) -> None: ...
def _get_base_type(
    type_: typing.Type[typing.Any],
) -> typing.Type[typing.Any]: ...
def _type_matching(
    actual: typing.Type[typing.Any], expected: typing.Type[typing.Any]
) -> bool: ...
def _handle_callable(
    attribute: attr.Attribute[typing.Any],
    callable_: typing.Callable[..., typing.Any],
    expected_type: typing.Type[typing.Callable[..., typing.Any]],
) -> None: ...
def _handle_set_or_list(
    attribute: attr.Attribute[typing.Any],
    container: typing.Union[typing.Set[typing.Any], typing.List[typing.Any]],
    expected_type: typing.Union[
        typing.Type[typing.Set[typing.Any]],
        typing.Type[typing.List[typing.Any]],
    ],
) -> None: ...
def _handle_dict(
    attribute: attr.Attribute[typing.Any],
    container: typing.Union[
        typing.Mapping[typing.Any, typing.Any],
        typing.MutableMapping[typing.Any, typing.Any],
    ],
    expected_type: typing.Union[
        typing.Type[typing.Mapping[typing.Any, typing.Any]],
        typing.Type[typing.MutableMapping[typing.Any, typing.Any]],
    ],
) -> None: ...
def _handle_tuple(
    attribute: attr.Attribute[typing.Any],
    container: typing.Tuple[typing.Any],
    expected_type: typing.Type[typing.Tuple[typing.Any]],
) -> None: ...
def _handle_union(
    attribute: attr.Attribute[typing.Any],
    value: typing.Any,
    expected_type: typing.Type[typing.Any],
) -> None: ...
