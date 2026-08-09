from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_session_statistics import (
    HEOSApplicationRunOperationsSessionStatistics,
)


class HEOSApplicationRunOperationsHealth(str, Enum):
    EMPTY = "empty"
    HEALTHY = "healthy"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsHealthSummary:
    health: HEOSApplicationRunOperationsHealth
    headline: str
    total_updates: int
    idle_updates: int
    healthy_updates: int
    degraded_updates: int
    rendered_frames: int
    latest_sequence: int | None

    @property
    def empty(self) -> bool:
        return self.health is HEOSApplicationRunOperationsHealth.EMPTY

    @property
    def healthy(self) -> bool:
        return self.health is HEOSApplicationRunOperationsHealth.HEALTHY

    @property
    def degraded(self) -> bool:
        return self.health is HEOSApplicationRunOperationsHealth.DEGRADED

    @classmethod
    def from_statistics(
        cls,
        statistics: HEOSApplicationRunOperationsSessionStatistics,
    ) -> HEOSApplicationRunOperationsHealthSummary:
        if statistics.empty:
            health = HEOSApplicationRunOperationsHealth.EMPTY
            headline = "No operations updates recorded."
        elif statistics.degraded_updates > 0:
            health = HEOSApplicationRunOperationsHealth.DEGRADED
            headline = (
                "Operations degraded with "
                f"{statistics.degraded_updates} degraded updates."
            )
        else:
            health = HEOSApplicationRunOperationsHealth.HEALTHY
            headline = (
                "Operations healthy across "
                f"{statistics.total_updates} updates."
            )

        return cls(
            health=health,
            headline=headline,
            total_updates=statistics.total_updates,
            idle_updates=statistics.idle_updates,
            healthy_updates=statistics.healthy_updates,
            degraded_updates=statistics.degraded_updates,
            rendered_frames=statistics.rendered_frames,
            latest_sequence=statistics.latest_sequence,
        )
