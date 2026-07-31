from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EnergyUnit(str, Enum):
    WATT = "W"
    KILOWATT = "kW"
    KILOWATT_HOUR = "kWh"
    VOLT = "V"
    AMPERE = "A"
    PERCENT = "%"


@dataclass(frozen=True)
class EnergyValue:
    value: float
    unit: EnergyUnit
    precision: int = 1

    def formatted(self) -> str:
        return f"{self.value:.{self.precision}f} {self.unit.value}"