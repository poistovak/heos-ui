from __future__ import annotations

from heos_ui.adapters import HomeAssistantSnapshot

from .client import WattpilotSnapshot


class WattpilotAdapter:

    def to_snapshot(
        self,
        snapshot: WattpilotSnapshot,
    ) -> HomeAssistantSnapshot:
        ...