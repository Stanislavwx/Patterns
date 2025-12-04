from __future__ import annotations

from drones.strategy.base import ReactionStrategy


class CrackReaction(ReactionStrategy):
    def react(self, mission, reading: dict) -> str:
        cracks = reading.get("crack_density", 0)
        limit = mission.config.thresholds.get("max_crack_density", 0.4)
        if cracks > limit:
            mission.telemetry.push("reaction", trigger="crack", value=cracks)
            mission.persistence.store(f"{mission.config.mission_id}_alert", {"crack_density": cracks})
            return "crack_alert"
        return "crack_ok"
