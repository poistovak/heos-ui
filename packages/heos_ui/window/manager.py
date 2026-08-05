from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.overlay import OverlayManager
from heos_ui.scene import SceneGraph


@dataclass(slots=True)
class WindowManager:
    """Coordinates scene and overlays."""

    scene: SceneGraph
    overlays: OverlayManager

    _running: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    @property
    def running(self) -> bool:
        return self._running

    @property
    def overlay_count(self) -> int:
        return self.overlays.count

    @property
    def root(self):
        return self.scene.root