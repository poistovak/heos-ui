from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_presenter import HEOSApplicationRunPresenter
from .heos_application_run_status import (
    HEOSApplicationRunStatusView,
    HEOSApplicationRunStatusWidget,
)
from .heos_application_run_summary import HEOSApplicationRunSummary


@dataclass(slots=True)
class HEOSApplicationRunStatusBinding:
    presenter: HEOSApplicationRunPresenter
    widget: HEOSApplicationRunStatusWidget

    def update(
        self,
        summary: HEOSApplicationRunSummary,
    ) -> HEOSApplicationRunStatusView:
        presentation = self.presenter.present(summary)

        return self.widget.update(presentation)

    @property
    def view(self) -> HEOSApplicationRunStatusView | None:
        return self.widget.view

    @property
    def has_data(self) -> bool:
        return self.widget.has_data

    def clear(self) -> None:
        self.widget.clear()
