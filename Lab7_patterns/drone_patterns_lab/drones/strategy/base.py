from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class ReactionStrategy(ABC):
    """Strategy for reacting to environment readings."""

    @abstractmethod
    def react(self, mission, reading: Dict[str, Any]) -> str:  # pragma: no cover - abstract
        ...
