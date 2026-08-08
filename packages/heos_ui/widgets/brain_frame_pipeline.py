from __future__ import annotations

from dataclasses import dataclass

from heos_ui.scene.paint import PaintCommand

from .brain_canvas_renderer import BrainCanvasRenderer
from .brain_presenter import BrainStatusPresentation
from .brain_renderer import BrainStatusRenderer
from .brain_scene_adapter import BrainSceneAdapter, BrainSceneLayout


@dataclass(slots=True)
class BrainFramePipeline:
    renderer: BrainStatusRenderer
    adapter: BrainSceneAdapter
    canvas_renderer: BrainCanvasRenderer

    def render(
        self,
        presentation: BrainStatusPresentation,
        layout: BrainSceneLayout,
    ) -> tuple[PaintCommand, ...]:
        scene = self.renderer.render(presentation)
        paint = self.adapter.adapt(scene, layout)

        return self.canvas_renderer.render(paint)
