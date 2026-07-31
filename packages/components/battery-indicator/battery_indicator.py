from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BatteryState(str, Enum):
    CHARGING = "charging"
    DISCHARGING = "discharging"
    IDLE = "idle"
    CRITICAL = "critical"


@dataclass(frozen=True)
class BatteryIndicator:
    soc: int
    state: BatteryState

    def percentage(self) -> str:
        return f"{self.soc}%"

    def label(self) -> str:
        return self.state.value.replace("_", " ").title()

    def is_low(self) -> bool:
        return self.soc <= 20