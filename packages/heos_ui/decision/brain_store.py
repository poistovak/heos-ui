from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.events.bus import EventBus

from .brain_snapshot import BrainRuntimeSnapshot


@dataclass(slots=True)
class BrainSnapshotStore:
    event_bus: EventBus
    topic: str = "brain.snapshot"
    _latest: BrainRuntimeSnapshot | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        self.event_bus.subscribe(
            self.topic,
            self.update,
        )

    def update(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> None:
        self._latest = snapshot

    @property
    def has_snapshot(self) -> bool:
        return self._latest is not None

    def latest(self) -> BrainRuntimeSnapshot | None:
        return self._latest

    def clear(self) -> None:
        self._latest = None