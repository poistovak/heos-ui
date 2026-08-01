from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FrameResult:
    """Result of one completed render frame."""

    frame_number: int
    pending_widgets: int
    rendered_widgets: int
