from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WattpilotSnapshot:
    connected: bool
    charging: bool
    charging_power: float
    energy_session: float

    phases: int
    current_limit: float

    mode: str

    online: bool = True