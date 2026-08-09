from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_dashboard_health import (
    HEOSApplicationRunOperationsDashboardHealth,
    HEOSApplicationRunOperationsDashboardHealthSummary,
)


class HEOSApplicationRunOperationsDashboardSeverity(str, Enum):
    NEUTRAL = "neutral"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardPresentation:
    title: str
    status: str
    detail: str
    refreshes: str
    frames: str
    sequence: str
    severity: HEOSApplicationRunOperationsDashboardSeverity


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardHealthPresenter:
    title: str = "HEOS Operations Dashboard"

    def present(
        self,
        summary: HEOSApplicationRunOperationsDashboardHealthSummary,
    ) -> HEOSApplicationRunOperationsDashboardPresentation:
        if (
            summary.health
            is HEOSApplicationRunOperationsDashboardHealth.EMPTY
        ):
            status = "IDLE"
            detail = "No dashboard refreshes recorded."
            refreshes = "Refreshes —"
            frames = "Frames —"
            sequence = "Sequence —"
            severity = (
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            )

        elif (
            summary.health
            is HEOSApplicationRunOperationsDashboardHealth.HEALTHY
        ):
            status = "HEALTHY"
            detail = (
                f"Healthy {summary.healthy_refreshes}, "
                f"idle {summary.idle_refreshes}."
            )
            refreshes = f"Refreshes {summary.total_refreshes}"
            frames = f"Frames {summary.rendered_frames}"
            sequence = f"Sequence {summary.latest_sequence}"
            severity = (
                HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
            )

        else:
            status = "DEGRADED"
            detail = (
                f"Degraded {summary.degraded_refreshes}, "
                f"healthy {summary.healthy_refreshes}."
            )
            refreshes = f"Refreshes {summary.total_refreshes}"
            frames = f"Frames {summary.rendered_frames}"
            sequence = f"Sequence {summary.latest_sequence}"
            severity = (
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            )

        return HEOSApplicationRunOperationsDashboardPresentation(
            title=self.title,
            status=status,
            detail=detail,
            refreshes=refreshes,
            frames=frames,
            sequence=sequence,
            severity=severity,
        )
