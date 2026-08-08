from __future__ import annotations

from dataclasses import dataclass

from heos_ui.layout import Rect
from heos_ui.scene.paint import PaintCommand, PaintList

from .brain_renderer import BrainRenderScene


@dataclass(frozen=True, slots=True)
class BrainSceneLayout:
    bounds: Rect
    title: Rect
    status: Rect
    health: Rect
    cycle: Rect
    execution: Rect
    targets: Rect


@dataclass(slots=True)
class BrainSceneAdapter:
    def adapt(
        self,
        scene: BrainRenderScene,
        layout: BrainSceneLayout,
    ) -> PaintList:
        paint = PaintList()

        paint.add(
            PaintCommand(
                command="rect",
                rect=layout.bounds,
            )
        )
        paint.add(
            PaintCommand(
                command="text",
                rect=layout.title,
            )
        )
        paint.add(
            PaintCommand(
                command="text",
                rect=layout.status,
            )
        )
        paint.add(
            PaintCommand(
                command="text",
                rect=layout.health,
            )
        )
        paint.add(
            PaintCommand(
                command="text",
                rect=layout.cycle,
            )
        )
        paint.add(
            PaintCommand(
                command="text",
                rect=layout.execution,
            )
        )
        paint.add(
            PaintCommand(
                command="text",
                rect=layout.targets,
            )
        )

        return paint