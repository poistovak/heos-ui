from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_dashboard_runtime_history_statistics import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics,
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth(Enum):
    EMPTY = "empty"
    HEALTHY = "healthy"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary:
    health: HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth
    total_cycles: int
    healthy_cycles: int
    degraded_cycles: int
    idle_cycles: int
    rendered_frames: int
    latest_cycle: int | None

    @property
    def empty(self) -> bool:
        return (
            self.health
            is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
        )

    @property
    def healthy(self) -> bool:
        return (
            self.health
            is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.HEALTHY
        )

    @property
    def degraded(self) -> bool:
        return (
            self.health
            is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
        )

    @classmethod
    def from_statistics(
        cls,
        statistics: HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary:
        if statistics.empty:
            health = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
            )
        elif statistics.degraded_cycles > 0:
            health = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
            )
        else:
            health = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.HEALTHY
            )

        return cls(
            health=health,
            total_cycles=statistics.total_cycles,
            healthy_cycles=statistics.healthy_cycles,
            degraded_cycles=statistics.degraded_cycles,
            idle_cycles=statistics.idle_cycles,
            rendered_frames=statistics.rendered_frames,
            latest_cycle=statistics.latest_cycle,
        )
