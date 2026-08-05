from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    payload: Any = None


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[
            str,
            list[Callable[[Any], None]],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        handler: Callable[[Any], None],
    ) -> None:
        self._handlers[event_name].append(handler)

    def publish(
        self,
        event: Event | str,
        payload: Any = None,
    ) -> None:
        if isinstance(event, Event):
            event_name = event.name
            value = event.payload
        else:
            event_name = event
            value = payload

        for handler in tuple(self._handlers.get(event_name, ())):
            handler(value)

    def subscriber_count(
        self,
        event_name: str,
    ) -> int:
        return len(self._handlers.get(event_name, ()))

    def clear(self) -> None:
        self._handlers.clear()