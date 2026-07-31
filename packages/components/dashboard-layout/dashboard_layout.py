from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardLayout:
    solar_power_kw: float
    battery_soc: int
    house_power_kw: float
    grid_power_kw: float

    def is_grid_import(self) -> bool:
        return self.grid_power_kw > 0

    def is_grid_export(self) -> bool:
        return self.grid_power_kw < 0

    def total_local_power(self) -> float:
        return self.solar_power_kw + max(0.0, -self.grid_power_kw)