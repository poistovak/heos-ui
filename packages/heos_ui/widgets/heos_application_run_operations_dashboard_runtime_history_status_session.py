from __future__ import annotations

import importlib
from dataclasses import dataclass

live_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_live_renderer"
)
presenter_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_presenter"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)
widget_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_widget"
)

LiveRenderer = (
    live_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusLiveRenderer
)
Presenter = (
    presenter_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresenter
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)
Widget = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusWidget
)
StatusView = (
    widget_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusView
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate:
    sequence: int
    view: StatusView
    frame: object


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSession:
    presenter: Presenter
    widget: Widget
    live_renderer: LiveRenderer
    _refresh_count: int = 0
    _latest_update: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate
        | None
    ) = None

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSession:
        return cls(
            presenter=Presenter(),
            widget=Widget(),
            live_renderer=LiveRenderer.create(),
        )

    @property
    def refresh_count(self) -> int:
        return self._refresh_count

    @property
    def latest_update(
        self,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate
        | None
    ):
        return self._latest_update

    @property
    def has_updates(self) -> bool:
        return self._latest_update is not None

    def refresh(
        self,
        snapshot: Snapshot,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate:
        presentation = self.presenter.present(snapshot)
        view = self.widget.update(presentation)
        result = self.live_renderer.render(view)

        self._refresh_count += 1

        update = (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate(
                sequence=self._refresh_count,
                view=view,
                frame=result.frame,
            )
        )
        self._latest_update = update
        return update

    def reset(self) -> None:
        self.widget.clear()
        self.live_renderer.clear()
        self._refresh_count = 0
        self._latest_update = None
