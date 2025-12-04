from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class EnvironmentEvent:
    name: str
    reading: Dict[str, Any]
    severity: str = "info"
