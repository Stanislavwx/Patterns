from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TelemetryRecord:
    step: str
    detail: Dict[str, Any] = field(default_factory=dict)


class Telemetry:
    """Collects mission steps for assertions and debugging."""

    def __init__(self) -> None:
        self.records: List[TelemetryRecord] = []

    def push(self, step: str, **detail: Any) -> None:
        self.records.append(TelemetryRecord(step, detail))

    def as_dicts(self) -> List[Dict[str, Any]]:
        return [dict(step=r.step, detail=r.detail) for r in self.records]
