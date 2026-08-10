from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

health_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_health"
)

RunHealth = (
    health_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealth
)
RunHealthState = (
    health_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunHealthState
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity(
    str,
    Enum,
):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunDiagnostic:
    code: str
    severity: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity
    )
    message: str
    action: str
    healthy: bool

    @classmethod
    def diagnose(
        cls,
        health: RunHealth,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunDiagnostic:
        if health.state is RunHealthState.EMPTY:
            return cls(
                code="RUN_EMPTY",
                severity=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity.INFO
                ),
                message="Run completed without runtime steps.",
                action="No action required.",
                healthy=True,
            )

        if health.state is RunHealthState.DEGRADED:
            if "not synchronized" in health.reason:
                return cls(
                    code="RUN_SYNC_MISMATCH",
                    severity=(
                        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity.WARNING
                    ),
                    message=health.reason,
                    action="Inspect runtime and status synchronization.",
                    healthy=False,
                )

            return cls(
                code="RUN_STATUS_COUNT_MISMATCH",
                severity=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity.WARNING
                ),
                message=health.reason,
                action="Inspect status update generation.",
                healthy=False,
            )

        return cls(
            code="RUN_HEALTHY",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusDiagnosticSeverity.SUCCESS
            ),
            message="Runtime history status run is healthy.",
            action="No action required.",
            healthy=True,
        )
