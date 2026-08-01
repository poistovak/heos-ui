from __future__ import annotations

from .events import RenderEvent, RenderEvents
from .loop import RenderLoop


class RenderDispatcher:
    """Dispatches render frames."""

    def __init__(
        self,
        loop: RenderLoop,
        events: RenderEvents,
    ) -> None:
        self._loop = loop
        self._events = events

    def dispatch(self) -> RenderEvent:
        rendered = self._loop.tick()

        event = RenderEvent(
            frame=self._loop.frame,
            rendered=rendered,
        )

        self._events.emit(event)

        return event