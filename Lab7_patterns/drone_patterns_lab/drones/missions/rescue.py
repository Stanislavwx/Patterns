from __future__ import annotations

from drones.template.base import DroneMission


class RescueMission(DroneMission):
    def perform_payload_action(self) -> None:
        self.telemetry.push("payload", action="drop_kit")
        self.controller.broadcast({"action": "flare", "mission": self.config.mission_id})

    def environment_requires_reaction(self) -> bool:
        # Rescue keeps reacting as long as visibility is low or until cycles exhausted.
        if self._remaining_reactions <= 0:
            return False
        last_visibility = 1.0
        if self.observed_events:
            last_visibility = self.observed_events[-1].reading.get("visibility", 1.0)
        return last_visibility < 0.7
