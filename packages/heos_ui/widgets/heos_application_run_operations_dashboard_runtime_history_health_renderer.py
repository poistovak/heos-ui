from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_runtime_history_health_widget import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView,
)
from .heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene:
    title: str
    status: str
    severity: HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity
    fields: tuple[
        HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField,
        ...,
    ]

    @property
    def field_count(self) -> int:
        return len(self.fields)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthRenderer:
    def render(
        self,
        view: HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene:
        fields = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField(
                label="Detail",
                value=view.detail,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField(
                label="Cycles",
                value=view.cycles,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField(
                label="Frames",
                value=view.frames,
            ),
            HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField(
                label="Latest",
                value=view.latest,
            ),
        )

        return HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene(
            title=view.title,
            status=view.status,
            severity=view.severity,
            fields=fields,
        )
