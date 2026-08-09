from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_presenter import HEOSApplicationRunSeverity
from .heos_application_run_status import HEOSApplicationRunStatusView


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunRenderField:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunRenderScene:
    title: str
    status: str
    severity: HEOSApplicationRunSeverity
    fields: tuple[HEOSApplicationRunRenderField, ...]

    @property
    def field_count(self) -> int:
        return len(self.fields)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunStatusRenderer:
    def render(
        self,
        view: HEOSApplicationRunStatusView,
    ) -> HEOSApplicationRunRenderScene:
        fields = (
            HEOSApplicationRunRenderField(
                label="Detail",
                value=view.detail,
            ),
            HEOSApplicationRunRenderField(
                label="Cycles",
                value=view.cycles,
            ),
        )

        return HEOSApplicationRunRenderScene(
            title=view.title,
            status=view.status,
            severity=view.severity,
            fields=fields,
        )
