from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.scene.paint import PaintCommand

from .brain_runtime_controller import BrainRuntimeController


@dataclass(slots=True)
class BrainRuntimeSession:
    runtime: BrainRuntimeController
    topic: str = "brain.snapshot"

    def publish(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> None:
        self.runtime.event_bus.publish(
            self.topic,
            snapshot,
        )

    def render(self) -> tuple[PaintCommand, ...]:
        return self.runtime.render()

    @property
    def has_data(self) -> bool:
        return self.runtime.has_data

    @property
    def status(self) -> str:
        return self.runtime.status

    @property
    def cycle(self) -> int | None:
        return self.runtime.cycle
