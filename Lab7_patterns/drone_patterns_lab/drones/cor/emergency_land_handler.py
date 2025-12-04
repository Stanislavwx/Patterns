from __future__ import annotations

from drones.cor.base import FailSafeHandler
from drones.utils.logger import get_logger


class EmergencyLandHandler(FailSafeHandler):
    def __init__(self, next_handler=None) -> None:
        super().__init__(next_handler)
        self.log = get_logger("EmergencyLandHandler")

    def _process(self, issue: dict, context: dict) -> str:
        controller = context.get("controller")
        if controller:
            self.log.warning("Emergency landing triggered: %s", issue)
            controller.land()
        return "emergency_land"
