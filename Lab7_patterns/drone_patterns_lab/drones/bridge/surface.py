from drones.bridge.base import MovementImplementor


class SurfacePlatform(MovementImplementor):
    def takeoff(self) -> bool:
        self._record("start_engines", ())
        return True

    def land(self) -> bool:
        self._record("stop_engines", ())
        return True

    def move_to(self, coord) -> bool:
        self._record("drive_to", tuple(coord))
        return True

    def adjust_course(self, vector) -> bool:
        self._record("adjust_surface", tuple(vector))
        return True

    def hold_position(self) -> bool:
        self._record("pause", ())
        return True

    def set_mode(self, mode: str) -> None:
        self._record("mode", (mode,))

    def broadcast(self, message) -> None:
        self._record("broadcast", (message,))
