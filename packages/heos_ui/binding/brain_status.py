from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_view import BrainViewModel
from heos_ui.events.bus import EventBus
from heos_ui.widgets.brain_status import BrainStatusWidget


@dataclass(slots=True)
class BrainStatusBinding:
    event_bus: EventBus
    widget: BrainStatusWidget
    topic: str = "brain.snapshot"

    def __post_init__(self) -> None:
        self.event_bus.subscribe(
            self.topic,
            self._on_snapshot,
        )

    def _on_snapshot(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> None:
        view = BrainViewModel.from_snapshot(snapshot)
        self.widget.update(view)