from typing import Dict, List, Any
import os
from controller.iot_facade import IOTFacade
from devices.base_device import Device, LoggingDeviceDecorator
from devices.smart_speaker import SmartSpeakerDevice
from devices.smart_light import SmartLightDevice
from devices.smart_curtains import SmartCurtainsDevice

class AppController:
    """Main application controller"""
    def __init__(self):
        self.facade = IOTFacade()
        self._register_default_devices()

    def _register_default_devices(self):
        """Register default devices with the system"""
        speaker_host = os.getenv("SPEAKER_HOST", "127.0.0.1")
        speaker_port = int(os.getenv("SPEAKER_PORT", "8001"))
        light_host = os.getenv("LIGHT_HOST", "127.0.0.1")
        light_port = int(os.getenv("LIGHT_PORT", "8002"))
        curtains_host = os.getenv("CURTAINS_HOST", "127.0.0.1")
        curtains_port = int(os.getenv("CURTAINS_PORT", "8003"))

        speaker = LoggingDeviceDecorator(
            SmartSpeakerDevice("speaker_001", speaker_host, speaker_port)
        )
        light = LoggingDeviceDecorator(
            SmartLightDevice("light_001", light_host, light_port)
        )
        curtains = LoggingDeviceDecorator(
            SmartCurtainsDevice("curtains_001", curtains_host, curtains_port)
        )
        self.facade.register_device(speaker)
        self.facade.register_device(light)
        self.facade.register_device(curtains)

    # Speaker
    def toggle_speaker(self) -> Dict[str, Any]:
        status = self.facade.get_device_status("speaker_001")
        if status and "is_on" in status:
            next_state = "off" if status["is_on"] else "on"
            if self.facade.perform_device_action("speaker_001", "power", state=next_state):
                return self.facade.get_device_status("speaker_001") or {}
        return {}

    def set_speaker_volume(self, volume: int) -> bool:
        return self.facade.perform_device_action("speaker_001", "set_volume", level=volume)

    # Light
    def toggle_light(self) -> Dict[str, Any]:
        status = self.facade.get_device_status("light_001")
        if status and "is_on" in status:
            next_state = "off" if status["is_on"] else "on"
            if self.facade.perform_device_action("light_001", "power", state=next_state):
                return self.facade.get_device_status("light_001") or {}
        return {}

    def set_light_brightness(self, brightness: int) -> bool:
        return self.facade.perform_device_action("light_001", "set_brightness", level=brightness)

    # Curtains
    def toggle_curtains(self) -> Dict[str, Any]:
        status = self.facade.get_device_status("curtains_001")
        if status and "is_open" in status:
            next_state = "close" if status["is_open"] else "open"
            if self.facade.perform_device_action("curtains_001", "power", state=next_state):
                return self.facade.get_device_status("curtains_001") or {}
        return {}

    def set_curtains_position(self, value: int) -> bool:
        return self.facade.perform_device_action("curtains_001", "position", value=value)

    def get_all_status(self) -> List[Dict[str, Any]]:
        return self.facade.get_all_status()

    def register_new_device(self, device: Device) -> str:
        return self.facade.register_device(device)
