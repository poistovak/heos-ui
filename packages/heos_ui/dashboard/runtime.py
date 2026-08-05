from __future__ import annotations

from dataclasses import dataclass

from heos_ui.overlay import OverlayManager
from heos_ui.scene import SceneGraph
from heos_ui.window import WindowManager

from .layout import DashboardLayout


@dataclass(slots=True)
class DashboardRuntime:
    """Runtime for the HEOS dashboard."""

    layout: DashboardLayout
    window: WindowManager

    @classmethod
    def create(
        cls,
        layout: DashboardLayout,
        scene: SceneGraph,
    ) -> "DashboardRuntime":
        return cls(
            layout=layout,
            window=WindowManager(
                scene=scene,
                overlays=OverlayManager(),
            ),
        )

    def start(self) -> None:
        self.window.start()

    def stop(self) -> None:
        self.window.stop()

    @property
    def running(self) -> bool:
        return self.window.running