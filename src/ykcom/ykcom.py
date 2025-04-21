"""The main functionality of `ykcom`."""

from __future__ import annotations

import inspect
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, TypeVar
from unittest.mock import MagicMock, patch

if TYPE_CHECKING:
    from types import TracebackType

    from .types import Patcher

MockTarget = str | Iterable[str]
P = ParamSpec("P")
T = TypeVar("T")


@dataclass(frozen=True, kw_only=True, slots=True)
class MockData:
    """Collection of mocked data.

    `specs` contains the set of supported names by this collection of mocks.
    `mock` is the actual mock object returned by `ykcom`. The names referred in specs are attached to it.
    """

    specs: set[str] = field(default_factory=set)
    mock: MagicMock = field(default_factory=MagicMock)


def _to_list(t: MockTarget) -> list[str]:
    """Convert the given mock target to a list of strings."""
    return [t] if isinstance(t, str) else list(t)


class ykcom:  # noqa: N801
    def __init__(self, base_path: str, target: MockTarget, *args: MockTarget, name: str | None = None) -> None:
        self._base_path = base_path
        self._target = target
        self._args = args
        self._name = name
        self._patchers: list[Patcher] = []
        self._mock_data = MockData()

    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        if not hasattr(func, "_ykcom"):
            func._ykcom = {}  # type: ignore[attr-defined]

        if self._name:
            if other := func._ykcom.get(self._name):  # type: ignore[attr-defined]
                self._mock_data = other
            else:
                func._ykcom[self._name] = self._mock_data  # type: ignore[attr-defined]

            self._update_signature_with_named_default(func)
        else:
            self._update_signature_with_positional_default(func)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if self._name:
                kwargs.update({self._name: self._mock_data.mock})
            else:
                args = [self._mock_data.mock, *args]  # type: ignore[assignment]

            try:
                self._start()
                return func(*args, **kwargs)
            finally:
                self._stop()

        # TODO test for standalone function
        # TODO test for multiple decorators
        # TODO handle classes
        # TODO check behavior on failed tests
        # TODO async
        return wrapper

    def __enter__(self) -> MagicMock:
        self._start()

        return self._mock_data.mock

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._stop()

    def _start(self) -> None:
        target = _to_list(self._target)

        for arg in self._args:
            target.extend(_to_list(arg))

        for t in target:
            to_patch = t if "." in t else f"{self._base_path}.{t}"
            name = to_patch.split(".")[-1]
            # TODO check for duplicated names

            self._patchers.append(patch(to_patch))
            self._mock_data.specs.add(name)
            self._mock_data.mock.mock_add_spec(list(self._mock_data.specs), spec_set=True)

            new_mock = self._patchers[-1].start()
            setattr(self._mock_data.mock, name, new_mock)
            self._mock_data.mock.attach_mock(new_mock, name)

    def _stop(self) -> None:
        for patcher in self._patchers:
            patcher.stop()

        # Must reset the mocks. The same `_mock_data` object is being reused when used with `pytest.mark.parametrize`.
        self._mock_data.mock.reset_mock()
        for name in self._mock_data.specs:
            getattr(self._mock_data.mock, name).reset_mock()

    def _update_signature_with_named_default(self, func: Callable[P, T]) -> None:
        new_params = []
        new_with_default = None
        for name, param in inspect.signature(func).parameters.items():
            if name == self._name:
                new_with_default = param.replace(default=self._mock_data.mock)
            else:
                new_params.append(param)

        if new_with_default is None:
            raise ValueError(f"'{self._name}' not found in the parameter list")

        new_params.append(new_with_default)

        func.__signature__ = inspect.signature(func).replace(parameters=new_params)  # type: ignore[attr-defined]

    def _update_signature_with_positional_default(self, func: Callable[P, T]) -> None:
        params = list(inspect.signature(func).parameters.values())

        func.__signature__ = inspect.signature(  # type: ignore[attr-defined]
            func,
        ).replace(parameters=params[1:] + [params[0].replace(default=self._mock_data.mock)])


# TODO define overload to mock without base path
