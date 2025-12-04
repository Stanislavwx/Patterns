from __future__ import annotations

from drones.cor.base import FailSafeHandler
from drones.utils.logger import get_logger


class SwarmReassignHandler(FailSafeHandler):
    def __init__(self, next_handler=None) -> None:
        super().__init__(next_handler)
        self.log = get_logger("SwarmReassignHandler")

    def _process(self, issue: dict, context: dict) -> str:
        if issue.get("type") not in {"swarm", "platform"}:
            return ""
        controller = context.get("controller")
        if controller:
            self.log.info("Reassigning swarm task due to %s", issue.get("reason", "unknown"))
            controller.broadcast({"action": "reassign", "mission": context.get("mission_id")})
            controller.set_swarm()
        return "swarm_reassigned"
