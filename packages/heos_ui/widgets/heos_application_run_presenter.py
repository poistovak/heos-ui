from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_summary import (
    HEOSApplicationRunStatus,
    HEOSApplicationRunSummary,
)


class HEOSApplicationRunSeverity(str, Enum):
    NEUTRAL = "neutral"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunPresentation:
    title: str
    status: str
    detail: str
    cycles: str
    severity: HEOSApplicationRunSeverity


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunPresenter:
    title: str = "HEOS Application"

    def present(
        self,
        summary: HEOSApplicationRunSummary,
    ) -> HEOSApplicationRunPresentation:
        if summary.status is HEOSApplicationRunStatus.EMPTY:
            status = "IDLE"
            detail = "No cycles processed."
            cycles = "Cycles —"
            severity = HEOSApplicationRunSeverity.NEUTRAL

        elif summary.status is HEOSApplicationRunStatus.COMPLETED:
            status = "COMPLETED"
            detail = (
                f"Processed {summary.processed}, "
                f"rendered {summary.rendered}."
            )
            cycles = self._cycles(summary)
            severity = HEOSApplicationRunSeverity.SUCCESS

        else:
            status = "INTERRUPTED"
            detail = (
                f"Processed {summary.processed}, "
                f"skipped {summary.skipped}."
            )
            cycles = self._cycles(summary)
            severity = HEOSApplicationRunSeverity.WARNING

        return HEOSApplicationRunPresentation(
            title=self.title,
            status=status,
            detail=detail,
            cycles=cycles,
            severity=severity,
        )

    @staticmethod
    def _cycles(
        summary: HEOSApplicationRunSummary,
    ) -> str:
        cycle_range = summary.cycle_range

        if cycle_range is None:
            return "Cycles —"

        first, last = cycle_range

        if first == last:
            return f"Cycle {first}"

        return f"Cycles {first}–{last}"
