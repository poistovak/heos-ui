from __future__ import annotations

from dataclasses import dataclass

from heos_ui.energy import EnergyGraph
from heos_ui.events.bus import EventBus
from heos_ui.logging import Logger
from heos_ui.telemetry import TelemetryService


@dataclass(slots=True)
class EnergyOrchestrator:
    graph: EnergyGraph
    telemetry: TelemetryService
    event_bus: EventBus
    logger: Logger

    def update(self) -> None:
        self.telemetry.record(
            "energy.nodes",
            float(len(self.graph.nodes)),
        )

        self.telemetry.record(
            "energy.flows",
            float(len(self.graph.flows)),
        )

        self.event_bus.publish(
            "energy.updated",
            self.graph,
        )

        self.logger.info(
            "Energy graph updated."
        )