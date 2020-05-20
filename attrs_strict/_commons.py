def is_newtype(type_):
    return (
        hasattr(type_, "__name__")
        and type_.__module__ == "typing"
        and type_.__name__ == "SomeNew"
    )


def format_type(type_):
    if is_newtype(type_):
        return "NewType({}, {})".format(type_.__name__, type_.__supertype__)

    return str(type_)
