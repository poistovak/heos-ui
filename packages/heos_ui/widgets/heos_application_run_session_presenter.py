from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_session_health import (
    HEOSApplicationRunSessionHealth,
    HEOSApplicationRunSessionHealthSummary,
)


class HEOSApplicationRunSessionSeverity(str, Enum):
    NEUTRAL = "neutral"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionPresentation:
    title: str
    status: str
    detail: str
    runs: str
    cycles: str
    severity: HEOSApplicationRunSessionSeverity


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionHealthPresenter:
    title: str = "HEOS Live Session"

    def present(
        self,
        summary: HEOSApplicationRunSessionHealthSummary,
    ) -> HEOSApplicationRunSessionPresentation:
        if summary.health is HEOSApplicationRunSessionHealth.EMPTY:
            status = "IDLE"
            detail = "No application runs recorded."
            runs = "Runs —"
            cycles = "Cycles —"
            severity = HEOSApplicationRunSessionSeverity.NEUTRAL

        elif summary.health is HEOSApplicationRunSessionHealth.HEALTHY:
            status = "HEALTHY"
            detail = (
                f"Completed {summary.completed_runs}, "
                f"interrupted {summary.interrupted_runs}."
            )
            runs = f"Runs {summary.total_runs}"
            cycles = (
                f"Processed {summary.processed}, "
                f"rendered {summary.rendered}."
            )
            severity = HEOSApplicationRunSessionSeverity.SUCCESS

        else:
            status = "DEGRADED"
            detail = (
                f"Interrupted {summary.interrupted_runs}, "
                f"skipped {summary.skipped}."
            )
            runs = f"Runs {summary.total_runs}"
            cycles = (
                f"Processed {summary.processed}, "
                f"rendered {summary.rendered}."
            )
            severity = HEOSApplicationRunSessionSeverity.WARNING

        return HEOSApplicationRunSessionPresentation(
            title=self.title,
            status=status,
            detail=detail,
            runs=runs,
            cycles=cycles,
            severity=severity,
        )
