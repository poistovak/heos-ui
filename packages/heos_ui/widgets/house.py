from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HouseState:
    """Current house consumption."""

    power: float
    today_energy: float
    online: bool = True


@dataclass(slots=True)
class HouseWidget:
    """House load dashboard widget."""

    title: str = "House"

    _state: HouseState | None = None

    def update(
        self,
        state: HouseState,
    ) -> None:
        self._state = state

    @property
    def state(self) -> HouseState | None:
        return self._state

    @property
    def power(self) -> float:
        if self._state is None:
            return 0.0

        return self._state.power

    @property
    def today_energy(self) -> float:
        if self._state is None:
            return 0.0

        return self._state.today_energy

    @property
    def online(self) -> bool:
        if self._state is None:
            return False

        return self._state.online