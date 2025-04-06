from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from unittest.mock import MagicMock


class Patcher(Protocol):
    def start(self) -> MagicMock: ...

    def stop(self) -> None: ...
