from __future__ import annotations

from drones.config.mission_config import MissionConfig


class ConfigLoader:
    """Tiny loader that translates dict payloads into MissionConfig objects."""

    @staticmethod
    def from_dict(payload: dict) -> MissionConfig:
        return MissionConfig.from_dict(payload)
