from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Device:
    id: str
    name: str
    device_type: str


@dataclass(slots=True)
class DeviceRegistry:
    _devices: dict[str, Device] = field(
        default_factory=dict,
        init=False,
    )

    def register(self, device: Device) -> None:
        if device.id in self._devices:
            raise ValueError(
                f"Device '{device.id}' already registered."
            )

        self._devices[device.id] = device

    def unregister(self, device_id: str) -> None:
        self._devices.pop(device_id)

    def get(self, device_id: str) -> Device | None:
        return self._devices.get(device_id)

    def all(self) -> tuple[Device, ...]:
        return tuple(self._devices.values())

    @property
    def count(self) -> int:
        return len(self._devices)