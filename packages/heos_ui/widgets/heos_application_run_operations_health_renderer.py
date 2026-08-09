from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
)
from .heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsRenderField:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsRenderScene:
    title: str
    status: str
    severity: HEOSApplicationRunOperationsSeverity
    fields: tuple[HEOSApplicationRunOperationsRenderField, ...]

    @property
    def field_count(self) -> int:
        return len(self.fields)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsHealthRenderer:
    def render(
        self,
        view: HEOSApplicationRunOperationsHealthView,
    ) -> HEOSApplicationRunOperationsRenderScene:
        fields = (
            HEOSApplicationRunOperationsRenderField(
                label="Detail",
                value=view.detail,
            ),
            HEOSApplicationRunOperationsRenderField(
                label="Updates",
                value=view.updates,
            ),
            HEOSApplicationRunOperationsRenderField(
                label="Frames",
                value=view.frames,
            ),
        )

        return HEOSApplicationRunOperationsRenderScene(
            title=view.title,
            status=view.status,
            severity=view.severity,
            fields=fields,
        )
