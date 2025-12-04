from drones.bridge.base import MovementImplementor


class SeaPlatform(MovementImplementor):
    def takeoff(self) -> bool:
        self._record("deploy", ())
        return True

    def land(self) -> bool:
        self._record("dock", ())
        return True

    def move_to(self, coord) -> bool:
        self._record("sail_to", tuple(coord))
        return True

    def adjust_course(self, vector) -> bool:
        self._record("adjust_rudder", tuple(vector))
        return True

    def hold_position(self) -> bool:
        self._record("hold", ())
        return True

    def set_mode(self, mode: str) -> None:
        self._record("mode", (mode,))

    def broadcast(self, message) -> None:
        self._record("broadcast", (message,))
