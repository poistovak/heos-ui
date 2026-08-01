from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RenderEvent:
    """Render loop event."""

    frame: int
    rendered: int


class RenderEvents:
    """Simple render event dispatcher."""

    def __init__(self) -> None:
        self._listeners: list[Callable[[RenderEvent], None]] = []

    def subscribe(
        self,
        listener: Callable[[RenderEvent], None],
    ) -> None:
        self._listeners.append(listener)

    def emit(self, event: RenderEvent) -> None:
        for listener in tuple(self._listeners):
            listener(event)