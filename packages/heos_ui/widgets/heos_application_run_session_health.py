from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_live_session_statistics import (
    HEOSApplicationRunLiveSessionStatistics,
)


class HEOSApplicationRunSessionHealth(str, Enum):
    EMPTY = "empty"
    HEALTHY = "healthy"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionHealthSummary:
    health: HEOSApplicationRunSessionHealth
    headline: str
    total_runs: int
    completed_runs: int
    interrupted_runs: int
    idle_runs: int
    processed: int
    rendered: int
    skipped: int
    latest_sequence: int | None

    @property
    def healthy(self) -> bool:
        return self.health is HEOSApplicationRunSessionHealth.HEALTHY

    @property
    def degraded(self) -> bool:
        return self.health is HEOSApplicationRunSessionHealth.DEGRADED

    @property
    def empty(self) -> bool:
        return self.health is HEOSApplicationRunSessionHealth.EMPTY

    @classmethod
    def from_statistics(
        cls,
        statistics: HEOSApplicationRunLiveSessionStatistics,
    ) -> HEOSApplicationRunSessionHealthSummary:
        if statistics.empty:
            health = HEOSApplicationRunSessionHealth.EMPTY
            headline = "No application runs recorded."
        elif statistics.interrupted_runs > 0:
            health = HEOSApplicationRunSessionHealth.DEGRADED
            headline = (
                f"Session degraded with "
                f"{statistics.interrupted_runs} interrupted runs."
            )
        else:
            health = HEOSApplicationRunSessionHealth.HEALTHY
            headline = (
                f"Session healthy across "
                f"{statistics.total_runs} runs."
            )

        return cls(
            health=health,
            headline=headline,
            total_runs=statistics.total_runs,
            completed_runs=statistics.completed_runs,
            interrupted_runs=statistics.interrupted_runs,
            idle_runs=statistics.idle_runs,
            processed=statistics.processed,
            rendered=statistics.rendered,
            skipped=statistics.skipped,
            latest_sequence=statistics.latest_sequence,
        )
