class TypeValidationError(Exception):
    def __repr__(self):
        return "<{}>".format(str(self))


class BadTypeError(TypeValidationError, ValueError):
    def __init__(self):
        self.containers = []

    def add_container(self, container):
        self.containers.append(container)

    def _render(self, error):
        if self.containers:
            backtrack = " in ".join(
                [str(container) for container in self.containers]
            )
            return "{} in {}".format(error, backtrack)

        return error


class AttributeTypeError(BadTypeError):
    def __init__(self, container, attribute):
        super(AttributeTypeError, self).__init__()
        self.container = container
        self.attribute = attribute

    def __str__(self):
        error = "{} must be {} (got {} that is a {})".format(
            self.attribute.name,
            self.attribute.type,
            self.container,
            type(self.container),
        )

        return self._render(error)


class TupleError(BadTypeError):
    def __init__(self, container, attribute, tuple_types):
        super(TupleError, self).__init__()
        self.attribute = attribute
        self.container = container
        self.tuple_types = tuple_types

    def __str__(self):
        error = (
            "Element {} has {} elements than types "
            "specified in {}. Expected {} received {}"
        ).format(
            self.container,
            self._more_or_less(),
            self.attribute,
            len(self.tuple_types),
            len(self.container),
        )

        return self._render(error)

    def _more_or_less(self):
        return "more" if len(self.container) > len(self.tuple_types) else "less"


class UnionError(BadTypeError):
    def __init__(self, container, attribute, expected_type):
        super(UnionError, self).__init__()
        self.attribute = attribute
        self.container = container
        self.expected_type = expected_type

    def __str__(self):
        error = "Value of {} {} is not of type {}".format(
            self.attribute, self.container, self.expected_type
        )

        return self._render(error)
