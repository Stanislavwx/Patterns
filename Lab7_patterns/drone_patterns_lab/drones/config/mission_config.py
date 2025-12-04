from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Coord:
    """Simple 3D coordinate used for navigation."""

    x: float
    y: float
    z: float = 0.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Coord":
        return cls(float(data.get("x", 0.0)), float(data.get("y", 0.0)), float(data.get("z", 0.0)))

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class MissionConfig:
    mission_id: str
    mission_type: str
    environment_type: str
    platform_type: str
    mode: str
    target_area: Coord
    base_area: Coord
    thresholds: Dict[str, Any] = field(default_factory=dict)
    behavior_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MissionConfig":
        return cls(
            mission_id=data["mission_id"],
            mission_type=data["mission_type"],
            environment_type=data["environment_type"],
            platform_type=data["platform_type"],
            mode=data.get("mode", "single"),
            target_area=Coord.from_dict(data.get("target_area", {})),
            base_area=Coord.from_dict(data.get("base_area", {})),
            thresholds=data.get("thresholds", {}) or {},
            behavior_params=data.get("behavior_params", {}) or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "mission_type": self.mission_type,
            "environment_type": self.environment_type,
            "platform_type": self.platform_type,
            "mode": self.mode,
            "target_area": vars(self.target_area),
            "base_area": vars(self.base_area),
            "thresholds": self.thresholds,
            "behavior_params": self.behavior_params,
        }
