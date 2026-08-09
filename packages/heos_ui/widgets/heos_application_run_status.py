from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_presenter import (
    HEOSApplicationRunPresentation,
    HEOSApplicationRunSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunStatusView:
    title: str
    status: str
    detail: str
    cycles: str
    severity: HEOSApplicationRunSeverity

    @property
    def warning(self) -> bool:
        return self.severity is HEOSApplicationRunSeverity.WARNING

    @property
    def successful(self) -> bool:
        return self.severity is HEOSApplicationRunSeverity.SUCCESS

    @property
    def neutral(self) -> bool:
        return self.severity is HEOSApplicationRunSeverity.NEUTRAL


@dataclass(slots=True)
class HEOSApplicationRunStatusWidget:
    _view: HEOSApplicationRunStatusView | None = None

    @property
    def view(self) -> HEOSApplicationRunStatusView | None:
        return self._view

    @property
    def has_data(self) -> bool:
        return self._view is not None

    def update(
        self,
        presentation: HEOSApplicationRunPresentation,
    ) -> HEOSApplicationRunStatusView:
        view = HEOSApplicationRunStatusView(
            title=presentation.title,
            status=presentation.status,
            detail=presentation.detail,
            cycles=presentation.cycles,
            severity=presentation.severity,
        )

        self._view = view
        return view

    def clear(self) -> None:
        self._view = None
