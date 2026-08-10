from __future__ import annotations

import importlib
from dataclasses import dataclass

supervisor_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_supervisor"
)

Supervisor = (
    supervisor_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSupervisor
)


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusApplication:
    supervisor: Supervisor
    _update_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusApplication:
        return cls(
            supervisor=Supervisor.create(),
        )

    @property
    def running(self) -> bool:
        return self.supervisor.running

    @property
    def update_count(self) -> int:
        return self._update_count

    @property
    def latest(self):
        return self.supervisor.latest

    @property
    def has_updates(self) -> bool:
        return self.supervisor.has_updates

    def launch(self) -> None:
        self.supervisor.start()

    def update(self):
        if not self.running:
            raise RuntimeError(
                "Runtime history status application is not running."
            )

        result = self.supervisor.refresh()
        self._update_count += 1
        return result

    def shutdown(self) -> None:
        self.supervisor.stop()

    def reset(self) -> None:
        self.supervisor.reset()
        self._update_count = 0
