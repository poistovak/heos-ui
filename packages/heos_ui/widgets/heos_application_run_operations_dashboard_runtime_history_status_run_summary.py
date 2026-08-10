from __future__ import annotations

import importlib
from dataclasses import dataclass

runner_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "runtime_runner"
)

RunResult = (
    runner_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunResult
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunSummary:
    step_count: int
    first_sequence: int | None
    last_sequence: int | None
    runtime_cycles: int
    status_updates: int
    synchronized: bool

    @property
    def empty(self) -> bool:
        return self.step_count == 0

    @classmethod
    def capture(
        cls,
        result: RunResult,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunSummary:
        if not result.steps:
            return cls(
                step_count=0,
                first_sequence=None,
                last_sequence=None,
                runtime_cycles=0,
                status_updates=0,
                synchronized=True,
            )

        first = result.steps[0]
        last = result.steps[-1]

        synchronized = all(
            step.runtime_update.statistics.total_cycles
            == int(step.status_update.view.cycles.removeprefix("Cycles "))
            for step in result.steps
        )

        return cls(
            step_count=result.step_count,
            first_sequence=first.sequence,
            last_sequence=last.sequence,
            runtime_cycles=last.runtime_update.statistics.total_cycles,
            status_updates=len(result.steps),
            synchronized=synchronized,
        )
