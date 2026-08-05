from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GridState:
    """Current grid state."""

    power: float
    importing: bool
    exporting: bool
    online: bool = True


@dataclass(slots=True)
class GridWidget:
    """Grid dashboard widget."""

    title: str = "Grid"

    _state: GridState | None = None

    def update(
        self,
        state: GridState,
    ) -> None:
        self._state = state

    @property
    def state(self) -> GridState | None:
        return self._state

    @property
    def power(self) -> float:
        return 0.0 if self._state is None else self._state.power

    @property
    def importing(self) -> bool:
        return False if self._state is None else self._state.importing

    @property
    def exporting(self) -> bool:
        return False if self._state is None else self._state.exporting

    @property
    def online(self) -> bool:
        return False if self._state is None else self._state.online