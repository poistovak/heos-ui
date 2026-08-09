from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_session_presenter import (
    HEOSApplicationRunSessionPresentation,
    HEOSApplicationRunSessionSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionHealthView:
    title: str
    status: str
    detail: str
    runs: str
    cycles: str
    severity: HEOSApplicationRunSessionSeverity

    @property
    def healthy(self) -> bool:
        return self.severity is HEOSApplicationRunSessionSeverity.SUCCESS

    @property
    def warning(self) -> bool:
        return self.severity is HEOSApplicationRunSessionSeverity.WARNING

    @property
    def neutral(self) -> bool:
        return self.severity is HEOSApplicationRunSessionSeverity.NEUTRAL


@dataclass(slots=True)
class HEOSApplicationRunSessionHealthWidget:
    _view: HEOSApplicationRunSessionHealthView | None = None

    @property
    def view(self) -> HEOSApplicationRunSessionHealthView | None:
        return self._view

    @property
    def has_data(self) -> bool:
        return self._view is not None

    def update(
        self,
        presentation: HEOSApplicationRunSessionPresentation,
    ) -> HEOSApplicationRunSessionHealthView:
        view = HEOSApplicationRunSessionHealthView(
            title=presentation.title,
            status=presentation.status,
            detail=presentation.detail,
            runs=presentation.runs,
            cycles=presentation.cycles,
            severity=presentation.severity,
        )

        self._view = view
        return view

    def clear(self) -> None:
        self._view = None
