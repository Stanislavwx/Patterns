from drones.bridge.base import MovementImplementor


class AirPlatform(MovementImplementor):
    def takeoff(self) -> bool:
        self._record("takeoff", ())
        return True

    def land(self) -> bool:
        self._record("land", ())
        return True

    def move_to(self, coord) -> bool:
        self._record("fly_to", tuple(coord))
        return True

    def adjust_course(self, vector) -> bool:
        self._record("adjust_air_course", tuple(vector))
        return True

    def hold_position(self) -> bool:
        self._record("hover", ())
        return True

    def set_mode(self, mode: str) -> None:
        self._record("mode", (mode,))

    def broadcast(self, message) -> None:
        self._record("broadcast", (message,))
