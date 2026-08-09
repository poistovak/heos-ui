from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .heos_application_run_report import HEOSApplicationRunReport


class HEOSApplicationRunStatus(str, Enum):
    EMPTY = "empty"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSummary:
    status: HEOSApplicationRunStatus
    headline: str
    processed: int
    rendered: int
    skipped: int
    first_cycle: int | None
    last_cycle: int | None

    @property
    def successful(self) -> bool:
        return self.status is HEOSApplicationRunStatus.COMPLETED

    @property
    def has_cycles(self) -> bool:
        return self.processed > 0

    @property
    def cycle_range(self) -> tuple[int, int] | None:
        if self.first_cycle is None or self.last_cycle is None:
            return None

        return self.first_cycle, self.last_cycle

    @classmethod
    def from_report(
        cls,
        report: HEOSApplicationRunReport,
    ) -> HEOSApplicationRunSummary:
        if report.empty:
            status = HEOSApplicationRunStatus.EMPTY
            headline = "No application cycles were processed."
        elif report.interrupted:
            status = HEOSApplicationRunStatus.INTERRUPTED
            headline = (
                f"Application run interrupted after "
                f"{report.processed} cycles."
            )
        else:
            status = HEOSApplicationRunStatus.COMPLETED
            headline = (
                f"Application run completed with "
                f"{report.processed} cycles."
            )

        return cls(
            status=status,
            headline=headline,
            processed=report.processed,
            rendered=report.rendered,
            skipped=report.skipped,
            first_cycle=report.first_cycle,
            last_cycle=report.last_cycle,
        )
