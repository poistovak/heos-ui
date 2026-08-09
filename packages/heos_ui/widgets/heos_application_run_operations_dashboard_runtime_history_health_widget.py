from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation,
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView:
    title: str
    status: str
    detail: str
    cycles: str
    frames: str
    latest: str
    severity: HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity

    @property
    def healthy(self) -> bool:
        return (
            self.severity
            is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
        )

    @property
    def warning(self) -> bool:
        return (
            self.severity
            is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
        )

    @property
    def neutral(self) -> bool:
        return (
            self.severity
            is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
        )


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget:
    _view: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView | None
    ) = None

    @property
    def view(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView | None:
        return self._view

    @property
    def has_data(self) -> bool:
        return self._view is not None

    def update(
        self,
        presentation: (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation
        ),
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView:
        view = HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView(
            title=presentation.title,
            status=presentation.status,
            detail=presentation.detail,
            cycles=presentation.cycles,
            frames=presentation.frames,
            latest=presentation.latest,
            severity=presentation.severity,
        )

        self._view = view
        return view

    def clear(self) -> None:
        self._view = None
