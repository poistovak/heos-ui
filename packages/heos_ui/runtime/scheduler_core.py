from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True)
class ScheduledTask:
    interval: float
    callback: Callable[[], None]
    elapsed: float = 0.0


@dataclass(slots=True)
class Scheduler:
    _tasks: list[ScheduledTask] = field(
        default_factory=list,
        init=False,
    )

    def every(
        self,
        interval: float,
        callback: Callable[[], None],
    ) -> None:
        self._tasks.append(
            ScheduledTask(interval, callback)
        )

    def tick(
        self,
        delta: float,
    ) -> None:
        for task in self._tasks:
            task.elapsed += delta

            if task.elapsed >= task.interval:
                task.elapsed = 0.0
                task.callback()

    @property
    def task_count(self) -> int:
        return len(self._tasks)

    def clear(self) -> None:
        self._tasks.clear()