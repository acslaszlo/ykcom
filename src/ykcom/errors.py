class YckomError(Exception):
    """Shared base error type for Ykcom."""


class NamedParameterNotFoundError(YckomError):
    """No parameter found with the provided name."""


class TargetAlreadyBoundError(YckomError):
    """Indicates that the same target has been assigned to multiple names."""


class NameCollisionError(YckomError):
    """The same name has been provided for multiple targets."""
