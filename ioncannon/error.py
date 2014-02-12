"""Errors."""


class NotFound(RuntimeError):

    """Exception to indicate model was not found."""

    pass


class NoFile(RuntimeError):

    """Exception to indicate model has no file."""

    pass
