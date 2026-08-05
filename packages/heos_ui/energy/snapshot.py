from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnergySnapshot:
    """Normalized state of the complete home energy system."""

    pv_power: float = 0.0
    house_power: float = 0.0
    grid_power: float = 0.0

    battery_soc: float | None = None
    battery_power: float = 0.0
    battery_online: bool = False

    ev_power: float = 0.0
    ev_connected: bool = False
    ev_charging: bool = False
    ev_online: bool = False

    heat_pump_power: float = 0.0
    heat_pump_running: bool = False
    heat_pump_online: bool = False

    def __post_init__(self) -> None:
        non_negative = {
            "pv_power": self.pv_power,
            "house_power": self.house_power,
            "ev_power": self.ev_power,
            "heat_pump_power": self.heat_pump_power,
        }

        for name, value in non_negative.items():
            if value < 0.0:
                raise ValueError(
                    f"{name} cannot be negative."
                )

        if (
            self.battery_soc is not None
            and not 0.0 <= self.battery_soc <= 100.0
        ):
            raise ValueError(
                "battery_soc must be between 0 and 100."
            )

    @property
    def surplus_power(self) -> float:
        """Return locally available PV surplus."""

        return max(
            0.0,
            self.pv_power - self.house_power,
        )

    @property
    def grid_import_power(self) -> float:
        """Positive grid power means import."""

        return max(
            0.0,
            self.grid_power,
        )

    @property
    def grid_export_power(self) -> float:
        """Negative grid power means export."""

        return max(
            0.0,
            -self.grid_power,
        )

    @property
    def battery_charging(self) -> bool:
        return (
            self.battery_online
            and self.battery_power > 0.0
        )

    @property
    def battery_discharging(self) -> bool:
        return (
            self.battery_online
            and self.battery_power < 0.0
        )