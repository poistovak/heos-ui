from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Action:
    priority: int
    target: str
    command: str
    parameters: dict[str, Any] = field(
        default_factory=dict,
    )


@dataclass(slots=True)
class ActionQueue:
    _queue: list[Action] = field(
        default_factory=list,
        init=False,
    )

    def enqueue(
        self,
        action: Action,
    ) -> None:
        self._queue.append(action)
        self._queue.sort(
            key=lambda item: item.priority,
            reverse=True,
        )

    def dequeue(self) -> Action | None:
        if not self._queue:
            return None

        return self._queue.pop(0)

    def peek(self) -> Action | None:
        if not self._queue:
            return None

        return self._queue[0]

    @property
    def count(self) -> int:
        return len(self._queue)

    def clear(self) -> None:
        self._queue.clear()