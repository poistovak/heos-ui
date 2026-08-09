from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_health import (
    HEOSApplicationRunOperationsHealth,
    HEOSApplicationRunOperationsHealthSummary,
)


class HEOSApplicationRunOperationsSeverity(str, Enum):
    NEUTRAL = "neutral"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsPresentation:
    title: str
    status: str
    detail: str
    updates: str
    frames: str
    severity: HEOSApplicationRunOperationsSeverity


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsHealthPresenter:
    title: str = "HEOS Operations"

    def present(
        self,
        summary: HEOSApplicationRunOperationsHealthSummary,
    ) -> HEOSApplicationRunOperationsPresentation:
        if summary.health is HEOSApplicationRunOperationsHealth.EMPTY:
            status = "IDLE"
            detail = "No operations updates recorded."
            updates = "Updates —"
            frames = "Frames —"
            severity = HEOSApplicationRunOperationsSeverity.NEUTRAL

        elif summary.health is HEOSApplicationRunOperationsHealth.HEALTHY:
            status = "HEALTHY"
            detail = (
                f"Healthy {summary.healthy_updates}, "
                f"idle {summary.idle_updates}."
            )
            updates = f"Updates {summary.total_updates}"
            frames = f"Frames {summary.rendered_frames}"
            severity = HEOSApplicationRunOperationsSeverity.SUCCESS

        else:
            status = "DEGRADED"
            detail = (
                f"Degraded {summary.degraded_updates}, "
                f"healthy {summary.healthy_updates}."
            )
            updates = f"Updates {summary.total_updates}"
            frames = f"Frames {summary.rendered_frames}"
            severity = HEOSApplicationRunOperationsSeverity.WARNING

        return HEOSApplicationRunOperationsPresentation(
            title=self.title,
            status=status,
            detail=detail,
            updates=updates,
            frames=frames,
            severity=severity,
        )
