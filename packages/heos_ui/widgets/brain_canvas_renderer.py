from __future__ import annotations

from dataclasses import dataclass

from heos_ui.scene.canvas import CanvasBackend
from heos_ui.scene.paint import PaintCommand, PaintList


@dataclass(slots=True)
class BrainCanvasRenderer:
    canvas: CanvasBackend

    def render(
        self,
        paint: PaintList,
    ) -> tuple[PaintCommand, ...]:
        self.canvas.begin_frame()

        for command in paint:
            self.canvas.submit(command)

        return self.canvas.end_frame()
