from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HeatPumpState:
    """Current heat pump state."""

    mode: str
    outdoor_temperature: float
    water_temperature: float
    compressor_power: float
    compressor_running: bool
    online: bool = True


@dataclass(slots=True)
class HeatPumpWidget:
    """Heat pump dashboard widget."""

    title: str = "Heat Pump"

    _state: HeatPumpState | None = None

    def update(
        self,
        state: HeatPumpState,
    ) -> None:
        self._state = state

    @property
    def state(self) -> HeatPumpState | None:
        return self._state

    @property
    def mode(self) -> str:
        return "offline" if self._state is None else self._state.mode

    @property
    def outdoor_temperature(self) -> float:
        return 0.0 if self._state is None else self._state.outdoor_temperature

    @property
    def water_temperature(self) -> float:
        return 0.0 if self._state is None else self._state.water_temperature

    @property
    def compressor_power(self) -> float:
        return 0.0 if self._state is None else self._state.compressor_power

    @property
    def compressor_running(self) -> bool:
        return False if self._state is None else self._state.compressor_running

    @property
    def online(self) -> bool:
        return False if self._state is None else self._state.online