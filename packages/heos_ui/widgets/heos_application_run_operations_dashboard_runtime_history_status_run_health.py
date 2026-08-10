from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

summary_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_summary"
)

RunSummary = (
    summary_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunSummary
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState(
    str,
    Enum,
):
    HEALTHY = "healthy"
    EMPTY = "empty"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealth:
    state: HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState
    healthy: bool
    reason: str
    step_count: int
    runtime_cycles: int
    status_updates: int

    @classmethod
    def evaluate(
        cls,
        summary: RunSummary,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealth:
        if summary.empty:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState.EMPTY
                ),
                healthy=True,
                reason="Run completed without runtime steps.",
                step_count=0,
                runtime_cycles=0,
                status_updates=0,
            )

        if not summary.synchronized:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState.DEGRADED
                ),
                healthy=False,
                reason="Runtime and status updates are not synchronized.",
                step_count=summary.step_count,
                runtime_cycles=summary.runtime_cycles,
                status_updates=summary.status_updates,
            )

        if summary.status_updates != summary.step_count:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState.DEGRADED
                ),
                healthy=False,
                reason="Status update count does not match step count.",
                step_count=summary.step_count,
                runtime_cycles=summary.runtime_cycles,
                status_updates=summary.status_updates,
            )

        return cls(
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState.HEALTHY
            ),
            healthy=True,
            reason="Runtime history status run is healthy.",
            step_count=summary.step_count,
            runtime_cycles=summary.runtime_cycles,
            status_updates=summary.status_updates,
        )
