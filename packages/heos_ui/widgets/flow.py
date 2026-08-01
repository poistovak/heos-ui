from __future__ import annotations

from dataclasses import dataclass

from .base import Widget
from .energy import BatteryState, PowerDirection


@dataclass(slots=True, kw_only=True)
class FlowWidget(Widget):
    """Widget representing the current household energy flow."""

    solar_power_w: float
    house_power_w: float
    battery_power_w: float = 0
    grid_power_w: float = 0
    balance_tolerance_w: float = 1

    def __post_init__(self) -> None:
        if self.solar_power_w < 0:
            raise ValueError("Solar power cannot be negative.")

        if self.house_power_w < 0:
            raise ValueError("House power cannot be negative.")

        if self.balance_tolerance_w < 0:
            raise ValueError("Balance tolerance cannot be negative.")

    @property
    def battery_state(self) -> BatteryState:
        """Return the current battery operating state."""

        if self.battery_power_w > 0:
            return BatteryState.CHARGING

        if self.battery_power_w < 0:
            return BatteryState.DISCHARGING

        return BatteryState.IDLE

    @property
    def grid_direction(self) -> PowerDirection:
        """Return the current grid power-flow direction."""

        if self.grid_power_w > 0:
            return PowerDirection.IMPORT

        if self.grid_power_w < 0:
            return PowerDirection.EXPORT

        return PowerDirection.IDLE

    @property
    def balance_w(self) -> float:
        """Return the signed energy-balance difference."""

        return (
            self.solar_power_w
            + self.grid_power_w
            - self.battery_power_w
            - self.house_power_w
        )

    @property
    def is_balanced(self) -> bool:
        """Return whether the energy flow is within tolerance."""

        return abs(self.balance_w) <= self.balance_tolerance_w

    def render(self) -> str:
        """Return a compact text representation of the energy flow."""

        return (
            f"{self.title}: "
            f"solar={self._format_power(self.solar_power_w)}, "
            f"house={self._format_power(self.house_power_w)}, "
            f"battery={self._format_power(abs(self.battery_power_w))} "
            f"({self.battery_state.value}), "
            f"grid={self._format_power(abs(self.grid_power_w))} "
            f"({self.grid_direction.value})"
        )

    @staticmethod
    def _format_power(power_w: float) -> str:
        if power_w < 1000:
            return f"{power_w:g} W"

        return f"{power_w / 1000:g} kW"