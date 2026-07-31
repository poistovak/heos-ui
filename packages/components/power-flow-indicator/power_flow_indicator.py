from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PowerNode(str, Enum):
    SOLAR = "solar"
    HOUSE = "house"
    BATTERY = "battery"
    GRID = "grid"
    EV = "ev"
    HEAT_PUMP = "heat_pump"


@dataclass(frozen=True)
class PowerFlowIndicator:
    source: PowerNode
    target: PowerNode
    power_kw: float
    precision: int = 1

    def formatted_power(self) -> str:
        return f"{self.power_kw:.{self.precision}f} kW"

    def direction_label(self) -> str:
        source = self.source.value.replace("_", " ").title()
        target = self.target.value.replace("_", " ").title()

        return f"{source} → {target}"

    def is_grid_import(self) -> bool:
        return self.source is PowerNode.GRID

    def is_grid_export(self) -> bool:
        return self.target is PowerNode.GRID