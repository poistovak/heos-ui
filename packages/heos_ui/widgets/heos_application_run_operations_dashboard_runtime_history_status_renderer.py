from __future__ import annotations

import importlib
from dataclasses import dataclass

widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)

StatusView = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)
StatusSeverity = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderScene:
    title: str
    status: str
    severity: StatusSeverity
    fields: tuple[
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField,
        ...,
    ]

    @property
    def field_count(self) -> int:
        return len(self.fields)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderer:
    def render(
        self,
        view: StatusView,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderScene:
        fields = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField(
                label="Detail",
                value=view.detail,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField(
                label="Cycles",
                value=view.cycles,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField(
                label="Runs",
                value=view.runs,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField(
                label="Refreshes",
                value=view.refreshes,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderField(
                label="Latest",
                value=view.latest,
            ),
        )

        return (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRenderScene(
                title=view.title,
                status=view.status,
                severity=view.severity,
                fields=fields,
            )
        )
