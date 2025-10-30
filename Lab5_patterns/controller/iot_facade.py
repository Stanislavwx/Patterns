from __future__ import annotations
from typing import Dict, Any, List, Optional
import httpx
from devices.base_device import Device

class IOTFacade:
    def __init__(self, timeout: float = 2.5):
        self._devices: Dict[str, Device] = {}
        self._client = httpx.Client(timeout=timeout)

    def register_device(self, device: Device) -> str:
        self._devices[device.device_id] = device
        return device.device_id

    def _endpoint(self, device: Device, path: str) -> str:
        return f"{device.base_url}{path}"

    def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        device = self._devices.get(device_id)
        if not device:
            return None
        try:
            r = self._client.get(self._endpoint(device, "/status"))
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {
                "device_id": device_id,
                "type": "unknown",
                "error": str(e),
                "connection": f"{device.host}:{device.port}"
            }

    def perform_device_action(self, device_id: str, action: str, **kwargs) -> bool:
        device = self._devices.get(device_id)
        if not device:
            return False

        if action == "power":
            state = kwargs.get("state")
            path = f"/power/{state}"
        elif action == "set_volume":
            level = int(kwargs.get("level", 0))
            path = f"/volume/{level}"
        elif action == "set_brightness":
            level = int(kwargs.get("level", 0))
            path = f"/brightness/{level}"
        elif action == "position":
            value = int(kwargs.get("value", 0))
            path = f"/position/{value}"
        else:
            return False

        try:
            r = self._client.post(self._endpoint(device, path))
            r.raise_for_status()
            return True
        except Exception:
            return False

    def get_all_status(self) -> List[Dict[str, Any]]:
        return [s for s in (self.get_device_status(did) for did in self._devices.keys()) if s]
