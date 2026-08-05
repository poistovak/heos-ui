from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class InputEvent:
    """Generic input event."""

    event_type: str
    target: str


@dataclass(slots=True)
class InputDispatcher:
    """Dispatches input events to registered handlers."""

    _handlers: dict[
        str,
        list[Callable[[InputEvent], None]],
    ] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def register(
        self,
        event_type: str,
        handler: Callable[[InputEvent], None],
    ) -> None:
        self._handlers.setdefault(
            event_type,
            [],
        ).append(handler)

    def dispatch(
        self,
        event: InputEvent,
    ) -> int:
        handlers = self._handlers.get(
            event.event_type,
            [],
        )

        for handler in handlers:
            handler(event)

        return len(handlers)

    @property
    def registered_events(self) -> tuple[str, ...]:
        return tuple(sorted(self._handlers))