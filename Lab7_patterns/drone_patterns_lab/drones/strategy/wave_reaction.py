from __future__ import annotations

from drones.strategy.base import ReactionStrategy


class WaveReaction(ReactionStrategy):
    def react(self, mission, reading: dict) -> str:
        wave_height = reading.get("wave_height", 0)
        limit = mission.config.thresholds.get("max_wave", 2)
        if wave_height > limit:
            mission.telemetry.push("reaction", trigger="wave", value=wave_height)
            mission.controller.adjust_course((0, 0, 1))
            issue = {"type": "navigation", "alternate": mission.config.base_area.to_tuple()}
            return mission.fail_safe.handle(issue, {"controller": mission.controller, "mission_id": mission.config.mission_id})
        return "waves_ok"
