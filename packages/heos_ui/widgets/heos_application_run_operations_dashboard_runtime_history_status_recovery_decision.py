from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

recovery_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_plan"
)

RecoveryPlan = (
    recovery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPlan
)
RecoveryPriority = (
    recovery_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryPriority
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState(
    str,
    Enum,
):
    SKIP = "skip"
    RETRY = "retry"
    HOLD = "hold"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision:
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState
    )
    diagnostic_code: str
    execute: bool
    reason: str
    action: str

    @classmethod
    def decide(
        cls,
        plan: RecoveryPlan,
    ) -> (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
    ):
        if not plan.required:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState.SKIP
                ),
                diagnostic_code=plan.diagnostic_code,
                execute=False,
                reason="Recovery is not required.",
                action=plan.action,
            )

        if not plan.retryable:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState.HOLD
                ),
                diagnostic_code=plan.diagnostic_code,
                execute=False,
                reason="Recovery requires manual intervention.",
                action=plan.action,
            )

        return cls(
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecisionState.RETRY
            ),
            diagnostic_code=plan.diagnostic_code,
            execute=True,
            reason="Recovery retry is permitted.",
            action=plan.action,
        )
