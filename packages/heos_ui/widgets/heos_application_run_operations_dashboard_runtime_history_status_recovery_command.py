from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum

authorization_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "authorization"
)
decision_module = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_status_"
    "recovery_decision"
)

Authorization = (
    authorization_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorization
)
AuthorizationState = (
    authorization_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusAuthorizationState
)
RecoveryDecision = (
    decision_module.
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryDecision
)


class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState(
    str,
    Enum,
):
    READY = "ready"
    BLOCKED = "blocked"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommand:
    state: (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState
    )
    diagnostic_code: str
    action: str
    executable: bool
    confidence: float
    reason: str

    @classmethod
    def build(
        cls,
        decision: RecoveryDecision,
        authorization: Authorization,
    ) -> HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommand:
        if decision.diagnostic_code != authorization.diagnostic_code:
            raise ValueError(
                "Recovery decision and authorization codes do not match."
            )

        if authorization.state is AuthorizationState.MANUAL:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState.MANUAL
                ),
                diagnostic_code=decision.diagnostic_code,
                action=decision.action,
                executable=False,
                confidence=authorization.confidence,
                reason="Recovery command requires manual authorization.",
            )

        if not authorization.authorized:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState.BLOCKED
                ),
                diagnostic_code=decision.diagnostic_code,
                action=decision.action,
                executable=False,
                confidence=authorization.confidence,
                reason="Recovery command is blocked by authorization.",
            )

        if not decision.execute:
            return cls(
                state=(
                    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState.BLOCKED
                ),
                diagnostic_code=decision.diagnostic_code,
                action=decision.action,
                executable=False,
                confidence=authorization.confidence,
                reason="Recovery decision does not permit execution.",
            )

        return cls(
            state=(
                HEOSApplicationRunOperationsDashboardRuntimeHistoryStatusRecoveryCommandState.READY
            ),
            diagnostic_code=decision.diagnostic_code,
            action=decision.action,
            executable=True,
            confidence=authorization.confidence,
            reason="Recovery command is ready for execution.",
        )
