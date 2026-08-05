from __future__ import annotations

from dataclasses import dataclass

from heos_ui.energy import EnergySnapshot

from .engine import PolicyEngine


@dataclass(slots=True)
class SnapshotPolicyBridge:
    engine: PolicyEngine

    def evaluate(
        self,
        snapshot: EnergySnapshot,
    ):
        return self.engine.evaluate(
            {
                "surplus": snapshot.surplus_power,
                "battery_soc": snapshot.battery_soc,
                "ev_connected": snapshot.ev_connected,
                "grid_power": snapshot.grid_power,
            }
        )