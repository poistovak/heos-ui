from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

from .heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

history_supervisor = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_supervisor"
)

HistorySupervisor = (
    history_supervisor.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisor
)
HistorySupervisorState = (
    history_supervisor.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisorState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState(
    str,
    Enum,
):
    STOPPED = "stopped"
    RUNNING = "running"


@dataclass(slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator:
    operations: HEOSApplicationRunOperationsSession
    supervisor: HistorySupervisor
    _cycle_count: int = 0

    @classmethod
    def create(
        cls,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator:
        return cls(
            operations=HEOSApplicationRunOperationsSession.create(),
            supervisor=HistorySupervisor.create(),
        )

    @property
    def state(
        self,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState:
        if self.supervisor.running:
            return (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState.
                RUNNING
            )

        return (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState.
            STOPPED
        )

    @property
    def running(self) -> bool:
        return self.supervisor.running

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    @property
    def latest(self):
        return self.supervisor.latest

    @property
    def has_updates(self) -> bool:
        return self.supervisor.has_updates

    def start(self) -> None:
        self.supervisor.start()

    def cycle(self):
        if not self.running:
            raise RuntimeError(
                "Runtime history orchestrator is not running."
            )

        update = self.supervisor.run(
            self.operations
        )
        self._cycle_count += 1
        return update

    def stop(self) -> None:
        self.supervisor.stop()

    def reset(self) -> None:
        self.supervisor.reset()
        self._cycle_count = 0
