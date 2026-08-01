from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import RenderDiagnostics
from .lifecycle import RenderLifecycle


@dataclass(frozen=True, slots=True)
class RuntimeSnapshot:
    """Complete runtime state."""

    diagnostics: RenderDiagnostics
    lifecycle: RenderLifecycle

    @property
    def frame(self) -> int:
        return self.lifecycle.frame

    @property
    def active(self) -> bool:
        return self.lifecycle.active

    @property
    def rendered_frames(self) -> int:
        return self.diagnostics.rendered_frames

    @property
    def total_widgets(self) -> int:
        return self.diagnostics.total_widgets