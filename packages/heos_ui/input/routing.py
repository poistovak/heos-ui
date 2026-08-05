from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .dispatcher import InputEvent


@dataclass(slots=True)
class EventRouter:
    """Routes events to widgets."""

    _routes: dict[
        str,
        Callable[[InputEvent], None],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def register(
        self,
        widget_id: str,
        handler: Callable[[InputEvent], None],
    ) -> None:
        self._routes[widget_id] = handler

    def unregister(
        self,
        widget_id: str,
    ) -> None:
        self._routes.pop(widget_id, None)

    def route(
        self,
        event: InputEvent,
    ) -> bool:
        handler = self._routes.get(event.target)

        if handler is None:
            return False

        handler(event)
        return True

    @property
    def registered_widgets(self) -> tuple[str, ...]:
        return tuple(sorted(self._routes))