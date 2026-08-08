from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.runtime.scheduler_core import Scheduler

from .recovery import RecoveryPolicy, RecoveryState


@dataclass(slots=True)
class RecoveryScheduler:
    recovery: RecoveryPolicy
    scheduler: Scheduler
    probe_delay: float = 30.0
    _scheduled: set[str] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.probe_delay <= 0.0:
            raise ValueError(
                "probe_delay must be greater than zero."
            )

    def schedule_probe(
        self,
        target: str,
    ) -> bool:
        if target in self._scheduled:
            return False

        if (
            self.recovery.state(target)
            is not RecoveryState.BACKOFF
        ):
            return False

        self._scheduled.add(target)

        def begin_probe() -> None:
            try:
                if (
                    self.recovery.state(target)
                    is RecoveryState.BACKOFF
                ):
                    self.recovery.begin_probe(target)
            finally:
                self._scheduled.discard(target)

        self.scheduler.every(
            self.probe_delay,
            begin_probe,
        )

        return True

    def is_scheduled(
        self,
        target: str,
    ) -> bool:
        return target in self._scheduled

    @property
    def scheduled_count(self) -> int:
        return len(self._scheduled)