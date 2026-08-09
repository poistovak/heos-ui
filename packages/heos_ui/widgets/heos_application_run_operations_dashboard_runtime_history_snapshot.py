from __future__ import annotations

import importlib
from dataclasses import dataclass

orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)

HistoryOrchestrator = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestrator
)
HistoryOrchestratorState = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot:
    state: HistoryOrchestratorState
    running: bool
    cycle_count: int
    run_count: int
    refresh_count: int
    has_updates: bool
    latest_sequence: int | None

    @classmethod
    def capture(
        cls,
        orchestrator: HistoryOrchestrator,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot:
        latest = orchestrator.latest

        return cls(
            state=orchestrator.state,
            running=orchestrator.running,
            cycle_count=orchestrator.cycle_count,
            run_count=orchestrator.supervisor.run_count,
            refresh_count=(
                orchestrator.supervisor.controller.session.refresh_count
            ),
            has_updates=orchestrator.has_updates,
            latest_sequence=(
                latest.sequence
                if latest is not None
                else None
            ),
        )
