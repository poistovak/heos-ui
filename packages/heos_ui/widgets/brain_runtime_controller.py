from __future__ import annotations

from dataclasses import dataclass

from heos_ui.binding.brain_status import BrainStatusBinding
from heos_ui.events.bus import EventBus
from heos_ui.scene.paint import PaintCommand
from heos_ui.widgets.brain_frame_controller import BrainFrameController


@dataclass(slots=True)
class BrainRuntimeController:
    event_bus: EventBus
    binding: BrainStatusBinding
    frame_controller: BrainFrameController

    @property
    def has_data(self) -> bool:
        return self.frame_controller.has_data

    @property
    def status(self) -> str:
        return self.frame_controller.status

    @property
    def cycle(self) -> int | None:
        return self.frame_controller.cycle

    def render(self) -> tuple[PaintCommand, ...]:
        return self.frame_controller.render()
