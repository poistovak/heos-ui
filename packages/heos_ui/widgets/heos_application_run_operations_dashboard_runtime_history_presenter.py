from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_dashboard_runtime_history_health import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth,
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary,
)


class HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity(Enum):
    NEUTRAL = "neutral"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation:
    title: str
    status: str
    detail: str
    cycles: str
    frames: str
    latest: str
    severity: HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter:
    title: str = "HEOS Operations Dashboard Runtime History"

    def present(
        self,
        summary: HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation:
        if (
            summary.health
            is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.EMPTY
        ):
            status = "EMPTY"
            detail = "No runtime history recorded."
            severity = (
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
            )
        elif (
            summary.health
            is HEOSApplicationRunOperationsDashboardRuntimeHistoryHealth.DEGRADED
        ):
            status = "DEGRADED"
            detail = (
                f"Degraded {summary.degraded_cycles}, "
                f"healthy {summary.healthy_cycles}, "
                f"idle {summary.idle_cycles}."
            )
            severity = (
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            )
        else:
            status = "HEALTHY"
            detail = (
                f"Healthy {summary.healthy_cycles}, "
                f"idle {summary.idle_cycles}."
            )
            severity = (
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
            )

        latest = (
            f"Latest cycle {summary.latest_cycle}"
            if summary.latest_cycle is not None
            else "Latest cycle —"
        )

        return HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation(
            title=self.title,
            status=status,
            detail=detail,
            cycles=f"Cycles {summary.total_cycles}",
            frames=f"Frames {summary.rendered_frames}",
            latest=latest,
            severity=severity,
        )
