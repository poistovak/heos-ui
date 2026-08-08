from __future__ import annotations

from dataclasses import dataclass

from heos_ui.scene.paint import PaintCommand

from .brain_frame_pipeline import BrainFramePipeline
from .brain_presenter import BrainStatusPresenter
from .brain_scene_adapter import BrainSceneLayout
from .brain_status import BrainStatusWidget


@dataclass(slots=True)
class BrainLiveRenderer:
    presenter: BrainStatusPresenter
    pipeline: BrainFramePipeline

    def render(
        self,
        widget: BrainStatusWidget,
        layout: BrainSceneLayout,
    ) -> tuple[PaintCommand, ...]:
        presentation = self.presenter.present(widget)

        return self.pipeline.render(
            presentation,
            layout,
        )
