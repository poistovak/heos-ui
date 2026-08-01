from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .base import Widget


class PowerDirection(str, Enum):
    """Direction of electrical power flow."""

    IDLE = "idle"
    IMPORT = "import"
    EXPORT = "export"


class BatteryState(str, Enum):
    """Current battery operating state."""

    IDLE = "idle"
    CHARGING = "charging"
    DISCHARGING = "discharging"


@dataclass(slots=True, kw_only=True)
class PowerWidget(Widget):
    """Widget displaying electrical power."""

    power_w: float

    @property
    def power_kw(self) -> float:
        """Return power in kilowatts."""

        return self.power_w / 1000

    def render(self) -> str:
        """Return the formatted power."""

        if abs(self.power_w) < 1000:
            return f"{self.title}: {self.power_w:g} W"

        return f"{self.title}: {self.power_kw:g} kW"


@dataclass(slots=True, kw_only=True)
class SolarWidget(PowerWidget):
    """Widget displaying photovoltaic production."""

    def __post_init__(self) -> None:
        if self.power_w < 0:
            raise ValueError("Solar power cannot be negative.")


@dataclass(slots=True, kw_only=True)
class GridWidget(PowerWidget):
    """Widget displaying grid power and flow direction."""

    @property
    def direction(self) -> PowerDirection:
        """Return the current grid power-flow direction."""

        if self.power_w > 0:
            return PowerDirection.IMPORT

        if self.power_w < 0:
            return PowerDirection.EXPORT

        return PowerDirection.IDLE

    def render(self) -> str:
        """Return grid power with its direction."""

        power = abs(self.power_w)

        if power < 1000:
            formatted = f"{power:g} W"
        else:
            formatted = f"{power / 1000:g} kW"

        return f"{self.title}: {formatted} ({self.direction.value})"


@dataclass(slots=True, kw_only=True)
class BatteryWidget(PowerWidget):
    """Widget displaying battery charge and power state."""

    state_of_charge: float

    def __post_init__(self) -> None:
        if not 0 <= self.state_of_charge <= 100:
            raise ValueError(
                "Battery state of charge must be between 0 and 100."
            )

    @property
    def state(self) -> BatteryState:
        """Return the current battery operating state."""

        if self.power_w > 0:
            return BatteryState.CHARGING

        if self.power_w < 0:
            return BatteryState.DISCHARGING

        return BatteryState.IDLE

    def render(self) -> str:
        """Return battery charge, power, and operating state."""

        power = abs(self.power_w)

        if power < 1000:
            formatted = f"{power:g} W"
        else:
            formatted = f"{power / 1000:g} kW"

        return (
            f"{self.title}: {self.state_of_charge:g}% · "
            f"{formatted} ({self.state.value})"
        )