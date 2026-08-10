from __future__ import annotations

import importlib
from dataclasses import dataclass

controller_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "session_controller"
)
orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

Controller = (
    controller_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSessionController
)
Orchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSupervisor:
    orchestrator: Orchestrator
    controller: Controller
    _running: bool = False
    _refresh_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSupervisor:
        return cls(
            orchestrator=Orchestrator.create(),
            controller=Controller.create(),
        )

    @property
    def running(self) -> bool:
        return self._running

    @property
    def refresh_count(self) -> int:
        return self._refresh_count

    @property
    def latest(self):
        return self.controller.latest_update

    @property
    def has_updates(self) -> bool:
        return self.controller.has_updates

    def start(self) -> None:
        self.orchestrator.start()
        self._running = True

    def refresh(self):
        if not self._running:
            raise RuntimeError(
                "Runtime history status supervisor is not running."
            )

        snapshot = Snapshot.capture(
            self.orchestrator
        )
        update = self.controller.tick(
            snapshot
        )
        self._refresh_count += 1
        return update

    def stop(self) -> None:
        self.orchestrator.stop()
        self._running = False

    def reset(self) -> None:
        self.orchestrator.reset()
        self.controller.reset()
        self._running = False
        self._refresh_count = 0
