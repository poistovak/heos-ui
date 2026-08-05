from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BatteryState:
    """Current battery state."""

    soc: float
    power: float
    capacity: float
    charging: bool
    online: bool = True


@dataclass(slots=True)
class BatteryWidget:
    """Battery dashboard widget."""

    title: str = "Battery"

    _state: BatteryState | None = None

    def update(
        self,
        state: BatteryState,
    ) -> None:
        self._state = state

    @property
    def state(self) -> BatteryState | None:
        return self._state

    @property
    def soc(self) -> float:
        return 0.0 if self._state is None else self._state.soc

    @property
    def power(self) -> float:
        return 0.0 if self._state is None else self._state.power

    @property
    def capacity(self) -> float:
        return 0.0 if self._state is None else self._state.capacity

    @property
    def charging(self) -> bool:
        return False if self._state is None else self._state.charging

    @property
    def online(self) -> bool:
        return False if self._state is None else self._state.online