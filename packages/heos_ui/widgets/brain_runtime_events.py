from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.events.bus import EventBus
from heos_ui.scene.paint import PaintCommand

from .brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)


class BrainRuntimeEventType(str, Enum):
    STARTED = "started"
    SNAPSHOT_PUBLISHED = "snapshot_published"
    FRAME_RENDERED = "frame_rendered"
    STOPPED = "stopped"


@dataclass(frozen=True, slots=True)
class BrainRuntimeEvent:
    event_type: BrainRuntimeEventType
    state: BrainRuntimeLifecycleState
    cycle: int | None


@dataclass(slots=True)
class BrainRuntimeEvents:
    runtime: BrainRuntimeLifecycle
    event_bus: EventBus
    topic: str = "brain.runtime"

    def _emit(
        self,
        event_type: BrainRuntimeEventType,
    ) -> BrainRuntimeEvent:
        event = BrainRuntimeEvent(
            event_type=event_type,
            state=self.runtime.state,
            cycle=self.runtime.session.cycle,
        )

        self.event_bus.publish(
            self.topic,
            event,
        )

        return event

    def start(self) -> BrainRuntimeEvent:
        self.runtime.start()

        return self._emit(
            BrainRuntimeEventType.STARTED,
        )

    def publish(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainRuntimeEvent:
        self.runtime.publish(snapshot)

        return self._emit(
            BrainRuntimeEventType.SNAPSHOT_PUBLISHED,
        )

    def render(
        self,
    ) -> tuple[
        tuple[PaintCommand, ...],
        BrainRuntimeEvent,
    ]:
        frame = self.runtime.render()

        event = self._emit(
            BrainRuntimeEventType.FRAME_RENDERED,
        )

        return frame, event

    def stop(self) -> BrainRuntimeEvent:
        self.runtime.stop()

        return self._emit(
            BrainRuntimeEventType.STOPPED,
        )
