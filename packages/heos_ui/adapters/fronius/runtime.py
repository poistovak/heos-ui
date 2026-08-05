from __future__ import annotations

from dataclasses import dataclass

from heos_ui.energy import EnergyGraph
from heos_ui.events.bus import EventBus
from heos_ui.telemetry import TelemetryService

from .client import FroniusSnapshot


@dataclass(slots=True)
class FroniusRuntimeAdapter:
    telemetry: TelemetryService
    event_bus: EventBus
    graph: EnergyGraph

    def update(
        self,
        snapshot: FroniusSnapshot,
    ) -> None:
        self.telemetry.record(
            "fronius.pv_power",
            snapshot.pv_power,
        )

        self.telemetry.record(
            "fronius.grid_power",
            snapshot.grid_power,
        )

        self.event_bus.publish(
            "fronius.updated",
            snapshot,
        )