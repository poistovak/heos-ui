from __future__ import annotations

from dataclasses import dataclass

from heos_ui.binding.brain_status import BrainStatusBinding
from heos_ui.events.bus import EventBus
from heos_ui.layout import Rect
from heos_ui.scene.canvas import CanvasBackend

from .brain_canvas_renderer import BrainCanvasRenderer
from .brain_frame_controller import BrainFrameController
from .brain_frame_pipeline import BrainFramePipeline
from .brain_live_renderer import BrainLiveRenderer
from .brain_presenter import BrainStatusPresenter
from .brain_renderer import BrainStatusRenderer
from .brain_runtime_controller import BrainRuntimeController
from .brain_scene_adapter import BrainSceneAdapter, BrainSceneLayout
from .brain_status import BrainStatusWidget


@dataclass(frozen=True, slots=True)
class BrainRuntimeFactory:
    @staticmethod
    def default_layout() -> BrainSceneLayout:
        return BrainSceneLayout(
            bounds=Rect(0, 0, 300, 200),
            title=Rect(16, 16, 268, 24),
            status=Rect(16, 48, 120, 24),
            health=Rect(148, 48, 136, 24),
            cycle=Rect(16, 88, 268, 20),
            execution=Rect(16, 120, 268, 20),
            targets=Rect(16, 152, 268, 20),
        )

    @classmethod
    def create(
        cls,
        *,
        canvas: CanvasBackend | None = None,
        layout: BrainSceneLayout | None = None,
        widget_id: str = "brain-status",
        title: str = "HEOS Brain",
    ) -> BrainRuntimeController:
        event_bus = EventBus()
        widget = BrainStatusWidget(
            id=widget_id,
            title=title,
        )

        binding = BrainStatusBinding(
            event_bus=event_bus,
            widget=widget,
        )

        backend = canvas or CanvasBackend()

        live_renderer = BrainLiveRenderer(
            presenter=BrainStatusPresenter(),
            pipeline=BrainFramePipeline(
                renderer=BrainStatusRenderer(),
                adapter=BrainSceneAdapter(),
                canvas_renderer=BrainCanvasRenderer(
                    canvas=backend,
                ),
            ),
        )

        frame_controller = BrainFrameController(
            widget=widget,
            renderer=live_renderer,
            layout=layout or cls.default_layout(),
        )

        return BrainRuntimeController(
            event_bus=event_bus,
            binding=binding,
            frame_controller=frame_controller,
        )
