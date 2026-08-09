from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_report import HEOSApplicationRunReport
from .heos_application_run_status import HEOSApplicationRunStatusView
from .heos_application_run_status_binding import (
    HEOSApplicationRunStatusBinding,
)
from .heos_application_run_summary import HEOSApplicationRunSummary


@dataclass(slots=True)
class HEOSApplicationRunStatusController:
    binding: HEOSApplicationRunStatusBinding
    _last_summary: HEOSApplicationRunSummary | None = None

    @property
    def has_data(self) -> bool:
        return self.binding.has_data

    @property
    def view(self) -> HEOSApplicationRunStatusView | None:
        return self.binding.view

    @property
    def last_summary(self) -> HEOSApplicationRunSummary | None:
        return self._last_summary

    def update(
        self,
        report: HEOSApplicationRunReport,
    ) -> HEOSApplicationRunStatusView:
        summary = HEOSApplicationRunSummary.from_report(report)
        self._last_summary = summary

        return self.binding.update(summary)

    def clear(self) -> None:
        self._last_summary = None
        self.binding.clear()
