from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Dict

from drones.observer.event_bus import EventBus
from drones.observer.events import EnvironmentEvent


class Environment(ABC):
    """Environment publishes events to missions."""

    def __init__(self, seed: int | None = None) -> None:
        self.bus = EventBus()
        if seed is not None:
            random.seed(seed)

    def subscribe(self, callback) -> None:
        self.bus.subscribe(callback)

    def start(self) -> EnvironmentEvent:
        reading = self.sample()
        event = EnvironmentEvent(name=self.__class__.__name__, reading=reading)
        self.bus.publish(event)
        return event

    @abstractmethod
    def sample(self) -> Dict:  # pragma: no cover - abstract
        ...
