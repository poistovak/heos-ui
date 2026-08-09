from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsPresentation,
    HEOSApplicationRunOperationsSeverity,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsHealthView:
    title: str
    status: str
    detail: str
    updates: str
    frames: str
    severity: HEOSApplicationRunOperationsSeverity

    @property
    def healthy(self) -> bool:
        return self.severity is HEOSApplicationRunOperationsSeverity.SUCCESS

    @property
    def warning(self) -> bool:
        return self.severity is HEOSApplicationRunOperationsSeverity.WARNING

    @property
    def neutral(self) -> bool:
        return self.severity is HEOSApplicationRunOperationsSeverity.NEUTRAL


@dataclass(slots=True)
class HEOSApplicationRunOperationsHealthWidget:
    _view: HEOSApplicationRunOperationsHealthView | None = None

    @property
    def view(self) -> HEOSApplicationRunOperationsHealthView | None:
        return self._view

    @property
    def has_data(self) -> bool:
        return self._view is not None

    def update(
        self,
        presentation: HEOSApplicationRunOperationsPresentation,
    ) -> HEOSApplicationRunOperationsHealthView:
        view = HEOSApplicationRunOperationsHealthView(
            title=presentation.title,
            status=presentation.status,
            detail=presentation.detail,
            updates=presentation.updates,
            frames=presentation.frames,
            severity=presentation.severity,
        )

        self._view = view
        return view

    def clear(self) -> None:
        self._view = None
