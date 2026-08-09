from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

from . import (
    heos_application_run_operations_dashboard_runtime_history_session as history_session,
)
from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

session_controller = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_session_controller"
)

HistoryUpdate = (
    history_session.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate
)
SessionController = (
    session_controller.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySessionController
)


class HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisorState(
    str,
    Enum,
):
    STOPPED = "stopped"
    RUNNING = "running"


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisor:
    controller: SessionController
    _run_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisor:
        return cls(
            controller=SessionController.create(),
        )

    @property
    def state(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisorState:
        if self.controller.running:
            return (
                HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisorState.
                RUNNING
            )

        return (
            HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisorState.
            STOPPED
        )

    @property
    def running(self) -> bool:
        return self.controller.running

    @property
    def run_count(self) -> int:
        return self._run_count

    @property
    def latest(self) -> HistoryUpdate | None:
        return self.controller.latest

    @property
    def has_updates(self) -> bool:
        return self.controller.has_updates

    def start(self) -> None:
        self.controller.start()

    def run(
        self,
        operations: HEOSApplicationRunOperationsSession,
    ) -> HistoryUpdate:
        if not self.running:
            raise RuntimeError(
                "Runtime history supervisor is not running."
            )

        update = self.controller.tick(operations)
        self._run_count += 1
        return update

    def stop(self) -> None:
        self.controller.stop()

    def reset(self) -> None:
        self.controller.reset()
        self._run_count = 0
