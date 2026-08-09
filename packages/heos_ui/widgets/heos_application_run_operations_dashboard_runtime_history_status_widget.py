from __future__ import annotations

import importlib
from dataclasses import dataclass

presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)

StatusPresentation = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresentation
)
StatusSeverity = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView:
    title: str
    status: str
    detail: str
    cycles: str
    runs: str
    refreshes: str
    latest: str
    severity: StatusSeverity


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusWidget:
    _view: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView | None
    ) = None

    @property
    def view(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView | None:
        return self._view

    @property
    def has_view(self) -> bool:
        return self._view is not None

    def update(
        self,
        presentation: StatusPresentation,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView:
        view = HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView(
            title=presentation.title,
            status=presentation.status,
            detail=presentation.detail,
            cycles=presentation.cycles,
            runs=presentation.runs,
            refreshes=presentation.refreshes,
            latest=presentation.latest,
            severity=presentation.severity,
        )

        self._view = view
        return view

    def clear(self) -> None:
        self._view = None
