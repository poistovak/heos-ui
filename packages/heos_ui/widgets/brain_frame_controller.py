from __future__ import annotations

from dataclasses import dataclass

from heos_ui.scene.paint import PaintCommand

from .brain_live_renderer import BrainLiveRenderer
from .brain_scene_adapter import BrainSceneLayout
from .brain_status import BrainStatusWidget


@dataclass(slots=True)
class BrainFrameController:
    widget: BrainStatusWidget
    renderer: BrainLiveRenderer
    layout: BrainSceneLayout

    def render(self) -> tuple[PaintCommand, ...]:
        return self.renderer.render(
            self.widget,
            self.layout,
        )

    @property
    def has_data(self) -> bool:
        return self.widget.has_data

    @property
    def status(self) -> str:
        return self.widget.status

    @property
    def cycle(self) -> int | None:
        return self.widget.cycle
