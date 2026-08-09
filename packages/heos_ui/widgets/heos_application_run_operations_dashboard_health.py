from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_dashboard_statistics import (
    HEOSApplicationRunOperationsDashboardStatistics,
)


class HEOSApplicationRunOperationsDashboardHealth(str, Enum):
    EMPTY = "empty"
    HEALTHY = "healthy"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardHealthSummary:
    health: HEOSApplicationRunOperationsDashboardHealth
    headline: str
    total_refreshes: int
    idle_refreshes: int
    healthy_refreshes: int
    degraded_refreshes: int
    rendered_frames: int
    latest_sequence: int | None

    @property
    def empty(self) -> bool:
        return (
            self.health
            is HEOSApplicationRunOperationsDashboardHealth.EMPTY
        )

    @property
    def healthy(self) -> bool:
        return (
            self.health
            is HEOSApplicationRunOperationsDashboardHealth.HEALTHY
        )

    @property
    def degraded(self) -> bool:
        return (
            self.health
            is HEOSApplicationRunOperationsDashboardHealth.DEGRADED
        )

    @classmethod
    def from_statistics(
        cls,
        statistics: HEOSApplicationRunOperationsDashboardStatistics,
    ) -> HEOSApplicationRunOperationsDashboardHealthSummary:
        if statistics.empty:
            health = HEOSApplicationRunOperationsDashboardHealth.EMPTY
            headline = "No dashboard refreshes recorded."
        elif statistics.degraded_refreshes > 0:
            health = HEOSApplicationRunOperationsDashboardHealth.DEGRADED
            headline = (
                "Dashboard degraded with "
                f"{statistics.degraded_refreshes} degraded refreshes."
            )
        else:
            health = HEOSApplicationRunOperationsDashboardHealth.HEALTHY
            headline = (
                "Dashboard healthy across "
                f"{statistics.total_refreshes} refreshes."
            )

        return cls(
            health=health,
            headline=headline,
            total_refreshes=statistics.total_refreshes,
            idle_refreshes=statistics.idle_refreshes,
            healthy_refreshes=statistics.healthy_refreshes,
            degraded_refreshes=statistics.degraded_refreshes,
            rendered_frames=statistics.rendered_frames,
            latest_sequence=statistics.latest_sequence,
        )
