from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardPresentation,
    HEOSApplicationRunOperationsDashboardSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardHealthView:
    title: str
    status: str
    detail: str
    refreshes: str
    frames: str
    sequence: str
    severity: HEOSApplicationRunOperationsDashboardSeverity

    @property
    def healthy(self) -> bool:
        return (
            self.severity
            is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
        )

    @property
    def warning(self) -> bool:
        return (
            self.severity
            is HEOSApplicationRunOperationsDashboardSeverity.WARNING
        )

    @property
    def neutral(self) -> bool:
        return (
            self.severity
            is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
        )


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardHealthWidget:
    _view: HEOSApplicationRunOperationsDashboardHealthView | None = None

    @property
    def view(
        self,
    ) -> HEOSApplicationRunOperationsDashboardHealthView | None:
        return self._view

    @property
    def has_data(self) -> bool:
        return self._view is not None

    def update(
        self,
        presentation: HEOSApplicationRunOperationsDashboardPresentation,
    ) -> HEOSApplicationRunOperationsDashboardHealthView:
        view = HEOSApplicationRunOperationsDashboardHealthView(
            title=presentation.title,
            status=presentation.status,
            detail=presentation.detail,
            refreshes=presentation.refreshes,
            frames=presentation.frames,
            sequence=presentation.sequence,
            severity=presentation.severity,
        )

        self._view = view
        return view

    def clear(self) -> None:
        self._view = None
