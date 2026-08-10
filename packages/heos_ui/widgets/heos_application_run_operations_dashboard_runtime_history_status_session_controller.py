from __future__ import annotations

import importlib
from dataclasses import dataclass

session_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_session"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

Session = (
    session_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSession
)
SessionUpdate = (
    session_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionUpdate
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionController:
    session: Session
    _tick_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionController
    ):
        return cls(
            session=Session.create(),
        )

    @property
    def tick_count(self) -> int:
        return self._tick_count

    @property
    def latest_update(self) -> SessionUpdate | None:
        return self.session.latest_update

    @property
    def has_updates(self) -> bool:
        return self.session.has_updates

    def tick(
        self,
        snapshot: Snapshot,
    ) -> SessionUpdate:
        update = self.session.refresh(snapshot)
        self._tick_count += 1
        return update

    def reset(self) -> None:
        self.session.reset()
        self._tick_count = 0
