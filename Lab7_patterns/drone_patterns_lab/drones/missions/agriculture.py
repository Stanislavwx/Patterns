from __future__ import annotations

from drones.template.base import DroneMission


class AgricultureMission(DroneMission):
    def perform_payload_action(self) -> None:
        if self.config.mode == "swarm":
            self.controller.set_swarm()
        self.telemetry.push("payload", action="spray_or_scan")
        self.controller.adjust_course((0.2, 0, 0))

    def environment_requires_reaction(self) -> bool:
        # Agriculture missions react more frequently to changing wind.
        return self._remaining_reactions > 0 and self.config.thresholds.get("enable_reaction", True)
