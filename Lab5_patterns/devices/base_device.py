from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any

class Device(ABC):
    def __init__(self, device_id: str, host: str = "127.0.0.1", port: int = 0):
        self.device_id = device_id
        self.host = host
        self.port = port

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def perform_action(self, action: str, **kwargs) -> bool:
        raise NotImplementedError


class LoggingDeviceDecorator(Device):
    def __init__(self, wrapped: Device):
        super().__init__(wrapped.device_id, wrapped.host, wrapped.port)
        self._wrapped = wrapped

    def get_status(self) -> Dict[str, Any]:
        return self._wrapped.get_status()

    def perform_action(self, action: str, **kwargs) -> bool:
        try:
            return self._wrapped.perform_action(action, **kwargs)
        finally:
            print(f"[LOG] device={self.device_id} action={action} kwargs={kwargs}")
