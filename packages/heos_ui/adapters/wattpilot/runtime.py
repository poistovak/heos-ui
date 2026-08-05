from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision import Action
from heos_ui.events.bus import EventBus
from heos_ui.telemetry import TelemetryService


@dataclass(slots=True)
class WattpilotRuntimeAdapter:
    telemetry: TelemetryService
    event_bus: EventBus

    def execute(self, action: Action) -> bool:
        self.telemetry.record(
            "wattpilot.last_command",
            float(hash(action.command) & 0xFFFF),
        )

        self.event_bus.publish(
            "wattpilot.command",
            action,
        )

        return True