from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Decision:
    priority: int
    target: str
    action: str
    reason: str


@dataclass(slots=True)
class DecisionPlanner:
    _queue: list[Decision] = field(
        default_factory=list,
        init=False,
    )

    def add(self, decision: Decision) -> None:
        self._queue.append(decision)
        self._queue.sort(
            key=lambda item: item.priority,
            reverse=True,
        )

    def next(self) -> Decision | None:
        if not self._queue:
            return None

        return self._queue.pop(0)

    def peek(self) -> Decision | None:
        if not self._queue:
            return None

        return self._queue[0]

    @property
    def count(self) -> int:
        return len(self._queue)

    def clear(self) -> None:
        self._queue.clear()