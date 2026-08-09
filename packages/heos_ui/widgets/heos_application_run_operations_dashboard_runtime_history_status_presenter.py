from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

orchestrator_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_orchestrator"
)
snapshot_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_snapshot"
)

OrchestratorState = (
    orchestrator_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryOrchestratorState
)
Snapshot = (
    snapshot_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySnapshot
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity(
    str,
    Enum,
):
    NEUTRAL = "neutral"
    ACTIVE = "active"
    STOPPED = "stopped"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresentation:
    title: str
    status: str
    detail: str
    cycles: str
    runs: str
    refreshes: str
    latest: str
    severity: HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresenter:
    title: str = "HEOS Runtime History"

    def present(
        self,
        snapshot: Snapshot,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresentation:
        if snapshot.running:
            status = "RUNNING"
            detail = "Runtime history orchestration is active."
            severity = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity.
                ACTIVE
            )
        elif snapshot.has_updates:
            status = "STOPPED"
            detail = "Runtime history orchestration is stopped."
            severity = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity.
                STOPPED
            )
        else:
            status = "IDLE"
            detail = "Runtime history has not produced an update."
            severity = (
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusSeverity.
                NEUTRAL
            )

        latest = (
            f"Latest sequence {snapshot.latest_sequence}"
            if snapshot.latest_sequence is not None
            else "Latest sequence —"
        )

        return (
            HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusPresentation(
                title=self.title,
                status=status,
                detail=detail,
                cycles=f"Cycles {snapshot.cycle_count}",
                runs=f"Runs {snapshot.run_count}",
                refreshes=f"Refreshes {snapshot.refresh_count}",
                latest=latest,
                severity=severity,
            )
        )
