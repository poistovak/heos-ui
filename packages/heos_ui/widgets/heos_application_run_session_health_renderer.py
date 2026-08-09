from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
)
from .heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionRenderField:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionRenderScene:
    title: str
    status: str
    severity: HEOSApplicationRunSessionSeverity
    fields: tuple[HEOSApplicationRunSessionRenderField, ...]

    @property
    def field_count(self) -> int:
        return len(self.fields)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionHealthRenderer:
    def render(
        self,
        view: HEOSApplicationRunSessionHealthView,
    ) -> HEOSApplicationRunSessionRenderScene:
        fields = (
            HEOSApplicationRunSessionRenderField(
                label="Detail",
                value=view.detail,
            ),
            HEOSApplicationRunSessionRenderField(
                label="Runs",
                value=view.runs,
            ),
            HEOSApplicationRunSessionRenderField(
                label="Cycles",
                value=view.cycles,
            ),
        )

        return HEOSApplicationRunSessionRenderScene(
            title=view.title,
            status=view.status,
            severity=view.severity,
            fields=fields,
        )
