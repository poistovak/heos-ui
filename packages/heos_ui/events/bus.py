from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

EventHandler = Callable[[Any], None]


@dataclass(slots=True)
class EventBus:
    """Simple publish/subscribe event bus."""

    _handlers: dict[str, list[EventHandler]] = field(default_factory=dict)

    def subscribe(self, event: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event, []).append(handler)

    def publish(self, event: str, payload: Any = None) -> None:
        for handler in self._handlers.get(event, []):
            handler(payload)