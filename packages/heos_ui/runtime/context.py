from __future__ import annotations

from dataclasses import dataclass

from .clock import FrameClock
from .diagnostics import RenderDiagnostics
from .lifecycle import RenderLifecycle


@dataclass(frozen=True, slots=True)
class RenderContext:
    """Immutable render context for a single frame."""

    clock: FrameClock
    lifecycle: RenderLifecycle
    diagnostics: RenderDiagnostics

    @property
    def frame(self) -> int:
        return self.clock.frame

    @property
    def active(self) -> bool:
        return self.lifecycle.active