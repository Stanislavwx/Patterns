from __future__ import annotations

from typing import Any

from drones.bridge.base import MovementImplementor
from drones.utils.logger import get_logger


class DroneController:
    """Abstraction side of the Bridge pattern."""

    def __init__(self, implementor: MovementImplementor) -> None:
        self.impl = implementor
        self.mode = "single"
        self.log = get_logger("DroneController")

    def goto(self, coord, retries: int = 3) -> bool:
        attempt = 0
        while attempt < retries:
            attempt += 1
            self.log.info("Navigating to %s (attempt %s)", coord, attempt)
            success = self.impl.move_to(coord)
            if success:
                return True
        self.log.error("Failed to reach %s", coord)
        return False

    def adjust_course(self, vector) -> bool:
        self.log.info("Adjusting course by %s", vector)
        return self.impl.adjust_course(vector)

    def set_swarm(self) -> None:
        self.mode = "swarm"
        self.impl.set_mode("swarm")

    def set_single(self) -> None:
        self.mode = "single"
        self.impl.set_mode("single")

    def broadcast(self, message: Any) -> None:
        self.log.info("Broadcasting %s", message)
        self.impl.broadcast(message)

    def takeoff(self) -> bool:
        self.log.info("Takeoff")
        return self.impl.takeoff()

    def hold_position(self) -> bool:
        self.log.info("Holding position")
        return self.impl.hold_position()

    def land(self) -> bool:
        self.log.info("Landing")
        return self.impl.land()
