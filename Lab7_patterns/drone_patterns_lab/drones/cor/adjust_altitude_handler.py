from __future__ import annotations

from drones.cor.base import FailSafeHandler
from drones.utils.logger import get_logger


class AdjustAltitudeHandler(FailSafeHandler):
    def __init__(self, next_handler=None) -> None:
        super().__init__(next_handler)
        self.log = get_logger("AdjustAltitudeHandler")

    def _process(self, issue: dict, context: dict) -> str:
        if issue.get("type") not in {"wind", "turbulence"}:
            return ""
        controller = context.get("controller")
        strength = issue.get("strength", 1.0)
        adjustment = (0, 0, max(1.0, strength))
        if controller:
            self.log.info("Adjusting altitude due to wind: %s", strength)
            controller.adjust_course(adjustment)
        return "altitude_adjusted"
