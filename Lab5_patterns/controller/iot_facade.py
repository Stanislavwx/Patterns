from __future__ import annotations
from typing import Dict, Any, List, Optional
import httpx

from devices.base_device import Device
from controller.routes import Route, make_route, DEFAULT_ROUTES


class IOTFacade:
    def __init__(self, timeout: float = 2.5, routes: Dict[str, Route] = DEFAULT_ROUTES):
        self._devices: Dict[str, Device] = {}
        self._client = httpx.Client(timeout=timeout)
        self._routes = routes

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
                "connection": f"{device.host}:{device.port}",
            }

    def perform_device_action(self, device_id: str, action: str, **kwargs) -> bool:
        device = self._devices.get(device_id)
        if not device:
            return False
        try:
            route = make_route(action, self._routes)
            path = route.build_path(**kwargs)
        except ValueError:
            return False
        try:
            url = self._endpoint(device, path)
            if route.method.upper() == "GET":
                r = self._client.get(url)
            else:
                r = self._client.post(url)
            r.raise_for_status()
            return True
        except Exception:
            return False

    def get_all_status(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for did in self._devices.keys():
            status = self.get_device_status(did)
            if status is not None:
                results.append(status)
        return results
