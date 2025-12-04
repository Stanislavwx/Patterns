from __future__ import annotations

from typing import Optional

from drones.utils.logger import get_logger


class FailSafeHandler:
    """Chain of Responsibility base handler."""

    def __init__(self, next_handler: Optional["FailSafeHandler"] = None) -> None:
        self._next = next_handler
        self.log = get_logger(self.__class__.__name__)

    def set_next(self, handler: "FailSafeHandler") -> "FailSafeHandler":
        self._next = handler
        return handler

    def handle(self, issue: dict, context: dict) -> str:
        resolved = self._process(issue, context)
        if resolved:
            return resolved
        if self._next:
            return self._next.handle(issue, context)
        return "unresolved"

    def _process(self, issue: dict, context: dict) -> str:  # pragma: no cover - abstract
        raise NotImplementedError
