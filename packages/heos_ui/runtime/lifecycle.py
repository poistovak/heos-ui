from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RenderLifecycle:
    """Tracks render frame lifecycle."""

    frame: int = 0
    active: bool = False

    def begin(self) -> int:
        if self.active:
            raise RuntimeError("Render frame already active.")

        self.frame += 1
        self.active = True
        return self.frame

    def end(self) -> None:
        if not self.active:
            raise RuntimeError("No active render frame.")

        self.active = False

    def reset(self) -> None:
        self.frame = 0
        self.active = False