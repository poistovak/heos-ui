from __future__ import annotations

from dataclasses import dataclass, field

from . import (
    heos_application_run_operations_dashboard_runtime_history_controller as history_controller,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_health as history_health,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as history_widget,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_live_renderer as live_renderer,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_presenter as history_presenter,
)
from . import (
    heos_application_run_operations_dashboard_runtime_history_statistics as history_statistics,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

HistoryController = (
    history_controller.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryController
)
HistoryStatistics = (
    history_statistics.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics
)
HistoryHealthSummary = (
    history_health.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthSummary
)
HistoryPresenter = (
    history_presenter.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthPresenter
)
HistoryPresentation = (
    history_presenter.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryPresentation
)
HistoryWidget = (
    history_widget.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthWidget
)
HistoryView = (
    history_widget.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
)
HistoryLiveRenderer = (
    live_renderer.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryLiveRenderer
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate:
    sequence: int
    statistics: HistoryStatistics
    health: HistoryHealthSummary
    presentation: HistoryPresentation
    view: HistoryView
    frame_result: object


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistorySession:
    controller: HistoryController
    presenter: HistoryPresenter
    widget: HistoryWidget
    renderer: HistoryLiveRenderer
    _history: list[
        HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate
    ] = field(default_factory=list, init=False)

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySession:
        return cls(
            controller=HistoryController.create(),
            presenter=HistoryPresenter(),
            widget=HistoryWidget(),
            renderer=HistoryLiveRenderer.create(),
        )

    @property
    def history(
        self,
    ) -> tuple[
        HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate,
        ...,
    ]:
        return tuple(self._history)

    @property
    def latest(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate | None:
        if not self._history:
            return None

        return self._history[-1]

    @property
    def refresh_count(self) -> int:
        return len(self._history)

    @property
    def has_updates(self) -> bool:
        return bool(self._history)

    def refresh(
        self,
        operations: HEOSApplicationRunOperationsSession,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate:
        self.controller.run(operations)

        statistics = HistoryStatistics.capture(
            self.controller.history
        )
        health = HistoryHealthSummary.from_statistics(
            statistics
        )
        presentation = self.presenter.present(
            health
        )
        view = self.widget.update(
            presentation
        )
        frame_result = self.renderer.render(
            view
        )

        update = (
            HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate(
                sequence=self.refresh_count + 1,
                statistics=statistics,
                health=health,
                presentation=presentation,
                view=view,
                frame_result=frame_result,
            )
        )

        self._history.append(update)
        return update

    def clear(self) -> None:
        self.controller.clear()
        self.widget.clear()
        self.renderer.clear()
        self._history.clear()
