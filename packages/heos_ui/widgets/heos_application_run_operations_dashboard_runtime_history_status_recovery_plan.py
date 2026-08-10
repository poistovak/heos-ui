from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

diagnostic_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "run_diagnostic"
)

RunDiagnostic = (
    diagnostic_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRunDiagnostic
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority(
    str,
    Enum,
):
    NONE = "none"
    NORMAL = "normal"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPlan:
    diagnostic_code: str
    required: bool
    retryable: bool
    priority: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority
    )
    action: str

    @classmethod
    def from_diagnostic(
        cls,
        diagnostic: RunDiagnostic,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPlan:
        if diagnostic.code in {
            "RUN_HEALTHY",
            "RUN_EMPTY",
        }:
            return cls(
                diagnostic_code=diagnostic.code,
                required=False,
                retryable=False,
                priority=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority.NONE
                ),
                action="No recovery required.",
            )

        if diagnostic.code == "RUN_SYNC_MISMATCH":
            return cls(
                diagnostic_code=diagnostic.code,
                required=True,
                retryable=True,
                priority=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority.HIGH
                ),
                action=(
                    "Inspect synchronization and retry the runtime status run."
                ),
            )

        return cls(
            diagnostic_code=diagnostic.code,
            required=True,
            retryable=True,
            priority=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority.NORMAL
            ),
            action=(
                "Inspect status update generation and retry the runtime status run."
            ),
        )
