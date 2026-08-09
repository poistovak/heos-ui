from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_operations_dashboard_canvas_renderer import (
    HEOSApplicationRunOperationsDashboardCanvasFrame,
)
from .heos_application_run_operations_dashboard_controller import (
    HEOSApplicationRunOperationsDashboardUpdate,
)
from .heos_application_run_operations_dashboard_health import (
    HEOSApplicationRunOperationsDashboardHealthSummary,
)
from .heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
    HEOSApplicationRunOperationsDashboardHealthWidget,
)
from .heos_application_run_operations_dashboard_live_renderer import (
    HEOSApplicationRunOperationsDashboardLiveRenderer,
)
from .heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardHealthPresenter,
    HEOSApplicationRunOperationsDashboardPresentation,
)
from .heos_application_run_operations_dashboard_session import (
    HEOSApplicationRunOperationsDashboardSession,
)
from .heos_application_run_operations_dashboard_statistics import (
    HEOSApplicationRunOperationsDashboardStatistics,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeCycle:
    cycle: int
    update: HEOSApplicationRunOperationsDashboardUpdate
    statistics: HEOSApplicationRunOperationsDashboardStatistics
    health: HEOSApplicationRunOperationsDashboardHealthSummary
    presentation: HEOSApplicationRunOperationsDashboardPresentation
    view: HEOSApplicationRunOperationsDashboardHealthView
    frame: HEOSApplicationRunOperationsDashboardCanvasFrame


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntime:
    dashboard: HEOSApplicationRunOperationsDashboardSession
    presenter: HEOSApplicationRunOperationsDashboardHealthPresenter
    widget: HEOSApplicationRunOperationsDashboardHealthWidget
    renderer: HEOSApplicationRunOperationsDashboardLiveRenderer
    _latest: HEOSApplicationRunOperationsDashboardRuntimeCycle | None = None
    _cycle: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntime:
        return cls(
            dashboard=(
                HEOSApplicationRunOperationsDashboardSession.create()
            ),
            presenter=(
                HEOSApplicationRunOperationsDashboardHealthPresenter()
            ),
            widget=HEOSApplicationRunOperationsDashboardHealthWidget(),
            renderer=(
                HEOSApplicationRunOperationsDashboardLiveRenderer.create()
            ),
        )

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle | None:
        return self._latest

    @property
    def cycle(self) -> int:
        return self._cycle

    @property
    def has_cycle(self) -> bool:
        return self._latest is not None

    def run(
        self,
        operations: HEOSApplicationRunOperationsSession,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeCycle:
        update = self.dashboard.refresh(operations)

        statistics = (
            HEOSApplicationRunOperationsDashboardStatistics.capture(
                self.dashboard
            )
        )

        health = (
            HEOSApplicationRunOperationsDashboardHealthSummary.from_statistics(
                statistics
            )
        )

        presentation = self.presenter.present(health)
        view = self.widget.update(presentation)
        frame = self.renderer.render(view)

        self._cycle += 1

        cycle = HEOSApplicationRunOperationsDashboardRuntimeCycle(
            cycle=self._cycle,
            update=update,
            statistics=statistics,
            health=health,
            presentation=presentation,
            view=view,
            frame=frame,
        )

        self._latest = cycle
        return cycle

    def clear(self) -> None:
        self.dashboard.clear()
        self.widget.clear()
        self.renderer.clear()
        self._latest = None
