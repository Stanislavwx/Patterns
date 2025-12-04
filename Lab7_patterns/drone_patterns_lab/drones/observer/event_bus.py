from __future__ import annotations

from typing import Callable, List, Protocol


class Subscriber(Protocol):
    def __call__(self, event) -> None:  # pragma: no cover - Protocol signature only
        ...


class EventBus:
    """Very small observer implementation."""

    def __init__(self) -> None:
        self._subscribers: List[Subscriber] = []

    def subscribe(self, callback: Subscriber) -> None:
        self._subscribers.append(callback)

    def publish(self, event) -> None:
        for callback in list(self._subscribers):
            callback(event)
