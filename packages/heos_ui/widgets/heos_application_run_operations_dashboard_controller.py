from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_canvas_renderer import (
    HEOSApplicationRunOperationsCanvasFrame,
)
from .heos_application_run_operations_health import (
    HEOSApplicationRunOperationsHealthSummary,
)
from .heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
    HEOSApplicationRunOperationsHealthWidget,
)
from .heos_application_run_operations_live_renderer import (
    HEOSApplicationRunOperationsLiveRenderer,
)
from .heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsHealthPresenter,
    HEOSApplicationRunOperationsPresentation,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)
from .heos_application_run_operations_session_statistics import (
    HEOSApplicationRunOperationsSessionStatistics,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardUpdate:
    statistics: HEOSApplicationRunOperationsSessionStatistics
    health: HEOSApplicationRunOperationsHealthSummary
    presentation: HEOSApplicationRunOperationsPresentation
    view: HEOSApplicationRunOperationsHealthView
    frame: HEOSApplicationRunOperationsCanvasFrame
    sequence: int


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardController:
    presenter: HEOSApplicationRunOperationsHealthPresenter
    widget: HEOSApplicationRunOperationsHealthWidget
    renderer: HEOSApplicationRunOperationsLiveRenderer
    _latest: HEOSApplicationRunOperationsDashboardUpdate | None = None
    _sequence: int = 0

    @classmethod
    def create(cls) -> HEOSApplicationRunOperationsDashboardController:
        return cls(
            presenter=HEOSApplicationRunOperationsHealthPresenter(),
            widget=HEOSApplicationRunOperationsHealthWidget(),
            renderer=HEOSApplicationRunOperationsLiveRenderer.create(),
        )

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardUpdate | None:
        return self._latest

    @property
    def sequence(self) -> int:
        return self._sequence

    @property
    def has_update(self) -> bool:
        return self._latest is not None

    def update(
        self,
        session: HEOSApplicationRunOperationsSession,
    ) -> HEOSApplicationRunOperationsDashboardUpdate:
        statistics = (
            HEOSApplicationRunOperationsSessionStatistics.capture(
                session
            )
        )
        health = HEOSApplicationRunOperationsHealthSummary.from_statistics(
            statistics
        )
        presentation = self.presenter.present(health)
        view = self.widget.update(presentation)
        frame = self.renderer.render(view)

        self._sequence += 1

        update = HEOSApplicationRunOperationsDashboardUpdate(
            statistics=statistics,
            health=health,
            presentation=presentation,
            view=view,
            frame=frame,
            sequence=self._sequence,
        )
        self._latest = update

        return update

    def clear(self) -> None:
        self.widget.clear()
        self.renderer.clear()
        self._latest = None
