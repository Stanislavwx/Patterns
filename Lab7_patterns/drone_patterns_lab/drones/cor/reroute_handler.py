from __future__ import annotations

from drones.cor.base import FailSafeHandler
from drones.utils.logger import get_logger


class ReRouteHandler(FailSafeHandler):
    def __init__(self, next_handler=None) -> None:
        super().__init__(next_handler)
        self.log = get_logger("ReRouteHandler")

    def _process(self, issue: dict, context: dict) -> str:
        if issue.get("type") not in {"navigation", "obstacle"}:
            return ""
        controller = context.get("controller")
        target = issue.get("alternate")
        if controller and target:
            self.log.info("Rerouting to %s", target)
            controller.goto(target, retries=1)
        return "rerouted"
