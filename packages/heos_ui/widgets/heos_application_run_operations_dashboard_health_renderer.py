from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
)
from .heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRenderField:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRenderScene:
    title: str
    status: str
    severity: HEOSApplicationRunOperationsDashboardSeverity
    fields: tuple[
        HEOSApplicationRunOperationsDashboardRenderField,
        ...,
    ]

    @property
    def field_count(self) -> int:
        return len(self.fields)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardHealthRenderer:
    def render(
        self,
        view: HEOSApplicationRunOperationsDashboardHealthView,
    ) -> HEOSApplicationRunOperationsDashboardRenderScene:
        fields = (
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Detail",
                value=view.detail,
            ),
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Refreshes",
                value=view.refreshes,
            ),
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Frames",
                value=view.frames,
            ),
            HEOSApplicationRunOperationsDashboardRenderField(
                label="Sequence",
                value=view.sequence,
            ),
        )

        return HEOSApplicationRunOperationsDashboardRenderScene(
            title=view.title,
            status=view.status,
            severity=view.severity,
            fields=fields,
        )
