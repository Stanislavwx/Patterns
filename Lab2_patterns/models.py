from abc import ABC, abstractmethod
import math

class IPort(ABC):
    @abstractmethod
    def incomingShip(self, s): ...
    @abstractmethod
    def outgoingShip(self, s): ...

class IShip(ABC):
    @abstractmethod
    def sailTo(self, p): ...
    @abstractmethod
    def reFuel(self, add): ...
    @abstractmethod
    def load(self, cont): ...
    @abstractmethod
    def unLoad(self, cont): ...

class Container(ABC):
    def __init__(self, ID: int, weight: int):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        ...

    def equals(self, other: "Container") -> bool:
        return type(self) is type(other) and self.ID == other.ID and self.weight == other.weight

class BasicContainer(Container):
    def consumption(self) -> float:
        return 2.50 * (self.weight / 1000.0)

class HeavyContainer(Container):
    def consumption(self) -> float:
        return 3.00 * (self.weight / 1000.0)

class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return 5.00 * (self.weight / 1000.0)

class LiquidContainer(HeavyContainer):
    def consumption(self) -> float:
        return 4.00 * (self.weight / 1000.0)

class Port(IPort):
    def __init__(self, ID: int, latitude: float, longitude: float):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current = []

    def incomingShip(self, s):
        if s not in self.current:
            self.current.append(s)
        if s not in self.history:
            self.history.append(s)

    def outgoingShip(self, s):
        if s in self.current:
            self.current.remove(s)
        if s not in self.history:
            self.history.append(s)

    def getDistance(self, other: "Port") -> float:
        dx = self.latitude - other.latitude
        dy = self.longitude - other.longitude
        return math.hypot(dx, dy)

class Ship(IShip):
    def __init__(self, ID: int, currentPort: Port,
                 totalWeightCapacity: int, maxNumberOfAllContainers: int,
                 maxNumberOfHeavyContainers: int, maxNumberOfRefrigeratedContainers: int,
                 maxNumberOfLiquidContainers: int, fuelConsumptionPerKM: float):
        self.ID = ID
        self.fuel = 0.0
        self.currentPort = currentPort
        self.totalWeightCapacity = totalWeightCapacity
        self.maxNumberOfAllContainers = maxNumberOfAllContainers
        self.maxNumberOfHeavyContainers = maxNumberOfHeavyContainers
        self.maxNumberOfRefrigeratedContainers = maxNumberOfRefrigeratedContainers
        self.maxNumberOfLiquidContainers = maxNumberOfLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.onboard = []
        self.visited_ports = []
        if self.currentPort:
            self.currentPort.incomingShip(self)
            self.visited_ports.append(self.currentPort.ID)

    def weightOnboard(self) -> int:
        return sum(c.weight for c in self.onboard)

    def countHeavy(self) -> int:
        return sum(1 for c in self.onboard if isinstance(c, HeavyContainer))

    def countRef(self) -> int:
        return sum(1 for c in self.onboard if isinstance(c, RefrigeratedContainer))

    def countLiq(self) -> int:
        return sum(1 for c in self.onboard if isinstance(c, LiquidContainer))

    def containersConsumption(self) -> float:
        return sum(c.consumption() for c in self.onboard)

    def getCurrentContainers(self):
        return sorted(self.onboard, key=lambda c: c.ID)

    def load(self, cont: Container) -> bool:
        if not self.currentPort:
            return False
        if cont not in self.currentPort.containers:
            return False
        if len(self.onboard) >= self.maxNumberOfAllContainers:
            return False
        if self.weightOnboard() + cont.weight > self.totalWeightCapacity:
            return False
        is_heavy = isinstance(cont, HeavyContainer)
        is_ref   = isinstance(cont, RefrigeratedContainer)
        is_liq   = isinstance(cont, LiquidContainer)
        if is_heavy and (self.countHeavy() + 1 > self.maxNumberOfHeavyContainers):
            return False
        if is_ref and (self.countRef() + 1 > self.maxNumberOfRefrigeratedContainers):
            return False
        if is_liq and (self.countLiq() + 1 > self.maxNumberOfLiquidContainers):
            return False
        self.onboard.append(cont)
        self.currentPort.containers.remove(cont)
        return True

    def unLoad(self, cont: Container) -> bool:
        if not self.currentPort:
            return False
        if cont not in self.onboard:
            return False
        self.onboard.remove(cont)
        self.currentPort.containers.append(cont)
        return True

    def reFuel(self, add: float):
        self.fuel += add

    def sailTo(self, p: Port, world=None) -> bool:
        if not p or not self.currentPort:
            return False
        per_km = self.fuelConsumptionPerKM + self.containersConsumption()
        dist = self.currentPort.getDistance(p)
        need = dist * per_km
        if self.fuel + 1e-9 >= need:
            self.fuel -= need
            self.currentPort.outgoingShip(self)
            self.currentPort = p
            self.currentPort.incomingShip(self)
            self.visited_ports.append(self.currentPort.ID)
            return True
        if world is not None:
            reachable = []
            for other in world.ports.values():
                if other is self.currentPort or other is p:
                    continue
                d2 = self.currentPort.getDistance(other)
                need2 = d2 * per_km
                if self.fuel + 1e-9 >= need2:
                    reachable.append((need2, other))
            if reachable:
                need2, nearest = min(reachable, key=lambda x: x[0])
                self.fuel -= need2
                self.currentPort.outgoingShip(self)
                self.currentPort = nearest
                self.currentPort.incomingShip(self)
                self.visited_ports.append(self.currentPort.ID)
                print(f"[info] Ship {self.ID} could not reach Port {p.ID}, stopped at Port {nearest.ID} to refuel")
                return True
        return False

class World:
    def __init__(self):
        self.ports = {}
        self.ships = {}
        self.containers = {}
