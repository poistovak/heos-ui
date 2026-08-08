from __future__ import annotations

from dataclasses import dataclass

from heos_ui.events.bus import EventBus

from .brain import BrainCycleReport
from .brain_snapshot import BrainRuntimeSnapshot


@dataclass(slots=True)
class BrainSnapshotPublisher:
    event_bus: EventBus
    topic: str = "brain.snapshot"

    def publish(
        self,
        report: BrainCycleReport,
    ) -> BrainRuntimeSnapshot:
        snapshot = BrainRuntimeSnapshot.from_report(report)

        self.event_bus.publish(
            self.topic,
            snapshot,
        )

        return snapshot