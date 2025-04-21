class YckomError(Exception):
    """Shared base error type for Ykcom."""


class TargetAlreadyBoundError(YckomError):
    """Indicates that the same target has been assigned to multiple names."""
