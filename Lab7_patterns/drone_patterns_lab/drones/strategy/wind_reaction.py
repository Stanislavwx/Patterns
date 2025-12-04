from __future__ import annotations

from drones.strategy.base import ReactionStrategy


class WindReaction(ReactionStrategy):
    def react(self, mission, reading: dict) -> str:
        speed = reading.get("wind_speed", 0)
        limit = mission.config.thresholds.get("max_wind", 10)
        if speed > limit:
            mission.telemetry.push("reaction", trigger="wind", value=speed)
            issue = {"type": "wind", "strength": speed}
            return mission.fail_safe.handle(issue, {"controller": mission.controller})
        return "wind_ok"
