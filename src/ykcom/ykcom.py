"""The main functionality of `ykcom`."""

from collections.abc import Generator, Iterable
from contextlib import contextmanager
from dataclasses import dataclass, field
from unittest.mock import MagicMock, patch

MockTarget = str | Iterable[str]


@dataclass(frozen=True, kw_only=True, slots=True)
class MockData:
    """Collection of mocked data.

    `mocks` contains the created MagicMock instances. `M` is a helper MagicMock which has all created mockes attached to
    it.
    """

    mocks: dict[str, MagicMock] = field(default_factory=dict)
    M: MagicMock = field(default_factory=MagicMock)


def _to_list(t: MockTarget) -> list[str]:
    """Convert the given mock target to a list of strings."""
    return [t] if isinstance(t, str) else list(t)


# TODO define overload to mock without base path
@contextmanager
def ykcom(base_path: str, target: MockTarget, *args: MockTarget) -> Generator[MockData]:
    # TODO doc
    patchers = []
    mock_data = MockData()
    target = _to_list(target)

    for arg in args:
        target.extend(_to_list(arg))

    try:
        for t in target:
            to_patch = t if "." in t else f"{base_path}.{t}"
            name = to_patch.split(".")[-1]
            # TODO check for duplicated names

            patchers.append(patch(to_patch))
            mock_data.mocks[name] = patchers[-1].start()
            mock_data.M.attach_mock(mock_data.mocks[name], name)

        yield mock_data
    finally:
        for patcher in patchers:
            patcher.stop()
