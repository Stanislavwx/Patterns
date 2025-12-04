from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple


class MovementImplementor(ABC):
    """Implementation side of the Bridge pattern."""

    def __init__(self) -> None:
        self.history: List[Tuple[str, tuple]] = []

    def _record(self, action: str, payload: tuple) -> None:
        self.history.append((action, payload))

    @abstractmethod
    def takeoff(self) -> bool:  # pragma: no cover - abstract
        ...

    @abstractmethod
    def land(self) -> bool:  # pragma: no cover - abstract
        ...

    @abstractmethod
    def move_to(self, coord) -> bool:  # pragma: no cover - abstract
        ...

    @abstractmethod
    def adjust_course(self, vector) -> bool:  # pragma: no cover - abstract
        ...

    @abstractmethod
    def hold_position(self) -> bool:  # pragma: no cover - abstract
        ...

    @abstractmethod
    def set_mode(self, mode: str) -> None:  # pragma: no cover - abstract
        ...

    @abstractmethod
    def broadcast(self, message) -> None:  # pragma: no cover - abstract
        ...
