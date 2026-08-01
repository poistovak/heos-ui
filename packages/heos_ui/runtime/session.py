from __future__ import annotations

from dataclasses import dataclass

from .context import RenderContext


@dataclass(slots=True)
class RenderSession:
    """Represents one render runtime session."""

    context: RenderContext
    frames_rendered: int = 0

    def begin_frame(self) -> None:
        """Record the start of a render frame."""

        self.frames_rendered += 1

    @property
    def current_frame(self) -> int:
        """Return the current frame number."""

        return self.context.frame

    @property
    def active(self) -> bool:
        """Return whether rendering is active."""

        return self.context.active